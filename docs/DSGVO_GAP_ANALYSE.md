# DSGVO-Gap-Analyse

Stand: 2026-06-17

Diese Datei beschreibt, was dieses Repo technisch bereits vorbereitet und was ein Betreiber vor einem produktiven Betrieb noch organisatorisch, rechtlich und betrieblich klaeren muss. Sie ist keine Rechtsberatung.

## Einordnung

CRCON verarbeitet je nach Konfiguration personenbezogene oder spielerbezogene Daten wie Spielernamen, Steam-/EOS-IDs, Chat, Join-/Leave-Zeiten, Moderationsaktionen, Admin-Auditlogs, Discord-Webhook-Inhalte und optionale Fehlertelemetrie.

Die EU-Kommission beschreibt die DSGVO-Verantwortung als Nachweispflicht: Eine Organisation muss nicht nur Datenschutzregeln einhalten, sondern die Einhaltung auch belegen koennen. Ausserdem muss frueh geklaert sein, wer Verantwortlicher und wer Auftragsverarbeiter ist.

## Bereits umgesetzt

| Bereich | Status | Nachweis im Repo |
| --- | --- | --- |
| Datenschutzfreundliche Defaults | erledigt | `default.env`, `.env.dsgvo.example`, `rconweb/rconweb/settings.py` |
| Keine Default-PII an Sentry | erledigt | `SENTRY_SEND_DEFAULT_PII=false` |
| HTTP-only Session-Cookies | erledigt | `SESSION_COOKIE_HTTPONLY=true` |
| Weniger Debug-Logging | erledigt | `LOGGING_LEVEL=INFO`, Python-Settings |
| Vorhersehbares Admin-Seed-Konto deaktiviert | erledigt | `DONT_SEED_ADMIN_USER=1` |
| Steam-Anreicherung nicht automatisch aktiv | erledigt | `config/crontab` |
| Retention-Befehl mit Dry-Run | erledigt | `rcon/privacy.py`, `rcon/cli.py`, `privacy_purge` |
| Datenlandkarte | erledigt | `docs/DATENLANDKARTE.md` |
| Betriebshinweise | erledigt | `docs/DSGVO_BETRIEB.md` |

## Muss vor Produktivbetrieb erledigt werden

| Prioritaet | Thema | Warum | Ergebnis |
| --- | --- | --- | --- |
| P0 | Verantwortlichen festlegen | Ohne Betreiber, Zweck und Kontakt kann keine DSGVO-Auskunft sauber beantwortet werden. | Name, Anschrift, Kontakt, Datenschutzkontakt in Betreiberunterlagen |
| P0 | Zwecke und Rechtsgrundlagen festlegen | Moderation, Sicherheit, Community-Verwaltung und optionale Statistik brauchen dokumentierte Zwecke. | ausgefuelltes `docs/VERZEICHNIS_VERARBEITUNGSTAETIGKEITEN.md` |
| P0 | Informationspflichten bereitstellen | Spieler und Admins muessen wissen, welche Daten verarbeitet werden. | Datenschutzhinweis fuer Website/Discord/Server-Regeln |
| P0 | Zugriffskonzept finalisieren | Admins sehen Spielerprofile, Logs, Chat und Moderationshistorie. | Rollenmodell, Admin-Liste, Review-Termin |
| P0 | TLS und Netzwerkhaertung pruefen | Direkte HTTP-/RCON-/DB-Ports duerfen nicht offen im Internet haengen. | Reverse Proxy mit TLS, Firewall-Regeln, keine offenen internen Ports |
| P0 | Backup- und Loeschfristen freigeben | `privacy_purge --execute` darf erst laufen, wenn Wiederherstellung und Fristen geklaert sind. | dokumentierte Fristen, getestetes Restore, automatisierter Purge |
| P0 | Auftragsverarbeiter pruefen | VPS/Hosting, Discord, Sentry, Backup-Ziel, Mail/Monitoring koennen externe Empfaenger sein. | AVV/DPA-Liste mit Anbieter, Zweck, Region, Status |
| P0 | Incident-Prozess festlegen | Bei Datenschutzverletzungen kann eine Meldung binnen 72 Stunden erforderlich sein. | Kontaktkette, Log-Sicherung, Meldeentscheidung, Vorlage |
| P1 | Betroffenenrechte-Prozess testen | Auskunft, Loeschung und Einschraenkung muessen praktisch durchfuehrbar sein. | Testfall nach `docs/BETROFFENENRECHTE_PROZESS.md` |
| P1 | DPIA-Schwelle pruefen | Hohe Risiken koennen eine Datenschutz-Folgenabschaetzung erfordern. | Entscheidung dokumentiert: nicht erforderlich oder DPIA-Datei |
| P1 | Webhook-Minimierung | Discord kann Chat, Spieler-IDs und Moderationsereignisse weitertragen. | nur notwendige Webhooks, Kanalrechte, Aufbewahrung in Discord |
| P1 | Audit fuer Admin-Konten | Alte Admins und geteilte Konten sind ein hohes Risiko. | monatlicher Review, keine Shared Accounts |
| P2 | Monitoring ohne Personenbezug | Metriken sollten moeglichst technische Betriebswerte sein. | Monitoring-Liste ohne Spieler- oder Chatdaten |

## Nicht allein durch Code loesbar

- Ein Repo kann keine Rechtsgrundlage festlegen.
- Ein Repo kann keine Datenschutzhinweise fuer deine konkrete Community veroeffentlichen.
- Ein Repo kann keine AVV/DPA mit Hostern oder Drittanbietern abschliessen.
- Ein Repo kann nicht beweisen, dass deine Firewall, Backups und Admin-Prozesse wirklich so betrieben werden.
- Ein Repo kann nicht entscheiden, ob in deinem konkreten Szenario eine DPIA oder ein Datenschutzbeauftragter noetig ist.

## Freigabeempfehlung

Vor dem ersten Live-Betrieb sollte der Betreiber diese Reihenfolge abarbeiten:

1. `docs/VERZEICHNIS_VERARBEITUNGSTAETIGKEITEN.md` ausfuellen.
2. `docs/TOM_CHECKLISTE.md` abarbeiten.
3. Datenschutzhinweis fuer Spieler/Admins veroeffentlichen.
4. `privacy_purge` trocken ausfuehren und Ergebnis pruefen.
5. Backup-Restore testen.
6. `privacy_purge --execute` manuell testen.
7. Erst danach automatisierte Loeschung aktivieren.

## Quellen

- EU-Kommission: [Rules for business and organisations](https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations_en)
- EU-Kommission: [Controller oder Processor](https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/obligations/controllerprocessor/what-data-controller-or-data-processor_en)
- EU-Kommission: [Accountability und Compliance-Nachweis](https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/obligations/how-can-i-demonstrate-my-organisation-compliant-gdpr_en)
- EU-Kommission: [Data protection by design and default](https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/obligations/what-does-data-protection-design-and-default-mean_en)
- EU-Kommission: [Data breach und 72-Stunden-Pruefung](https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/obligations/what-data-breach-and-what-do-we-have-do-case-data-breach_en)
- EU-Kommission: [DPIA-Erforderlichkeit](https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/obligations/when-data-protection-impact-assessment-dpia-required_en)
