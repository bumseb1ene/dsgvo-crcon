# Produktionsfreigabe fuer eine CRCON-Instanz

Stand: 2026-06-17

Diese Checkliste ist der letzte Betreiber-Gate vor einem echten Produktivbetrieb. Sie sammelt die Nachweise, die nicht allein durch Code bewiesen werden koennen.

## Instanzdaten

| Feld | Eintrag |
| --- | --- |
| Community/Server | TODO |
| Hostname | TODO |
| Verantwortlicher | TODO |
| Technischer Betreiber | TODO |
| Freigabe geplant am | TODO |
| Review geplant am | TODO |

## Pflichtnachweise

| Bereich | Nachweis | Status |
| --- | --- | --- |
| VVT ausgefuellt | `docs/VERZEICHNIS_VERARBEITUNGSTAETIGKEITEN.md` fuer diese Instanz kopiert/ausgefuellt | offen |
| Datenschutzhinweis veroeffentlicht | Link zu Website/Discord/Server-Regeln | offen |
| Anbieter geprueft | `docs/ANBIETER_UND_AVV_REGISTER.md` ausgefuellt | offen |
| TOMs abgehakt | `docs/TOM_CHECKLISTE.md` mit Datum/Verantwortlichem | offen |
| Betroffenenrechte getestet | Testfall aus `docs/BETROFFENENRECHTE_PROZESS.md` durchgespielt | offen |
| Incident-Prozess bereit | `docs/INCIDENT_RESPONSE.md` Kontaktkette und Vorlage ausgefuellt | offen |
| DPIA-Entscheidung | dokumentiert: nicht erforderlich oder DPIA erstellt | offen |

## Technische Freigabe

| Bereich | Pruefung | Ergebnis |
| --- | --- | --- |
| Secrets | `.env` liegt nur auf Zielsystem und nicht in Git | TODO |
| Django Secret | `RCONWEB_API_SECRET` oder `SECRET_KEY` ist stark und eindeutig pro Instanz | TODO |
| Admin-Seed | `DONT_SEED_ADMIN_USER=1` | TODO |
| Django Debug | `DJANGO_DEBUG=false` | TODO |
| Cookie-Sicherheit | `SESSION_COOKIE_HTTPONLY=true`, `SESSION_COOKIE_SECURE=true`, `CSRF_COOKIE_SECURE=true` | TODO |
| Logging | `LOGGING_LEVEL=INFO` oder restriktiver | TODO |
| Sentry | leer/deaktiviert oder `SENTRY_SEND_DEFAULT_PII=false` plus Anbieterpruefung | TODO |
| Steam API | deaktiviert oder Zweck/Rechtsgrundlage/Hinweis dokumentiert | TODO |
| GitHub Actions | DSGVO preflight auf `main` bestanden | TODO |
| TLS | Hostname ist per HTTPS erreichbar | TODO |
| Firewall | keine oeffentlichen Redis/Postgres/Backend/RCON-Ports | TODO |
| Backups | verschluesselt, Zugriff begrenzt, Restore getestet | TODO |
| Logrotate | aktiv und Frist passend | TODO |
| Webhooks | nur notwendige Ereignisse, Kanalrechte geprueft | TODO |

## Empfohlene Kommandonachweise

Diese Kommandos sind Beispiele und muessen zur echten Compose-Datei und Instanz passen:

```bash
python3 scripts/dsgvo_preflight.py
docker compose -f docker-templates/one-server.yaml config
docker compose exec backend_1 /code/manage.py privacy_purge
docker compose exec backend_1 /code/manage.py privacy_purge --execute
```

Nachweise eintragen:

| Kommando | Datum | Ergebnis | Bearbeiter |
| --- | --- | --- | --- |
| `python3 scripts/dsgvo_preflight.py` | TODO | TODO | TODO |
| Compose-Konfiguration validiert | TODO | TODO | TODO |
| `privacy_purge` Dry-Run | TODO | TODO | TODO |
| `privacy_purge --execute` Testlauf | TODO | TODO | TODO |
| Backup-Restore-Test | TODO | TODO | TODO |
| Offene Ports geprueft | TODO | TODO | TODO |
| TLS geprueft | TODO | TODO | TODO |

## Freigabeentscheidung

| Entscheidung | Eintrag |
| --- | --- |
| Produktivbetrieb freigegeben | ja / nein |
| Einschraenkungen | TODO |
| Offene Restpunkte | TODO |
| Verantwortlicher | TODO |
| Datum | TODO |

## Nach Produktivstart

- [ ] Erster Admin-Review nach 7 Tagen.
- [ ] Erster `privacy_purge`-Log nach 24 Stunden pruefen.
- [ ] Discord-/Sentry-/Hosting-Logs auf unerwartete personenbezogene Inhalte pruefen.
- [ ] Backup-Job und Restore-Faehigkeit erneut pruefen.
- [ ] Review-Termin fuer VVT/TOMs/Anbieter setzen.
