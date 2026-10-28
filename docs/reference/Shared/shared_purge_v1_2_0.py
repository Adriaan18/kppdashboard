# shared.purge
# Author:  Adriaan
# Version: 1.2.0  (2026-10-28)
# Scope:   Gateway scope, Jython 2.7. Project Library script  shared/purge.
#          Scheduled gateway event "Retention Purge" (cron 30 3 * * *  = daily 03:30), body only:
#              shared.purge.run()
#
# MASTER data-retention purge. Every purge lives in JOBS below - add new ones there, nowhere else, so one event owns
# all retention (same single-owner rule as the matview refresh).
#   kind "table"  batched DELETE of rows older than "keep" on column "ts", 5,000 rows a statement by "key"
#                 (short locks; the capture timers keep writing). Cutoff: timestamp (no zone) columns are NZ local,
#                 timestamptz columns use now(), date columns current_date.
#   kind "nq"     a named query that deletes by itself and returns the row count (e.g. Workmate Diag_Purge);
#                 optional hooks "after": f(rows) on success, "on_error": f(message) on failure
#   kind "call"   a project library function f(dry) returning the rows deleted - "func": lambda dry: pkg.mod.purge(dry)
# A job runs only when "live" is True. Add a new job with live False, check it with run(dry=True) in the Script
# Console, then set live True. One row per job per run goes to public.purge_log (created on the first run).
#
# Console (Designer Script Console)
#   shared.purge.run(dry=True)     every job: cutoff and rows that would go - nothing deleted
#   shared.purge.run()             the real run (what the scheduled event does)
#   shared.purge.log(10)           the last 10 purge_log rows
#
# History
#   1.0.0  first issue - COS Watch cuts and marks (2 months); Workmate Diag_Log prepared, not live
#   1.1.0  Workmate Diag_Log LIVE (takes over from the scheduled event DiagRetentionPurge - disable that one in the
#          same save). It still writes its own line into Diag_Log through workmate.diag, as the old event did.
#   1.2.0  HMI alarm history (alarm.hmi_history, forensics.alarmHistory) - keep 30 days. A new table: nothing goes
#          until it is a month old (the engine never writes an alarm older than 30 days); run(dry=True) shows 0 rows.

import re
from java.lang import System, Throwable

SCRIPT_VERSION = "1.2.0"
DB       = "KPP_production"
DRY_RUN  = False          # module-wide override; the console uses run(dry=True)
BATCH    = 5000
MAX_BATCHES = 400         # per job per run = 2,000,000 rows; the rest goes the next night
ZONE     = "Pacific/Auckland"

JOBS = [
    {"name": "COS Watch cuts", "kind": "table", "table": "kppstems.cos_watch", "ts": "event_ts", "key": "id",
     "keep": "2 months", "live": True},
    {"name": "COS Watch marks", "kind": "table", "table": "kppstems.cos_watch_mark", "ts": "mark_ts", "key": "id",
     "keep": "2 months", "live": True},
    # Took over from the scheduled event DiagRetentionPurge (Workmate Diag_Log, 30 days) - that event is disabled.
    {"name": "Workmate Diag_Log", "kind": "nq", "path": "Workmate/Diag/Diag_Purge", "params": {"days": 30},
     "live": True,
     "after": lambda n: workmate.diag.log("Diag", "retention purge: %s rows older than 30 days deleted (shared.purge)" % n),
     "on_error": lambda msg: workmate.diag.error(None, "Diag", "retention purge FAILED (shared.purge): %s" % msg)},
    # HMI alarm history - booth Alarms popup HISTORY tab and the AI box (forensics.alarmHistory 1.0.0)
    {"name": "HMI alarm history", "kind": "table", "table": "alarm.hmi_history", "ts": "event_ts", "key": "id",
     "keep": "30 days", "live": True},
]

_log = system.util.getLogger("shared.purge")
RX_TABLE = re.compile(r"^[a-z_][a-z0-9_]*\.[a-z_][a-z0-9_]*$")
RX_COL = re.compile(r"^[a-z_][a-z0-9_]*$")
RX_KEEP = re.compile(r"^[1-9][0-9]{0,2} (day|days|week|weeks|month|months|year|years)$")

LOG_DDL = """CREATE TABLE IF NOT EXISTS public.purge_log (
    id             bigserial PRIMARY KEY,
    run_ts         timestamptz NOT NULL DEFAULT now(),
    job            text NOT NULL,
    target         text,
    cutoff         text,
    rows_deleted   bigint,
    batches        integer,
    ms             integer,
    dry            boolean,
    status         text,
    message        text,
    script_version text
)"""
LOG_SQL = """INSERT INTO public.purge_log (job, target, cutoff, rows_deleted, batches, ms, dry, status, message, script_version)
 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""


def _now():
    return System.currentTimeMillis()


def _q(sql):
    import system
    return system.db.runQuery(sql, DB)


def _cutoff_expr(job):
    """SQL expression for the cutoff, matched to the column type. Raises on a bad job definition."""
    table, ts, keep = job["table"], job["ts"], job["keep"]
    if not RX_TABLE.match(table) or not RX_COL.match(ts) or not RX_COL.match(job.get("key", "id")) or not RX_KEEP.match(keep):
        raise ValueError("bad job definition (table / column / keep)")
    schema, name = table.split(".")
    ds = _q("SELECT data_type FROM information_schema.columns WHERE table_schema = '%s' AND table_name = '%s' "
            "AND column_name = '%s'" % (schema, name, ts))
    if ds.getRowCount() == 0:
        raise ValueError("column %s.%s not found" % (table, ts))
    dt = str(ds.getValueAt(0, 0))
    if "with time zone" in dt:
        base = "now()"
    elif dt == "date":
        base = "current_date"
    elif dt.startswith("timestamp"):
        base = "(now() AT TIME ZONE '%s')" % ZONE
    else:
        raise ValueError("column %s.%s is %s, not a date or timestamp" % (table, ts, dt))
    return "(%s - interval '%s')" % (base, keep)


def _table_job(job, dry):
    import system
    expr = _cutoff_expr(job)
    t, ts, key = job["table"], job["ts"], job.get("key", "id")
    ds = _q("SELECT %s, count(*), min(%s) FROM %s WHERE %s < %s" % (expr, ts, t, ts, expr))
    cutoff, waiting, oldest = str(ds.getValueAt(0, 0)), int(ds.getValueAt(0, 1)), ds.getValueAt(0, 2)
    if dry:
        return {"cutoff": cutoff, "rows": waiting, "batches": 0,
                "message": "would delete %d rows (oldest %s)" % (waiting, str(oldest))}
    sql = "DELETE FROM %s WHERE %s IN (SELECT %s FROM %s WHERE %s < %s ORDER BY %s LIMIT %d)" % (
        t, key, key, t, ts, expr, key, BATCH)
    total, batches = 0, 0
    while batches < MAX_BATCHES:
        n = system.db.runUpdateQuery(sql, DB)
        batches += 1
        total += n
        if n < BATCH:
            break
    left = max(0, waiting - total)
    msg = "deleted %d rows in %d batches" % (total, batches)
    if batches >= MAX_BATCHES:
        msg += " - batch cap reached, about %d left for the next run" % left
    return {"cutoff": cutoff, "rows": total, "batches": batches, "message": msg}


def _nq_job(job, dry):
    import system
    if dry:
        return {"cutoff": str(job.get("params")), "rows": None, "batches": 0,
                "message": "named query - no dry run; would run %s" % job["path"]}
    try:
        n = system.db.runNamedQuery(job["path"], job.get("params", {}))
    except:
        n = system.db.runNamedQuery(system.util.getProjectName(), job["path"], job.get("params", {}))
    msg = "named query %s" % job["path"]
    if job.get("after"):
        try:
            job["after"](n)
        except:
            msg += " (after-hook failed)"
    return {"cutoff": str(job.get("params")), "rows": n, "batches": 1, "message": msg}


def _call_job(job, dry):
    n = job["func"](dry)
    return {"cutoff": "", "rows": n, "batches": 1, "message": "function"}


def _write_log(job, res, ms, dry, status):
    import system
    try:
        target = job.get("table") or job.get("path") or job["name"]
        rows = res.get("rows")
        system.db.runPrepUpdate(LOG_SQL, [job["name"], target, res.get("cutoff"), None if rows is None else long(rows),
                                          res.get("batches"), int(ms), bool(dry), status, (res.get("message") or "")[:500],
                                          SCRIPT_VERSION], DB)
    except Throwable, t:
        _log.warn("purge_log insert failed: %s" % str(t)[:200])
    except Exception, e:
        _log.warn("purge_log insert failed: %s" % str(e)[:200])


def run(dry=None):
    """Every job once. Safe to run again at any time. Returns one result dict per job."""
    import system
    if dry is None:
        dry = DRY_RUN
    try:
        system.db.runUpdateQuery(LOG_DDL, DB)
    except Throwable, t:
        _log.warn("purge_log create failed: %s" % str(t)[:200])
    except Exception, e:
        _log.warn("purge_log create failed: %s" % str(e)[:200])
    out = []
    for job in JOBS:
        t0 = _now()
        if not job.get("live") and not dry:
            res, status = {"cutoff": None, "rows": None, "batches": 0, "message": "not live - skipped"}, "skip"
        else:
            try:
                kind = job.get("kind")
                if kind == "table":
                    res = _table_job(job, dry)
                elif kind == "nq":
                    res = _nq_job(job, dry)
                elif kind == "call":
                    res = _call_job(job, dry)
                else:
                    raise ValueError("unknown kind %s" % str(kind))
                status = "dry" if dry else "ok"
            except Throwable, t:
                res, status = {"cutoff": None, "rows": None, "batches": 0, "message": str(t)[:400]}, "error"
            except Exception, e:
                res, status = {"cutoff": None, "rows": None, "batches": 0, "message": str(e)[:400]}, "error"
        ms = _now() - t0
        if status == "error" and job.get("on_error"):
            try:
                job["on_error"](res.get("message"))
            except:
                pass
        line = "purge v%s %-20s %-5s %s | cutoff %s | %s ms" % (SCRIPT_VERSION, job["name"], status,
                                                              res.get("message"), str(res.get("cutoff")), ms)
        if status == "error":
            _log.warn(line)
        else:
            _log.info(line)
        print line
        if status != "skip" or not dry:
            _write_log(job, res, ms, dry, status)
        out.append(dict(res, job=job["name"], status=status))
    return out


def log(n=10):
    """The last n purge_log rows."""
    ds = _q("SELECT run_ts, job, status, rows_deleted, batches, ms, cutoff, message FROM public.purge_log "
            "ORDER BY id DESC LIMIT %d" % max(1, min(200, int(n))))
    for r in range(ds.getRowCount()):
        print "%s | %-20s %-5s | rows %s | batches %s | %s ms | cutoff %s | %s" % tuple(
            [str(ds.getValueAt(r, c)) for c in range(8)])