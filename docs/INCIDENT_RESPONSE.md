# Incident-Response fuer Datenschutzvorfaelle

Stand: 2026-06-17

Diese Vorlage beschreibt, wie ein CRCON-Betreiber einen moeglichen Datenschutzvorfall strukturiert prueft. Sie ersetzt keine Rechtsberatung.

## Was als Vorfall zaehlt

Ein Vorfall kann insbesondere vorliegen, wenn Vertraulichkeit, Verfuegbarkeit oder Integritaet von CRCON-Daten betroffen ist, zum Beispiel:

- `.env`, Datenbank-Dump, Backup oder Logdatei wurde oeffentlich.
- Discord-Webhook oder Sentry hat mehr Spieler-/Chatdaten gesendet als geplant.
- Admin-Konto, API-Key, SSH-Key oder RCON-Passwort wurde kompromittiert.
- Datenbank oder Backup wurde geloescht, verschluesselt oder unberechtigt veraendert.
- Falsche Rollen haben Zugriff auf Spielerprofile, Logs, Chat oder Moderationsdaten.
- Ein Screenshot oder Export mit Spielerlisten, Chat oder IDs wurde extern geteilt.

## Sofortmassnahmen

1. Uhrzeit des Bekanntwerdens notieren.
2. Zugriff begrenzen, ohne Beweise unnoetig zu zerstoeren.
3. Betroffene Secrets rotieren: `HLL_PASSWORD`, `HLL_DB_PASSWORD`, `RCONWEB_API_SECRET`, Webhook-URLs, API-Keys, SSH-Keys.
4. Betroffene Webhooks, Tokens oder Admin-Konten deaktivieren.
5. Relevante Logs und Konfiguration sichern.
6. Verantwortlichen und Datenschutzkontakt informieren.
7. Risiko fuer betroffene Personen einschaetzen.

## 72-Stunden-Pruefung

Wenn ein Vorfall wahrscheinlich ein Risiko fuer Rechte und Freiheiten betroffener Personen darstellt, kann eine Meldung an die Aufsichtsbehoerde ohne unnoetige Verzoegerung und spaetestens binnen 72 Stunden nach Bekanntwerden erforderlich sein. Bei hohem Risiko muessen betroffene Personen eventuell ebenfalls informiert werden.

## Bewertungsbogen

| Feld | Eintrag |
| --- | --- |
| Incident-ID | TODO |
| Bekannt geworden am/um | TODO |
| Entdeckt durch | TODO |
| Kurzbeschreibung | TODO |
| Betroffene Systeme | CRCON / Postgres / Redis / Discord / Sentry / Backup / Hosting / TODO |
| Betroffene Daten | TODO |
| Betroffene Personen | Spieler / Admins / Moderatoren / TODO |
| Zeitraum | TODO |
| Vertraulichkeit betroffen | ja / nein / unklar |
| Integritaet betroffen | ja / nein / unklar |
| Verfuegbarkeit betroffen | ja / nein / unklar |
| Risiko fuer Personen | niedrig / mittel / hoch / unklar |
| Meldung an Aufsicht noetig | ja / nein / pruefen |
| Betroffene informieren | ja / nein / pruefen |
| Rechtsberatung eingebunden | ja / nein / TODO |
| Entscheidung durch | TODO |

## Technische Checkliste

- [ ] GitHub auf versehentliche Secrets, `.env`, Dumps, Logs, Screenshots pruefen.
- [ ] VPS-Dateirechte und offene Ports pruefen.
- [ ] Admin-Liste und API-Keys pruefen.
- [ ] Discord-Webhooks deaktivieren oder rotieren.
- [ ] Sentry-Projekt und Events pruefen, falls aktiv.
- [ ] Backups auf Integritaet und Zugriff pruefen.
- [ ] `privacy_purge` nicht blind ausfuehren, solange Beweissicherung noetig ist.
- [ ] Nach Stabilisierung Root Cause und dauerhafte Massnahmen dokumentieren.

## Kommunikationsvorlage intern

```text
Betreff: CRCON Datenschutzvorfall pruefen

Bekannt geworden:
Betroffene Systeme:
Moegliche Daten:
Aktueller Status:
Sofortmassnahmen:
Naechste Entscheidung bis:
Verantwortlich:
```

## Abschluss

| Feld | Eintrag |
| --- | --- |
| Ursache | TODO |
| Dauerhafte Massnahmen | TODO |
| Secrets rotiert | TODO |
| Anbieter informiert | TODO |
| Aufsicht informiert | TODO |
| Betroffene informiert | TODO |
| Dokumentation abgelegt | TODO |
| Review-Termin | TODO |

## Quellen fuer die Betreiberpruefung

- EU-Kommission: [Data breach und 72-Stunden-Pruefung](https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/obligations/what-data-breach-and-what-do-we-have-do-case-data-breach_en)
