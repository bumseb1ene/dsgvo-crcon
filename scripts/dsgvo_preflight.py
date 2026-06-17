#!/usr/bin/env python3
"""Technical DSGVO baseline preflight for this CRCON repo.

This script checks repo defaults and documentation gates. It does not prove
legal compliance; it is a repeatable technical smoke test before production.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


TRUE_VALUES = {"1", "true", "yes", "on"}
FALSE_VALUES = {"0", "false", "no", "off", ""}
SAFE_LOG_LEVELS = {"INFO", "WARNING", "ERROR", "CRITICAL"}

REQUIRED_DOCS = [
    "docs/DSGVO_BETRIEB.md",
    "docs/DATENLANDKARTE.md",
    "docs/DSGVO_GAP_ANALYSE.md",
    "docs/VERZEICHNIS_VERARBEITUNGSTAETIGKEITEN.md",
    "docs/TOM_CHECKLISTE.md",
    "docs/BETROFFENENRECHTE_PROZESS.md",
    "docs/DATENSCHUTZHINWEIS_TEMPLATE.md",
    "docs/ANBIETER_UND_AVV_REGISTER.md",
    "docs/INCIDENT_RESPONSE.md",
    "docs/PRODUKTIONSFREIGABE.md",
]

REQUIRED_ENV = {
    "DJANGO_DEBUG": FALSE_VALUES,
    "DONT_SEED_ADMIN_USER": TRUE_VALUES,
    "SESSION_COOKIE_HTTPONLY": TRUE_VALUES,
    "SESSION_COOKIE_SECURE": TRUE_VALUES,
    "CSRF_COOKIE_SECURE": TRUE_VALUES,
    "SECURE_SSL_REDIRECT": FALSE_VALUES,
    "SECURE_PROXY_SSL_HEADER": FALSE_VALUES,
    "SENTRY_SEND_DEFAULT_PII": FALSE_VALUES,
}


@dataclass
class Finding:
    severity: str
    topic: str
    message: str


def read_text(root: Path, relative: str) -> str:
    return (root / relative).read_text(encoding="utf-8")


def parse_env(root: Path, relative: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in read_text(root, relative).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip().strip('"').strip("'")
        values[key.strip()] = value
    return values


class Checker:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.findings: list[Finding] = []
        self.passes = 0

    def pass_(self) -> None:
        self.passes += 1

    def fail(self, topic: str, message: str) -> None:
        self.findings.append(Finding("FAIL", topic, message))

    def warn(self, topic: str, message: str) -> None:
        self.findings.append(Finding("WARN", topic, message))

    def require_file(self, relative: str) -> None:
        if (self.root / relative).is_file():
            self.pass_()
        else:
            self.fail("required-files", f"Missing {relative}")

    def require_text(self, relative: str, pattern: str, topic: str, message: str) -> None:
        try:
            content = read_text(self.root, relative)
        except FileNotFoundError:
            self.fail(topic, f"Missing {relative}")
            return
        if re.search(pattern, content, re.MULTILINE):
            self.pass_()
        else:
            self.fail(topic, message)

    def check_required_docs(self) -> None:
        for relative in REQUIRED_DOCS:
            self.require_file(relative)

    def check_env_defaults(self) -> None:
        for env_file in ("default.env", ".env.dsgvo.example"):
            try:
                values = parse_env(self.root, env_file)
            except FileNotFoundError:
                self.fail("env", f"Missing {env_file}")
                continue

            for key, expected in REQUIRED_ENV.items():
                actual = values.get(key, "").strip().lower()
                if actual in expected:
                    self.pass_()
                else:
                    self.fail("env", f"{env_file}: {key} should be one of {sorted(expected)}, got {actual or '<missing>'}")

            level = values.get("LOGGING_LEVEL", "").strip().upper()
            if level in SAFE_LOG_LEVELS:
                self.pass_()
            else:
                self.fail("env", f"{env_file}: LOGGING_LEVEL should be one of {sorted(SAFE_LOG_LEVELS)}, got {level or '<missing>'}")

            sentry_level = values.get("SENTRY_BREADCRUMB_LEVEL", "").strip().upper()
            if sentry_level in SAFE_LOG_LEVELS:
                self.pass_()
            else:
                self.fail(
                    "env",
                    f"{env_file}: SENTRY_BREADCRUMB_LEVEL should be one of {sorted(SAFE_LOG_LEVELS)}, got {sentry_level or '<missing>'}",
                )

    def check_python_settings(self) -> None:
        checks = [
            (
                "rconweb/rconweb/settings.py",
                r'send_default_pii=env_bool\("SENTRY_SEND_DEFAULT_PII",\s*False\)',
                "settings",
                "Sentry send_default_pii must default to False",
            ),
            (
                "rconweb/rconweb/settings.py",
                r'SESSION_COOKIE_HTTPONLY\s*=\s*env_bool\("SESSION_COOKIE_HTTPONLY",\s*True\)',
                "settings",
                "Session cookies must default to HTTP-only",
            ),
            (
                "rconweb/rconweb/settings.py",
                r'DEBUG\s*=\s*env_bool\("DJANGO_DEBUG",\s*False\)',
                "settings",
                "Django DEBUG must parse DJANGO_DEBUG as a boolean and default to False",
            ),
            (
                "rconweb/rconweb/settings.py",
                r'raise ImproperlyConfigured\("RCONWEB_API_SECRET must be set when DJANGO_DEBUG=false"\)',
                "settings",
                "Production settings must fail closed when RCONWEB_API_SECRET is missing",
            ),
            (
                "rconweb/rconweb/settings.py",
                r'os\.getenv\("SENTRY_BREADCRUMB_LEVEL",\s*"INFO"\)',
                "settings",
                "Sentry breadcrumbs must default to INFO",
            ),
            (
                "rconweb/rconweb/settings.py",
                r'SESSION_COOKIE_SECURE\s*=\s*env_bool\("SESSION_COOKIE_SECURE",\s*not DEBUG\)',
                "settings",
                "Session cookies must be secure by default outside DEBUG",
            ),
            (
                "rconweb/rconweb/settings.py",
                r'CSRF_COOKIE_SECURE\s*=\s*env_bool\("CSRF_COOKIE_SECURE",\s*not DEBUG\)',
                "settings",
                "CSRF cookies must be secure by default outside DEBUG",
            ),
            (
                "rconweb/rconweb/settings.py",
                r'SECURE_SSL_REDIRECT\s*=\s*env_bool\("SECURE_SSL_REDIRECT",\s*False\)',
                "settings",
                "SECURE_SSL_REDIRECT must be explicitly configurable",
            ),
            (
                "rconweb/rconweb/settings.py",
                r'env_bool\("SECURE_PROXY_SSL_HEADER",\s*False\)',
                "settings",
                "SECURE_PROXY_SSL_HEADER must be opt-in",
            ),
            (
                "rconweb/rconweb/settings.py",
                r'os\.getenv\("LOGGING_LEVEL",\s*"INFO"\)',
                "settings",
                "Django web logging must default to INFO",
            ),
            (
                "rcon/settings.py",
                r'os\.getenv\("LOGGING_LEVEL",\s*"INFO"\)',
                "settings",
                "Worker logging must default to INFO",
            ),
            (
                "rcon/privacy.py",
                r"inactive_player_days:\s*int\s*=\s*0",
                "retention",
                "Inactive player profile purge must be available and disabled by default",
            ),
            (
                "rcon/cli.py",
                r"--inactive-player-days",
                "retention",
                "privacy_purge CLI must expose inactive profile retention",
            ),
            (
                "rcon/privacy.py",
                r"br\.expires_at IS NULL\s+OR br\.expires_at >= :cutoff\s+OR br\.created_at >= :cutoff",
                "retention",
                "Inactive profile purge must preserve active or recently expired blacklist records",
            ),
        ]
        for relative, pattern, topic, message in checks:
            self.require_text(relative, pattern, topic, message)

    def check_cron(self) -> None:
        try:
            lines = read_text(self.root, "config/crontab").splitlines()
        except FileNotFoundError:
            self.fail("cron", "Missing config/crontab")
            return

        active_lines = [line.strip() for line in lines if line.strip() and not line.lstrip().startswith("#")]
        active_cron = "\n".join(active_lines)

        if "privacy_purge" in active_cron:
            self.pass_()
        else:
            self.fail("cron", "config/crontab should run privacy_purge as a dry-run report")

        for line in active_lines:
            if "privacy_purge" in line and "--execute" in line:
                self.fail("cron", "privacy_purge must stay dry-run by default; remove --execute from config/crontab")
                return
        self.pass_()

        for line in active_lines:
            if "enrich_db_users" in line:
                self.fail("cron", "Steam enrichment cron must stay disabled until purpose and legal basis are documented")
                return
        self.pass_()

    def check_compose_templates(self) -> None:
        required = {
            "DJANGO_DEBUG": r"DJANGO_DEBUG:\s*\$\{DJANGO_DEBUG\}",
            "DONT_SEED_ADMIN_USER": r"DONT_SEED_ADMIN_USER:\s*\$\{DONT_SEED_ADMIN_USER\}",
            "SENTRY_BREADCRUMB_LEVEL": r"SENTRY_BREADCRUMB_LEVEL:\s*\$\{SENTRY_BREADCRUMB_LEVEL\}",
            "SESSION_COOKIE_HTTPONLY": r"SESSION_COOKIE_HTTPONLY:\s*\$\{SESSION_COOKIE_HTTPONLY\}",
            "SESSION_COOKIE_SECURE": r"SESSION_COOKIE_SECURE:\s*\$\{SESSION_COOKIE_SECURE\}",
            "CSRF_COOKIE_SECURE": r"CSRF_COOKIE_SECURE:\s*\$\{CSRF_COOKIE_SECURE\}",
            "SECURE_SSL_REDIRECT": r"SECURE_SSL_REDIRECT:\s*\$\{SECURE_SSL_REDIRECT\}",
            "SECURE_PROXY_SSL_HEADER": r"SECURE_PROXY_SSL_HEADER:\s*\$\{SECURE_PROXY_SSL_HEADER\}",
            "SENTRY_SEND_DEFAULT_PII": r"SENTRY_SEND_DEFAULT_PII:\s*\$\{SENTRY_SEND_DEFAULT_PII\}",
        }
        for relative in ("docker-templates/one-server.yaml", "docker-templates/ten-servers.yaml"):
            for key, pattern in required.items():
                self.require_text(relative, pattern, "compose", f"{relative}: missing {key} pass-through")

    def check_tracked_files(self) -> None:
        try:
            proc = subprocess.run(
                ["git", "ls-files"],
                cwd=self.root,
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except (OSError, subprocess.CalledProcessError) as exc:
            self.warn("git", f"Could not inspect tracked files: {exc}")
            return

        forbidden_names = {".env", "dev.env"}
        forbidden_dirs = ("logs/", "db_data/", "redis_data/", "certs/", "pw/")
        forbidden_suffixes = (".log", ".sqlite", ".db", ".dump")
        allowed_names = {"default.env", ".env.dsgvo.example", "example.dev.env"}

        for raw in proc.stdout.splitlines():
            path = raw.replace("\\", "/")
            lower = path.lower()
            name = Path(path).name
            if name in allowed_names:
                self.pass_()
                continue
            if name in forbidden_names:
                self.fail("tracked-files", f"Sensitive env file is tracked: {path}")
                continue
            if lower.startswith(forbidden_dirs):
                self.fail("tracked-files", f"Runtime data path is tracked: {path}")
                continue
            if lower.endswith(forbidden_suffixes):
                self.fail("tracked-files", f"Runtime data/log file is tracked: {path}")
                continue
            self.pass_()

    def run(self) -> int:
        self.check_required_docs()
        self.check_env_defaults()
        self.check_python_settings()
        self.check_cron()
        self.check_compose_templates()
        self.check_tracked_files()
        return 1 if any(f.severity == "FAIL" for f in self.findings) else 0

    def print_report(self) -> None:
        failures = [f for f in self.findings if f.severity == "FAIL"]
        warnings = [f for f in self.findings if f.severity == "WARN"]

        for finding in self.findings:
            print(f"[{finding.severity}] {finding.topic}: {finding.message}")

        print(
            f"Summary: {self.passes} passed, "
            f"{len(warnings)} warnings, {len(failures)} failures"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the CRCON DSGVO technical preflight.")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root. Defaults to the parent of this script directory.",
    )
    args = parser.parse_args()

    checker = Checker(args.root.resolve())
    exit_code = checker.run()
    checker.print_report()
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
