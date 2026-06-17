# DSGVO-Betrieb fuer CRCON

Diese Repo-Variante ist eine technische und organisatorische Basis fuer einen datenschutzfreundlichen CRCON-Betrieb. Sie ersetzt keine Rechtsberatung und macht eine Instanz nicht automatisch DSGVO-konform; der Betreiber muss Zwecke, Rechtsgrundlagen, Informationspflichten und Auftragsverarbeiter selbst festlegen.

## Was geaendert wurde

- Sentry sendet standardmaessig keine Default-PII mehr (`SENTRY_SEND_DEFAULT_PII=false`).
- Session-Cookies sind standardmaessig HTTP-only (`SESSION_COOKIE_HTTPONLY=true`).
- Die Python/Django-Logger fallen ohne explizite Konfiguration auf `INFO` statt `DEBUG` zurueck.
- Das vorhersehbare `admin`/`admin`-Seed-Konto ist im Env-Beispiel deaktiviert (`DONT_SEED_ADMIN_USER=1`).
- Der automatische Steam-Profil-Cron ist deaktiviert, bis der Zweck dokumentiert und ein API-Key bewusst gesetzt ist.
- Logrotate rotiert taeglich und haelt standardmaessig sieben komprimierte Logdateien.
- `privacy_purge` bietet einen Dry-Run und eine ausfuehrbare Fristenloeschung fuer alte personenbezogene oder spielerbezogene Daten.

## Erstinstallation

```powershell
Copy-Item .env.dsgvo.example .env
```

Danach in `.env` mindestens setzen:

- `HLL_DB_PASSWORD`
- `RCONWEB_API_SECRET`
- `HLL_HOST`
- `HLL_PORT`
- `HLL_PASSWORD`
- `RCONWEB_EXTERNAL_ADDRESS`

Fuer Produktion: CRCON nicht direkt oeffentlich per HTTP exponieren. Verwende einen TLS-Reverse-Proxy, binde direkte Ports lokal oder firewallseitig, und setze pro Instanz einen eigenen Hostnamen.

Start mit der Ein-Server-Vorlage:

```bash
docker compose -f docker-templates/one-server.yaml up -d
```

## Loeschkonzept

Vor jedem echten Lauf immer zuerst trocken pruefen:

```bash
docker compose exec backend_1 /code/manage.py privacy_purge
```

Erst nach Review und getesteter Sicherung ausfuehren:

```bash
docker compose exec backend_1 /code/manage.py privacy_purge --execute
```

Standardfristen im Befehl:

| Datenbereich | Standard |
| --- | ---: |
| Raw/strukturierte Game-Logs | 30 Tage |
| Spieler-Sessions | 180 Tage |
| Population-Snapshots | 90 Tage |
| Match-Statistiken mit Spielerbezug | 365 Tage |
| Admin-Auditlog | 365 Tage |
| Moderationsaktionen | 365 Tage |
| Spielerkommentare | 365 Tage |
| Steam-Profil-/Ban-Cache | 180 Tage |
| abgelaufene Blacklist-Eintraege | 365 Tage |

Beispiel fuer kuerzere Game-Logs und laengere Auditlogs:

```bash
docker compose exec backend_1 /code/manage.py privacy_purge --logs-days 14 --audit-days 730
```

Der Cron in `config/crontab` schreibt taeglich einen Dry-Run nach `/logs/privacy_purge.log`. Fuege `--execute` erst hinzu, wenn die Fristen intern freigegeben sind.

## Zugriffe und Rollen

- Nutze keine gemeinsamen Admin-Konten.
- Vergib die sehr detaillierten CRCON-Rechte nach Need-to-know, besonders fuer:
  - Spielerprofile, Player IDs, Spielerhistorie
  - Game-Logs, strukturierte Logs, Auditlogs
  - VIP-, Admin-, Blacklist- und Watchlist-Funktionen
  - Discord-Webhook-Konfigurationen
  - Raw RCON Commands
- Entferne alte Admin-Benutzer nach Teamwechseln sofort.
- Dokumentiere, wer produktiven Datenbankzugriff hat.

## Externe Dienste

Aktiviere externe Dienste erst nach dokumentierter Pruefung:

- Discord-Webhooks koennen Spielernamen, Steam/EOS-IDs, Chat, Kills, Teamkills, Admin-Aktionen und Watchlist-Treffer an Discord uebermitteln.
- Sentry kann Fehlerkontext und Breadcrumbs an einen externen Dienst senden. `send_default_pii` bleibt in diesem Repo standardmaessig aus.
- Steam API reichert Spielerprofile, Land und Ban-Informationen an. Der Cron ist deaktiviert, bis der Betreiber den Zweck dokumentiert.

## Backup und Wiederherstellung

- Backups verschluesseln.
- Zugriff auf Backups auf Admins mit Betriebsnotwendigkeit begrenzen.
- Backup-Aufbewahrung mit dem Loeschkonzept abgleichen.
- Wiederherstellung regelmaessig testen, bevor `privacy_purge --execute` automatisiert wird.

## Betroffenenrechte

Fuer Auskunft oder Loeschanfragen zuerst Spieler-ID, bekannte Namen und Zeitraum erfassen. CRCON speichert Spielerbezug an mehreren Stellen: Logs, Sessions, Stats, Aktionen, Kommentare, VIPs, Watchlist, Flags, Blacklists und Steam-Cache. Aktive Moderationsentscheidungen koennen je nach Zweck und Rechtsgrundlage weiter aufbewahrt werden; das muss der Betreiber dokumentieren.

## Minimaler Produktions-Check

- `.env` enthaelt keine echten Secrets im Git.
- `DONT_SEED_ADMIN_USER=1` ist gesetzt.
- Direkte CRCON-Ports sind nicht ungeschuetzt oeffentlich.
- TLS ist am Reverse Proxy aktiv.
- Sentry bleibt leer oder ist mit AVV/DPA und `SENTRY_SEND_DEFAULT_PII=false` dokumentiert.
- Steam API ist nur aktiv, wenn Zweck und Informationspflichten klar sind.
- Discord-Webhooks sind minimiert und nur fuer notwendige Ereignisse aktiv.
- `privacy_purge` wurde trocken getestet.
- Backups sind verschluesselt und rueckspielbar.
