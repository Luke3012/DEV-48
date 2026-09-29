from pathlib import Path
import shutil

import pytest

from dev48.models import Catalog
from dev48.runners import run_exercise, run_javascript


ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("slug,source", [
    ("two-sum", "def two_sum(nums,target):\n for i,x in enumerate(nums):\n  for j,y in enumerate(nums):\n   if i!=j and x+y==target:return [i,j]\n return None\n"),
    ("three-sum", "def three_sum(a):\n a=sorted(a)\n return [[a[i],a[j],a[k]] for i in range(len(a)) for j in range(i+1,len(a)) for k in range(j+1,len(a)) if a[i]+a[j]+a[k]==0]\n"),
    ("number-islands", "def num_islands(g):\n def visit(r,c):\n  if 0<=r<len(g) and 0<=c<len(g[0]) and g[r][c]=='1':\n   visit(r+1,c);visit(r-1,c);visit(r,c+1);visit(r,c-1)\n n=0\n for r in range(len(g)):\n  for c in range(len(g[0])):\n   if g[r][c]=='1':n+=1;visit(r,c)\n return n\n"),
    ("search-range", "from bisect import bisect_left,bisect_right\ndef search_range(a,t):\n lo=bisect_left(a,t)\n return [lo,bisect_right(a,t)] if lo<len(a) and a[lo]==t else [-1,-1]\n"),
    ("kth-largest", "def kth_largest(a,k):\n return sorted(a)[k-1]\n"),
    ("coin-change", "def coin_change(coins,amount):\n count=0\n for coin in sorted(coins,reverse=True):\n  count+=amount//coin;amount%=coin\n return -1 if amount else count\n"),
    ("subarray-sum", "def subarray_sum(a,k):\n counts={0:1};total=answer=0\n for x in a:\n  total+=x;answer+=counts.get(total-k,0);counts[total]=1\n return answer\n"),
    ("linked-list-cycle", "class ListNode:\n def __init__(self,val=0,next=None):self.val,self.next=val,next\ndef has_cycle(head):\n seen=set()\n while head:\n  if head.val in seen:return True\n  seen.add(head.val);head=head.next\n return False\n"),
    ("clone-graph", "class Node:\n def __init__(self,val=0,neighbors=None):self.val=val;self.neighbors=[] if neighbors is None else neighbors\ndef clone_graph(node):\n return node\n"),
])
def test_amazon_algorithmic_mistakes_are_rejected(slug, source):
    catalog = Catalog(ROOT / "content", track="amazon-sde-oa")
    result = run_exercise(catalog.exercise_by_id[f"sde-e-{slug}"], source, ROOT, language="python")
    assert not result.passed, (slug, result)


@pytest.mark.parametrize("language", ["node", "cpp"])
def test_final_parcel_repository_requires_cross_file_repairs(tmp_path, language, monkeypatch):
    from dev48.workspace import ensure_lab_workspace
    from dev48.runners import run_lab_tests

    if language == "cpp" and not (shutil.which("g++") or shutil.which("clang++")):
        pytest.skip("C++ compiler unavailable")
    catalog = Catalog(ROOT / "content", track="amazon-sde-oa")
    lab = catalog.lab_by_id["lab-amazon-mock-repository"].for_repository_language(language)
    workspace = ensure_lab_workspace(tmp_path, lab)
    # The repository assessment must remain executable with network APIs denied.
    preload = tmp_path / "deny_network.cjs"
    preload.write_text(
        "const deny = () => { throw new Error('DEV48 network disabled'); };\n"
        "for (const name of ['http','https']) { const m=require(name); m.request=deny; m.get=deny; }\n"
        "for (const name of ['net','tls']) { const m=require(name); m.connect=deny; if(m.createConnection)m.createConnection=deny; }\n"
        "global.fetch=deny; require('module').syncBuiltinESMExports();\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("NODE_OPTIONS", f'--require="{preload.as_posix()}"')
    monkeypatch.setenv("npm_config_offline", "true")
    initial = run_lab_tests(workspace)
    assert not initial.passed
    if language == "node":
        repairs = {
            "src/repository.js": [("parcel.customerId !== customerId", "parcel.customerId === customerId"),
                                  ("parcel.id >= id", "parcel.id === id")],
            "src/transitions.js": [("Object.values(successors).includes(target)", "successors[current] === target"),
                                   ("events: parcel.events", "events: [...parcel.events]")],
            "src/service.js": [("parcel.status !== status", "parcel.status === status"),
                               ("  parcel.events.push('viewed');\n", ""),
                               ("const key = requestId;", "const key = `${id}:${requestId}`;"),
                               ("if (requests.has(key)) return requests.get(key).response;",
                                "if (requests.has(key)) {\n    const previous = requests.get(key);\n    if (previous.target !== target) return { status: 409, body: { error: 'conflicting retry' } };\n    return previous.response;\n  }")],
            "src/controller.js": [("const body = getCustomerParcels", "const body = await getCustomerParcels"),
                                  ("if (parcel) return { status: 404", "if (!parcel) return { status: 404")],
        }
    else:
        repairs = {
            "src/repository.cpp": [("parcel.id >= id", "parcel.id == id"),
                                   ("parcel.customer_id != customer", "parcel.customer_id == customer")],
            "src/transitions.cpp": [("target == \"in_transit\" || target == \"delivered\"",
                                     "(current == \"ready\" && target == \"in_transit\") || (current == \"in_transit\" && target == \"delivered\")")],
            "src/service.cpp": [("parcel.status != status", "parcel.status == status"),
                                ('    parcel->events.push_back("viewed");\n', ""),
                                ("const auto key = request_id;", 'const auto key = id + ":" + request_id;'),
                                ("if (previous != requests.end()) return previous->second.second;",
                                 "if (previous != requests.end()) {\n        if (previous->second.first != target) return {409, std::nullopt};\n        return previous->second.second;\n    }")],
            "src/controller.cpp": [("return parcel ? Response{404, std::nullopt} : Response{200, parcel};",
                                    "return parcel ? Response{200, parcel} : Response{404, std::nullopt};")],
        }
    for relative, replacements in repairs.items():
        path = workspace / relative
        source = path.read_text(encoding="utf-8")
        for before, after in replacements:
            assert before in source, relative
            source = source.replace(before, after)
        path.write_text(source, encoding="utf-8")
    repaired = run_lab_tests(workspace)
    assert repaired.passed, repaired.output


def test_amazon_local_material_and_python_runner_need_no_network(monkeypatch):
    import socket

    def deny_network(*args, **kwargs):
        raise AssertionError("Network access attempted")

    monkeypatch.setattr(socket.socket, "connect", deny_network)
    catalog = Catalog(ROOT / "content", track="amazon-sde-oa")
    assert all(catalog.lesson_body(lesson).strip() for lesson in catalog.lessons)
    assert all(card.question and card.answer for card in catalog.flashcards)
    assert all(scenario.brief and scenario.options for scenario in catalog.work_scenarios)
    exercise = catalog.exercise_by_id["sde-e-two-sum"]
    result = run_exercise(exercise, exercise.variants["python"]["solution"], ROOT, "python")
    assert result.passed


def test_every_official_short_solution_passes():
    catalog = Catalog(ROOT / "content")
    failures = []
    for exercise in catalog.exercises:
        result = run_exercise(exercise, exercise.solution, ROOT)
        if not result.passed:
            failures.append((exercise.id, result.output, result.details))
    assert failures == []


def test_wrong_javascript_is_rejected():
    result = run_javascript(
        "function add(a,b){ return 0; }",
        ({"name":"somma","expression":"add(2,3)","expected":5},),
    )
    assert not result.passed
    assert result.score == 0


def test_javascript_timeout_is_stopped():
    result = run_javascript("while(true) {}", ({"name": "non deve terminare", "expression": "true", "expected": True},))
    assert not result.passed
    assert "Tempo scaduto" in result.output


def test_every_official_dotnet_angular_solution_passes():
    catalog = Catalog(ROOT / "content", track="dotnet-angular")
    failures = []
    for exercise in catalog.exercises:
        result = run_exercise(exercise, exercise.solution, ROOT)
        if not result.passed:
            failures.append((exercise.id, result.output, result.details))
    assert failures == []


def test_every_amazon_python_variant_passes_behavioral_tests():
    catalog = Catalog(ROOT / "content", track="amazon-sde-oa")
    failures = []
    for exercise in catalog.exercises:
        variant = exercise.variants["python"]
        result = run_exercise(exercise, variant["solution"], ROOT, language="python")
        if not result.passed:
            failures.append((exercise.id, result.output, result.details))
    assert failures == []


def test_cpp_runner_reports_missing_compiler_or_runs_all_amazon_variants():
    catalog = Catalog(ROOT / "content", track="amazon-sde-oa")
    compiler = shutil.which("g++") or shutil.which("clang++")
    if not compiler:
        from dev48.runners import run_cpp
        result = run_cpp("int add(int a,int b){return a+b;}", ({"name":"somma","assertion":"add(2,3)==5"},))
        assert not result.passed
        assert "Compilatore C++ non trovato" in result.output
        pytest.skip("GCC/Clang non è installato in questo ambiente")
    failures = []
    for exercise in catalog.exercises:
        variant = exercise.variants["cpp"]
        result = run_exercise(exercise, variant["solution"], ROOT, language="cpp")
        if not result.passed:
            failures.append((exercise.id, result.output, result.details))
    assert failures == []


def test_python_runner_limits_infinite_solutions():
    from dev48.runners import run_python
    result = run_python("while True: pass", ({"name":"termina","expression":"True","expected":True},))
    assert not result.passed
    assert "Tempo scaduto" in result.output


def test_python_runner_reports_syntax_runtime_and_wrong_answers():
    from dev48.runners import run_python

    syntax = run_python("def solve(:\n    return 1", ({"name": "sintassi", "expression": "True", "expected": True},))
    assert not syntax.passed
    assert "Errore di sintassi Python" in syntax.output

    runtime = run_python("def solve(value):\n    raise RuntimeError('failure')", ({"name": "runtime", "expression": "solve(1)", "expected": 1},))
    assert not runtime.passed
    assert "RuntimeError" in "\n".join(runtime.details)

    wrong = run_python("def solve(value):\n    return value + 1", ({"name": "risposta errata", "expression": "solve(1)", "expected": 1},))
    assert not wrong.passed
    assert wrong.score == 0


def test_python_runner_limits_large_stdout():
    from dev48.runners import run_python

    result = run_python("print('x' * 1_200_000)", ({"name": "output", "expression": "True", "expected": True},))
    assert not result.passed
    assert "limite di output" in result.output.lower()


@pytest.mark.parametrize(
    ("process_result", "expected_message"),
    [
        ((0, "output troncato", "limite", False, True), "limite di output"),
        ((-9, "", "", True, False), "90 secondi"),
    ],
)
def test_node_lab_runner_enforces_output_and_time_limits(monkeypatch, tmp_path, process_result, expected_message):
    import dev48.runners as runners

    (tmp_path / "package.json").write_text('{"scripts":{"test":"node test.js"}}', encoding="utf-8")
    monkeypatch.setattr(runners.shutil, "which", lambda name: "npm" if name == "npm" else None)
    monkeypatch.setattr(runners, "_run_process_limited", lambda *args, **kwargs: process_result)

    result = runners.run_lab_tests(tmp_path)

    assert not result.passed
    assert expected_message in result.output.casefold()


def test_cpp_lab_runner_rejects_output_limited_compilation(monkeypatch, tmp_path):
    import dev48.runners as runners

    (tmp_path / "src").mkdir()
    (tmp_path / "tests").mkdir()
    (tmp_path / "src" / "main.cpp").write_text("int main() { return 0; }", encoding="utf-8")
    (tmp_path / "tests" / "main.cpp").write_text("int main();", encoding="utf-8")
    monkeypatch.setattr(runners.shutil, "which", lambda name: "g++" if name == "g++" else None)
    monkeypatch.setattr(runners, "_run_process_limited", lambda *args, **kwargs: (1, "partial", "limit", False, True))

    result = runners.run_cpp_lab_tests(tmp_path)

    assert not result.passed
    assert "oltre il limite" in result.output.casefold()


def test_amazon_node_labs_execute_with_expected_initial_failures(tmp_path):
    from dev48.runners import run_lab_tests
    from dev48.workspace import ensure_lab_workspace

    catalog = Catalog(ROOT / "content", track="amazon-sde-oa")
    if shutil.which("npm") is None:
        pytest.skip("npm non è installato in questo ambiente")
    results = []
    for lab in catalog.labs:
        if lab.workspace_template == "amazon_node":
            workspace = ensure_lab_workspace(tmp_path, lab)
            result = run_lab_tests(workspace)
            results.append((lab.id, result.passed, result.output))
    assert len(results) == 4
    assert all(not passed and "node --test" in output for _, passed, output in results), results


def test_amazon_cpp_labs_fail_initially_and_pass_after_focused_fixes(tmp_path):
    from dev48.runners import run_lab_tests
    from dev48.workspace import ensure_lab_workspace

    if not (shutil.which("g++") or shutil.which("clang++")):
        pytest.skip("GCC/Clang non è installato in questo ambiente")
    catalog = Catalog(ROOT / "content", track="amazon-sde-oa")
    labs = [lab for lab in catalog.labs if lab.workspace_template == "amazon_cpp"]
    assert len(labs) == 2
    for lab in labs:
        workspace = ensure_lab_workspace(tmp_path, lab)
        initial = run_lab_tests(workspace)
        assert not initial.passed, (lab.id, initial.output)
        assert "Errore del compilatore" not in initial.output, initial.output
        for source in (workspace / "src").glob("*.cpp"):
            text = source.read_text(encoding="utf-8")
            text = text.replace("if (!subject.active)", "if (subject.active)")
            text = text.replace("subject.id >= id", "subject.id == id")
            text = text.replace("item.id >= id", "item.id == id")
            text = text.replace("index > items.size()", "index >= items.size()")
            source.write_text(text, encoding="utf-8")
        repaired = run_lab_tests(workspace)
        assert repaired.passed, (lab.id, repaired.output)


def test_app_runner_passes_a_root_node_project(tmp_path):
    from dev48.runners import run_lab_tests

    (tmp_path / "package.json").write_text(
        '{"private":true,"type":"module","scripts":{"test":"node --test"}}',
        encoding="utf-8",
    )
    tests_dir = tmp_path / "test"
    tests_dir.mkdir()
    (tests_dir / "pass.test.js").write_text(
        "import test from 'node:test'; import assert from 'node:assert/strict'; "
        "test('runner', () => assert.equal(2 + 2, 4));\n",
        encoding="utf-8",
    )

    result = run_lab_tests(tmp_path)

    assert result.passed
    assert "tests 1" in result.output


def test_cpp_runner_rejects_nonzero_exit_even_after_passing_marker(monkeypatch, tmp_path):
    import dev48.runners as runners

    monkeypatch.setattr(runners.shutil, "which", lambda _: "fake-cpp")
    calls = 0

    def fake_process(args, **kwargs):
        nonlocal calls
        calls += 1
        if calls == 1:
            binary = Path(args[args.index("-o") + 1])
            binary.write_text("fake executable", encoding="utf-8")
            return 0, "", "", False, False
        return 1, "DEV48_RESULT:0:1\n", "failure after assertions", False, False

    monkeypatch.setattr(runners, "_run_process_limited", fake_process)
    result = runners.run_cpp("int add(int a, int b) { return a + b; }", ({"name": "sum", "assertion": "add(2,3)==5"},))
    assert not result.passed
    assert "Errore di esecuzione C++" in result.output


def test_cpp_runner_rejects_output_limited_results(monkeypatch):
    import dev48.runners as runners

    monkeypatch.setattr(runners.shutil, "which", lambda _: "fake-cpp")
    calls = 0

    def fake_process(args, **kwargs):
        nonlocal calls
        calls += 1
        if calls == 1:
            Path(args[args.index("-o") + 1]).write_text("fake executable", encoding="utf-8")
            return 0, "", "", False, False
        return 0, "DEV48_RESULT:0:1\n", "", False, True

    monkeypatch.setattr(runners, "_run_process_limited", fake_process)
    result = runners.run_cpp("int add(int a, int b) { return a + b; }", ({"name": "sum", "assertion": "add(2,3)==5"},))
    assert not result.passed
    assert "oltre il limite" in result.output.casefold()


def test_csharp_runner_detects_compiler_error():
    from dev48.runners import run_csharp
    result = run_csharp("public class Bad { public static int Broken( => 123; }", ({"name": "test", "expression": "1", "expected": 1},))
    assert not result.passed
    assert "CS" in result.output


def test_angular_signals_runner():
    from dev48.runners import run_angular
    code = """
    export class Counter {
        count = signal(10);
        double = computed(() => this.count() * 2);
        inc() { this.count.update(x => x + 1); }
    }
    """
    tests = (
        {"name": "initial", "expression": "(new Counter()).count()", "expected": 10},
        {"name": "computed double", "expression": "(new Counter()).double()", "expected": 20},
    )
    result = run_angular(code, tests)
    assert result.passed
    assert result.score == 100


def test_theory_check_discloses_that_it_checks_terms_only():
    from dev48.runners import run_semantic_text
    result = run_semantic_text(
        "This answer uses signal and computed, but does not explain them.",
        ({"name": "signal", "alternatives": ["signal"]}, {"name": "computed", "alternatives": ["computed"]}),
    )
    assert result.passed
    assert "non che la spiegazione sia corretta" in result.output


def test_typescript_comment_text_does_not_satisfy_code_requirement():
    from dev48.runners import run_typescript
    result = run_typescript(
        "// export interface OrderDto { id: number }\nconst answer = 1;",
        ({"name": "OrderDto", "mode": "contains", "value": "export interface OrderDto"},),
    )
    assert not result.passed


def test_typescript_url_strings_are_not_stripped_as_comments():
    from dev48.runners import run_typescript
    result = run_typescript(
        'const endpoint: string = "https://api.example.test/subjects";',
        ({"name": "endpoint", "mode": "contains", "value": "https://api.example.test/subjects"},),
    )
    assert result.passed


def test_angular_runner_does_not_accept_markup_as_a_solution():
    from dev48.runners import run_angular
    result = run_angular(
        "<div>counter</div>",
        ({"name": "increment", "mode": "contains", "value": ".update("},),
    )
    assert not result.passed
    assert "Errore di sintassi" in result.output or "Errore di sintassi" in "\n".join(result.details)

