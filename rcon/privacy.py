from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Iterable

from sqlalchemy import text
from sqlalchemy.orm import Session


@dataclass(frozen=True)
class RetentionResult:
    label: str
    rows: int
    cutoff: datetime
    action: str


def _cutoff(days: int) -> datetime:
    return datetime.now(tz=timezone.utc) - timedelta(days=days)


def _count_or_delete(
    sess: Session,
    *,
    label: str,
    where_sql: str,
    params: dict,
    dry_run: bool,
    delete_sql: str | None = None,
) -> RetentionResult:
    count_sql = f"SELECT COUNT(*) FROM {where_sql}"
    rows = int(sess.execute(text(count_sql), params).scalar() or 0)

    if not dry_run and rows:
        sess.execute(text(delete_sql or f"DELETE FROM {where_sql}"), params)

    return RetentionResult(
        label=label,
        rows=rows,
        cutoff=params["cutoff"],
        action="would delete" if dry_run else "deleted",
    )


def _inactive_player_candidates_sql() -> str:
    return """
        SELECT p.id
        FROM steam_id_64 p
        WHERE p.created < :cutoff
          AND NOT EXISTS (
            SELECT 1 FROM player_names pn
            WHERE pn.playersteamid_id = p.id
              AND COALESCE(pn.last_seen, pn.created) >= :cutoff
          )
          AND NOT EXISTS (
            SELECT 1 FROM player_sessions ps
            WHERE ps.playersteamid_id = p.id
              AND COALESCE(ps."end", ps.start, ps.created) >= :cutoff
          )
          AND NOT EXISTS (
            SELECT 1 FROM players_actions pa
            WHERE pa.playersteamid_id = p.id
              AND pa.time >= :cutoff
          )
          AND NOT EXISTS (
            SELECT 1 FROM player_comments pc
            WHERE pc.playersteamid_id = p.id
              AND pc.creation_time >= :cutoff
          )
          AND NOT EXISTS (
            SELECT 1 FROM steam_info si
            WHERE si.playersteamid_id = p.id
              AND COALESCE(si.updated, si.created) >= :cutoff
          )
          AND NOT EXISTS (
            SELECT 1 FROM player_soldier psd
            WHERE psd.playersteamid_id = p.id
              AND psd.updated >= :cutoff
          )
          AND NOT EXISTS (
            SELECT 1 FROM player_account pacct
            WHERE pacct.playersteamid_id = p.id
              AND pacct.updated >= :cutoff
          )
          AND NOT EXISTS (
            SELECT 1 FROM player_optins po
            WHERE po.playersteamid_id = p.id
              AND po.modified >= :cutoff
          )
          AND NOT EXISTS (
            SELECT 1 FROM log_lines ll
            WHERE (ll.player1_steamid = p.id OR ll.player2_steamid = p.id)
              AND ll.event_time >= :cutoff
          )
          AND NOT EXISTS (
            SELECT 1 FROM player_at_count pac
            JOIN server_counts sc ON sc.id = pac.servercount_id
            WHERE pac.playersteamid_id = p.id
              AND sc.datapoint_time >= :cutoff
          )
          AND NOT EXISTS (
            SELECT 1 FROM player_stats pst
            JOIN map_history mh ON mh.id = pst.map_id
            WHERE pst.playersteamid_id = p.id
              AND COALESCE(mh."end", mh.start, mh.creation_time) >= :cutoff
          )
          AND NOT EXISTS (
            SELECT 1 FROM blacklist_record br
            WHERE br.player_id_id = p.id
              AND (
                br.expires_at IS NULL
                OR br.expires_at >= :cutoff
                OR br.created_at >= :cutoff
              )
          )
          AND NOT EXISTS (
            SELECT 1 FROM player_vip pv
            WHERE pv.playersteamid_id = p.id
              AND pv.expiration >= :cutoff
          )
          AND NOT EXISTS (
            SELECT 1 FROM player_watchlist pw
            WHERE pw.playersteamid_id = p.id
              AND (pw.is_watched IS TRUE OR pw.modified >= :cutoff)
          )
          AND NOT EXISTS (
            SELECT 1 FROM player_flags pf
            WHERE pf.playersteamid_id = p.id
          )
    """


def _purge_inactive_player_profiles(
    sess: Session,
    *,
    dry_run: bool,
    inactive_player_days: int,
) -> list[RetentionResult]:
    cutoff = _cutoff(inactive_player_days)
    params = {"cutoff": cutoff}
    candidates = _inactive_player_candidates_sql()

    dependent_rules = [
        (
            "inactive profile log lines",
            "log_lines WHERE player1_steamid IN ({ids}) OR player2_steamid IN ({ids})",
        ),
        (
            "inactive profile population snapshots",
            "player_at_count WHERE playersteamid_id IN ({ids})",
        ),
        (
            "inactive profile match statistics",
            "player_stats WHERE playersteamid_id IN ({ids})",
        ),
        (
            "inactive profile moderation actions",
            "players_actions WHERE playersteamid_id IN ({ids})",
        ),
        (
            "inactive profile comments",
            "player_comments WHERE playersteamid_id IN ({ids})",
        ),
        (
            "inactive profile sessions",
            "player_sessions WHERE playersteamid_id IN ({ids})",
        ),
        (
            "inactive profile Steam cache",
            "steam_info WHERE playersteamid_id IN ({ids})",
        ),
        (
            "inactive profile expired blacklist records",
            "blacklist_record WHERE player_id_id IN ({ids})",
        ),
        (
            "inactive profile expired VIP rows",
            "player_vip WHERE playersteamid_id IN ({ids})",
        ),
        (
            "inactive profile opt-ins",
            "player_optins WHERE playersteamid_id IN ({ids})",
        ),
        (
            "inactive profile non-watched watchlist rows",
            "player_watchlist WHERE playersteamid_id IN ({ids})",
        ),
        (
            "inactive profile soldier details",
            "player_soldier WHERE playersteamid_id IN ({ids})",
        ),
        (
            "inactive profile account details",
            "player_account WHERE playersteamid_id IN ({ids})",
        ),
        (
            "inactive profile aliases",
            "player_names WHERE playersteamid_id IN ({ids})",
        ),
    ]

    results: list[RetentionResult] = []
    for label, where_template in dependent_rules:
        where_sql = where_template.format(ids=candidates)
        results.append(
            _count_or_delete(
                sess,
                label=label,
                where_sql=where_sql,
                params=params,
                dry_run=dry_run,
            )
        )

    results.append(
        _count_or_delete(
            sess,
            label="inactive player identity rows",
            where_sql=f"steam_id_64 WHERE id IN ({candidates})",
            params=params,
            dry_run=dry_run,
        )
    )

    return results


def purge_old_personal_data(
    sess: Session,
    *,
    dry_run: bool = True,
    logs_days: int = 30,
    audit_days: int = 365,
    actions_days: int = 365,
    comments_days: int = 365,
    sessions_days: int = 180,
    population_days: int = 90,
    stats_days: int = 365,
    steam_days: int = 180,
    expired_blacklists_days: int = 365,
    inactive_player_days: int = 0,
) -> list[RetentionResult]:
    """Delete old personal or player-linkable data according to configured windows.

    This intentionally avoids active VIP, watchlist, flags, comments inside the
    selected window, and non-expiring blacklist records. Run with dry_run=True
    first and capture the output for the deletion log.
    """

    results: list[RetentionResult] = []

    rules = [
        (
            "raw/structured game logs",
            "log_lines WHERE event_time < :cutoff",
            {"cutoff": _cutoff(logs_days)},
        ),
        (
            "admin audit log",
            "audit_log WHERE creation_time < :cutoff",
            {"cutoff": _cutoff(audit_days)},
        ),
        (
            "player moderation actions",
            "players_actions WHERE time < :cutoff",
            {"cutoff": _cutoff(actions_days)},
        ),
        (
            "player comments",
            "player_comments WHERE creation_time < :cutoff",
            {"cutoff": _cutoff(comments_days)},
        ),
        (
            "player sessions",
            'player_sessions WHERE COALESCE("end", start, created) < :cutoff',
            {"cutoff": _cutoff(sessions_days)},
        ),
        (
            "old Steam profile/cache data",
            "steam_info WHERE COALESCE(updated, created) < :cutoff",
            {"cutoff": _cutoff(steam_days)},
        ),
        (
            "expired blacklist records",
            "blacklist_record WHERE expires_at IS NOT NULL AND expires_at < :cutoff",
            {"cutoff": _cutoff(expired_blacklists_days)},
        ),
    ]

    for label, where_sql, params in rules:
        results.append(
            _count_or_delete(
                sess,
                label=label,
                where_sql=where_sql,
                params=params,
                dry_run=dry_run,
            )
        )

    population_cutoff = _cutoff(population_days)
    population_params = {"cutoff": population_cutoff}
    results.append(
        _count_or_delete(
            sess,
            label="per-player population snapshots",
            where_sql=(
                "player_at_count WHERE servercount_id IN "
                "(SELECT id FROM server_counts WHERE datapoint_time < :cutoff)"
            ),
            params=population_params,
            dry_run=dry_run,
        )
    )
    results.append(
        _count_or_delete(
            sess,
            label="server population aggregates",
            where_sql="server_counts WHERE datapoint_time < :cutoff",
            params=population_params,
            dry_run=dry_run,
        )
    )

    stats_cutoff = _cutoff(stats_days)
    stats_params = {"cutoff": stats_cutoff}
    results.append(
        _count_or_delete(
            sess,
            label="per-player match statistics",
            where_sql=(
                "player_stats WHERE map_id IN "
                "(SELECT id FROM map_history WHERE COALESCE(\"end\", start, creation_time) < :cutoff)"
            ),
            params=stats_params,
            dry_run=dry_run,
        )
    )
    results.append(
        _count_or_delete(
            sess,
            label="population snapshots for expired match history",
            where_sql=(
                "player_at_count WHERE servercount_id IN "
                "(SELECT sc.id FROM server_counts sc "
                "JOIN map_history mh ON mh.id = sc.map_id "
                "WHERE COALESCE(mh.\"end\", mh.start, mh.creation_time) < :cutoff)"
            ),
            params=stats_params,
            dry_run=dry_run,
        )
    )
    results.append(
        _count_or_delete(
            sess,
            label="population aggregates for expired match history",
            where_sql=(
                "server_counts WHERE map_id IN "
                "(SELECT id FROM map_history WHERE COALESCE(\"end\", start, creation_time) < :cutoff)"
            ),
            params=stats_params,
            dry_run=dry_run,
        )
    )
    results.append(
        _count_or_delete(
            sess,
            label="match history aggregates",
            where_sql='map_history WHERE COALESCE("end", start, creation_time) < :cutoff',
            params=stats_params,
            dry_run=dry_run,
        )
    )

    if inactive_player_days > 0:
        results.extend(
            _purge_inactive_player_profiles(
                sess,
                dry_run=dry_run,
                inactive_player_days=inactive_player_days,
            )
        )

    if not dry_run:
        sess.commit()

    return results


def format_retention_results(results: Iterable[RetentionResult]) -> str:
    lines = []
    for result in results:
        cutoff = result.cutoff.isoformat(timespec="seconds")
        lines.append(
            f"{result.action}: {result.rows} row(s) from {result.label} older than {cutoff}"
        )
    return "\n".join(lines)
