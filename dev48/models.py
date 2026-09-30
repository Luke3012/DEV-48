from __future__ import annotations

from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any
import json
import re


_LESSON_LANGUAGE_PAIR = re.compile(
    r"(?ms)^\*\*Versione Python\*\*[ \t]*\r?\n[ \t]*\r?\n"
    r"```python\r?\n(?P<python>.*?)^```[ \t]*\r?\n[ \t]*\r?\n"
    r"\*\*Versione C\+\+\*\*[ \t]*\r?\n[ \t]*\r?\n"
    r"```cpp\r?\n(?P<cpp>.*?)^```[ \t]*(?:\r?\n|$)"
)
_LESSON_LANGUAGE_MARKER = re.compile(r"(?m)^\*\*Versione (?:Python|C\+\+)\*\*[ \t]*$")


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
    recommended_day: int | None = None


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
    variants: dict[str, dict[str, Any]] = field(default_factory=dict)
    no_ai: bool = False
    no_internet: bool = False
    timed: bool = False
    solution_after_attempts: int = 2


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
    repository_variants: dict[str, str] = field(default_factory=dict)

    def for_repository_language(self, language: str) -> Lab:
        template = self.repository_variants.get(language)
        if not template:
            return self
        return replace(self, id=self.id if language == "node" else f"{self.id}-{language}",
                       workspace_template=template)


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
    kind: str = "timed"
    coding_exercise_id: str = ""
    repository_lab_id: str = ""


@dataclass(frozen=True)
class WorkScenario:
    id: str
    module: str
    title: str
    brief: str
    options: tuple[dict[str, str], ...]
    recommended_order: tuple[str, ...]
    principles: tuple[str, ...]
    learning_focus: str = ""


@dataclass(frozen=True)
class WorkStylePrompt:
    id: str
    title: str
    prompt: str
    reflection_prompts: tuple[str, ...]


@dataclass(frozen=True)
class TrackDefinition:
    id: str
    name: str
    catalog_file: str
    card_label: str
    card_heading: str
    card_subtitle: str
    card_points: tuple[str, ...]
    window_title: str
    window_subtitle: str
    color: str


TRACK_DEFINITIONS = (
    TrackDefinition(
        id="dotnet-angular", name="Percorso Angular e .NET",
        catalog_file="catalog_dotnet_angular.json", card_label="PERCORSO 01",
        card_heading="ANGULAR & .NET", card_subtitle="Dalle basi alle applicazioni complete",
        card_points=(
            "C# e TypeScript · tipi, funzioni e dati",
            "ASP.NET Core · API e servizi",
            "Entity Framework Core · SQLite e relazioni",
            "Angular 22 · componenti, Signals e routing",
            "Laboratori full-stack · client Angular e server .NET",
        ),
        window_title="DEV//48 — Angular & .NET",
        window_subtitle=".NET 10 · Minimal API · EF Core · Angular 22 Signals",
        color="#22d3ee",
    ),
    TrackDefinition(
        id="web-js-react", name="Percorso JavaScript e React",
        catalog_file="catalog.json", card_label="PERCORSO 02",
        card_heading="JAVASCRIPT & REACT", card_subtitle="Dalle basi alle applicazioni web",
        card_points=(
            "JavaScript · funzioni, dati e asincronia",
            "HTML e CSS · semantica, accessibilità e layout",
            "TypeScript · tipi e contratti dei dati",
            "React 19 · componenti, stato e form",
            "Node.js e SQLite · API e database",
            "Test con Vitest · logica e interfaccia",
        ),
        window_title="DEV//48 — JavaScript & React",
        window_subtitle="JavaScript · React 19 · Node.js · SQL",
        color="#c084fc",
    ),
    TrackDefinition(
        id="amazon-sde-oa", name="Preparazione Amazon SDE-I OA",
        catalog_file="catalog_amazon_sde.json", card_label="PERCORSO 03",
        card_heading="AMAZON SDE-I OA", card_subtitle="Algoritmi, progetti e prove a tempo",
        card_points=(
            "Problemi di algoritmi e strutture dati · Python o C++",
            "Pattern · mappe, finestre, grafi, heap e programmazione dinamica",
            "Repository esistenti · test e debugging multi-file",
            "Assistente AI · esplorare il codice e verificare ipotesi",
            "Leadership Principles · scenari Work Simulation e Work Style",
            "Prova completa · 40 minuti di coding + 60 di repository",
        ),
        window_title="DEV//48 — Amazon SDE-I OA",
        window_subtitle="Algoritmi · debugging di repository · scenari di lavoro",
        color="#f59e0b",
    ),
)


class Catalog:
    def __init__(self, root: Path, track: str = "web-js-react") -> None:
        self.root = root
        self.track = track
        track_map = {definition.id: definition for definition in TRACK_DEFINITIONS}
        if track not in track_map:
            choices = ", ".join(track_map)
            raise ValueError(f"Traccia sconosciuta: {track!r}. Valori disponibili: {choices}")
        definition = track_map[track]
        self.track_definition = definition
        self.track = definition.id
        target_file = definition.catalog_file
        catalog_path = root / target_file
        if not catalog_path.exists():
            raise FileNotFoundError(f"Catalogo per la traccia {track!r} non trovato: {catalog_path}")

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
        self.work_scenarios = [WorkScenario(**{
            **item,
            "options": tuple(item["options"]),
            "recommended_order": tuple(item["recommended_order"]),
            "principles": tuple(item["principles"]),
        }) for item in raw.get("work_scenarios", [])]
        self.work_style = [WorkStylePrompt(**{
            **item, "reflection_prompts": tuple(item["reflection_prompts"]),
        }) for item in raw.get("work_style", [])]
        self.study_plan = self.meta.get("study_plan", [])
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
            "variants": {
                language: {**variant, "tests": tuple(variant.get("tests", []))}
                for language, variant in item.get("variants", {}).items()
            },
        })

    def lesson_body(self, lesson: Lesson, language: str | None = None) -> str:
        """Return shared lesson prose with only the selected code variant visible."""
        body = (self.root / lesson.body_file).read_text(encoding="utf-8")
        if language is None:
            return body
        if language not in {"python", "cpp"}:
            raise ValueError(f"Lingua DSA non supportata: {language}")

        def select_variant(match: re.Match[str]) -> str:
            code = match.group(language).rstrip()
            label = "C++" if language == "cpp" else "Python"
            return f"**Esempio in {label}**\n\n```{language}\n{code}\n```"

        rendered, _ = _LESSON_LANGUAGE_PAIR.subn(select_variant, body)
        if _LESSON_LANGUAGE_MARKER.search(rendered):
            raise ValueError(f"Blocco linguaggio non chiuso nella lezione {lesson.id}")
        return rendered

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
            "work simulation": [x.id for x in self.work_scenarios],
            "work style": [x.id for x in self.work_style],
        }
        all_ids = [item_id for ids in collections.values() for item_id in ids]
        duplicates = sorted({item_id for item_id in all_ids if all_ids.count(item_id) > 1})
        if duplicates:
            errors.append(f"ID duplicati (catalogo): {', '.join(duplicates)}")
        for label, ids in collections.items():
            duplicates = sorted({item for item in ids if ids.count(item) > 1})
            if duplicates:
                errors.append(f"ID duplicati ({label}): {', '.join(duplicates)}")
        known_lessons = set(collections["lezione"])
        known_modules = {item["id"] for item in self.modules}
        for exercise in self.exercises:
            if exercise.lesson_id not in known_lessons:
                errors.append(f"{exercise.id}: lesson_id inesistente")
            if len(exercise.hints) < 2:
                errors.append(f"{exercise.id}: servono almeno due indizi")
            for language, variant in exercise.variants.items():
                if not variant.get("starter") or not variant.get("solution") or not variant.get("tests"):
                    errors.append(f"{exercise.id}/{language}: starter, soluzione e test sono obbligatori")
                if len(variant.get("tests", ())) == 0:
                    errors.append(f"{exercise.id}/{language}: nessun test configurato")
        for lesson in self.lessons:
            if lesson.module not in known_modules:
                errors.append(f"{lesson.id}: module inesistente")
        for lesson in self.lessons:
            if not (self.root / lesson.body_file).is_file():
                errors.append(f"{lesson.id}: file Markdown mancante")
        for scenario in self.work_scenarios:
            option_ids = [item.get("id", "") for item in scenario.options]
            if len(option_ids) < 3 or len(option_ids) != len(set(option_ids)) or len(scenario.recommended_order) != len(option_ids) or set(option_ids) != set(scenario.recommended_order):
                errors.append(f"{scenario.id}: opzioni e graduatoria non corrispondono")
            if any(not item.get("effectiveness") or not item.get("reasoning") for item in scenario.options):
                errors.append(f"{scenario.id}: ogni opzione deve includere efficacia e ragionamento")
            if len({item.get("text", "").strip() for item in scenario.options}) != len(scenario.options):
                errors.append(f"{scenario.id}: le azioni devono essere distinte")
            if self.track == "amazon-sde-oa" and not scenario.learning_focus:
                errors.append(f"{scenario.id}: focus didattico mancante")
        for simulation in self.simulations:
            if simulation.kind not in {"timed", "coding", "repository", "full_mock"}:
                errors.append(f"{simulation.id}: tipo di simulazione non supportato")
            if simulation.coding_exercise_id and simulation.coding_exercise_id not in self.exercise_by_id:
                errors.append(f"{simulation.id}: esercizio coding inesistente")
            if simulation.repository_lab_id and simulation.repository_lab_id not in self.lab_by_id:
                errors.append(f"{simulation.id}: laboratorio repository inesistente")
            if simulation.kind in {"coding", "full_mock"} and not simulation.coding_exercise_id:
                errors.append(f"{simulation.id}: manca l'esercizio coding")
            if simulation.kind in {"repository", "full_mock"} and not simulation.repository_lab_id:
                errors.append(f"{simulation.id}: manca il laboratorio repository")
        for prompt in self.work_style:
            if not prompt.prompt.strip() or not prompt.reflection_prompts:
                errors.append(f"{prompt.id}: prompt di familiarizzazione incompleto")
        if self.track == "amazon-sde-oa":
            if len(self.study_plan) != 6:
                errors.append("Piano Amazon: deve contenere sei giorni consigliati")
            if len(self.work_scenarios) < 30 or len(self.work_style) < 1:
                errors.append("Percorso Amazon: contenuti Work Simulation o Work Style incompleti")
            if len(self.flashcards) < 120 or len(self.flashcards) > 180:
                errors.append("Percorso Amazon: la banca flashcard deve contenere 120-180 carte")
            for exercise in self.exercises:
                if set(exercise.variants) != {"python", "cpp"}:
                    errors.append(f"{exercise.id}: devono essere disponibili Python e C++")
                if exercise.id != "sde-e-language-trial" and not (exercise.no_ai and exercise.no_internet and exercise.timed):
                    errors.append(f"{exercise.id}: mancano i vincoli di pratica autonoma")
        for day in self.study_plan:
            missing = set(day.get("lesson_ids", ())) - known_lessons
            if missing:
                errors.append(f"Piano {day.get('day', '?')}: lezioni inesistenti {', '.join(sorted(missing))}")
            missing = set(day.get("exercise_ids", ())) - set(collections["esercizio"])
            if missing:
                errors.append(f"Piano {day.get('day', '?')}: esercizi inesistenti {', '.join(sorted(missing))}")
            missing = set(day.get("lab_ids", ())) - set(collections["laboratorio"])
            if missing:
                errors.append(f"Piano {day.get('day', '?')}: laboratori inesistenti {', '.join(sorted(missing))}")
            missing = set(day.get("simulation_ids", ())) - set(collections["simulazione"])
            if missing:
                errors.append(f"Piano {day.get('day', '?')}: simulazioni inesistenti {', '.join(sorted(missing))}")
            missing = set(day.get("scenario_ids", ())) - set(collections["work simulation"])
            if missing:
                errors.append(f"Piano {day.get('day', '?')}: scenari inesistenti {', '.join(sorted(missing))}")
            missing = set(day.get("work_style_ids", ())) - set(collections["work style"])
            if missing:
                errors.append(f"Piano {day.get('day', '?')}: prompt Work Style inesistenti {', '.join(sorted(missing))}")
        if self.study_plan:
            planned = [lesson_id for day in self.study_plan for lesson_id in day.get("lesson_ids", ())]
            for day in self.study_plan:
                for choice in day.get("choices", []):
                    for branch in choice["options"].values():
                        planned.extend(branch.get("lesson_ids", []))
                        for item_id in branch.get("lesson_ids", []):
                            if item_id not in self.lesson_by_id:
                                errors.append(f"Piano di studio: lezione opzionale sconosciuta {item_id}")
                        for item_id in branch.get("lab_ids", []):
                            if item_id not in self.lab_by_id:
                                errors.append(f"Piano di studio: lab opzionale sconosciuto {item_id}")
            expected_lessons = (
                {lesson.id for lesson in self.lessons if lesson.mandatory}
                if self.track == "amazon-sde-oa"
                else known_lessons
            )
            if set(planned) != expected_lessons:
                errors.append("Piano di studio: ogni lezione obbligatoria deve comparire almeno una volta")
            if len(planned) != len(set(planned)):
                errors.append("Piano di studio: una lezione compare in più giorni")
        return errors
