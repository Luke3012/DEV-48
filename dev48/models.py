from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import json


@dataclass(frozen=True)
class Lesson:
    id: str
    module: str
    title: str
    minutes: int
    difficulty: str
    mandatory: bool
    objectives: tuple[str, ...]
    summary: str
    body_file: str


@dataclass(frozen=True)
class Exercise:
    id: str
    lesson_id: str
    title: str
    kind: str
    difficulty: str
    minutes: int
    xp: int
    prompt: str
    starter: str
    solution: str
    hints: tuple[str, ...]
    tests: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    explanation: str = ""
    creative_goals: tuple[str, ...] = ()
    bonus_xp: int = 0


@dataclass(frozen=True)
class Lab:
    id: str
    module: str
    title: str
    minutes: int
    difficulty: str
    description: str
    requirements: tuple[str, ...]
    rubric: tuple[str, ...]
    workspace_template: str
    creative_goals: tuple[str, ...] = ()
    bonus_xp: int = 0


@dataclass(frozen=True)
class Flashcard:
    id: str
    module: str
    question: str
    answer: str


@dataclass(frozen=True)
class Simulation:
    id: str
    title: str
    minutes: int
    brief: str
    checklist: tuple[str, ...]


TRACK_DEFINITIONS = (
    ("dotnet-angular", "Angular & .NET Enterprise", "catalog_dotnet_angular.json"),
    ("web-js-react", "JavaScript & React Academy", "catalog.json"),
)


class Catalog:
    def __init__(self, root: Path, track: str = "web-js-react") -> None:
        self.root = root
        self.track = track
        track_map = {t[0]: t[2] for t in TRACK_DEFINITIONS}
        target_file = track_map.get(track, "catalog.json")
        catalog_path = root / target_file
        if not catalog_path.exists():
            catalog_path = root / "catalog.json"
            self.track = "web-js-react"

        raw = json.loads(catalog_path.read_text(encoding="utf-8"))
        self.meta = raw["meta"]
        self.modules = raw["modules"]
        self.lessons = [self._lesson(item) for item in raw["lessons"]]
        self.exercises = [self._exercise(item) for item in raw["exercises"]]
        self.labs = [
            Lab(**{
                **item,
                "requirements": tuple(item["requirements"]),
                "rubric": tuple(item["rubric"]),
                "creative_goals": tuple(item.get("creative_goals", ())),
                "bonus_xp": int(item.get("bonus_xp", 0)),
            })
            for item in raw["labs"]
        ]
        self.flashcards = [Flashcard(**item) for item in raw["flashcards"]]
        self.simulations = [Simulation(**{**item, "checklist": tuple(item["checklist"])}) for item in raw["simulations"]]
        self.lesson_by_id = {item.id: item for item in self.lessons}
        self.exercise_by_id = {item.id: item for item in self.exercises}
        self.lab_by_id = {item.id: item for item in self.labs}

    @staticmethod
    def _lesson(item: dict[str, Any]) -> Lesson:
        return Lesson(**{**item, "objectives": tuple(item["objectives"])})

    @staticmethod
    def _exercise(item: dict[str, Any]) -> Exercise:
        return Exercise(**{
            **item,
            "hints": tuple(item["hints"]),
            "tests": tuple(item.get("tests", [])),
            "creative_goals": tuple(item.get("creative_goals", ())),
            "bonus_xp": int(item.get("bonus_xp", 0)),
        })

    def lesson_body(self, lesson: Lesson) -> str:
        return (self.root / lesson.body_file).read_text(encoding="utf-8")

    def exercises_for(self, lesson_id: str) -> list[Exercise]:
        return [item for item in self.exercises if item.lesson_id == lesson_id]

    def validate(self) -> list[str]:
        errors: list[str] = []
        collections = {
            "lezione": [x.id for x in self.lessons],
            "esercizio": [x.id for x in self.exercises],
            "laboratorio": [x.id for x in self.labs],
            "flashcard": [x.id for x in self.flashcards],
            "simulazione": [x.id for x in self.simulations],
        }
        for label, ids in collections.items():
            duplicates = sorted({item for item in ids if ids.count(item) > 1})
            if duplicates:
                errors.append(f"ID duplicati ({label}): {', '.join(duplicates)}")
        known_lessons = set(collections["lezione"])
        for exercise in self.exercises:
            if exercise.lesson_id not in known_lessons:
                errors.append(f"{exercise.id}: lesson_id inesistente")
            if len(exercise.hints) < 2:
                errors.append(f"{exercise.id}: servono almeno due indizi")
        for lesson in self.lessons:
            if not (self.root / lesson.body_file).is_file():
                errors.append(f"{lesson.id}: file Markdown mancante")
        return errors
