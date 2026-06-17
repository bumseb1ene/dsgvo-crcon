# Prozess fuer Betroffenenrechte

Stand: 2026-06-17

Diese Vorlage hilft dabei, Auskunfts-, Loesch-, Einschraenkungs- oder Berichtigungsanfragen zu CRCON-Daten strukturiert zu bearbeiten. Sie ist keine Rechtsberatung.

## Eingang erfassen

| Feld | Eintrag |
| --- | --- |
| Eingangsdatum | TODO |
| Anfrageart | Auskunft / Loeschung / Berichtigung / Einschraenkung / Widerspruch |
| Kontaktweg | TODO |
| Betroffene Person | TODO |
| Bekannte Spielernamen | TODO |
| Steam64/EOS/Windows-ID | TODO |
| Server/Zeitraum | TODO |
| Bearbeiter | TODO |
| Frist | TODO |

## Identitaet und Zuordnung

Vor einer Antwort muss die Anfrage plausibel einer Person oder einem Spielerprofil zugeordnet werden. Je nach Community-Prozess kann das ueber bekannte IDs, Serverregeln, Discord-Verifikation oder einen anderen dokumentierten Weg erfolgen.

Nicht unkritisch herausgeben:

- Daten anderer Spieler aus Chat oder Logs.
- Admin-interne Bewertungen, soweit sie Rechte Dritter oder laufende Moderation betreffen.
- Secrets, interne IPs, API-Keys oder Sicherheitsdetails.

## Datenstellen in CRCON pruefen

| Bereich | Beispiele | Vorgehen |
| --- | --- | --- |
| Spielerkennung | IDs, Aliasnamen | Suche nach Steam64/EOS/Windows-ID und bekannten Namen |
| Logs | Chat, Kills, Teamkills, Admin-Aktionen | Zeitraum eingrenzen, Drittdaten minimieren |
| Sessions | Join/Leave, Servername | relevante Zeitraeume exportieren oder zusammenfassen |
| Statistiken | Match- und Spielerwerte | Personenbezug pruefen, ggf. Auszug erstellen |
| Moderation | Kicks, Bans, Kommentare, Flags, Watchlist | aktive Faelle und Aufbewahrungsgrund pruefen |
| VIP/Admin | VIPs, Rollen, Adminrechte | nur eigene Daten der betroffenen Person |
| Externe Systeme | Discord, Sentry, Backups | Anbieter/Logs separat pruefen |

## Auskunft bearbeiten

1. Anfrage erfassen.
2. Identitaet und Spielerzuordnung pruefen.
3. Relevante CRCON-Datenstellen durchsuchen.
4. Drittdaten minimieren oder schwaerzen.
5. Rechtsgrundlagen, Zwecke, Empfaenger und Fristen aus dem VVT ergaenzen.
6. Antwort dokumentieren.

## Loeschung bearbeiten

1. Pruefen, ob aktive Moderationsgruende, Sicherheitsgruende oder gesetzliche Pflichten gegen sofortige Loeschung sprechen.
2. Wenn Loeschung moeglich ist, betroffene Datensaetze identifizieren.
3. Vorher Backup-/Restore-Konzept beachten.
4. Manuelle Loeschung oder naechsten `privacy_purge --execute`-Lauf dokumentieren.
5. Externe Ziele wie Discord, Sentry oder Exporte separat pruefen.
6. Ergebnis und Restdaten begruenden.

## Einschraenkung bearbeiten

Wenn Loeschung noch nicht moeglich ist, kann je nach Fall eine Einschraenkung notwendig sein:

- Zugriff auf den Fall begrenzen.
- Datensatz fuer normale Auswertung ausnehmen.
- Discord-/Webhook-Weitergabe stoppen.
- Review-Datum setzen.

## Antwort dokumentieren

| Feld | Eintrag |
| --- | --- |
| Entscheidung | TODO |
| Datenquellen geprueft | TODO |
| Export/Antwort erstellt am | TODO |
| Drittdaten entfernt | TODO |
| Geloeschte Daten | TODO |
| Weiter aufbewahrte Daten und Grund | TODO |
| Externe Systeme geprueft | TODO |
| Abschlussdatum | TODO |

## Testszenario fuer Betreiber

Vor Produktivbetrieb sollte einmal mit einem Testspieler geprueft werden:

1. Testspieler erzeugt Log-, Session- und Statistikdaten.
2. Betreiber fuehrt eine simulierte Auskunft durch.
3. Betreiber prueft, welche Daten geloescht werden koennen.
4. Betreiber dokumentiert die Grenzen, z. B. aktive Moderationsfaelle oder Discord-Posts.
