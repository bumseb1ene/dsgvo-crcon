# Anbieter- und AVV-Register

Stand: 2026-06-17

Dieses Register ist fuer alle externen Anbieter auszufuellen, die im CRCON-Betrieb personenbezogene oder spielerbezogene Daten verarbeiten koennen. Es ersetzt keine Rechtsberatung und keinen Vertrag.

## Pruefliste pro Anbieter

| Frage | Antwort |
| --- | --- |
| Ist der Anbieter Verantwortlicher, Auftragsverarbeiter oder gemeinsamer Verantwortlicher? | TODO |
| Welche Daten gehen an den Anbieter? | TODO |
| In welchem Land oder welcher Region wird verarbeitet? | TODO |
| Gibt es einen AVV/DPA oder eine andere passende Vereinbarung? | TODO |
| Gibt es Unterauftragsverarbeiter? | TODO |
| Gibt es Drittlandtransfer ausserhalb EU/EWR? | TODO |
| Gibt es Standardvertragsklauseln oder andere Schutzmassnahmen? | TODO |
| Wie lange speichert der Anbieter Daten? | TODO |
| Wie werden Daten geloescht oder exportiert? | TODO |
| Wer im Team ist fuer diesen Anbieter verantwortlich? | TODO |

## Anbieteruebersicht

| Anbieter | Rolle | Datenbezug | Zweck | Region | AVV/DPA | Drittlandpruefung | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TODO Hosting/VPS | TODO | Datenbank, Logs, Backups, Runtime | Betrieb CRCON | TODO | TODO | TODO | offen |
| TODO DNS/Reverse Proxy | TODO | Hostname, ggf. IP/Request-Metadaten | Erreichbarkeit/TLS | TODO | TODO | TODO | offen |
| Discord | TODO | Webhook-Nachrichten mit Spieler-/Chat-/Moderationsbezug, falls aktiv | Benachrichtigung | TODO | TODO | TODO | offen |
| Sentry | TODO | Fehlerkontext, Breadcrumbs, technische Metadaten, falls aktiv | Fehleranalyse | TODO | TODO | TODO | offen |
| Steam API | TODO | Steam-ID, Profil, Land, Ban-Informationen, falls aktiv | Profil-/Ban-Anreicherung | TODO | TODO | TODO | offen |
| Backup-Ziel | TODO | Datenbank-Dumps, Logs, Konfiguration | Wiederherstellung | TODO | TODO | TODO | offen |
| Mail/Ticket/Support | TODO | Supportdaten, Spieler-IDs, Screenshots, falls genutzt | Anfragebearbeitung | TODO | TODO | TODO | offen |
| GitHub | TODO | Code, Issues, ggf. keine Produktivdaten | Quellcodeverwaltung | TODO | TODO | TODO | offen |

## Anbieterentscheidung dokumentieren

Kopiere diesen Block je Anbieter:

```text
Anbieter:
Dienst:
Rolle:
Verarbeitete Daten:
Zweck:
Region:
Vertragsdokument/AVV/DPA:
Unterauftragsverarbeiter geprueft am:
Drittlandtransfer:
Schutzmassnahmen:
Konfiguration zur Minimierung:
Speicher-/Loeschfrist:
Risikoentscheidung:
Freigegeben durch:
Freigegeben am:
Review am:
```

## CRCON-spezifische Hinweise

- Discord-Webhooks koennen personenbezogene Inhalte enthalten, wenn Chat, Spielernamen, IDs oder Moderationsgruende gepostet werden.
- Sentry bleibt in dieser Repo-Variante standardmaessig ohne Default-PII; trotzdem koennen Fehlerkontexte sensible Werte enthalten, wenn Code oder Konfiguration sie mitschicken.
- Steam API ist in der DSGVO-Baseline nicht automatisch per Cron aktiv. Erst aktivieren, wenn Zweck, Rechtsgrundlage und Hinweistext dokumentiert sind.
- Backups sind nicht nur ein technisches Thema: Wenn personenbezogene Daten aus der Datenbank gesichert werden, muss die Backup-Frist zum Loeschkonzept passen.
- GitHub sollte keine `.env`, Logs, Datenbank-Dumps, Screenshots mit Spielerlisten oder Webhook-URLs enthalten.

## Mindestfreigabe vor Aktivierung

- [ ] Anbieter im Register angelegt.
- [ ] Rolle geklaert: Verantwortlicher, Auftragsverarbeiter oder gemeinsamer Verantwortlicher.
- [ ] AVV/DPA oder passende Alternative dokumentiert.
- [ ] Drittlandtransfer geprueft.
- [ ] Datenminimierung in CRCON-Konfiguration umgesetzt.
- [ ] Speicher- und Loeschfristen dokumentiert.
- [ ] Review-Termin gesetzt.

## Quellen fuer die Betreiberpruefung

- EU-Kommission: [Controller oder Processor](https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/obligations/controllerprocessor/what-data-controller-or-data-processor_en)
