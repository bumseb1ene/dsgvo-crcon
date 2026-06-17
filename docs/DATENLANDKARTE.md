# Datenlandkarte

Diese Uebersicht zeigt die wichtigsten personenbezogenen oder spielerbezogenen Datenflaechen in CRCON.

| Bereich | Beispiele | Hauptspeicherort | Risiko | Massnahme |
| --- | --- | --- | --- | --- |
| Auth/Admin | Benutzername, Passwort-Hash, API-Key-Hash, Rechte | Django-Tabellen `auth_*`, `api_djangoapikey` | Admin-Kompromittierung | individuelle Konten, minimale Rechte, HTTPS |
| Spielerkennung | Steam64/EOS/Windows-ID, Aliasnamen | `steam_id_64`, `player_names`, `player_soldier`, `player_account` | dauerhafte Wiedererkennbarkeit | Fristen, Auskunftsprozess, kein unnoetiger Export |
| Live-/Game-Logs | Chat, Kills, Teamkills, Admin-Aktionen, Raw Logline | `log_lines`, `/logs/*.log` | hoher Kontextbezug | kurze Logfrist, Webhook-Minimierung |
| Sessions | Join/Leave-Zeiten, Servername | `player_sessions` | Bewegungsprofil im Serverkontext | Fristenloeschung |
| Statistiken | Matchleistung, K/D, Waffen, Level, Name | `player_stats`, `map_history` | Profilbildung | begrenzte Aufbewahrung |
| Moderation | Kicks, Bans, Messages, Gruende, Admin | `players_actions`, `blacklist_record`, `player_comments`, `player_flags`, `player_watchlist` | sensible Bewertungen | Need-to-know, getrennte Fristen, aktive Faelle behalten |
| VIP/Adminlisten | VIP-Status, Ablauf, Adminrollen | `player_vip`, RCON-Antworten, Config | Mitgliedschaft/Privilegien | Zugriff beschraenken |
| Steam-Cache | Profil, Land, Ban-Informationen | `steam_info` | externe Anreicherung | Cron deaktiviert, Zweck dokumentieren |
| Webhooks | Discord-Nachrichten und Queues | Redis, Discord, Webhook-Konfig | Drittland-/Plattformtransfer je nach Setup | nur notwendige Webhooks, AVV/DPA pruefen |
| Fehlertelemetrie | Stacktraces, Breadcrumbs | Sentry, falls aktiviert | externe Uebermittlung | standardmaessig keine PII |

## Standard-Datenfluesse

1. CRCON liest RCON-Daten vom HLL-Server.
2. Backend speichert Betriebsdaten in Postgres und kurzlebige Queues/Caches in Redis.
3. Frontend zeigt Daten nur nach Login und Berechtigung.
4. Optional senden Webhook- und Sentry-Integrationen Daten an externe Dienste.
5. `privacy_purge` entfernt alte Daten nach den konfigurierten Fristen.

## Nicht in dieses Repo committen

- `.env` mit echten Passwoertern
- Datenbank-Dumps
- `/logs`
- Discord-Webhook-URLs
- Sentry-DSNs
- Steam API Keys
- Screenshots mit Spielerlisten oder Chat
