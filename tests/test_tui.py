import asyncio

from textual.widgets import Button, DataTable, Input

from dev48.app import (
    CurriculumScreen, DashboardScreen, Dev48App, ExerciseScreen, FlashcardsScreen,
    ChallengesScreen, GlossaryScreen, LabScreen, LabsScreen, LessonScreen,
    SimulationScreen,
)


def test_dashboard_smoke(tmp_path):
    async def scenario():
        app = Dev48App(tmp_path / "data", tmp_path / "workspace")
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
        app = Dev48App(tmp_path / "data", tmp_path / "workspace")
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
        app = Dev48App(tmp_path / "data", tmp_path / "workspace")
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
        app = Dev48App(tmp_path / "data", tmp_path / "workspace")
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
        app = Dev48App(tmp_path / "data", tmp_path / "workspace")
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
        app = Dev48App(tmp_path / "data", tmp_path / "workspace")
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


def test_resume_last_and_wide_lesson_layout(tmp_path):
    async def scenario():
        app = Dev48App(tmp_path / "data", tmp_path / "workspace")
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
    app = Dev48App(tmp_path / "data", tmp_path / "workspace")
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
