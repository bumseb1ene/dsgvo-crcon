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
