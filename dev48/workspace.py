from __future__ import annotations

from pathlib import Path
import json
import shutil
import subprocess

from .models import Lab


def ensure_lab_workspace(root: Path, lab: Lab) -> Path:
    target = root / lab.id
    target.mkdir(parents=True, exist_ok=True)
    readme = target / "README.md"
    if not readme.exists():
        requirements = "\n".join(f"- [ ] {item}" for item in lab.requirements)
        rubric = "\n".join(f"- {item}" for item in lab.rubric)
        readme.write_text(
            f"# {lab.title}\n\n{lab.description}\n\n## Requisiti\n\n{requirements}\n\n## Valutazione\n\n{rubric}\n",
            encoding="utf-8",
        )
    if lab.workspace_template == "react":
        _ensure_react_project(target, lab)
    else:
        solution = target / "solution.js"
        if not solution.exists():
            solution.write_text(
                "// DEV//48 — descrivi prima input, output e casi limite.\n\nexport function solve(input) {\n  // TODO\n  return input;\n}\n",
                encoding="utf-8",
            )
        test = target / "solution.test.js"
        if not test.exists():
            test.write_text(
                "import test from 'node:test';\nimport assert from 'node:assert/strict';\nimport { solve } from './solution.js';\n\ntest('gestisce una lista vuota', () => {\n  assert.deepEqual(solve([]), []);\n});\n\ntest('restituisce soltanto gli elementi attivi senza mutare input', () => {\n  const input = [{id:1, active:true}, {id:2, active:false}];\n  const snapshot = structuredClone(input);\n  assert.deepEqual(solve(input), [{id:1, active:true}]);\n  assert.deepEqual(input, snapshot);\n});\n",
                encoding="utf-8",
            )
        package = target / "package.json"
        if not package.exists():
            package.write_text(json.dumps({"type":"module","scripts":{"test":"node --test"}}, indent=2), encoding="utf-8")
        solution_guide = target / "SOLUTION.md"
        if not solution_guide.exists():
            solution_guide.write_text(
                "# Soluzione commentata\n\nAprila dopo almeno due tentativi reali.\n\n"
                "```js\nexport function solve(input) {\n  if (!Array.isArray(input)) throw new TypeError('input deve essere un array');\n  return input.filter(item => item.active === true);\n}\n```\n\n"
                "`filter` crea un nuovo array, quindi l'input non viene mutato. Il controllo iniziale rende esplicito il contratto della funzione. Aggiungeresti poi i requisiti specifici del brief mantenendo test piccoli e indipendenti.\n",
                encoding="utf-8",
            )
    return target


def _ensure_react_project(target: Path, lab: Lab) -> None:
    files = {
        "package.json": json.dumps({
            "name": lab.id, "private": True, "version": "1.0.0", "type": "module",
            "scripts": {"dev":"vite", "test":"vitest", "build":"vite build"},
            "dependencies": {"react":"19.2.8", "react-dom":"19.2.8"},
            "devDependencies": {"@vitejs/plugin-react":"6.0.5", "vite":"8.2.1", "vitest":"4.1.10", "jsdom":"29.1.1", "@testing-library/react":"16.3.2", "@testing-library/jest-dom":"7.0.0"},
        }, indent=2),
        "index.html": '<!doctype html><html lang="it"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DEV48 Lab</title></head><body><div id="root"></div><script type="module" src="/src/main.jsx"></script></body></html>',
        "vite.config.js": "import { defineConfig } from 'vite';\nimport react from '@vitejs/plugin-react';\nexport default defineConfig({ plugins:[react()], test:{ environment:'jsdom', globals:true, setupFiles:'./src/testSetup.js' } });\n",
        "src/main.jsx": "import React from 'react';\nimport { createRoot } from 'react-dom/client';\nimport App from './App.jsx';\nimport './styles.css';\ncreateRoot(document.getElementById('root')).render(<React.StrictMode><App /></React.StrictMode>);\n",
        "src/App.jsx": """import { useMemo, useState } from 'react';

const initialSubjects = [
  { id: 1, name: 'Mario Rossi', zone: 'Centro', active: true },
  { id: 2, name: 'Anna Bianchi', zone: 'Nord', active: false },
];

export default function App() {
  const [subjects, setSubjects] = useState(initialSubjects);
  const [query, setQuery] = useState('');
  const visibleSubjects = useMemo(
    () => subjects.filter(subject => subject.name.toLowerCase().includes(query.toLowerCase())),
    [subjects, query],
  );

  function removeSubject(id) {
    // TODO: implementazione immutabile
  }

  return (
    <main className="page">
      <h1>Archivio soggetti</h1>
      <label htmlFor="search">Cerca</label>
      <input id="search" value={query} onChange={event => setQuery(event.target.value)} />
      <p>{visibleSubjects.length} risultati</p>
      <ul>
        {visibleSubjects.map(subject => (
          <li key={subject.id}>
            <span>{subject.name}</span>
            <button onClick={() => removeSubject(subject.id)}>Elimina</button>
          </li>
        ))}
      </ul>
    </main>
  );
}
""",
        "src/styles.css": """:root{font-family:Inter,system-ui;background:#0b1020;color:#e7eefc}*{box-sizing:border-box}.page{width:min(100% - 2rem,60rem);margin:3rem auto;padding:2rem;background:#131b2f;border:1px solid #283654;border-radius:18px}input{display:block;width:100%;margin:.5rem 0 1rem;padding:.8rem;background:#0b1020;color:inherit;border:1px solid #3b4e75;border-radius:8px}li{display:flex;justify-content:space-between;padding:1rem;border-bottom:1px solid #283654}button{background:#8b5cf6;color:white;border:0;padding:.55rem .9rem;border-radius:8px}""",
        "src/testSetup.js": "import '@testing-library/jest-dom/vitest';\n",
        "src/App.test.jsx": """import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import App from './App.jsx';

describe('DEV48 lab', () => {
  it('filters subjects', () => {
    render(<App />);
    fireEvent.change(screen.getByLabelText('Cerca'), { target: { value: 'Anna' } });
    expect(screen.getByText('Anna Bianchi')).toBeInTheDocument();
    expect(screen.queryByText('Mario Rossi')).not.toBeInTheDocument();
  });

  it('removes a subject', () => {
    render(<App />);
    const buttons = screen.getAllByRole('button', { name: 'Elimina' });
    fireEvent.click(buttons[0]);
    expect(screen.queryByText('Mario Rossi')).not.toBeInTheDocument();
  });
});
""",
    }
    for relative, content in files.items():
        path = target / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_text(content, encoding="utf-8")
    solution_guide = target / "SOLUTION.md"
    if not solution_guide.exists():
        solution_guide.write_text(
            "# Soluzione commentata\n\nAprila dopo almeno due tentativi reali.\n\n"
            "La parte minima che completa lo starter è:\n\n"
            "```jsx\nfunction removeSubject(id) {\n  setSubjects(current => current.filter(subject => subject.id !== id));\n}\n```\n\n"
            "L'updater funzionale usa sempre lo stato più recente. `filter` restituisce un nuovo array e conserva l'immutabilità richiesta da React. Dopo aver ottenuto i test verdi, estendi il progetto seguendo il brief e aggiungi test per lista vuota, input non valido ed errore API.\n",
            encoding="utf-8",
        )


def open_vscode(path: Path) -> tuple[bool, str]:
    code = shutil.which("code")
    if not code:
        return False, f"VS Code CLI non trovato. Apri manualmente: {path}"
    subprocess.Popen([code, str(path)], cwd=path)
    return True, f"Aperto in VS Code: {path}"


def install_lab_dependencies(path: Path) -> tuple[bool, str]:
    npm = shutil.which("npm")
    if not npm:
        return False, "npm non trovato."
    process = subprocess.run([npm, "install"], cwd=path, capture_output=True, text=True, timeout=300, encoding="utf-8", errors="replace")
    return process.returncode == 0, (process.stdout + "\n" + process.stderr)[-8000:]
