# Verzeichnis der Verarbeitungstaetigkeiten

Stand: 2026-06-17

Diese Vorlage ist fuer den konkreten CRCON-Betrieb auszufuellen. Sie ersetzt keine Rechtsberatung und enthaelt Platzhalter, die der Betreiber pruefen muss.

## Stammdaten

| Feld | Eintrag |
| --- | --- |
| Verantwortlicher | TODO |
| Anschrift | TODO |
| Datenschutzkontakt | TODO |
| Technischer Betreiber | TODO |
| Hosting-Anbieter | TODO |
| CRCON-Instanz/Hostname | TODO |
| Server/Community | TODO |
| Erstellt am | TODO |
| Review-Intervall | TODO, z. B. quartalsweise |

## Verarbeitung 1: Serverbetrieb und Moderation

| Feld | Eintrag |
| --- | --- |
| Zweck | Betrieb und Moderation eines Hell-Let-Loose-Servers, Missbrauchsvermeidung, Durchsetzung von Serverregeln |
| Betroffene Personen | Spieler, Admins, Moderatoren |
| Datenkategorien | Steam64/EOS/Windows-ID, Spielernamen, Join-/Leave-Zeiten, Team, Squad, Chat, Kills, Teamkills, Admin-Aktionen, Moderationsgruende |
| Systeme | CRCON Backend, Postgres, Redis, RCON-Verbindung, optional Discord-Webhooks |
| Rechtsgrundlage | TODO: festlegen und begruenden |
| Empfaenger | TODO: interne Admins, Hosting-Anbieter, ggf. Discord |
| Drittlandtransfer | TODO: pruefen fuer Discord/Sentry/Hosting |
| Speicherfrist | TODO: z. B. Game-Logs 30 Tage, Moderation 365 Tage |
| Loeschung | `privacy_purge`, manuelle Fallpruefung bei aktiven Bans/Reports |
| TOMs | Rollenrechte, TLS, Firewall, getrennte Admin-Konten, Backup-Verschluesselung |

## Verarbeitung 2: Admin- und Benutzerverwaltung

| Feld | Eintrag |
| --- | --- |
| Zweck | Zugriff auf CRCON verwalten und nachvollziehen |
| Betroffene Personen | Admins, Moderatoren, technische Betreiber |
| Datenkategorien | Benutzername, Passwort-Hash, Rollen/Rechte, API-Key-Hash, Login-/Auditdaten |
| Systeme | Django Auth, API-Key-Tabelle, Auditlogs |
| Rechtsgrundlage | TODO |
| Empfaenger | TODO |
| Speicherfrist | TODO: Konto bis Rollenende, Audit z. B. 365 Tage |
| Loeschung | Konten nach Teamwechsel deaktivieren/loeschen, Auditfrist per `privacy_purge` |
| TOMs | keine Shared Accounts, starke Passwoerter, Need-to-know, Admin-Review |

## Verarbeitung 3: Statistik und Community-Auswertung

| Feld | Eintrag |
| --- | --- |
| Zweck | Serverqualitaet, Spielbalance, Community-Verwaltung |
| Betroffene Personen | Spieler |
| Datenkategorien | Spielername, Steam/EOS-ID, Match-Statistiken, Level, Waffen, Map-Historie |
| Systeme | CRCON Statistiktabellen, Frontend |
| Rechtsgrundlage | TODO |
| Empfaenger | TODO: interne Admins, ggf. oeffentliche Anzeige falls aktiviert |
| Speicherfrist | TODO: z. B. 90 bis 365 Tage oder anonymisierte Langzeitwerte |
| Loeschung | `privacy_purge`, optional Export/Anonymisierung statt Personenbezug |
| TOMs | Zugriff beschraenken, keine unnoetigen oeffentlichen Ranglisten |

## Verarbeitung 4: Externe Integrationen

| Feld | Discord | Sentry | Steam API |
| --- | --- | --- | --- |
| Aktiviert | TODO | TODO | TODO |
| Zweck | TODO | Fehleranalyse | Profil-/Ban-Anreicherung |
| Daten | Chat/Admin-Events/Spielerbezug je nach Webhook | Fehlerkontext, Breadcrumbs, ggf. URL/User-Kontext | Steam-ID, Profil, Land, Ban-Info |
| Empfaenger/AVV | TODO | TODO | TODO |
| Drittlandtransfer | TODO | TODO | TODO |
| Minimierung | nur notwendige Webhooks | `SENTRY_SEND_DEFAULT_PII=false` | Cron deaktiviert bis Zweck freigegeben |
| Speicherfrist | TODO | TODO | `steam-info-days` im Purge |

## Verarbeitung 5: Backups und Logs

| Feld | Eintrag |
| --- | --- |
| Zweck | Wiederherstellung, Sicherheit, Fehleranalyse |
| Datenkategorien | Datenbankinhalt, Systemlogs, CRCON-Logs, ggf. Secrets wenn falsch konfiguriert |
| Speicherorte | TODO: Backup-Ziel, Log-Pfad, Rotation |
| Rechtsgrundlage | TODO |
| Empfaenger | TODO: Hosting/Backup-Anbieter |
| Speicherfrist | TODO: passend zum Loeschkonzept |
| Loeschung | Backup-Rotation, Logrotate, manuelle Notfallloeschung |
| TOMs | Verschluesselung, Zugriffsbeschraenkung, Restore-Test, Secrets nicht in Logs |

## Review-Fragen

- Sind alle aktivierten Webhooks in dieser Datei dokumentiert?
- Sind alle Admins mit produktivem Datenzugriff bekannt?
- Sind reale Loeschfristen kuerzer oder gleich den Purge-Parametern?
- Gibt es oeffentliche Statistiken oder Discord-Posts mit Spielerbezug?
- Sind Hosting, Backup, Discord, Sentry und sonstige Dienstleister geprueft?
- Wurde die DPIA-Schwelle dokumentiert?
