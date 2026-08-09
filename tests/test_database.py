from dev48.database import InstanceLock, ProgressStore


def test_progress_persists_and_backups(tmp_path):
    store = ProgressStore(tmp_path / "data")
    store.save_answer("ex-1", "exercise", "prima risposta")
    attempts = store.record_attempt("ex-1", "exercise", "soluzione", False, 20)
    assert attempts == 1
    store.set_hint("ex-1", 2)
    store.complete_lesson("lesson-1")
    store.close()

    restored = ProgressStore(tmp_path / "data")
    assert restored.get("ex-1")["answer"] == "soluzione"
    assert restored.get("ex-1")["attempts"] == 1
    assert restored.get("ex-1")["hint_level"] == 2
    assert restored.get("lesson-1")["status"] == "completed"
    assert (tmp_path / "data" / "backups" / "progress_latest.json").exists()
    restored.close()


def test_instance_lock_rejects_second_instance(tmp_path):
    first = InstanceLock(tmp_path / "app.lock")
    second = InstanceLock(tmp_path / "app.lock")
    assert first.acquire()
    assert not second.acquire()
    first.release()
    assert second.acquire()
    second.release()

