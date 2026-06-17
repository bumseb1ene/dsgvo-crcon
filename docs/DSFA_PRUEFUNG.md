# DSFA-Pruefung fuer CRCON

Stand: 2026-06-17

Diese Vorlage dokumentiert, ob fuer eine konkrete CRCON-Instanz eine Datenschutz-Folgenabschaetzung (DSFA/DPIA) erforderlich ist. Sie ersetzt keine Rechtsberatung. Der Betreiber muss die Entscheidung fuer seine Community, Serverkonfiguration, Integrationen und Empfaenger selbst treffen.

## Instanz

| Feld | Eintrag |
| --- | --- |
| Community/Server | TODO |
| CRCON-Hostname | TODO |
| Verantwortlicher | TODO |
| Datenschutzkontakt | TODO |
| Technischer Betreiber | TODO |
| Pruefung erstellt am | TODO |
| Naechste Pruefung | TODO |
| Entscheidung durch | TODO |

## Kurzbeschreibung der Verarbeitung

CRCON verarbeitet je nach Konfiguration Spielerkennungen, Spielernamen, Join-/Leave-Zeiten, Chat, Kills, Teamkills, Moderationsaktionen, Admin-Auditlogs, VIP-/Admin-Status, Statistiken, optionale Discord-Webhooks, optionale Sentry-Fehlerdaten und optionale Steam-Profil-/Ban-Anreicherung.

Verweis auf VVT: `docs/VERZEICHNIS_VERARBEITUNGSTAETIGKEITEN.md`

## Schwellenpruefung

Eine DSFA ist nach der EU-Kommission erforderlich, wenn eine Verarbeitung voraussichtlich ein hohes Risiko fuer Rechte und Freiheiten natuerlicher Personen zur Folge hat. Genannt werden insbesondere systematische und umfassende Bewertungen persoenlicher Aspekte, umfangreiche Verarbeitung besonderer Kategorien personenbezogener Daten und systematische umfangreiche Ueberwachung oeffentlicher Bereiche.

| Kriterium | Bewertung | Begruendung |
| --- | --- | --- |
| Systematische und umfassende Bewertung persoenlicher Aspekte oder Profiling | ja / nein / unklar | TODO |
| Umfangreiche Verarbeitung besonderer Kategorien personenbezogener Daten | ja / nein / unklar | TODO |
| Systematische umfangreiche Ueberwachung oeffentlich zugaenglicher Bereiche | ja / nein / unklar | TODO |
| Grosse Anzahl betroffener Spieler oder sehr aktive Community | ja / nein / unklar | TODO |
| Umfangreiche Chat-/Verhaltensauswertung oder dauerhafte Spielerprofile | ja / nein / unklar | TODO |
| Oeffentliche Ranglisten, Statistiken oder Discord-Verbreitung mit Spielerbezug | ja / nein / unklar | TODO |
| Automatisierte Moderationsentscheidungen mit spuerbaren Folgen fuer Spieler | ja / nein / unklar | TODO |
| Datenuebermittlung an Drittanbieter oder Drittlaender | ja / nein / unklar | TODO |
| Verarbeitung schutzbeduerftiger Gruppen, soweit bekannt | ja / nein / unklar | TODO |
| Kombination mehrerer Datenquellen, z. B. CRCON, Discord, Steam API, Support | ja / nein / unklar | TODO |

## Risikobewertung

| Risiko | Eintritt | Auswirkung | Massnahmen | Restrisiko |
| --- | --- | --- | --- | --- |
| Unberechtigter Zugriff auf Spielerprofile, Chat oder Moderationshistorie | niedrig / mittel / hoch | niedrig / mittel / hoch | Rollen, keine Shared Accounts, Admin-Review | TODO |
| Unbeabsichtigte Veroeffentlichung von IDs, Chat oder Screenshots | niedrig / mittel / hoch | niedrig / mittel / hoch | Support-Regeln, GitHub-/Discord-Pruefung, Sensibilisierung | TODO |
| Zu lange Speicherung von Game-Logs, Statistiken oder Steam-Cache | niedrig / mittel / hoch | niedrig / mittel / hoch | `privacy_purge`, Logrotate, Backup-Fristen | TODO |
| Nicht dokumentierte Webhook-Weitergabe an Discord | niedrig / mittel / hoch | niedrig / mittel / hoch | Webhook-Minimierung, Kanalrechte, AVV-/Transferpruefung | TODO |
| Externe Fehler- oder Monitoringdaten enthalten Personenbezug | niedrig / mittel / hoch | niedrig / mittel / hoch | `SENTRY_SEND_DEFAULT_PII=false`, Anbieterpruefung | TODO |
| Betroffenenrechte koennen praktisch nicht erfuellt werden | niedrig / mittel / hoch | niedrig / mittel / hoch | Prozess testen, Datenquellenliste, Auskunfts-/Loeschfall | TODO |
| Verlust oder Offenlegung von Backups | niedrig / mittel / hoch | niedrig / mittel / hoch | Verschluesselung, Zugriffsbeschraenkung, Restore-Test | TODO |

## Entscheidung

| Feld | Eintrag |
| --- | --- |
| DSFA erforderlich | ja / nein / unklar |
| Begruendung | TODO |
| Datenschutzaufsicht vorab zu konsultieren | ja / nein / pruefen |
| Rechtsberatung / Datenschutzbeauftragter eingebunden | ja / nein / nicht vorhanden / TODO |
| Freigabe fuer Produktivbetrieb trotz Restrisiko | ja / nein |
| Bedingungen fuer Freigabe | TODO |

Wenn die Entscheidung `unklar` ist oder ein hohes Restrisiko bleibt, vor Produktivstart Datenschutzberatung einholen und keine automatisierte Loeschung oder neue Integrationen aktivieren, bis die Entscheidung dokumentiert ist.

## Review-Ausloeser

Die DSFA-Pruefung ist erneut durchzufuehren, wenn sich der Betrieb wesentlich aendert:

- neue oeffentliche Statistiken, Ranglisten oder Spielerprofile
- neue Discord-, Sentry-, Monitoring-, Support- oder Backup-Anbieter
- Steam-Anreicherung oder andere externe Datenquellen werden aktiviert
- neue automatisierte Moderations- oder Scoring-Funktionen
- deutlich groessere Community oder mehrere Server in einer gemeinsamen Instanz
- Datenschutzvorfall oder relevante Beschwerde
- wesentliche CRCON-Upstream-Aenderung an Datenmodell, Logs oder Webhooks

## Quellen

- EU-Kommission: [When is a Data Protection Impact Assessment (DPIA) required?](https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/obligations/when-data-protection-impact-assessment-dpia-required_en)
- EU-Kommission: [Rules for business and organisations](https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations_en)
