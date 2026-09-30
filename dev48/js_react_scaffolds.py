"""Executable, task-specific JS/React labs. Never overwrite learner files.

Reference implementations live alongside starters and independent behavioural
tests so a generated solution guide cannot drift from the runnable solution.
"""
from __future__ import annotations

import json
from pathlib import Path

from .models import Lab
from .js_react_ui_scaffolds import REACT_LABS, react_base_files


NODE_TEST_HEADER = "import test from 'node:test';\nimport assert from 'node:assert/strict';\n"

CRUD_REFERENCE = """export function addSubject(items, subject) {
  if (items.some(item => item.id === subject.id)) throw new Error('ID duplicato');
  return [...items, { ...subject }];
}
export function updateSubject(items, id, patch) {
  return items.map(item => item.id === id ? { ...item, ...patch, id: item.id } : item);
}
export function removeSubject(items, id) { return items.filter(item => item.id !== id); }
export function searchSubjects(items, query) {
  const normalized = query.trim().toLowerCase();
  return items.filter(item => item.name.toLowerCase().includes(normalized));
}
export function summarizeSubjects(items) {
  return { total: items.length, active: items.filter(item => item.active).length,
    checks: items.reduce((total, item) => total + item.checks, 0) };
}
"""

FETCH_REFERENCE = """export function createClient(request) {
  let state = { status: 'idle', data: [], error: '' };
  let version = 0;
  let controller;
  function cancel() {
    version += 1;
    controller?.abort();
    state = { status: 'idle', data: [], error: '' };
  }
  async function load(url) {
    controller?.abort();
    controller = new AbortController();
    const current = ++version;
    const signal = controller.signal;
    state = { status: 'loading', data: [], error: '' };
    try {
      const response = await request(url, { signal });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      if (!Array.isArray(data) || !data.every(item => item !== null &&
          typeof item === 'object' && Number.isInteger(item.id) && typeof item.name === 'string')) {
        throw new Error('Risposta non valida');
      }
      if (current === version) state = { status: data.length ? 'success' : 'empty', data, error: '' };
    } catch (error) {
      if (current === version) state = { status: 'error', data: [], error: error.message };
    }
    return state;
  }
  return { load, cancel, getState: () => state };
}
"""

TS_REFERENCE = """export interface Subject { id: number; name: string; active: boolean; note?: string }
export type LoadResult =
  | { status: 'success'; data: Subject[] }
  | { status: 'empty' }
  | { status: 'error'; message: string };
export function isSubject(value: unknown): value is Subject {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) return false;
  return 'id' in value && typeof value.id === 'number' && Number.isFinite(value.id) &&
    'name' in value && typeof value.name === 'string' &&
    'active' in value && typeof value.active === 'boolean' &&
    (!('note' in value) || value.note === undefined || typeof value.note === 'string');
}
export function describeResult(result: LoadResult): string {
  if (result.status === 'error') return result.message;
  if (result.status === 'empty') return 'Nessun soggetto';
  return `${result.data.length} soggetti`;
}
"""

DEBUG_REFERENCE = """export function isMissing(value) { return value === null || value === undefined; }
export function names(items) { return items.map(item => item.name); }
export function move(user, city) { return { ...user, profile: { ...user.profile, city } }; }
export function findById(items, id) { return items.find(item => item.id === id); }
export function total(items) { return items.reduce((sum, item) => sum + item.checks, 0); }
export function parseCount(value) {
  if ((typeof value !== 'number' && typeof value !== 'string') ||
      (typeof value === 'string' && !value.trim())) throw new Error('Valore invalido');
  const number = Number(value);
  if (!Number.isFinite(number) || number < 0) throw new Error('Valore invalido');
  return number;
}
"""

PLAIN_LABS = {
    "lab-js-crud": {
        "starters": {"solution.mjs": """export function addSubject(items, subject) { throw new Error('TODO'); }
export function updateSubject(items, id, patch) { throw new Error('TODO'); }
export function removeSubject(items, id) { throw new Error('TODO'); }
export function searchSubjects(items, query) { throw new Error('TODO'); }
export function summarizeSubjects(items) { throw new Error('TODO'); }
"""},
        "references": {"solution.mjs": CRUD_REFERENCE},
        "tests": {"solution.test.mjs": NODE_TEST_HEADER + """import { addSubject, updateSubject, removeSubject, searchSubjects, summarizeSubjects } from './solution.mjs';
const fixture = () => [{id:1,name:'Anna',active:true,checks:4}, {id:2,name:'Mario',active:false,checks:2}];
test('aggiunge senza mutare e rifiuta duplicati', () => {
  const items=fixture(), before=structuredClone(items), added={id:3,name:'Sara',active:true,checks:1};
  assert.deepEqual(addSubject(items,added), [...before,added]);
  assert.deepEqual(items,before);
  assert.throws(() => addSubject(items,{id:1,name:'Duplicato'}));
});
test('modifica solo la riga scelta e conserva ID e campi', () => {
  const items=fixture(), before=structuredClone(items);
  const result=updateSubject(items,2,{name:'Mario Rossi',id:99});
  assert.deepEqual(result,[before[0],{...before[1],name:'Mario Rossi'}]);
  assert.deepEqual(items,before); assert.notEqual(result[1],items[1]);
  assert.deepEqual(updateSubject(items,8,{name:'Altro'}),before);
});
test('eliminazione, ID assente e vuoto', () => {
  const items=fixture(), before=structuredClone(items);
  assert.deepEqual(removeSubject(items,1),[before[1]]);
  assert.deepEqual(removeSubject(items,9),before);
  assert.deepEqual(removeSubject([],9),[]); assert.deepEqual(items,before);
});
test('ricerca normalizzata e nessuna corrispondenza', () => {
  assert.deepEqual(searchSubjects(fixture(),' AN '),[fixture()[0]]);
  assert.deepEqual(searchSubjects(fixture(),'zzz'),[]);
  assert.deepEqual(searchSubjects(fixture(),''),fixture());
});
test('riepilogo iniziale, vuoto e dopo un aggiornamento', () => {
  assert.deepEqual(summarizeSubjects(fixture()),{total:2,active:1,checks:6});
  assert.deepEqual(summarizeSubjects([]),{total:0,active:0,checks:0});
  const items=updateSubject(fixture(),2,{active:true,checks:5});
  assert.deepEqual(summarizeSubjects(searchSubjects(items,'')),{total:2,active:2,checks:9});
});
"""},
        "notes": "Le firme sono fornite, le implementazioni sono TODO. La suite verifica output e conservazione dell'input. Non impone map/filter né una formattazione specifica.",
    },
    "lab-js-debug": {
        "starters": {"solution.mjs": """export function isMissing(value) { return !value; }
export function names(items) { return items.map(item => { item.name; }); }
export function move(user, city) { const copy={...user}; copy.profile.city=city; return copy; }
export function findById(items, id) { return items.find(item => item.id >= id); }
export function total(items) { return items.reduce((sum,item) => sum + item.checks); }
export function parseCount(value) { return Number(value); }
"""},
        "references": {"solution.mjs": DEBUG_REFERENCE},
        "tests": {"solution.test.mjs": NODE_TEST_HEADER + """import { isMissing,names,move,findById,total,parseCount } from './solution.mjs';
test('assenza non è zero o false', () => {
  assert.equal(isMissing(null),true); assert.equal(isMissing(undefined),true);
  for(const value of [0,false,'','0']) assert.equal(isMissing(value),false);
});
test('callback restituisce i nomi', () => { assert.deepEqual(names([{name:'Anna'},{name:'Mario'}]),['Anna','Mario']); assert.deepEqual(names([]),[]); });
test('copia annidata conserva la città originale', () => {
  const user={id:1,profile:{city:'Roma',age:30}}, before=structuredClone(user);
  assert.deepEqual(move(user,'Milano'),{id:1,profile:{city:'Milano',age:30}}); assert.deepEqual(user,before);
});
test('ID esatto e assenza', () => {
  const items=[{id:8},{id:0},{id:2}]; assert.deepEqual(findById(items,0),{id:0}); assert.equal(findById(items,3),undefined);
});
test('aggregazione definita anche su vuoto', () => { assert.equal(total([{checks:4},{checks:2}]),6); assert.equal(total([]),0); });
test('validazione numerica non confonde assenza e zero', () => {
  assert.equal(parseCount('12'),12); assert.equal(parseCount(0),0);
  for(const value of ['',null,undefined,false,-1,'abc',Infinity]) assert.throws(() => parseCount(value));
});
"""},
        "notes": "Sei funzioni esistono già e contengono difetti. Non ci sono TODO che indicano la riga da correggere: usa i sintomi nei sei test e conserva un diario delle ipotesi.",
    },
    "lab-fetch": {
        "starters": {"solution.mjs": """export function createClient(request) {
  // Contratto: load(url) è async; getState() restituisce {status,data,error}; cancel() annulla la richiesta corrente.
  throw new Error('TODO: client asincrono');
}
"""},
        "references": {"solution.mjs": FETCH_REFERENCE},
        "tests": {"solution.test.mjs": NODE_TEST_HEADER + """import { createClient } from './solution.mjs';
const response = data => ({ok:true,status:200,json:async () => data});
function deferred() { let resolve; const promise=new Promise(done => {resolve=done;}); return {promise,resolve}; }
test('idle, loading, successo con URL e signal', async () => {
  const pending=deferred(); let received;
  const client=createClient((url, options) => {received={url,...options}; return pending.promise;});
  assert.equal(client.getState().status,'idle'); const work=client.load('/subjects');
  assert.equal(client.getState().status,'loading'); assert.equal(received.url,'/subjects'); assert.ok(received.signal instanceof AbortSignal);
  pending.resolve(response([{id:1,name:'Anna'}])); await work;
  assert.deepEqual(client.getState(),{status:'success',data:[{id:1,name:'Anna'}],error:''});
});
test('successo vuoto distinto dal fallimento', async () => {
  const client=createClient(async () => response([])); await client.load('/'); assert.equal(client.getState().status,'empty');
});
test('HTTP fallito non legge il JSON, retry riesce', async () => {
  let calls=0,read=false;
  const client=createClient(async () => ++calls === 1 ? {ok:false,status:503,json:async () => {read=true;return [];}} : response([{id:2,name:'Mario'}]));
  await client.load('/'); assert.equal(client.getState().status,'error'); assert.match(client.getState().error,/503/); assert.equal(read,false);
  await client.load('/'); assert.equal(client.getState().status,'success'); assert.equal(calls,2);
});
test('rete, JSON e forma errati sono errori', async () => {
  for(const request of [async () => {throw new Error('offline');}, async () => ({ok:true,json:async () => {throw new Error('JSON');}}), async () => response({items:[]}), async () => response([{id:'1',name:4}])]) {
    const client=createClient(request); await client.load('/'); assert.equal(client.getState().status,'error'); assert.ok(client.getState().error);
  }
});
test('risposta vecchia ignorata anche se il trasporto ignora signal', async () => {
  const first=deferred(), second=deferred(); let signal;
  const client=createClient((url,options) => {if(url==='/first'){signal=options.signal;return first.promise;} return second.promise;});
  const a=client.load('/first'), b=client.load('/second'); assert.equal(signal.aborted,true);
  second.resolve(response([{id:2,name:'Nuova'}])); await b;
  first.resolve(response([{id:1,name:'Vecchia'}])); await a;
  assert.deepEqual(client.getState().data,[{id:2,name:'Nuova'}]);
});
test('cancel non accetta una risposta tardiva', async () => {
  const pending=deferred(); const client=createClient(() => pending.promise); const work=client.load('/'); client.cancel();
  pending.resolve(response([{id:1,name:'Tardi'}])); await work; assert.equal(client.getState().status,'idle');
});
"""},
        "notes": "Trasporto e Promise controllate sono forniti nei test. Non serve una connessione né un server. Il modello di stato non è una prova dei messaggi visibili: il lab React API completa quel collegamento.",
    },
    "lab-ts-model": {
        "starters": {"model.ts": """export interface Subject { id: number; name: string; active: boolean; note?: string }
// TODO: definisci LoadResult e completa le due funzioni senza any o cast.
export function isSubject(value: unknown): value is Subject { return false; }
export function describeResult(result: unknown): string { return ''; }
"""},
        "references": {"model.ts": TS_REFERENCE},
        "tests": {"model.test.mjs": NODE_TEST_HEADER + """import { isSubject,describeResult } from './model.ts';
test('contratto valido con nota facoltativa', () => {
  assert.equal(isSubject({id:1,name:'Anna',active:true}),true);
  assert.equal(isSubject({id:2,name:'Mario',active:false,note:'Nord'}),true);
});
test('campi presenti ma invalidi non soddisfano il contratto', () => {
  for(const value of [null,[],{id:'1',name:'Anna',active:true},{id:1,name:2,active:true},{id:1,name:'Anna'}, {id:Infinity,name:'Anna',active:true}, {id:1,name:'Anna',active:true,note:9}]) assert.equal(isSubject(value),false);
});
test('descrive stati alternativi senza leggere campi assenti', () => {
  assert.equal(describeResult({status:'success',data:[{id:1,name:'Anna',active:true}]}),'1 soggetti');
  assert.equal(describeResult({status:'empty'}),'Nessun soggetto');
  assert.equal(describeResult({status:'error',message:'offline'}),'offline');
});
"""},
        "notes": "Node 24 rimuove i tipi ed esegue i test a runtime. La union e le annotazioni vanno controllate separatamente con un compilatore TypeScript disponibile nell'ambiente; questi test non certificano la correttezza statica dei tipi.",
    },
    "lab-debug-app": {
        "starters": {
            "repository.mjs": """export function find(items,id) { return items.find(item => item.id >= id); }
export function update(items,id,patch) { return items.map(item => { if(item.id===id) Object.assign(item,patch); return item; }); }
""",
            "format.mjs": "export function label(item) { return item.name.trim(); }\n",
            "service.mjs": """import {find,update} from './repository.mjs';
import {label} from './format.mjs';
export function search(items,query) { return items.filter(item => item.name.includes(query)); }
export function rename(items,id,name) { return update(items,id,{name}); }
export function describe(items,id) { return label(find(items,id)); }
""",
        },
        "references": {
            "repository.mjs": "export function find(items,id) { return items.find(item => item.id === id); }\nexport function update(items,id,patch) { return items.map(item => item.id===id ? {...item,...patch,id:item.id} : item); }\n",
            "format.mjs": "export function label(item) { return item ? item.name.trim() : 'Soggetto assente'; }\n",
            "service.mjs": """import {find,update} from './repository.mjs';
import {label} from './format.mjs';
export function search(items,query) { return items.filter(item => item.name.toLowerCase().includes(query.trim().toLowerCase())); }
export function rename(items,id,name) {
  if (!name.trim()) throw new Error('Nome obbligatorio');
  return update(items,id,{name:name.trim()});
}
export function describe(items,id) { return label(find(items,id)); }
""",
        },
        "tests": {"app.test.mjs": NODE_TEST_HEADER + """import {search,rename,describe} from './service.mjs';
const fixture=() => [{id:8,name:'Sara',active:true},{id:0,name:'Anna',active:false},{id:2,name:'Mario',active:true}];
test('ricerca esatta per ID zero e assente', () => { assert.equal(describe(fixture(),0),'Anna'); assert.equal(describe(fixture(),3),'Soggetto assente'); });
test('ricerca normalizza e conserva dati', () => { const items=fixture(),before=structuredClone(items); assert.deepEqual(search(items,' AN '),[before[1]]); assert.deepEqual(items,before); });
test('rename integra servizio e repository senza mutare input', () => { const items=fixture(),before=structuredClone(items); const next=rename(items,2,' Mario Rossi '); assert.equal(describe(next,2),'Mario Rossi'); assert.deepEqual(items,before); assert.equal(next[0].name,'Sara'); });
test('nome vuoto rifiutato, ID assente conserva contenuto', () => { assert.throws(() => rename(fixture(),2,'  ')); assert.deepEqual(rename(fixture(),99,'Nuovo'),fixture()); });
test('stati senza elementi', () => { assert.deepEqual(search([],''),[]); assert.equal(describe([],1),'Soggetto assente'); });
"""},
        "notes": "Sono forniti tre moduli che collaborano e contengono difetti. I test osservano il comportamento del servizio, senza richiedere uno specifico nome di helper o stile di implementazione.",
    },
}


PLAIN_LABS["lab-html-dashboard"] = {
    "starters": {
        "index.html": '<!doctype html><html lang="it"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="stylesheet" href="/styles.css"><title>Archivio</title></head><body><!-- TODO: struttura semantica, ricerca e card --></body></html>\n',
        "styles.css": "/* TODO: layout fluido, griglia, focus e breakpoint */\n",
    },
    "references": {
        "index.html": """<!doctype html>
<html lang="it"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="stylesheet" href="/styles.css"><title>Archivio</title></head><body>
<nav aria-label="Principale"><a href="#archive">Archivio</a></nav>
<main id="archive"><h1>Archivio soggetti</h1>
<form role="search"><label for="search">Cerca</label>
<input id="search" name="search" type="search" aria-describedby="search-help">
<p id="search-help">Questa dashboard è statica: il filtro sarà implementato nel laboratorio React.</p>
<button type="submit">Cerca</button></form>
<section aria-labelledby="subjects-title"><h2 id="subjects-title">Soggetti</h2>
<div class="cards"><article><h3>Anna Bianchi</h3><p>Attiva · Nord</p></article>
<article><h3>Mario Rossi</h3><p>Inattivo · Centro</p></article></div></section>
</main></body></html>
""",
        "styles.css": """* { box-sizing: border-box; }
body { font-family: system-ui, sans-serif; margin: 0; color: #1d2838; background: #f4f6f8; }
nav, main { width: calc(100% - 2rem); max-width: 64rem; margin: 1rem auto; }
label, input { display: block; }
input { max-width: 100%; padding: .5rem; }
.cards { display: grid; gap: 1rem; grid-template-columns: 1fr; }
article { padding: 1rem; border: 1px solid #bac5d3; background: white; overflow-wrap: anywhere; }
button { padding: .5rem 1rem; }
:focus-visible { outline: 3px solid #255ca8; outline-offset: 3px; }
@media (min-width: 48rem) { .cards { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
""",
    },
    "extra": {"preview.mjs": """import {createServer} from 'node:http';
import {readFileSync} from 'node:fs';
const files={'/':['index.html','text/html; charset=utf-8'],'/styles.css':['styles.css','text/css; charset=utf-8']};
createServer((req,res) => {
  const entry=files[new URL(req.url,'http://localhost').pathname];
  if(!entry){res.writeHead(404);res.end('Not found');return;}
  res.writeHead(200,{'Content-Type':entry[1]});res.end(readFileSync(entry[0]));
}).listen(4174,'127.0.0.1',() => console.log('http://127.0.0.1:4174'));
"""},
    "tests": {"dashboard.test.mjs": NODE_TEST_HEADER + """import {readFileSync} from 'node:fs';
const html=readFileSync('index.html','utf8').replace(/<!--[\\s\\S]*?-->/g,'');
const css=readFileSync('styles.css','utf8').replace(/\\/\\*[\\s\\S]*?\\*\\//g,'');
test('struttura: main, heading, navigazione e card', () => {
  for(const tag of ['main','h1','h2','nav','a','article','button']) assert.match(html,new RegExp(`<${tag}\\\\b`));
});
test('struttura: label, campo e descrizione corrispondenti', () => {
  assert.match(html,/<label[^>]*for=["']search["']/); assert.match(html,/<input[^>]*id=["']search["']/);
  assert.match(html,/aria-describedby=["']search-help["']/); assert.match(html,/id=["']search-help["']/);
});
test('regole CSS presenti: layout fluido, griglia, focus e breakpoint', () => {
  for(const pattern of [/max-width\\s*:/,/display\\s*:\\s*grid/,/:focus-visible/,/@media\\s*\\(\\s*min-width/]) assert.match(css,pattern);
});
"""},
    "notes": "HTML e CSS sono TODO. I tre test verificano struttura e presenza di regole, non effettuano rendering. Per la prova reale avvia `node preview.mjs`, apri http://127.0.0.1:4174 e controlla tastiera, larghezze intermedie e zoom. Il form è statico: il filtro funzionante appartiene al lab React.",
}


SQL_SCHEMA = """CREATE TABLE subjects (
  id INTEGER PRIMARY KEY, name TEXT NOT NULL,
  active INTEGER NOT NULL CHECK(active IN (0,1)), zone TEXT NOT NULL
);
CREATE TABLE measures (
  id INTEGER PRIMARY KEY, subject_id INTEGER NOT NULL REFERENCES subjects(id), type TEXT NOT NULL
);
CREATE TABLE checks (
  id INTEGER PRIMARY KEY, subject_id INTEGER NOT NULL REFERENCES subjects(id),
  amount INTEGER NOT NULL CHECK(amount >= 0)
);
CREATE INDEX idx_subjects_zone_active ON subjects(zone,active);
"""
SQL_TRANSACTION = """export function removeSubject(db,id) {
  if (!db.prepare('SELECT id FROM subjects WHERE id = ?').get(id)) return false;
  db.exec('BEGIN');
  try {
    db.prepare('DELETE FROM checks WHERE subject_id = ?').run(id);
    db.prepare('DELETE FROM measures WHERE subject_id = ?').run(id);
    db.prepare('DELETE FROM subjects WHERE id = ?').run(id);
    db.exec('COMMIT');
    return true;
  } catch (error) {
    db.exec('ROLLBACK');
    throw error;
  }
}
"""
PLAIN_LABS["lab-sql"] = {
    "starters": {
        "schema.sql": """-- TODO: aggiungi vincoli, riferimenti e un indice motivato.
CREATE TABLE subjects(id INTEGER PRIMARY KEY,name TEXT,active INTEGER,zone TEXT);
CREATE TABLE measures(id INTEGER PRIMARY KEY,subject_id INTEGER,type TEXT);
CREATE TABLE checks(id INTEGER PRIMARY KEY,subject_id INTEGER,amount INTEGER);
""",
        "queries.sql": "-- name: active\nSELECT ...;\n\n-- name: all_measures\nSELECT ...;\n",
        "solution.mjs": "export function removeSubject(db,id) { throw new Error('TODO: transazione'); }\n",
    },
    "references": {
        "schema.sql": SQL_SCHEMA,
        "queries.sql": "-- name: active\nSELECT id,name FROM subjects WHERE active=1 ORDER BY name;\n\n-- name: all_measures\nSELECT s.name,m.type FROM subjects s LEFT JOIN measures m ON m.subject_id=s.id ORDER BY s.name;\n",
        "solution.mjs": SQL_TRANSACTION,
    },
    "extra": {"database.mjs": """import {DatabaseSync} from 'node:sqlite';
import {readFileSync} from 'node:fs';
export function database() {
  const db=new DatabaseSync(':memory:');
  db.exec('PRAGMA foreign_keys=ON'); db.exec(readFileSync('schema.sql','utf8'));
  db.exec(`INSERT INTO subjects VALUES(1,'Mario',1,'Centro'),(2,'Anna',0,'Nord'),(3,'Sara',1,'Sud');
    INSERT INTO measures VALUES(1,1,'Obbligo'),(2,3,'Controllo');
    INSERT INTO checks VALUES(1,1,4);`);
  return db;
}
export function query(name) {
  const sections=readFileSync('queries.sql','utf8').split('-- name: ').slice(1);
  const section=sections.find(part => part.split('\\n')[0].trim()===name);
  if(!section) throw new Error(`Query mancante: ${name}`);
  return section.slice(section.indexOf('\\n')+1).trim();
}
"""},
    "tests": {"database.test.mjs": NODE_TEST_HEADER + """import {database,query} from './database.mjs';
import {removeSubject} from './solution.mjs';
function rows(db,sql){return db.prepare(sql).all().map(row => Object.values(row));}
test('query dei soli attivi in ordine e LEFT JOIN con assenza', () => {
  const db=database();try {
    assert.deepEqual(rows(db,query('active')),[[1,'Mario'],[3,'Sara']]);
    assert.deepEqual(rows(db,query('all_measures')),[['Anna',null],['Mario','Obbligo'],['Sara','Controllo']]);
  } finally {db.close();}
});
test('vincoli realmente applicati dal database', () => {
  const db=database();try {
    for(const sql of ["INSERT INTO subjects VALUES(4,NULL,1,'Nord')", "INSERT INTO subjects VALUES(4,'Altro',2,'Nord')", "INSERT INTO measures VALUES(8,99,'Controllo')", "INSERT INTO checks VALUES(8,1,-1)"]) assert.throws(() => db.exec(sql));
  } finally {db.close();}
});
test('eliminazione atomica conserva gli altri soggetti', () => {
  const db=database();try {
    assert.equal(removeSubject(db,1),true); assert.equal(removeSubject(db,99),false);
    assert.deepEqual(rows(db,'SELECT id FROM subjects ORDER BY id'),[[2],[3]]);
    assert.deepEqual(rows(db,'SELECT subject_id FROM measures ORDER BY id'),[[3]]);
    assert.deepEqual(rows(db,'SELECT subject_id FROM checks'),[]);
  } finally {db.close();}
});
test('errore dopo le prime cancellazioni esegue rollback', () => {
  const db=database();try {
    db.exec("CREATE TRIGGER prevent_delete BEFORE DELETE ON subjects BEGIN SELECT RAISE(ABORT,'stop'); END;");
    assert.throws(() => removeSubject(db,1));
    assert.deepEqual(rows(db,'SELECT id FROM subjects ORDER BY id'),[[1],[2],[3]]);
    assert.deepEqual(rows(db,'SELECT subject_id FROM measures ORDER BY id'),[[1],[3]]);
    assert.deepEqual(rows(db,'SELECT subject_id FROM checks'),[[1]]);
  } finally {db.close();}
});
"""},
    "notes": "Database in memoria e fixture sono forniti. Completa schema, le due query mantenendo i marcatori `-- name:` e la transazione. Node 24 usa SQLite reale tramite node:sqlite; l'API integrata può emettere un avviso sperimentale. Il test di rollback provoca un errore dopo le prime cancellazioni, non si limita a cercare BEGIN nel testo.",
}


GIT_SETUP = """import {existsSync,mkdirSync,writeFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
if(existsSync('repo/.git')) { console.log('Repository già presente: nessun file riscritto.'); }
else {
  mkdirSync('repo',{recursive:true});
  const git=(...args) => execFileSync('git',args,{cwd:'repo',stdio:'pipe'});
  git('init','-b','main'); git('config','user.name','DEV48 Lab'); git('config','user.email','lab@example.invalid');
  git('config','commit.gpgsign','false'); git('config','core.autocrlf','false');
  writeFileSync('repo/search.txt','Ricerca: nome\\n'); git('add','search.txt'); git('commit','-m','Base della ricerca');
  git('switch','-c','feature-search'); writeFileSync('repo/search.txt','Ricerca: nome senza maiuscole\\n');
  git('add','search.txt'); git('commit','-m','Ricerca senza maiuscole');
  git('switch','main'); writeFileSync('repo/search.txt','Ricerca: nome e zona\\n');
  git('add','search.txt'); git('commit','-m','Ricerca per zona');
  console.log('Repository didattica creata in repo/. Entra nella cartella e confronta i branch.');
}
"""
GIT_RESOLUTION = """import {execFileSync} from 'node:child_process';
import {writeFileSync} from 'node:fs';
import './setup.mjs';
const git=(...args) => execFileSync('git',args,{cwd:'repo',stdio:'pipe'});
try { git('merge','feature-search'); } catch { /* conflitto atteso */ }
writeFileSync('repo/search.txt','Ricerca: nome e zona senza maiuscole\\n');
git('add','search.txt'); git('commit','-m','Integra zona e ricerca senza maiuscole');
"""
PLAIN_LABS["lab-git"] = {
    "starters": {},
    "references": {"resolve.mjs": GIT_RESOLUTION},
    "extra": {"setup.mjs": GIT_SETUP},
    "tests": {"git.test.mjs": NODE_TEST_HEADER + """import {execFileSync} from 'node:child_process';
import {readFileSync,existsSync} from 'node:fs';
const git=(...args) => execFileSync('git',args,{cwd:'repo',encoding:'utf8'}).trim();
test('repository didattica esistente: prima esegui node setup.mjs', () => {assert.equal(existsSync('repo/.git'),true);});
test('risoluzione conserva le due intenzioni senza marcatori', () => {
  assert.equal(readFileSync('repo/search.txt','utf8').trim(),'Ricerca: nome e zona senza maiuscole');
  assert.equal(git('diff','--name-only','--diff-filter=U'),'');
});
test('main contiene il merge ed è pulito', () => {
  assert.equal(git('branch','--show-current'),'main'); assert.equal(git('status','--porcelain'),'');
  assert.equal(git('rev-list','--parents','-n','1','HEAD').split(/\\s+/).length,3);
  git('merge-base','--is-ancestor','feature-search','main');
});
"""},
    "notes": "È fornito setup.mjs: eseguilo una volta per creare repo/ con due storie divergenti. Lavora soltanto nella repository didattica, non nella repository DEV48. Esegui `git merge feature-search` da repo/, controlla i due requisiti e registra la risoluzione dopo aver esaminato il diff. Non serve una rete o un remote. La soluzione automatica resolve.mjs è riportata solo nella guida.",
}


def lab_files(lab: Lab, completed: bool = False) -> dict[str, str] | None:
    spec = PLAIN_LABS.get(lab.id) or REACT_LABS.get(lab.id)
    if spec is None:
        return None
    is_react = lab.id in REACT_LABS
    files = {**(react_base_files(lab.id, api=lab.id in {"lab-react-api", "lab-final"}) if is_react else {}),
        **spec.get("extra", {}), **spec["tests"], **(spec["references"] if completed else spec["starters"])}
    if not is_react:
        files["package.json"] = json.dumps({"name": lab.id, "private": True, "type": "module",
            "engines": {"node": ">=24.0.0"}, "scripts": {"test": "node --test"}}, indent=2)
    files["dev48-scaffold.json"] = json.dumps({"course": "web-js-react", "version": 2, "lab": lab.id}, indent=2)
    requirements = "\n".join(f"- [ ] {item}" for item in lab.requirements)
    commands = ("Esegui `npm install`, poi `npm test` oppure il pulsante Esegui test in DEV48. "
        "La suite esegue React in jsdom. Per la prova nel browser usa `npm run dev`; "
        "nei lab API e finale avvia anche `npm run api` in un secondo terminale. "
        "Verifica tastiera, Invio e focus nel browser: jsdom non certifica layout o accessibilità completa." if is_react else
        "Esegui `npm test` oppure il pulsante Esegui test in DEV48. Non ci sono dipendenze da scaricare.")
    files["README.md"] = (f"# {lab.title}\n\n{lab.description}\n\n## Requisiti\n\n{requirements}\n\n"
        f"## Cosa è fornito e cosa completare\n\n{spec['notes']}\n\n"
        f"## Avvio e verifica\n\nUsa Node.js 24 LTS. {commands} I test provano i casi dichiarati, non ogni possibile input.\n\n"
        "## Metodo\n\nScegli un test che fallisce, formula un'ipotesi, applica una correzione e riprova. "
        "Annota qui una decisione, un caso aggiunto e un limite rimasto. Consulta SOLUTION.md dopo due tentativi reali.\n")
    blocks = []
    for name, source in spec["references"].items():
        language = {".ts": "typescript", ".jsx": "jsx", ".sql": "sql", ".html": "html", ".css": "css"}.get(Path(name).suffix, "javascript")
        blocks.append(f"## {name}\n\n```{language}\n{source.rstrip()}\n```\n")
    files["SOLUTION.md"] = "# Soluzione di riferimento\n\nConfronta comportamento e casi limite, non soltanto il testo.\n\n" + "\n".join(blocks)
    return files


def ensure_js_react_scaffold(target: Path, lab: Lab) -> bool:
    files = lab_files(lab)
    if files is None:
        return False
    # Existing generic workspaces may already contain learner code and tests.
    # Keep the whole old project intact; revised starters are for fresh folders.
    if (target / "package.json").exists() and not (target / "dev48-scaffold.json").exists():
        return True
    for relative, content in files.items():
        path = target / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_text(content.rstrip() + "\n", encoding="utf-8")
    return True
