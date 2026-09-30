import asyncio
from pathlib import Path

from textual.widgets import Button, DataTable, Input, Static, TextArea
from textual.containers import ScrollableContainer

from dev48.app import (
    AdaptiveFooter, CodeTextArea, CodingSimulationScreen, ConfirmAmazonResetScreen, CurriculumScreen, DashboardScreen, Dev48App, ExerciseScreen,
    FlashcardsScreen, FullMockScreen, ChallengesScreen, GlossaryScreen, LabScreen,
    FooterHint, LabsScreen, LessonScreen, SimulationScreen, TrackSelectionScreen,
    WorkScenarioScreen, WorkStyleScreen, assessment_prompt, exercise_progress_id,
)
from dev48.models import Catalog


def test_coding_simulation_starts_fresh_and_locks_clock(tmp_path):
    async def scenario():
        app = Dev48App(tmp_path / "data", tmp_path / "workspace", select_track=False)
        try:
            async with app.run_test(size=(150, 40)) as pilot:
                app.catalog = Catalog(Path(__file__).resolve().parents[1] / "content", track="amazon-sde-oa")
                screen = CodingSimulationScreen(app.catalog.simulations[0])
                app.push_screen(screen)
                await pilot.pause()
                editor = screen.query_one("#coding-sim-editor", TextArea)
                assert not editor.display
                assert not screen.query_one("#coding-sim-prompt").display
                assert editor.text == screen.variant()["starter"]
                screen.action_toggle()
                language = screen.language
                screen.remaining = 2
                screen.action_toggle()
                screen.action_reset()
                screen.action_toggle_language()
                assert screen.running and screen.remaining == 2
                assert screen.language == language
                screen.tick()
                screen.tick()
                assert screen.remaining == 0 and not screen.running
                assert editor.read_only
                assert screen.query_one("#run", Button).disabled
        finally:
            app.shutdown_resources()
    asyncio.run(scenario())


def test_code_editor_auto_indents_and_handles_braces(tmp_path):
    async def scenario():
        app = Dev48App(tmp_path / "data", tmp_path / "workspace", select_track=False)
        try:
            app.catalog = Catalog(Path(__file__).resolve().parents[1] / "content", track="dotnet-angular")
            exercise = next(item for item in app.catalog.exercises if item.kind == "csharp")
            async with app.run_test(size=(160, 48)) as pilot:
                app.push_screen(ExerciseScreen(exercise.id))
                await pilot.pause()
                editor = app.screen.query_one("#editor", TextArea)
                assert isinstance(editor, CodeTextArea)

                source = "public class Example {\n    void Run() {"
                editor.text = source
                editor.cursor_location = (1, len("    void Run() {"))
                await pilot.press("enter")
                assert editor.text == source + "\n        "
                assert editor.cursor_location == (2, 8)

                await pilot.press("}")
                assert editor.text == source + "\n    }"
                await pilot.press("ctrl+z")
                assert editor.text == source + "\n        "
                await pilot.press("ctrl+z")
                assert editor.text == source

                editor.text = "    // TODO"
                editor.cursor_location = (0, len("    // TODO"))
                await pilot.press("enter")
                assert editor.text == "    // TODO\n    "
                await pilot.press("enter")
                assert editor.text == "    // TODO\n    \n    "

                editor.text = "    code word"
                editor.cursor_location = (0, len("    code word"))
                await pilot.press("shift+left", "shift+left", "shift+left", "shift+left")
                await pilot.press("enter")
                assert editor.text == "    code \n    "
                assert editor.cursor_location == (1, 4)

                editor.text = "    // {"
                editor.cursor_location = (0, len("    // {"))
                await pilot.press("enter")
                assert editor.text == "    // {\n    "

                editor.text = "    /*\n        "
                editor.cursor_location = (1, 8)
                await pilot.press("}")
                assert editor.text == "    /*\n        }"

                editor.text = '    var raw = """\n    {'
                editor.cursor_location = (1, len("    {"))
                await pilot.press("enter")
                assert editor.text == '    var raw = """\n    {\n    '
        finally:
            app.shutdown_resources()
    asyncio.run(scenario())


def test_code_text_area_is_limited_to_programming_editors(tmp_path):
    async def scenario():
        content = Path(__file__).resolve().parents[1] / "content"
        app = Dev48App(tmp_path / "data", tmp_path / "workspace", select_track=False)
        try:
            async with app.run_test(size=(160, 48)) as pilot:
                app.catalog = Catalog(content, track="dotnet-angular")
                csharp = next(item for item in app.catalog.exercises if item.kind == "csharp")
                app.push_screen(ExerciseScreen(csharp.id))
                await pilot.pause()
                assert isinstance(app.screen.query_one("#editor", TextArea), CodeTextArea)
                app.pop_screen()
                await pilot.pause()

                reflection = next(item for item in app.catalog.exercises if item.kind == "reflection")
                app.push_screen(ExerciseScreen(reflection.id))
                await pilot.pause()
                editor = app.screen.query_one("#editor", TextArea)
                assert not isinstance(editor, CodeTextArea)
                editor.text = "    nota"
                editor.cursor_location = (0, len("    nota"))
                await pilot.press("enter")
                assert editor.text == "    nota\n"
                app.pop_screen()
                await pilot.pause()

                app.catalog = Catalog(content, track="web-js-react")
                study_answer = next(item for item in app.catalog.exercises if item.kind == "reflection")
                app.push_screen(ExerciseScreen(study_answer.id))
                await pilot.pause()
                assert not isinstance(app.screen.query_one("#editor", TextArea), CodeTextArea)
                app.pop_screen()
                await pilot.pause()

                app.catalog = Catalog(content, track="amazon-sde-oa")
                simulation = next(item for item in app.catalog.simulations if item.kind == "coding")
                app.push_screen(CodingSimulationScreen(simulation))
                await pilot.pause()
                assert isinstance(app.screen.query_one("#coding-sim-editor", TextArea), CodeTextArea)
                app.pop_screen()
                await pilot.pause()

                mock = next(item for item in app.catalog.simulations if item.kind == "full_mock")
                app.push_screen(FullMockScreen(mock))
                await pilot.pause()
                assert isinstance(app.screen.query_one("#mock-editor", TextArea), CodeTextArea)
        finally:
            app.shutdown_resources()
    asyncio.run(scenario())


def test_assessment_prompts_withhold_pattern_without_changing_contract():
    catalog = Catalog(Path(__file__).resolve().parents[1] / "content", track="amazon-sde-oa")
    for exercise in catalog.exercises:
        assert exercise.prompt.startswith("**Pattern:**")
        assert assessment_prompt(exercise) == exercise.prompt.split("\n\n", 1)[1]
        assert "**Pattern:**" not in assessment_prompt(exercise)


def test_full_mock_timer_advances_while_coding_runner_is_busy(monkeypatch, tmp_path):
    import time
    from dev48.runners import RunResult

    def slow_runner(*args, **kwargs):
        time.sleep(0.2)
        return RunResult(True, 100, "late coding result", ())

    monkeypatch.setattr("dev48.app.run_exercise", slow_runner)

    async def scenario():
        app = Dev48App(tmp_path / "data", tmp_path / "workspace", select_track=False)
        try:
            app.catalog = Catalog(Path(__file__).resolve().parents[1] / "content", track="amazon-sde-oa")
            async with app.run_test(size=(160, 48)) as pilot:
                app.push_screen(FullMockScreen(app.catalog.simulations[-1]))
                await pilot.pause()
                screen = app.screen
                screen.start_coding()
                task = asyncio.create_task(screen.action_run_coding())
                await asyncio.sleep(0.03)
                assert not task.done()
                screen.remaining = 1
                screen.tick()
                assert screen.phase == 1 and screen.remaining == 3600
                await task
                assert "late coding result" not in str(screen.query_one("#mock-result", Static).content)
                screen.finish_mock()
        finally:
            app.shutdown_resources()

    asyncio.run(scenario())


def test_dashboard_smoke(tmp_path):
    async def scenario():
        app = Dev48App(tmp_path / "data", tmp_path / "workspace", select_track=False)
        try:
            async with app.run_test(size=(140, 45)) as pilot:
                await pilot.pause()
                assert isinstance(app.screen, DashboardScreen)
                assert app.screen.query_one("#continue")
                assert app.focused.id == "continue"
                await pilot.press("right")
                await pilot.pause()
                assert app.focused.id == "curriculum"
                await pilot.resize_terminal(140, 16)
                await pilot.pause()
                assert app.has_class("compact-height")
                assert app.screen.query_one("#dashboard-actions").region.bottom <= app.size.height - 1
        finally:
            app.shutdown_resources()

    asyncio.run(scenario())


def test_dashboard_actions_stay_visible_in_short_terminal(tmp_path):
    async def scenario():
        app = Dev48App(tmp_path / "data", tmp_path / "workspace", select_track=False)
        try:
            async with app.run_test(size=(100, 16)) as pilot:
                await pilot.pause()
                actions = app.screen.query_one("#dashboard-actions")
                primary = app.screen.query_one("#continue")
                assert actions.region.height >= 3
                assert actions.region.bottom <= app.size.height - 1
                assert primary.region.height > 0
                assert primary.region.bottom <= app.size.height - 1
                for button in actions.query(Button):
                    assert actions.region.contains_region(button.region), (actions.region, button.id, button.region)
                await pilot.click("#continue")
                await pilot.pause()
                assert isinstance(app.screen, LessonScreen)
        finally:
            app.shutdown_resources()

    asyncio.run(scenario())


def test_every_screen_remains_operable_in_short_terminal(tmp_path):
    async def scenario():
        app = Dev48App(tmp_path / "data", tmp_path / "workspace", select_track=False)
        try:
            async with app.run_test(size=(150, 16)) as pilot:
                await pilot.pause()
                assert app.has_class("compact-height")
                app.catalog = Catalog(Path(__file__).resolve().parents[1] / "content", track="amazon-sde-oa")
                app.store.set_active_track("amazon-sde-oa")
                app.sync_app_title()
                lesson = next(
                    item for item in app.catalog.lessons
                    if app.catalog.exercises_for(item.id)
                )
                exercise = app.catalog.exercises_for(lesson.id)[0]
                lab = app.catalog.labs[0]
                simulation = app.catalog.simulations[0]
                cases = (
                    (CurriculumScreen(), "#table", False),
                    (LessonScreen(lesson.id), "#lesson-scroll", True),
                    (ExerciseScreen(exercise.id), "#editor", True),
                    (LabsScreen(), "#table", False),
                    (LabScreen(lab.id), "#lab-scroll", True),
                    (FlashcardsScreen(), "#card", True),
                    (GlossaryScreen(), "#glossary-scroll", False),
                    (ChallengesScreen(), "#table", False),
                    (CodingSimulationScreen(simulation), "#coding-sim-editor", True),
                )
                for screen, main_selector, has_actions in cases:
                    app.push_screen(screen)
                    await pilot.pause()
                    if isinstance(screen, CodingSimulationScreen):
                        screen.action_toggle()
                        await pilot.pause()
                    main = app.screen.query_one(main_selector)
                    assert main.region.height > 0, type(screen).__name__
                    assert main.region.y < app.size.height - 1, type(screen).__name__
                    if has_actions:
                        actions = app.screen.query_one(".actions")
                        assert actions.region.height >= 3, type(screen).__name__
                        assert actions.region.bottom <= app.size.height - 1, type(screen).__name__
                        for button in actions.query(Button):
                            assert actions.region.contains_region(button.region), (type(screen).__name__, actions.region, button.id, button.region)
                    app.pop_screen()
                    await pilot.pause()
        finally:
            app.shutdown_resources()

    asyncio.run(scenario())


def test_curriculum_search_and_shortcuts(tmp_path):
    async def scenario():
        app = Dev48App(tmp_path / "data", tmp_path / "workspace", select_track=False)
        try:
            async with app.run_test(size=(140, 45)) as pilot:
                await pilot.pause()
                await pilot.press("ctrl+k")
                await pilot.pause()
                assert isinstance(app.screen, CurriculumScreen)
                assert app.focused.id == "table"
                search = app.screen.query_one("#search", Input)
                search.value = "React"
                await pilot.pause()
                assert app.screen.query_one("#table", DataTable).row_count > 0
                await pilot.press("ctrl+g")
                await pilot.pause()
                assert isinstance(app.screen, GlossaryScreen)
                await pilot.press("ctrl+d")
                await pilot.pause()
                assert isinstance(app.screen, DashboardScreen)
        finally:
            app.shutdown_resources()

    asyncio.run(scenario())


def test_continue_opens_first_required_lesson(tmp_path):
    async def scenario():
        app = Dev48App(tmp_path / "data", tmp_path / "workspace", select_track=False)
        try:
            async with app.run_test(size=(140, 45)) as pilot:
                await pilot.pause()
                await pilot.click("#continue")
                await pilot.pause()
                assert isinstance(app.screen, LessonScreen)
                assert app.screen.lesson_id == next(item.id for item in app.catalog.lessons if item.mandatory)
                assert app.focused.id == "lesson-scroll"
                lesson_id = app.screen.lesson_id
                await pilot.click("#advance")
                await pilot.pause()
                assert isinstance(app.screen, ExerciseScreen)
                assert app.screen.exercise.lesson_id == lesson_id
        finally:
            app.shutdown_resources()

    asyncio.run(scenario())


def test_all_exercise_editors_and_libraries_mount(tmp_path):
    async def scenario():
        app = Dev48App(tmp_path / "data", tmp_path / "workspace", select_track=False)
        try:
            async with app.run_test(size=(150, 48)) as pilot:
                await pilot.pause()
                representatives = {}
                for exercise in app.catalog.exercises:
                    representatives.setdefault(exercise.kind, exercise)
                for exercise in representatives.values():
                    app.push_screen(ExerciseScreen(exercise.id))
                    await pilot.pause()
                    assert app.screen.query_one("#editor")
                    scope = app.screen.query_one("#exercise-scope", Static)
                    assert "Come funziona il controllo" in scope.content
                    if exercise.kind == "angular":
                        assert "mock" in scope.content
                        assert "non mostra la pagina nel browser" in scope.content
                    assert app.focused.id == "editor"
                    app.pop_screen()
                    await pilot.pause()
                for screen_type in (LabsScreen, FlashcardsScreen, ChallengesScreen):
                    app.push_screen(screen_type())
                    await pilot.pause()
                    assert isinstance(app.screen, screen_type)
                    expected_focus = {LabsScreen: "table", FlashcardsScreen: "flip", ChallengesScreen: "table"}[screen_type]
                    assert app.focused.id == expected_focus
                    app.pop_screen()
                    await pilot.pause()
        finally:
            app.shutdown_resources()

    asyncio.run(scenario())


def test_theory_toggle_preserves_reading_editor_and_cursor_positions(tmp_path):
    async def scenario():
        app = Dev48App(tmp_path / "data", tmp_path / "workspace", select_track=False)
        try:
            async with app.run_test(size=(170, 48)) as pilot:
                await pilot.pause()
                exercise = next(item for item in app.catalog.exercises if item.kind == "reflection")
                lesson_screen = LessonScreen(exercise.lesson_id)
                app.push_screen(lesson_screen)
                await pilot.pause()
                lesson_scroll = lesson_screen.query_one("#lesson-scroll", ScrollableContainer)
                lesson_scroll.scroll_to(y=12, animate=False, force=True)
                await pilot.pause()
                lesson_position = lesson_scroll.scroll_y

                app.push_screen(ExerciseScreen(exercise.id))
                await pilot.pause()
                editor = app.screen.query_one("#editor", TextArea)
                editor.text = "Prima versione da rivedere.\nSeconda riga della risposta."
                editor.cursor_location = (1, 12)
                prompt = app.screen.query_one("#exercise-prompt", ScrollableContainer)
                prompt.scroll_to(y=5, animate=False, force=True)
                await pilot.pause()
                prompt_position = prompt.scroll_y

                await pilot.press("f1")
                await pilot.pause()
                theory = app.screen.query_one("#theory-scroll", ScrollableContainer)
                assert theory.display
                assert not prompt.display
                assert editor.text == "Prima versione da rivedere.\nSeconda riga della risposta."
                assert editor.cursor_location == (1, 12)
                assert app.store.get(exercise.id)["answer"] == editor.text
                theory.scroll_to(y=12, animate=False, force=True)
                await pilot.pause()
                theory_position = theory.scroll_y

                await pilot.press("f1")
                await pilot.pause()
                assert prompt.display
                assert not theory.display
                assert prompt.scroll_y == prompt_position
                assert editor.cursor_location == (1, 12)

                await pilot.press("f1")
                await pilot.pause()
                assert app.screen.query_one("#theory-scroll").scroll_y == theory_position
                assert editor.text == "Prima versione da rivedere.\nSeconda riga della risposta."
                await pilot.press("escape")
                await pilot.pause()
                assert app.screen.query_one("#exercise-prompt").display
                assert not app.screen.query_one("#theory-scroll").display
                assert app.screen.query_one("#back").label.plain == "← LEZIONE"
                assert editor.cursor_location == (1, 12)

                await pilot.press("escape")
                await pilot.pause()
                assert app.screen is lesson_screen
                assert lesson_scroll.scroll_y == lesson_position
                assert app.store.get(exercise.id)["answer"] == "Prima versione da rivedere.\nSeconda riga della risposta."
        finally:
            app.shutdown_resources()

    asyncio.run(scenario())


def test_reflection_check_does_not_award_xp_or_claim_to_grade_meaning(tmp_path):
    async def scenario():
        app = Dev48App(tmp_path / "data", tmp_path / "workspace", select_track=False)
        try:
            async with app.run_test(size=(150, 45)) as pilot:
                await pilot.pause()
                exercise = next(item for item in app.catalog.exercises if item.kind == "reflection")
                app.push_screen(ExerciseScreen(exercise.id))
                await pilot.pause()
                app.screen.query_one("#editor", TextArea).text = exercise.solution
                app.screen.run_current()
                await pilot.pause()
                state = app.store.get(exercise.id)
                assert state["status"] == "completed"
                assert state["score"] == 0
                assert "AUTOVERIFICA" in str(app.screen.query_one("#result").content)
        finally:
            app.shutdown_resources()

    asyncio.run(scenario())


def test_resume_last_and_wide_lesson_layout(tmp_path):
    async def scenario():
        app = Dev48App(tmp_path / "data", tmp_path / "workspace", select_track=False)
        last = app.catalog.lessons[3]
        app.store.complete_lesson(last.id)
        try:
            async with app.run_test(size=(210, 52)) as pilot:
                await pilot.pause()
                assert app.focused.id == "continue"
                assert "RIPRENDI ATTIVITÀ" in str(app.screen.query_one("#resume").label)
                await pilot.click("#resume")
                await pilot.pause()
                assert isinstance(app.screen, LessonScreen)
                assert app.screen.lesson_id == last.id
                markdown = app.screen.query_one("#lesson-markdown")
                assert markdown.size.width > 150
                assert app.focused.id == "lesson-scroll"
                scroller = app.screen.query_one("#lesson-scroll")
                before = scroller.scroll_y
                await pilot.press("down")
                await pilot.pause()
                assert scroller.scroll_y > before
        finally:
            app.shutdown_resources()

    asyncio.run(scenario())


def test_guided_sequence_lesson_exercises_next_lesson(tmp_path):
    app = Dev48App(tmp_path / "data", tmp_path / "workspace", select_track=False)
    try:
        mandatory = [item for item in app.catalog.lessons if item.mandatory]
        first, second = mandatory[:2]
        exercises = app.catalog.exercises_for(first.id)

        assert app.next_step() == ("lesson", first)
        app.store.complete_lesson(first.id)
        assert app.next_step() == ("exercise", exercises[0])
        app.store.record_attempt(exercises[0].id, "exercise", exercises[0].solution, True, exercises[0].xp)
        assert app.next_step() == ("exercise", exercises[1])
        app.store.record_attempt(exercises[1].id, "exercise", exercises[1].solution, True, exercises[1].xp)
        assert app.next_step() == ("lesson", second)
    finally:
        app.shutdown_resources()


def test_continue_returns_to_theory_for_unstarted_first_exercise_but_resume_reopens_it(tmp_path):
    async def scenario():
        app = Dev48App(tmp_path / "data", tmp_path / "workspace", select_track=False)
        lesson = next(
            item for item in app.catalog.lessons
            if item.mandatory and app.catalog.exercises_for(item.id)
        )
        exercise = app.catalog.exercises_for(lesson.id)[0]
        app.store.complete_lesson(lesson.id)
        app.store.set_setting("last_item", exercise_progress_id(exercise, app.coding_language))
        try:
            async with app.run_test(size=(150, 40)) as pilot:
                await pilot.pause()
                assert app.next_step() == ("lesson", lesson)

                await pilot.click("#resume")
                await pilot.pause()
                assert isinstance(app.screen, ExerciseScreen)
                assert app.screen.exercise_id == exercise.id

                await pilot.press("escape")
                await pilot.pause()
                assert isinstance(app.screen, DashboardScreen)
                assert app.next_step() == ("lesson", lesson)

                await pilot.click("#continue")
                await pilot.pause()
                assert isinstance(app.screen, LessonScreen)
                assert app.screen.lesson_id == lesson.id

                progress_id = exercise_progress_id(exercise, app.coding_language)
                app.store.set_setting(f"exercise_started:{progress_id}", "1")
                assert app.next_step() == ("exercise", exercise)
        finally:
            app.shutdown_resources()

    asyncio.run(scenario())


def test_exercise_started_marker_tracks_edits_and_language_variants(tmp_path):
    async def scenario():
        app = Dev48App(tmp_path / "data", tmp_path / "workspace", select_track=False)
        app.catalog = Catalog(Path(__file__).resolve().parents[1] / "content", track="amazon-sde-oa")
        exercise = next(item for item in app.catalog.exercises if len(item.variants) > 1)
        languages = list(exercise.variants)
        app.coding_language = languages[0]
        app.store.set_setting("amazon_coding_language", languages[0])
        lesson = app.catalog.lesson_by_id[exercise.lesson_id]
        app.store.complete_lesson(lesson.id)
        progress_first = exercise_progress_id(exercise, languages[0])
        progress_second = exercise_progress_id(exercise, languages[1])
        app.store.set_setting("last_item", progress_first)
        try:
            async with app.run_test(size=(150, 40)) as pilot:
                await pilot.pause()
                screen = ExerciseScreen(exercise.id)
                app.push_screen(screen)
                await pilot.pause()
                assert not app.exercise_has_started(exercise, languages[0])

                screen.action_toggle_language()
                await pilot.pause()
                assert screen.coding_language == languages[1]
                assert not app.exercise_has_started(exercise, languages[1])

                await pilot.press("x")
                await pilot.pause()
                assert app.store.get_setting(f"exercise_started:{progress_second}") == "1"
                assert app.exercise_has_started(exercise, languages[1])
                assert not app.exercise_has_started(exercise, languages[0])

                editor = screen.query_one("#editor", TextArea)
                editor.text = exercise.variants[languages[1]].get("starter", exercise.starter)
                await pilot.pause()
                assert app.exercise_has_started(exercise, languages[1])

                app.store.save_answer(progress_first, "exercise", "edited legacy answer")
                assert app.exercise_has_started(exercise, languages[0])
        finally:
            app.shutdown_resources()

    asyncio.run(scenario())


def test_adaptive_footer_wraps_all_shortcuts_in_narrow_terminal(tmp_path):
    async def scenario():
        app = Dev48App(tmp_path / "data", tmp_path / "workspace", select_track=False)
        lesson = next(
            item for item in app.catalog.lessons
            if item.mandatory and app.catalog.exercises_for(item.id)
        )
        exercise = app.catalog.exercises_for(lesson.id)[0]
        try:
            async with app.run_test(size=(48, 16)) as pilot:
                await pilot.pause()
                app.push_screen(ExerciseScreen(exercise.id))
                await pilot.pause()

                footer = app.screen.query_one(AdaptiveFooter)
                hints = list(footer.query(FooterHint))
                expected_actions = {
                    binding.action
                    for _node, binding, _enabled, _tooltip in app.screen.active_bindings.values()
                    if binding.show and binding.key != app.COMMAND_PALETTE_BINDING
                }
                assert {hint.action for hint in hints} == expected_actions
                assert len(footer.query(".footer-row")) > 1
                assert footer.region.bottom <= app.size.height
                for hint in hints:
                    assert footer.region.contains_region(hint.region), (footer.region, hint.action, hint.region)
                actions = app.screen.query_one("#exercise-actions")
                assert actions.region.bottom <= footer.region.y

                narrow_row_count = len(footer.query(".footer-row"))
                await pilot.resize_terminal(220, 16)
                await pilot.pause()
                footer = app.screen.query_one(AdaptiveFooter)
                hints = list(footer.query(FooterHint))
                assert {hint.action for hint in hints} == expected_actions
                assert len(footer.query(".footer-row")) < narrow_row_count
                for hint in hints:
                    assert footer.region.contains_region(hint.region), (footer.region, hint.action, hint.region)
        finally:
            app.shutdown_resources()

    asyncio.run(scenario())


def test_track_selection_screen_interaction(tmp_path):
    async def scenario():
        app = Dev48App(tmp_path / "data", tmp_path / "workspace", select_track=True)
        try:
            async with app.run_test(size=(140, 45)) as pilot:
                await pilot.pause()
                assert isinstance(app.screen, TrackSelectionScreen)
                # Press '1' to choose Angular & .NET
                await pilot.press("1")
                await pilot.pause()
                assert isinstance(app.screen, DashboardScreen)
                assert app.catalog.track == "dotnet-angular"
                assert "Angular & .NET" in app.title
                assert "Signals" in app.sub_title

                # Ctrl+T opens the track chooser; the track changes after selection.
                await pilot.press("ctrl+t")
                await pilot.pause()
                assert isinstance(app.screen, TrackSelectionScreen)
                await pilot.press("2")
                await pilot.pause()
                assert isinstance(app.screen, DashboardScreen)
                assert app.catalog.track == "web-js-react"
                assert "JavaScript & React" in app.title
                assert "React 19" in app.sub_title

                await pilot.press("ctrl+t")
                await pilot.pause()
                assert isinstance(app.screen, TrackSelectionScreen)
                await pilot.press("3")
                await pilot.pause()
                assert isinstance(app.screen, DashboardScreen)
                assert app.catalog.track == "amazon-sde-oa"
                assert "Amazon SDE-I OA" in app.title
                assert len(app.catalog.work_scenarios) == 36

                await pilot.press("ctrl+t")
                await pilot.pause()
                assert isinstance(app.screen, TrackSelectionScreen)
                await pilot.press("2")
                await pilot.pause()

                # Open curriculum screen
                await pilot.press("ctrl+k")
                await pilot.pause()
                assert isinstance(app.screen, CurriculumScreen)
                # The global shortcut opens the chooser from the curriculum; Escape restores it.
                await pilot.press("ctrl+t")
                await pilot.pause()
                assert isinstance(app.screen, TrackSelectionScreen)
                await pilot.press("escape")
                await pilot.pause()
                assert isinstance(app.screen, CurriculumScreen)
                assert app.catalog.track == "web-js-react"
        finally:
            app.shutdown_resources()

    asyncio.run(scenario())


def test_three_track_cards_fit_responsive_terminal_sizes(tmp_path):
    async def scenario():
        app = Dev48App(tmp_path / "data", tmp_path / "workspace", select_track=True)
        try:
            async with app.run_test(size=(110, 35)) as pilot:
                await pilot.pause()
                assert isinstance(app.screen, TrackSelectionScreen)
                for track in ("dotnet-angular", "web-js-react", "amazon-sde-oa"):
                    card = app.screen.query_one(f"#track-card-{track}")
                    button = app.screen.query_one(f"#btn-track-{track}", Button)
                    assert card.region.width > 0 and card.region.width <= app.size.width
                    assert button.region.width > 0 and button.region.right <= app.size.width

                await pilot.resize_terminal(82, 20)
                await pilot.pause()
                assert isinstance(app.screen, TrackSelectionScreen)
                assert app.screen.query_one("#track-card-list").region.height > 0
                await pilot.press("3")
                await pilot.pause()
                assert isinstance(app.screen, DashboardScreen)
                assert app.catalog.track == "amazon-sde-oa"
        finally:
            app.shutdown_resources()

    asyncio.run(scenario())


def test_amazon_work_screens_and_full_mock_sequence(tmp_path):
    async def scenario():
        app = Dev48App(tmp_path / "data", tmp_path / "workspace", select_track=False)
        try:
            app.catalog = Catalog(Path(__file__).resolve().parents[1] / "content", track="amazon-sde-oa")
            app.store.set_active_track("amazon-sde-oa")
            async with app.run_test(size=(160, 48)) as pilot:
                scenario_screen = WorkScenarioScreen(app.catalog.work_scenarios[0])
                app.push_screen(scenario_screen)
                await pilot.pause()
                assert isinstance(app.screen, WorkScenarioScreen)
                assert app.screen.query_one("#scenario-answer", TextArea)
                assert "Filo conduttore:" in app.screen.feedback_text("A > B > C > D")
                app.screen.query_one("#scenario-answer", TextArea).text = "B > A > C > D"
                await pilot.click("#submit")
                await pilot.pause()
                assert app.screen.query_one("#scenario-feedback")
                assert app.store.get(app.catalog.work_scenarios[0].id)["answer"] == "B > A > C > D"
                app.pop_screen()
                await pilot.pause()

                app.push_screen(WorkScenarioScreen(app.catalog.work_scenarios[0]))
                await pilot.pause()
                assert app.screen.query_one("#scenario-answer", TextArea).text == "B > A > C > D"
                app.pop_screen()
                app.store.set_setting(f"scenario_revision:{app.catalog.work_scenarios[0].id}", "old-content")
                app.push_screen(WorkScenarioScreen(app.catalog.work_scenarios[0]))
                await pilot.pause()
                assert app.screen.query_one("#scenario-answer", TextArea).text == ""
                assert app.store.get(app.catalog.work_scenarios[0].id)["answer"] == "B > A > C > D"
                app.pop_screen()
                await pilot.pause()

                app.push_screen(WorkStyleScreen())
                await pilot.pause()
                app.screen.query_one("#work-style-answer", TextArea).text = "Nota personale di prova"
                await pilot.click("#save")
                await pilot.pause()
                assert app.store.get("sde-style-01")["answer"] == "Nota personale di prova"
                app.pop_screen()
                await pilot.pause()

                simulation = app.catalog.simulations[-1]
                app.push_screen(FullMockScreen(simulation))
                await pilot.pause()
                screen = app.screen
                assert isinstance(screen, FullMockScreen)
                assert not screen.query_one("#mock-coding-prompt", ScrollableContainer).display
                await pilot.click("#repository-language")
                await pilot.pause()
                assert screen.lab.workspace_template == "amazon_cpp"
                assert screen.lab.id.endswith("-cpp")
                screen.query_one("#repository-language", Button).press()
                await pilot.pause()
                assert screen.lab.workspace_template == "amazon_node"
                repository_prompt = screen.repository_prompt_text()
                assert screen.lab.description not in repository_prompt
                assert all(requirement not in repository_prompt for requirement in screen.lab.requirements)
                assert "README" in repository_prompt and "Avvia i test" in repository_prompt
                await pilot.click("#start")
                await pilot.pause()
                assert screen.locked and screen.phase == 0
                assert 40 * 60 - 10 <= screen.remaining <= 40 * 60
                assert screen.query_one("#mock-coding-prompt", ScrollableContainer).display
                await pilot.press("ctrl+t")
                await pilot.pause()
                assert app.screen is screen
                await pilot.press("escape")
                await pilot.press("ctrl+d")
                await pilot.pause()
                assert app.screen is screen
                screen.remaining = 1
                screen.running = True
                screen.tick()
                assert screen.phase == 1 and screen.remaining == 60 * 60
                await pilot.pause()
                assert screen.phase == 1
                assert (tmp_path / "workspace" / "lab-amazon-mock-repository" / "package.json").is_file()
                await pilot.press("escape")
                await pilot.pause()
                assert app.screen is screen and screen.locked
                screen.remaining = 1
                screen.running = True
                screen.tick()
                await pilot.pause()
                assert screen.phase == 2 and not screen.locked
                await pilot.click("#finish-mock")
                await pilot.pause()
                assert isinstance(app.screen, DashboardScreen)
                app.store.set_setting("amazon_repository_language", "cpp")
                app.push_screen(FullMockScreen(simulation))
                await pilot.pause()
                cpp_screen = app.screen
                cpp_screen.start_coding()
                cpp_screen.start_repository()
                await pilot.pause()
                assert (tmp_path / "workspace" / "lab-amazon-mock-repository-cpp" / "CMakeLists.txt").is_file()
                assert cpp_screen.query_one("#repository-language", Button).disabled
                cpp_screen.finish_mock()
                app.pop_screen()
        finally:
            app.shutdown_resources()

    asyncio.run(scenario())


def test_amazon_exercise_hides_hints_and_saves_language_variants(tmp_path):
    async def scenario():
        app = Dev48App(tmp_path / "data", tmp_path / "workspace", select_track=False)
        try:
            app.catalog = Catalog(Path(__file__).resolve().parents[1] / "content", track="amazon-sde-oa")
            app.store.set_active_track("amazon-sde-oa")
            exercise = app.catalog.exercise_by_id["sde-e-two-sum"]
            async with app.run_test(size=(160, 48)) as pilot:
                app.push_screen(ExerciseScreen(exercise.id))
                await pilot.pause()
                screen = app.screen
                editor = screen.query_one("#editor", TextArea)
                editor.text = "python attempt"
                screen.action_toggle_language()
                await pilot.pause()
                assert screen.coding_language == "cpp"
                editor = screen.query_one("#editor", TextArea)
                editor.text = "cpp attempt"
                screen.action_toggle_language()
                await pilot.pause()
                assert screen.coding_language == "python"
                assert screen.query_one("#editor", TextArea).text == "python attempt"
                screen.show_solution()
                await pilot.pause()
                assert "SOLUZIONE NON ANCORA DISPONIBILE" in str(screen.query_one("#result", Static).content)
                for _ in range(2):
                    app.store.record_attempt(screen.progress_id, "exercise", "tentativo", False, 0)
                screen.show_solution()
                await pilot.pause()
                result = str(screen.query_one("#result", Static).content)
                assert "SOLUZIONE" in result and "def two_sum" in result
        finally:
            app.shutdown_resources()

    asyncio.run(scenario())


def test_amazon_hints_and_theory_answers_are_saved_per_language(tmp_path):
    async def scenario():
        app = Dev48App(tmp_path / "data", tmp_path / "workspace", select_track=False)
        try:
            app.catalog = Catalog(Path(__file__).resolve().parents[1] / "content", track="amazon-sde-oa")
            app.store.set_active_track("amazon-sde-oa")
            exercise = app.catalog.exercise_by_id["sde-e-two-sum"]
            async with app.run_test(size=(160, 48)) as pilot:
                app.push_screen(ExerciseScreen(exercise.id))
                await pilot.pause()
                screen = app.screen
                screen.query_one("#editor", TextArea).text = "python answer"
                screen.action_hint()
                assert app.store.get("sde-e-two-sum@python")["hint_level"] == 1
                assert app.store.get(exercise.id) == {}

                screen.action_toggle_language()
                await pilot.pause()
                assert screen.coding_language == "cpp"
                assert app.store.get("sde-e-two-sum@python")["answer"] == "python answer"
                screen.query_one("#editor", TextArea).text = "cpp answer"
                screen.action_hint()
                screen.action_toggle_theory()
                assert app.store.get("sde-e-two-sum@cpp")["answer"] == "cpp answer"
                assert app.store.get("sde-e-two-sum@cpp")["hint_level"] == 1
                assert app.store.get(exercise.id) == {}

                screen.action_toggle_theory()
                screen.action_toggle_language()
                await pilot.pause()
                assert screen.coding_language == "python"
                assert screen.query_one("#editor", TextArea).text == "python answer"
        finally:
            app.shutdown_resources()

    asyncio.run(scenario())


def test_amazon_lesson_screen_switches_theory_example_language(tmp_path):
    async def scenario():
        app = Dev48App(tmp_path / "data", tmp_path / "workspace", select_track=False)
        app.catalog = Catalog(Path(__file__).resolve().parents[1] / "content", track="amazon-sde-oa")
        app.store.set_active_track("amazon-sde-oa")
        app.coding_language = "python"
        app.store.set_setting("amazon_coding_language", "python")
        lesson = app.catalog.lesson_by_id["sde-l-sliding-window"]
        try:
            async with app.run_test(size=(150, 44)) as pilot:
                app.push_screen(LessonScreen(lesson.id))
                await pilot.pause()
                screen = app.screen
                assert "PYTHON" in str(screen.query_one("#language", Button).label)

                screen.action_toggle_language()
                await pilot.pause()
                assert app.coding_language == "cpp"
                assert app.store.get_setting("amazon_coding_language") == "cpp"
                assert "CPP" in str(screen.query_one("#language", Button).label)
                assert "long long max_sum_k" in app.catalog.lesson_body(lesson, app.coding_language)
        finally:
            app.shutdown_resources()

    asyncio.run(scenario())


def test_active_track_persists_and_progress_stats_stay_separate(tmp_path):
    content = Path(__file__).resolve().parents[1] / "content"
    data_dir = tmp_path / "data"
    workspace_dir = tmp_path / "workspace"
    app = Dev48App(data_dir, workspace_dir, select_track=False)
    try:
        react = Catalog(content, track="web-js-react")
        react_lesson = react.lessons[0]
        react_exercise = react.exercises[0]
        app.store.complete_lesson(react_lesson.id)
        app.store.record_attempt(react_exercise.id, "exercise", react_exercise.solution, True, react_exercise.xp)

        amazon = Catalog(content, track="amazon-sde-oa")
        amazon_lesson = amazon.lesson_by_id["sde-l-oa-format"]
        amazon_exercise = amazon.exercise_by_id["sde-e-two-sum"]
        app.store.complete_lesson(amazon_lesson.id)
        app.store.record_attempt("sde-e-two-sum@python", "exercise", "python code", True, amazon_exercise.xp)
        app.catalog = amazon
        app.coding_language = "python"
        app.store.set_active_track("amazon-sde-oa")
        assert app.stats()["completed_lessons"] == 1
        assert app.stats()["completed_exercises"] == 1
    finally:
        app.shutdown_resources()

    restarted = Dev48App(data_dir, workspace_dir, select_track=False)
    try:
        assert restarted.catalog.track == "amazon-sde-oa"
        assert restarted.stats()["completed_lessons"] == 1
        assert restarted.stats()["completed_exercises"] == 1
        restarted.catalog = Catalog(content, track="web-js-react")
        assert restarted.stats()["completed_lessons"] == 1
        assert restarted.stats()["completed_exercises"] == 1
    finally:
        restarted.shutdown_resources()


def test_amazon_dashboard_reset_is_confirmed_and_track_scoped(tmp_path):
    async def scenario():
        content = Path(__file__).resolve().parents[1] / "content"
        app = Dev48App(tmp_path / "data", tmp_path / "workspace", select_track=False)
        react = Catalog(content, track="web-js-react")
        react_lesson = react.lessons[0]
        react_exercise = react.exercises[0]
        app.store.complete_lesson(react_lesson.id)
        app.store.record_attempt(react_exercise.id, "exercise", react_exercise.solution, True, react_exercise.xp)

        amazon = Catalog(content, track="amazon-sde-oa")
        lesson = amazon.lesson_by_id["sde-l-oa-format"]
        exercise = amazon.exercise_by_id["sde-e-two-sum"]
        app.catalog = amazon
        app.store.set_active_track("amazon-sde-oa")
        app.coding_language = "cpp"
        app.store.set_setting("amazon_coding_language", "cpp")
        app.store.complete_lesson(lesson.id)
        app.store.record_attempt("sde-e-two-sum@python", "exercise", "python answer", True, exercise.xp)
        app.store.record_attempt("sde-e-two-sum@cpp", "exercise", "cpp answer", True, exercise.xp)
        app.store.set_setting("scenario_revision:sde-ws-01", "2")
        app.store.set_setting("last_item", lesson.id)
        lab_file = tmp_path / "workspace" / "lab-amazon-mock-repository" / "README.md"
        lab_file.parent.mkdir(parents=True)
        lab_file.write_text("learner work", encoding="utf-8")

        try:
            async with app.run_test(size=(150, 44)) as pilot:
                app.push_screen(DashboardScreen())
                await pilot.pause()
                assert app.screen.query_one("#reset-amazon-progress", Button)
                assert app.stats()["completed_lessons"] == 1
                await pilot.click("#reset-amazon-progress")
                await pilot.pause()
                assert isinstance(app.screen, ConfirmAmazonResetScreen)
                assert lesson.id in app.store.completed_ids()

                await pilot.click("#confirm")
                await pilot.pause()
                assert isinstance(app.screen, DashboardScreen)
                assert app.stats()["completed_lessons"] == 0
                assert app.stats()["completed_exercises"] == 0
                completed = app.store.completed_ids()
                assert lesson.id not in completed
                assert exercise_progress_id(exercise, "python") not in completed
                assert exercise_progress_id(exercise, "cpp") not in completed
                assert app.store.get_setting("last_item") in (None, "")
                assert app.store.get_setting("scenario_revision:sde-ws-01") in (None, "")
                assert app.store.get_setting("amazon_coding_language") == "cpp"
                assert lab_file.read_text(encoding="utf-8") == "learner work"

                app.catalog = react
                assert app.stats()["completed_lessons"] == 1
                assert app.stats()["completed_exercises"] == 1
        finally:
            app.shutdown_resources()

    asyncio.run(scenario())


def test_lesson_and_action_buttons_arrows_and_enter(tmp_path):
    async def scenario():
        app = Dev48App(tmp_path / "data", tmp_path / "workspace", select_track=False)
        try:
            async with app.run_test(size=(140, 45)) as pilot:
                await pilot.pause()
                lesson = app.catalog.lessons[0]

                # 1. LessonScreen: enter on scroll container immediately advances
                app.push_screen(LessonScreen(lesson.id))
                await pilot.pause()
                assert isinstance(app.screen, LessonScreen)
                assert app.focused.id == "lesson-scroll"
                await pilot.press("enter")
                await pilot.pause()
                assert isinstance(app.screen, ExerciseScreen)
                app.pop_screen()
                await pilot.pause()
                app.pop_screen()
                await pilot.pause()

                # 2. LessonScreen: arrow keys toggle between buttons, enter triggers focused
                app.push_screen(LessonScreen(lesson.id))
                await pilot.pause()
                assert app.focused.id == "lesson-scroll"
                # Right moves to advance
                await pilot.press("right")
                await pilot.pause()
                assert app.focused.id == "advance"
                # Right moves to back
                await pilot.press("right")
                await pilot.pause()
                assert app.focused.id == "back"
                # Right cycles back to advance
                await pilot.press("right")
                await pilot.pause()
                assert app.focused.id == "advance"
                # Left moves to back
                await pilot.press("left")
                await pilot.pause()
                assert app.focused.id == "back"
                # Enter on back pops screen
                await pilot.press("enter")
                await pilot.pause()
                assert isinstance(app.screen, DashboardScreen)

                # 3. LabScreen: arrows cycle through lab buttons
                lab = app.catalog.labs[0]
                app.push_screen(LabScreen(lab.id))
                await pilot.pause()
                assert isinstance(app.screen, LabScreen)
                # Press right -> focus moves to #open
                await pilot.press("right")
                await pilot.pause()
                assert app.focused.id == "open"
                # Press right -> #install
                await pilot.press("right")
                await pilot.pause()
                assert app.focused.id == "install"
                # Press left -> #open
                await pilot.press("left")
                await pilot.pause()
                assert app.focused.id == "open"
                # Move to #back and press enter
                await pilot.press("left")
                await pilot.pause()
                assert app.focused.id == "back"
                await pilot.press("enter")
                await pilot.pause()
                assert isinstance(app.screen, DashboardScreen)
        finally:
            app.shutdown_resources()

    asyncio.run(scenario())
