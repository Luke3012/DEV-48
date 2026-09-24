import asyncio

from textual.widgets import Button, DataTable, Input, Static, TextArea
from textual.containers import ScrollableContainer

from dev48.app import (
    CurriculumScreen, DashboardScreen, Dev48App, ExerciseScreen, FlashcardsScreen,
    ChallengesScreen, GlossaryScreen, LabScreen, LabsScreen, LessonScreen,
    SimulationScreen, TrackSelectionScreen,
)


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
                lesson = app.catalog.lessons[0]
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
                    (SimulationScreen(simulation), "#lab-scroll", True),
                )
                for screen, main_selector, has_actions in cases:
                    app.push_screen(screen)
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
                        assert "non controlla il DOM" in scope.content
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
                assert "ULTIMA" in str(app.screen.query_one("#resume").label)
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

                # Press 'ctrl+t' on Dashboard to switch to JS & React
                await pilot.press("ctrl+t")
                await pilot.pause()
                assert app.catalog.track == "web-js-react"
                assert "Web Development Academy" in app.title
                assert "React 19" in app.sub_title

                # Open curriculum screen
                await pilot.press("ctrl+k")
                await pilot.pause()
                assert isinstance(app.screen, CurriculumScreen)
                # Press ctrl+t while not in Dashboard -> should not switch track
                await pilot.press("ctrl+t")
                await pilot.pause()
                assert app.catalog.track == "web-js-react"
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
