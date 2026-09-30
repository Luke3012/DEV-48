from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator
import json
import os
import sqlite3
import ctypes


SCHEMA = """
PRAGMA journal_mode=WAL;
CREATE TABLE IF NOT EXISTS progress (
    item_id TEXT PRIMARY KEY,
    item_type TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'started',
    attempts INTEGER NOT NULL DEFAULT 0,
    score INTEGER NOT NULL DEFAULT 0,
    answer TEXT NOT NULL DEFAULT '',
    hint_level INTEGER NOT NULL DEFAULT 0,
    seconds_spent INTEGER NOT NULL DEFAULT 0,
    updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    item_id TEXT,
    payload TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL
);
"""


class InstanceLock:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.acquired = False

    @staticmethod
    def _running(pid: int) -> bool:
        if pid <= 0:
            return False
        if os.name == "nt":
            # Su Windows os.kill(pid, 0) non e' un controllo innocuo in tutte
            # le versioni di Python: puo' inviare CTRL_C_EVENT e terminare il
            # processo che stiamo verificando. OpenProcess interroga invece il
            # PID senza mandare alcun segnale.
            process_query_limited_information = 0x1000
            kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
            handle = kernel32.OpenProcess(process_query_limited_information, False, pid)
            if not handle:
                return False
            kernel32.CloseHandle(handle)
            return True
        try:
            os.kill(pid, 0)
            return True
        except (OSError, ProcessLookupError, ValueError):
            return False

    def acquire(self) -> bool:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.path.exists():
            try:
                pid = int(self.path.read_text(encoding="utf-8").strip())
            except (ValueError, OSError):
                pid = -1
            if self._running(pid):
                return False
            self.path.unlink(missing_ok=True)
        try:
            fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode("ascii"))
            os.close(fd)
            self.acquired = True
            return True
        except FileExistsError:
            return False

    def release(self) -> None:
        if self.acquired:
            self.path.unlink(missing_ok=True)
            self.acquired = False


class ProgressStore:
    def __init__(self, data_dir: Path) -> None:
        data_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir = data_dir
        self.db_path = data_dir / "progress.sqlite3"
        self.backup_dir = data_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        self.connection.executescript(SCHEMA)
        self.connection.commit()

    @staticmethod
    def now() -> str:
        return datetime.now(timezone.utc).isoformat()

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        try:
            yield self.connection
            self.connection.commit()
        except Exception:
            self.connection.rollback()
            raise

    def get(self, item_id: str) -> dict:
        row = self.connection.execute("SELECT * FROM progress WHERE item_id = ?", (item_id,)).fetchone()
        return dict(row) if row else {}

    def save_answer(self, item_id: str, item_type: str, answer: str) -> None:
        with self.transaction() as db:
            db.execute(
                """INSERT INTO progress(item_id,item_type,status,answer,updated_at)
                   VALUES(?,?,?,?,?)
                   ON CONFLICT(item_id) DO UPDATE SET answer=excluded.answer,
                   item_type=excluded.item_type, updated_at=excluded.updated_at""",
                (item_id, item_type, "started", answer, self.now()),
            )
        self.set_setting("last_item", item_id)

    def _solution_seen_since_pass(self, item_id: str) -> bool:
        rows = self.connection.execute(
            "SELECT id,event_type,payload FROM events WHERE item_id=? ORDER BY id",
            (item_id,),
        ).fetchall()
        last_pass_id = 0
        viewed_after_pass = False
        for row in rows:
            if row["event_type"] == "attempt":
                try:
                    passed = bool(json.loads(row["payload"]).get("passed"))
                except (TypeError, json.JSONDecodeError):
                    passed = False
                if passed:
                    last_pass_id = int(row["id"])
                    viewed_after_pass = False
            elif row["event_type"] == "solution_viewed" and int(row["id"]) > last_pass_id:
                viewed_after_pass = True
        return viewed_after_pass

    def mark_solution_viewed(self, item_id: str) -> None:
        with self.transaction() as db:
            db.execute(
                "INSERT INTO events(event_type,item_id,payload,created_at) VALUES(?,?,?,?)",
                ("solution_viewed", item_id, "{}", self.now()),
            )

    def record_attempt(
        self,
        item_id: str,
        item_type: str,
        answer: str,
        passed: bool,
        score: int,
        solution_seen: bool | None = None,
    ) -> int:
        old = self.get(item_id)
        attempts = int(old.get("attempts", 0)) + 1
        status = "completed" if passed else "started"
        best_score = max(int(old.get("score", 0)), score)
        after_solution = self._solution_seen_since_pass(item_id) if solution_seen is None else solution_seen
        with self.transaction() as db:
            db.execute(
                """INSERT INTO progress(item_id,item_type,status,attempts,score,answer,updated_at)
                   VALUES(?,?,?,?,?,?,?)
                   ON CONFLICT(item_id) DO UPDATE SET status=excluded.status,
                   attempts=excluded.attempts, score=excluded.score,
                   answer=excluded.answer, updated_at=excluded.updated_at""",
                (item_id, item_type, status, attempts, best_score, answer, self.now()),
            )
            db.execute(
                "INSERT INTO events(event_type,item_id,payload,created_at) VALUES(?,?,?,?)",
                ("attempt", item_id, json.dumps({"passed": passed, "score": score, "after_solution": after_solution}), self.now()),
            )
        self.set_setting("last_item", item_id)
        self.backup()
        return attempts

    def complete_lesson(self, lesson_id: str, xp: int = 20) -> None:
        old = self.get(lesson_id)
        score = max(int(old.get("score", 0)), xp)
        with self.transaction() as db:
            db.execute(
                """INSERT INTO progress(item_id,item_type,status,score,updated_at)
                   VALUES(?,?,?,?,?) ON CONFLICT(item_id) DO UPDATE SET
                   status='completed', score=MAX(score, excluded.score), updated_at=excluded.updated_at""",
                (lesson_id, "lesson", "completed", score, self.now()),
            )
        self.set_setting("last_item", lesson_id)
        self.backup()

    def set_hint(self, item_id: str, level: int) -> None:
        old = self.get(item_id)
        with self.transaction() as db:
            db.execute(
                """INSERT INTO progress(item_id,item_type,status,hint_level,updated_at)
                   VALUES(?,?,?,?,?) ON CONFLICT(item_id) DO UPDATE SET
                   hint_level=MAX(hint_level, excluded.hint_level), updated_at=excluded.updated_at""",
                (item_id, old.get("item_type", "exercise"), old.get("status", "started"), level, self.now()),
            )

    def add_time(self, item_id: str, item_type: str, seconds: int) -> None:
        if seconds <= 0:
            return
        old = self.get(item_id)
        with self.transaction() as db:
            db.execute(
                """INSERT INTO progress(item_id,item_type,status,seconds_spent,updated_at)
                   VALUES(?,?,?,?,?) ON CONFLICT(item_id) DO UPDATE SET
                   seconds_spent=seconds_spent + excluded.seconds_spent,
                   updated_at=excluded.updated_at""",
                (item_id, item_type, old.get("status", "started"), seconds, self.now()),
            )

    def set_setting(self, key: str, value: str) -> None:
        self.connection.execute(
            "INSERT INTO settings(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (key, value),
        )
        self.connection.commit()

    def get_setting(self, key: str, default: str = "") -> str:
        row = self.connection.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
        return str(row["value"]) if row else default

    def get_active_track(self, default: str = "dotnet-angular") -> str:
        return self.get_setting("active_track", default)

    def set_active_track(self, track: str) -> None:
        self.set_setting("active_track", track)

    def stats(self, total_lessons: int, total_exercises: int, track_item_ids: set[str] | None = None) -> dict:
        if track_item_ids is not None:
            # Calcolo isolato per la traccia attiva
            id_list = list(track_item_ids)
            placeholders = ",".join("?" for _ in id_list) if id_list else "''"
            completed_lessons = self.connection.execute(
                f"SELECT COUNT(*) n FROM progress WHERE item_type='lesson' AND status='completed' AND item_id IN ({placeholders})",
                id_list,
            ).fetchone()["n"]
            completed_exercises = self.connection.execute(
                f"SELECT COUNT(*) n FROM progress WHERE item_type='exercise' AND status='completed' AND item_id IN ({placeholders})",
                id_list,
            ).fetchone()["n"]
            xp = self.connection.execute(
                f"SELECT COALESCE(SUM(score),0) xp FROM progress WHERE item_id IN ({placeholders})",
                id_list,
            ).fetchone()["xp"]
            attempts = self.connection.execute(
                f"SELECT COALESCE(SUM(attempts),0) n FROM progress WHERE item_id IN ({placeholders})",
                id_list,
            ).fetchone()["n"]
        else:
            completed_lessons = self.connection.execute(
                "SELECT COUNT(*) n FROM progress WHERE item_type='lesson' AND status='completed'"
            ).fetchone()["n"]
            completed_exercises = self.connection.execute(
                "SELECT COUNT(*) n FROM progress WHERE item_type='exercise' AND status='completed'"
            ).fetchone()["n"]
            xp = self.connection.execute("SELECT COALESCE(SUM(score),0) xp FROM progress").fetchone()["xp"]
            attempts = self.connection.execute("SELECT COALESCE(SUM(attempts),0) n FROM progress").fetchone()["n"]
        return {
            "completed_lessons": completed_lessons,
            "completed_exercises": completed_exercises,
            "total_lessons": total_lessons,
            "total_exercises": total_exercises,
            "xp": xp,
            "attempts": attempts,
            "percent": int(100 * (completed_lessons + completed_exercises) / max(1, total_lessons + total_exercises)),
        }

    def completed_ids(self) -> set[str]:
        rows = self.connection.execute("SELECT item_id FROM progress WHERE status='completed'").fetchall()
        return {row["item_id"] for row in rows}

    def reset_items(self, item_ids: set[str], setting_keys: set[str] | None = None) -> dict[str, int]:
        """Remove progress and event history for selected items only."""
        ids = sorted(item_id for item_id in item_ids if item_id)
        keys = sorted(key for key in (setting_keys or set()) if key)
        deleted = {"progress": 0, "events": 0, "settings": 0}
        if not ids and not keys:
            return deleted

        with self.transaction() as db:
            if ids:
                placeholders = ",".join("?" for _ in ids)
                deleted["progress"] = db.execute(
                    f"DELETE FROM progress WHERE item_id IN ({placeholders})", ids
                ).rowcount
                deleted["events"] = db.execute(
                    f"DELETE FROM events WHERE item_id IN ({placeholders})", ids
                ).rowcount
            if keys:
                placeholders = ",".join("?" for _ in keys)
                deleted["settings"] = db.execute(
                    f"DELETE FROM settings WHERE key IN ({placeholders})", keys
                ).rowcount

        self.backup()
        return deleted

    def review_items(self, track_item_ids: set[str]) -> list[dict]:
        """Return unresolved failures and passes made after opening the solution."""
        result = []
        for item_id in track_item_ids:
            row = self.connection.execute(
                "SELECT payload FROM events WHERE item_id=? AND event_type='attempt' ORDER BY id DESC LIMIT 1",
                (item_id,),
            ).fetchone()
            state = self.get(item_id)
            if not row or not state:
                continue
            try:
                payload = json.loads(row["payload"])
            except (TypeError, json.JSONDecodeError):
                payload = {}
            if not payload.get("passed"):
                result.append({"item_id": item_id, "kind": "failed", "attempts": int(state.get("attempts", 0))})
            elif payload.get("after_solution"):
                result.append({"item_id": item_id, "kind": "after_solution", "attempts": int(state.get("attempts", 0))})
        return result

    def backup(self) -> Path:
        progress = [dict(row) for row in self.connection.execute("SELECT * FROM progress ORDER BY item_id")]
        settings = {row["key"]: row["value"] for row in self.connection.execute("SELECT * FROM settings")}
        payload = {"exported_at": self.now(), "progress": progress, "settings": settings}
        target = self.backup_dir / "progress_latest.json"
        temporary = target.with_suffix(".tmp")
        temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        temporary.replace(target)
        return target

    def close(self) -> None:
        self.backup()
        self.connection.close()
