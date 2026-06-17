# TOM-Checkliste fuer CRCON

Stand: 2026-06-17

Technische und organisatorische Massnahmen muessen zum konkreten Betrieb passen. Diese Liste ist eine Betreiber-Checkliste fuer CRCON und keine Rechtsberatung.

## Zugriffskontrolle

- [ ] Keine gemeinsamen Admin-Konten.
- [ ] Jeder Admin hat nur die benoetigten CRCON-Rechte.
- [ ] Ehemalige Admins werden sofort deaktiviert.
- [ ] Monatlicher Review der Admin- und API-Key-Liste.
- [ ] Datenbankzugriff ist auf wenige technische Betreiber begrenzt.
- [ ] SSH-Zugriff ist schluesselbasiert und personengebunden.

## Netzwerk und Transport

- [ ] CRCON-Frontend ist nur ueber TLS erreichbar.
- [ ] Direkte Backend-, Redis-, Postgres- und RCON-Ports sind nicht oeffentlich offen.
- [ ] Firewall erlaubt nur notwendige Ports.
- [ ] Reverse Proxy setzt sichere Header, soweit kompatibel.
- [ ] Produktionsinstanzen nutzen eigene Hostnamen pro Community/Server.

## Secrets

- [ ] `.env` wird nicht in Git committed.
- [ ] `HLL_PASSWORD`, `HLL_DB_PASSWORD`, `RCONWEB_API_SECRET`, Webhook-URLs und API-Keys sind eindeutig pro Instanz.
- [ ] Secrets liegen nicht in Screenshots, Support-Tickets oder Chatverlaeufen.
- [ ] Rotationsprozess fuer kompromittierte Secrets ist dokumentiert.

## Logging und Datenminimierung

- [ ] `LOGGING_LEVEL=INFO` oder restriktiver.
- [ ] Debug-Logs sind in Produktion deaktiviert.
- [ ] Logrotate ist aktiv.
- [ ] Webhooks senden nur Ereignisse, die wirklich benoetigt werden.
- [ ] Steam-Profilanreicherung ist nur aktiv, wenn Zweck und Hinweistext dokumentiert sind.
- [ ] Sentry ist aus oder mit `SENTRY_SEND_DEFAULT_PII=false` und AVV/DPA dokumentiert.

## Loeschung und Aufbewahrung

- [ ] Loeschfristen sind im VVT freigegeben.
- [ ] `privacy_purge` wurde trocken getestet.
- [ ] `privacy_purge --execute` wurde manuell mit Backup getestet.
- [ ] Automatisierte Loeschung ist erst nach Freigabe aktiv.
- [ ] Backup-Aufbewahrung widerspricht den Datenbank-Loeschfristen nicht.
- [ ] Alte Exporte, Dumps und Support-Screenshots werden geloescht.

## Backups

- [ ] Backups sind verschluesselt.
- [ ] Backup-Zugriff ist beschraenkt.
- [ ] Restore wurde getestet und dokumentiert.
- [ ] Backup-Logs enthalten keine Secrets.
- [ ] Backup-Anbieter ist im VVT/AVV-Register dokumentiert.

## Incident Response

- [ ] Verantwortliche Kontaktkette ist dokumentiert.
- [ ] Verfahren fuer Passwort-/Secret-Rotation ist getestet.
- [ ] Verfahren fuer Forensik und Log-Sicherung ist dokumentiert.
- [ ] Entscheidungspfad fuer Datenschutzverletzungen ist definiert.
- [ ] 72-Stunden-Pruefung fuer meldepflichtige Datenschutzverletzungen ist bekannt.
- [ ] Kommunikationsvorlage fuer Betroffene ist vorbereitet.

## Anbieter und Auftragsverarbeitung

- [ ] Hoster/VPS-Anbieter geprueft.
- [ ] Backup-Ziel geprueft.
- [ ] Discord-Nutzung geprueft.
- [ ] Sentry oder anderes Monitoring geprueft.
- [ ] Mail-/Ticket-/Supportsysteme geprueft.
- [ ] Drittlandtransfer und Standardvertragsklauseln, falls relevant, dokumentiert.

## Regelmaessige Reviews

- [ ] Monatlich: Admins, API-Keys, Webhooks.
- [ ] Quartalsweise: VVT, TOMs, Loeschfristen, Anbieter.
- [ ] Nach jedem groesseren CRCON-Update: neue Datenfelder und neue Integrationen pruefen.
- [ ] Nach jedem Incident: Ursachenanalyse und Massnahmen aktualisieren.
