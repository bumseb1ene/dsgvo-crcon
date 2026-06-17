# Datenschutzhinweis-Vorlage fuer CRCON

Stand: 2026-06-17

Diese Vorlage ist fuer Website, Discord-Regeln oder Server-Regeln gedacht. Sie muss vor Veroeffentlichung an den konkreten Betreiber, die konkrete Community und die aktivierten CRCON-Funktionen angepasst werden. Sie ist keine Rechtsberatung.

## Kurzfassung fuer Server-Regeln oder Discord

Beim Spielen auf unseren Hell-Let-Loose-Servern werden technische und spielbezogene Daten in CRCON verarbeitet, damit wir den Server betreiben, Missbrauch verhindern und Regeln durchsetzen koennen. Dazu koennen Spielernamen, Steam-/EOS-/Windows-IDs, Join-/Leave-Zeiten, Chat, Kills, Teamkills, Moderationsaktionen, VIP-/Admin-Status und technische Logs gehoeren. Details, Kontakt, Rechtsgrundlagen, Speicherfristen und Rechte stehen im vollstaendigen Datenschutzhinweis: TODO_LINK.

## Vollstaendiger Hinweis

### Verantwortlicher

| Feld | Eintrag |
| --- | --- |
| Verantwortlicher | TODO |
| Anschrift | TODO |
| Kontakt | TODO |
| Datenschutzkontakt | TODO |
| Datenschutzbeauftragter, falls vorhanden | TODO |

### Wofuer wir CRCON nutzen

Wir nutzen CRCON fuer den Betrieb und die Moderation unserer Hell-Let-Loose-Server. Dazu gehoeren insbesondere:

- Serverbetrieb und technische Fehleranalyse.
- Anzeige von Live-Spielerstatus fuer berechtigte Admins.
- Durchsetzung von Server- und Community-Regeln.
- Bearbeitung von Kicks, Bans, Reports, Watchlists, VIPs und Adminrechten.
- Auswertung der Serverqualitaet, soweit aktiviert.
- Optional: Benachrichtigungen in Discord und Fehleranalyse ueber Sentry.

### Welche Daten verarbeitet werden koennen

| Bereich | Beispiele |
| --- | --- |
| Spielerkennung | Steam64-ID, EOS-ID, Windows-ID, Spielernamen, Aliasnamen |
| Spielbetrieb | Join-/Leave-Zeiten, Team, Squad, Server, Map, Match-Zeit |
| Kommunikation | Chatnachrichten und Admin-Kommunikation, soweit vom Server/CRCON verarbeitet |
| Spielereignisse | Kills, Teamkills, Rollen, Waffen, Spielstatistiken |
| Moderation | Kicks, Bans, Gruende, Kommentare, Flags, Watchlist, VIP-Status |
| Admins | Benutzername, Rollen, Rechte, Auditlog, API-Key-Hash |
| Technik | Logdateien, Fehlerkontext, IP-/Hostdaten je nach Reverse Proxy und Hosting |

### Woher die Daten kommen

- Direkt aus dem Hell-Let-Loose-Server ueber RCON.
- Aus Eingaben von Admins und Moderatoren in CRCON.
- Aus optionalen Integrationen wie Discord-Webhooks, Sentry oder Steam API.
- Aus technischen Betriebslogs des Hostings oder Reverse Proxy, falls aktiviert.

### Rechtsgrundlagen

TODO: Rechtsgrundlagen fuer den konkreten Betrieb festlegen und pruefen.

Moegliche Pruefpunkte:

- Betrieb und Sicherheit des Servers.
- Durchsetzung von Serverregeln und Community-Regeln.
- Verwaltung von Admins, VIPs und Moderationsfaellen.
- Einwilligung nur dort verwenden, wo sie wirklich freiwillig, informiert und widerrufbar ist.

### Empfaenger und externe Anbieter

| Empfaenger | Zweck | Status |
| --- | --- | --- |
| Interne Admins/Moderatoren | Betrieb, Moderation, Support | TODO |
| Hosting/VPS-Anbieter | Betrieb der CRCON-Instanz | TODO |
| Discord | Webhook-Benachrichtigungen, falls aktiviert | TODO |
| Sentry | Fehleranalyse, falls aktiviert | TODO |
| Steam API | Profil-/Ban-Anreicherung, falls aktiviert | TODO |
| Backup-Anbieter | Wiederherstellung, falls extern | TODO |

Details muessen im Anbieter- und AVV-Register dokumentiert werden.

### Drittlandtransfer

TODO: Pruefen, ob Daten ausserhalb der EU/des EWR verarbeitet werden, insbesondere bei Discord, Sentry, Hosting, Backup und Steam API. Wenn ein Drittlandtransfer stattfindet, muessen die passende Grundlage und Schutzmassnahmen dokumentiert werden.

### Speicherfristen

| Datenbereich | Beispiel-Frist | Betreiberentscheidung |
| --- | ---: | --- |
| Game-Logs und Chat | 30 Tage | TODO |
| Spieler-Sessions | 180 Tage | TODO |
| Population-Snapshots | 90 Tage | TODO |
| Match-Statistiken mit Spielerbezug | 365 Tage | TODO |
| Admin-Auditlog | 365 Tage | TODO |
| Moderationsaktionen | 365 Tage oder aktive Fallfrist | TODO |
| Steam-Profil-/Ban-Cache | 180 Tage | TODO |
| Backups | TODO | TODO |

Die technische Loeschung erfolgt ueber `privacy_purge`, sobald die Fristen freigegeben und getestet sind.

### Betroffenenrechte

Betroffene Personen koennen je nach Voraussetzungen Auskunft, Berichtigung, Loeschung, Einschraenkung, Datenuebertragbarkeit oder Widerspruch verlangen. Anfragen gehen an: TODO_KONTAKT.

Bitte gib nach Moeglichkeit bekannte Spielernamen, Steam64-/EOS-/Windows-ID, Server und ungefaehren Zeitraum an, damit wir die Daten korrekt zuordnen koennen.

### Beschwerderecht

Du hast das Recht, dich bei einer Datenschutzaufsichtsbehoerde zu beschweren. Zustaendige Behoerde: TODO.

### Automatisierte Entscheidungen

TODO: Pruefen und eintragen.

Standardannahme fuer diese Vorlage: CRCON unterstuetzt Admin- und Moderationsentscheidungen, trifft aber keine vollautomatisierten Entscheidungen mit rechtlicher oder vergleichbar erheblicher Wirkung. Wenn Bots, Auto-Bans, Auto-Kicks, Score-Regeln oder externe Automationen genutzt werden, muss dieser Abschnitt konkret angepasst werden.

### Aenderungen

Dieser Datenschutzhinweis wird aktualisiert, wenn sich Zwecke, Datenkategorien, Anbieter, Fristen oder Integrationen aendern.

## Quellen fuer die Betreiberpruefung

- EU-Kommission: [Welche Informationen muessen betroffene Personen erhalten?](https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/principles-gdpr/what-information-must-be-given-individuals-whose-data-collected_en)
- EU-Kommission: [Rules for business and organisations](https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations_en)
