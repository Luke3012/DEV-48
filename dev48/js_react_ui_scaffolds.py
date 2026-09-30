"""React lab assets using the existing pinned React/Vite/Vitest toolchain."""
from __future__ import annotations

import json


FIXTURES = """export const initialSubjects = [
  {id:1,name:'Mario Rossi',zone:'Centro',active:true},
  {id:2,name:'Anna Bianchi',zone:'Nord',active:false},
];
"""

STYLE = """*{box-sizing:border-box}body{margin:0;font-family:system-ui,sans-serif;background:#f4f6f8;color:#18293e}
.page{width:calc(100% - 2rem);max-width:56rem;margin:2rem auto;padding:1.5rem;background:white;border:1px solid #ccd5df;border-radius:12px}
label{display:block;margin-top:.8rem}input{display:block;width:100%;max-width:28rem;padding:.65rem;margin:.35rem 0 .7rem;border:1px solid #74859a;border-radius:5px}
button{padding:.6rem .8rem;margin:.25rem;border:1px solid #74859a;border-radius:5px;background:#edf2f8;color:inherit;cursor:pointer}
button:disabled{cursor:wait;opacity:.65}li{padding:.7rem 0;border-bottom:1px solid #dde4ec;overflow-wrap:anywhere}li span{margin-right:.5rem}
ul{padding-left:1.25rem}[role=alert]{color:#9b2222}:focus-visible{outline:3px solid #255ca8;outline-offset:3px}
@media(max-width:30rem){.page{padding:1rem;margin:1rem auto}li button{display:inline-block}}
"""


def react_base_files(name: str, api: bool = False) -> dict[str, str]:
    scripts = {"dev": "vite", "test": "vitest run", "build": "vite build"}
    if api:
        scripts["api"] = "node server.mjs"
    return {
        "package.json": json.dumps({"name": name, "private": True, "version": "1.0.0", "type": "module",
            "engines": {"node": ">=24.0.0"}, "scripts": scripts,
            "dependencies": {"react": "19.2.8", "react-dom": "19.2.8"},
            "devDependencies": {"@vitejs/plugin-react": "6.0.5", "vite": "8.2.1", "vitest": "4.1.10",
                "jsdom": "29.1.1", "@testing-library/react": "16.3.2", "@testing-library/jest-dom": "7.0.0"}}, indent=2),
        "index.html": '<!doctype html><html lang="it"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DEV48 React Lab</title></head><body><div id="root"></div><script type="module" src="/src/main.jsx"></script></body></html>',
        "vite.config.js": "import { defineConfig } from 'vite';\nimport react from '@vitejs/plugin-react';\nexport default defineConfig({ plugins:[react()], cacheDir:'.vite', server:{proxy:{'/api':'http://127.0.0.1:3001'}}, test:{environment:'jsdom',globals:true,setupFiles:'./src/testSetup.js'} });\n",
        "src/main.jsx": "import { StrictMode } from 'react';\nimport { createRoot } from 'react-dom/client';\nimport App from './App.jsx';\nimport './styles.css';\ncreateRoot(document.getElementById('root')).render(<StrictMode><App /></StrictMode>);\n",
        "src/styles.css": STYLE,
        "src/fixtures.js": FIXTURES,
        "src/testSetup.js": "import '@testing-library/jest-dom/vitest';\nimport {cleanup} from '@testing-library/react';\nimport {afterEach} from 'vitest';\nafterEach(cleanup);\n",
    }


LIST_REFERENCE = """import {useState} from 'react';
import {initialSubjects} from './fixtures.js';
export default function App({initialItems=initialSubjects}) {
  const [items,setItems]=useState(initialItems);
  const [query,setQuery]=useState('');
  const visible=items.filter(item => item.name.toLowerCase().includes(query.trim().toLowerCase()));
  function remove(id) { setItems(current => current.filter(item => item.id!==id)); }
  return <main className="page"><h1>Archivio soggetti</h1>
    <label htmlFor="search">Cerca</label><input id="search" type="search" value={query} onChange={event => setQuery(event.target.value)} />
    <p>{visible.length} risultati</p>
    {items.length===0 ? <p>Archivio vuoto</p> : visible.length===0 ? <p>Nessuna corrispondenza</p> :
      <ul>{visible.map(item => <li key={item.id}><span>{item.name}</span>
        <button aria-label={`Elimina ${item.name}`} onClick={() => remove(item.id)}>Elimina</button></li>)}</ul>}
  </main>;
}
"""

FORM_REFERENCE = """import {useState} from 'react';
import {initialSubjects} from './fixtures.js';
export default function App({initialItems=initialSubjects}) {
  const [items,setItems]=useState(initialItems);
  const [name,setName]=useState('');
  const [editing,setEditing]=useState(null);
  const [error,setError]=useState('');
  function clear() { setName('');setEditing(null);setError(''); }
  function edit(item) { setEditing(item.id);setName(item.name);setError(''); }
  function submit(event) {
    event.preventDefault();
    const clean=name.trim();
    if(!clean){setError('Inserisci un nome');return;}
    setItems(current => editing===null ? [...current,{id:Math.max(0,...current.map(item => item.id))+1,name:clean,zone:'',active:true}] :
      current.map(item => item.id===editing ? {...item,name:clean} : item));
    clear();
  }
  return <main className="page"><h1>Form soggetti</h1>
    <form noValidate onSubmit={submit}><label htmlFor="name">Nome</label>
      <input id="name" value={name} onChange={event => setName(event.target.value)}
        aria-invalid={Boolean(error)} aria-describedby={error ? 'name-error' : undefined} />
      {error && <p id="name-error" role="alert">{error}</p>}
      <button type="submit">{editing===null ? 'Crea soggetto' : 'Salva modifica'}</button>
      {editing!==null && <button type="button" onClick={clear}>Annulla modifica</button>}
    </form>
    <ul>{items.map(item => <li key={item.id}><span>{item.name}</span><small>{item.zone} · {item.active ? 'attivo' : 'inattivo'}</small>
      <button onClick={() => edit(item)} aria-label={`Modifica ${item.name}`}>Modifica</button></li>)}</ul>
  </main>;
}
"""

API_CLIENT = """export function isSubject(value) {
  return value!==null && typeof value==='object' && Number.isInteger(value.id) && typeof value.name==='string';
}
export function createApi(base='/api/subjects', request=fetch) {
  async function call(path='',options={}) {
    const response=await request(base+path,options);
    if(!response.ok) {
      let message=`HTTP ${response.status}`;
      try {const body=await response.json();if(typeof body.error==='string')message=body.error;} catch { /* fallback HTTP */ }
      throw new Error(message);
    }
    return response.json();
  }
  async function save(path,method,name) {
    const item=await call(path,{method,headers:{'Content-Type':'application/json'},body:JSON.stringify({name})});
    if(!isSubject(item)) throw new Error('Risposta non valida');
    return item;
  }
  return {
    async load(query='',{signal}={}) {
      const data=await call(`?query=${encodeURIComponent(query)}`,{signal});
      if(!Array.isArray(data)||!data.every(isSubject))throw new Error('Risposta non valida');
      return data;
    },
    create: name => save('','POST',name),
    update: (id,name) => save(`/${id}`,'PATCH',name),
    remove: id => call(`/${id}`,{method:'DELETE'}),
  };
}
export const api=createApi();
"""

REMOTE_HOOK = """import {useEffect,useState} from 'react';
import {isSubject} from './api.js';
export function useSubjects(api,query) {
  const [result,setResult]=useState({status:'loading',data:[],error:''});
  const [attempt,setAttempt]=useState(0);
  useEffect(() => {
    let ignore=false;
    const controller=new AbortController();
    setResult({status:'loading',data:[],error:''});
    async function load() {
      try {
        const data=await api.load(query,{signal:controller.signal});
        if(!Array.isArray(data)||!data.every(isSubject))throw new Error('Risposta non valida');
        if(!ignore)setResult({status:data.length ? 'success' : 'empty',data,error:''});
      } catch(error) {
        if(!ignore)setResult({status:'error',data:[],error:error.message});
      }
    }
    load();
    return () => {ignore=true;controller.abort();};
  },[api,query,attempt]);
  return {...result,reload:() => setAttempt(value => value+1)};
}
"""

API_REFERENCE = """import {useRef,useState} from 'react';
import {api as defaultApi} from './api.js';
import {useSubjects} from './useSubjects.js';
export default function App({api=defaultApi}) {
  const [query,setQuery]=useState('');
  const result=useSubjects(api,query);
  const [name,setName]=useState('');
  const [editing,setEditing]=useState(null);
  const [error,setError]=useState('');
  const [busy,setBusy]=useState(false);
  const [actionError,setActionError]=useState('');
  const inFlight=useRef(false);
  function clear(){setName('');setEditing(null);setError('');setActionError('');}
  function edit(item){setEditing(item.id);setName(item.name);setError('');setActionError('');}
  async function submit(event) {
    event.preventDefault();
    if(inFlight.current)return;
    const clean=name.trim();
    if(!clean){setError('Inserisci un nome');return;}
    inFlight.current=true;setBusy(true);setError('');setActionError('');
    try {
      if(editing===null)await api.create(clean);else await api.update(editing,clean);
      clear();result.reload();
    } catch(failure){setActionError(failure.message);}
    finally{inFlight.current=false;setBusy(false);}
  }
  async function remove(id) {
    if(inFlight.current)return;
    inFlight.current=true;setBusy(true);setError('');setActionError('');
    try {await api.remove(id);if(editing===id)clear();result.reload();}
    catch(failure){setActionError(failure.message);}
    finally{inFlight.current=false;setBusy(false);}
  }
  return <main className="page"><h1>Archivio API</h1>
    <label htmlFor="search">Cerca</label><input id="search" type="search" value={query} disabled={busy} onChange={event => setQuery(event.target.value)} />
    <button disabled={busy} onClick={result.reload}>Ricarica</button>
    <form noValidate onSubmit={submit}><label htmlFor="name">Nome</label>
      <input id="name" value={name} disabled={busy} onChange={event => setName(event.target.value)}
        aria-invalid={Boolean(error)} aria-describedby={error ? 'name-error' : undefined} />
      {error && <p id="name-error" role="alert">{error}</p>}
      <button disabled={busy} type="submit">{editing===null ? 'Crea soggetto' : 'Salva modifica'}</button>
      {editing!==null && <button disabled={busy} type="button" onClick={clear}>Annulla modifica</button>}
    </form>
    {actionError && <p role="alert">{actionError}</p>}
    {busy && <p role="status">Salvataggio…</p>}
    {result.status==='loading' && <p role="status">Caricamento…</p>}
    {result.status==='error' && <div><p role="alert">{result.error}</p><button disabled={busy} onClick={result.reload}>Riprova</button></div>}
    {result.status==='empty' && <p>Nessun soggetto</p>}
    {result.status==='success' && <><p>{result.data.length} risultati</p>
      <ul>{result.data.map(item => <li key={item.id}><span>{item.name}</span>
        <button disabled={busy} onClick={() => edit(item)} aria-label={`Modifica ${item.name}`}>Modifica</button>
        <button disabled={busy} onClick={() => remove(item.id)} aria-label={`Elimina ${item.name}`}>Elimina</button></li>)}</ul></>}
  </main>;
}
"""

API_SERVER = """import {createServer} from 'node:http';
import {pathToFileURL} from 'node:url';
import {initialSubjects} from './src/fixtures.js';
export function createStore(initial=initialSubjects) {
  let items=structuredClone(initial);
  let nextId=Math.max(0,...items.map(item => item.id))+1;
  return {
    list(query=''){return structuredClone(items.filter(item => item.name.toLowerCase().includes(query.trim().toLowerCase())));},
    create(name){const item={id:nextId++,name,zone:'',active:true};items=[...items,item];return {...item};},
    update(id,name){const item=items.find(item => item.id===id);if(!item)return null;items=items.map(current => current.id===id ? {...current,name} : current);return {...item,name};},
    remove(id){if(!items.some(item => item.id===id))return false;items=items.filter(item => item.id!==id);return true;},
  };
}
export function createApiServer(store=createStore()) {
  return createServer(async (req,res) => {
    function send(status,data){res.writeHead(status,{'Content-Type':'application/json'});res.end(JSON.stringify(data));}
    try {
      const url=new URL(req.url,'http://127.0.0.1');
      const collection=url.pathname==='/api/subjects';
      const match=url.pathname.match(/^\\/api\\/subjects\\/(\\d+)$/);
      if(req.method==='GET' && collection){send(200,store.list(url.searchParams.get('query')??''));return;}
      if(req.method==='DELETE' && match){const id=Number(match[1]);send(store.remove(id)?200:404,{id});return;}
      if((req.method==='POST' && collection)||(req.method==='PATCH' && match)) {
        let raw='';for await(const chunk of req){raw+=chunk;if(raw.length>16384){send(413,{error:'Richiesta troppo grande'});return;}}
        let body;try{body=JSON.parse(raw);}catch{send(400,{error:'JSON non valido'});return;}
        if(!body||typeof body.name!=='string'||!body.name.trim()){send(400,{error:'Nome obbligatorio'});return;}
        const item=req.method==='POST'?store.create(body.name.trim()):store.update(Number(match[1]),body.name.trim());
        if(!item){send(404,{error:'Soggetto assente'});return;}
        send(req.method==='POST'?201:200,item);return;
      }
      send(404,{error:'Risorsa assente'});
    } catch {send(500,{error:'Errore del server'});}
  });
}
if(process.argv[1] && pathToFileURL(process.argv[1]).href===import.meta.url) {
  createApiServer().listen(3001,'127.0.0.1',() => console.log('API didattica: http://127.0.0.1:3001/api/subjects'));
}
"""

TEST_HEADER = """import {act,fireEvent,render,screen,waitFor} from '@testing-library/react';
import {describe,expect,it,vi} from 'vitest';
import App from './App.jsx';
import {initialSubjects} from './fixtures.js';
"""

LIST_TESTS = TEST_HEADER + """describe('archivio con ricerca', () => {
  it('ricerca controllata normalizzata e conteggio derivato', () => {
    render(<App />);
    fireEvent.change(screen.getByLabelText('Cerca'),{target:{value:' ANNA '}});
    expect(screen.getByText('Anna Bianchi')).toBeInTheDocument();
    expect(screen.queryByText('Mario Rossi')).not.toBeInTheDocument();
    expect(screen.getByText('1 risultati')).toBeInTheDocument();
    expect(screen.getByLabelText('Cerca')).toHaveValue(' ANNA ');
  });
  it('nessuna corrispondenza è distinta da archivio vuoto', () => {
    const view=render(<App />);
    fireEvent.change(screen.getByLabelText('Cerca'),{target:{value:'zzz'}});
    expect(screen.getByText('Nessuna corrispondenza')).toBeInTheDocument();
    expect(screen.queryByText('Archivio vuoto')).not.toBeInTheDocument();
    view.unmount();render(<App initialItems={[]} />);
    expect(screen.getByText('Archivio vuoto')).toBeInTheDocument();
  });
  it('elimina durante un filtro conservando query e gli altri dati', () => {
    const items=structuredClone(initialSubjects), before=structuredClone(items);
    render(<App initialItems={items} />);
    fireEvent.change(screen.getByLabelText('Cerca'),{target:{value:'mario'}});
    fireEvent.click(screen.getByRole('button',{name:'Elimina Mario Rossi'}));
    expect(screen.queryByText('Mario Rossi')).not.toBeInTheDocument();
    expect(screen.getByLabelText('Cerca')).toHaveValue('mario');
    expect(screen.getByText('0 risultati')).toBeInTheDocument();
    fireEvent.change(screen.getByLabelText('Cerca'),{target:{value:''}});
    expect(screen.getByText('Anna Bianchi')).toBeInTheDocument();
    expect(items).toEqual(before);
  });
  it('elimina l ultimo elemento senza mutare input congelato', () => {
    const items=Object.freeze([Object.freeze({id:1,name:'Anna'})]);
    render(<App initialItems={items} />);
    fireEvent.click(screen.getByRole('button',{name:'Elimina Anna'}));
    expect(screen.getByText('Archivio vuoto')).toBeInTheDocument();
    expect(screen.getByText('0 risultati')).toBeInTheDocument();
    expect(items).toHaveLength(1);
  });
});
"""

FORM_TESTS = TEST_HEADER + """describe('form controllato', () => {
  it('crea con nome normalizzato e azzera soltanto dopo successo', () => {
    render(<App />);fireEvent.change(screen.getByLabelText('Nome'),{target:{value:' Sara Neri '}});
    fireEvent.submit(screen.getByRole('button',{name:'Crea soggetto'}).closest('form'));
    expect(screen.getByText('Sara Neri')).toBeInTheDocument();expect(screen.getByLabelText('Nome')).toHaveValue('');
    expect(screen.getByText('Mario Rossi')).toBeInTheDocument();
  });
  it('rifiuta spazi, associa l errore e conserva il campo', () => {
    render(<App />);const input=screen.getByLabelText('Nome');
    fireEvent.change(input,{target:{value:'   '}});fireEvent.submit(input.closest('form'));
    expect(screen.getByRole('alert')).toHaveTextContent('Inserisci un nome');
    expect(input).toHaveAttribute('aria-invalid','true');
    expect(input).toHaveAttribute('aria-describedby',screen.getByRole('alert').id);
    expect(input).toHaveValue('   ');expect(screen.getAllByRole('button',{name:/Modifica /})).toHaveLength(2);
    fireEvent.change(input,{target:{value:'Sara'}});fireEvent.submit(input.closest('form'));
    expect(screen.queryByRole('alert')).not.toBeInTheDocument();expect(screen.getByText('Sara')).toBeInTheDocument();
  });
  it('modifica il record e conserva altri campi, righe e input originale', () => {
    const items=structuredClone(initialSubjects), before=structuredClone(items);render(<App initialItems={items} />);
    fireEvent.click(screen.getByRole('button',{name:'Modifica Mario Rossi'}));
    expect(screen.getByLabelText('Nome')).toHaveValue('Mario Rossi');
    fireEvent.change(screen.getByLabelText('Nome'),{target:{value:' Mario Verdi '}});
    fireEvent.click(screen.getByRole('button',{name:'Salva modifica'}));
    expect(screen.getByText('Mario Verdi')).toBeInTheDocument();expect(screen.getByText('Centro · attivo')).toBeInTheDocument();
    expect(screen.getByText('Anna Bianchi')).toBeInTheDocument();expect(items).toEqual(before);
    expect(screen.getAllByRole('button',{name:/Modifica /})).toHaveLength(2);
  });
  it('annulla una modifica senza salvare o mutare il record', () => {
    render(<App />);fireEvent.click(screen.getByRole('button',{name:'Modifica Anna Bianchi'}));
    fireEvent.change(screen.getByLabelText('Nome'),{target:{value:'Altro nome'}});
    fireEvent.click(screen.getByRole('button',{name:'Annulla modifica'}));
    expect(screen.getByLabelText('Nome')).toHaveValue('');expect(screen.getByText('Anna Bianchi')).toBeInTheDocument();
    expect(screen.queryByText('Altro nome')).not.toBeInTheDocument();
  });
});
"""

API_TEST_HELPERS = """function deferred(){let resolve,reject;const promise=new Promise((done,fail)=>{resolve=done;reject=fail;});return {promise,resolve,reject};}
function memoryApi() {
  let items=structuredClone(initialSubjects), next=3;
  return {
    load:vi.fn(async query => structuredClone(items.filter(item => item.name.toLowerCase().includes(query.trim().toLowerCase())))),
    create:vi.fn(async name => {const item={id:next++,name,active:true,zone:''};items=[...items,item];return item;}),
    update:vi.fn(async (id,name) => {items=items.map(item => item.id===id ? {...item,name} : item);return items.find(item => item.id===id);}),
    remove:vi.fn(async id => {items=items.filter(item => item.id!==id);return {id};}),
  };
}
"""

API_TESTS = TEST_HEADER + "import {StrictMode} from 'react';\n" + API_TEST_HELPERS + """describe('UI remota', () => {
  it('loading e dati sono stati visibili distinti', async () => {
    const pending=deferred(),api=memoryApi();api.load.mockReturnValue(pending.promise);render(<App api={api} />);
    expect(screen.getByText('Caricamento…')).toHaveAttribute('role','status');
    expect(screen.queryByText('Nessun soggetto')).not.toBeInTheDocument();
    await act(async () => pending.resolve(initialSubjects));
    expect(await screen.findByText('Mario Rossi')).toBeInTheDocument();expect(screen.queryByText('Caricamento…')).not.toBeInTheDocument();
  });
  it('errore, retry e successo vuoto', async () => {
    const api=memoryApi();api.load.mockRejectedValueOnce(new Error('offline')).mockResolvedValueOnce([]);
    render(<App api={api} />);expect(await screen.findByRole('alert')).toHaveTextContent('offline');
    fireEvent.click(screen.getByRole('button',{name:'Riprova'}));
    expect(await screen.findByText('Nessun soggetto')).toBeInTheDocument();expect(api.load).toHaveBeenCalledTimes(2);
  });
  it('cambio ricerca ignora la risposta precedente anche senza annullamento nel trasporto', async () => {
    const first=deferred(),second=deferred(),api=memoryApi();
    api.load.mockImplementation(query => query==='B' ? second.promise : first.promise);
    render(<App api={api} />);const oldSignal=api.load.mock.calls[0][1].signal;
    fireEvent.change(screen.getByLabelText('Cerca'),{target:{value:'B'}});expect(oldSignal.aborted).toBe(true);
    await act(async () => second.resolve([{id:2,name:'Nuova B'}]));
    expect(await screen.findByText('Nuova B')).toBeInTheDocument();
    await act(async () => first.resolve([{id:1,name:'Vecchia A'}]));
    expect(screen.queryByText('Vecchia A')).not.toBeInTheDocument();expect(screen.getByText('Nuova B')).toBeInTheDocument();
  });
  it('cleanup funziona anche nel ciclo aggiuntivo Strict Mode', async () => {
    const api=memoryApi(),pending=[];api.load.mockImplementation(() => {const item=deferred();pending.push(item);return item.promise;});
    const view=render(<StrictMode><App api={api} /></StrictMode>);
    expect(api.load).toHaveBeenCalledTimes(2);expect(api.load.mock.calls[0][1].signal.aborted).toBe(true);
    view.unmount();expect(api.load.mock.calls[1][1].signal.aborted).toBe(true);
    await act(async () => {for(const item of pending)item.resolve([]);});
  });
  it('salvataggio fallito conserva campo e lista; doppio submit non duplica la richiesta', async () => {
    const api=memoryApi(),pending=deferred();api.create.mockReturnValue(pending.promise);render(<App api={api} />);
    await screen.findByText('Mario Rossi');const input=screen.getByLabelText('Nome');
    fireEvent.change(input,{target:{value:' Sara '}});const form=input.closest('form');fireEvent.submit(form);fireEvent.submit(form);
    expect(api.create).toHaveBeenCalledTimes(1);expect(api.create).toHaveBeenCalledWith('Sara');
    expect(screen.getByRole('button',{name:'Crea soggetto'})).toBeDisabled();
    await act(async () => pending.reject(new Error('Salvataggio fallito')));
    expect(await screen.findByRole('alert')).toHaveTextContent('Salvataggio fallito');expect(input).toHaveValue(' Sara ');
    expect(input).toHaveAttribute('aria-invalid','false');expect(screen.getByText('Mario Rossi')).toBeInTheDocument();
    expect(screen.getByRole('button',{name:'Crea soggetto'})).not.toBeDisabled();
  });
  it('creazione, modifica ed eliminazione si riflettono nella lista', async () => {
    const api=memoryApi();render(<App api={api} />);await screen.findByText('Mario Rossi');
    fireEvent.change(screen.getByLabelText('Nome'),{target:{value:'Sara'}});fireEvent.click(screen.getByRole('button',{name:'Crea soggetto'}));
    await screen.findByText('Sara');expect(screen.getByLabelText('Nome')).toHaveValue('');
    fireEvent.click(screen.getByRole('button',{name:'Modifica Sara'}));fireEvent.change(screen.getByLabelText('Nome'),{target:{value:'Sara Neri'}});
    fireEvent.click(screen.getByRole('button',{name:'Salva modifica'}));await screen.findByText('Sara Neri');expect(api.update).toHaveBeenCalledWith(3,'Sara Neri');
    fireEvent.click(screen.getByRole('button',{name:'Elimina Sara Neri'}));
    await waitFor(() => expect(screen.queryByText('Sara Neri')).not.toBeInTheDocument());
    await screen.findByText('Mario Rossi');expect(api.remove).toHaveBeenCalledWith(3);
  });
  it('input invalido non chiama il server ed errore eliminazione conserva il record', async () => {
    const api=memoryApi();api.remove.mockRejectedValue(new Error('Eliminazione fallita'));render(<App api={api} />);await screen.findByText('Mario Rossi');
    fireEvent.change(screen.getByLabelText('Nome'),{target:{value:'  '}});fireEvent.click(screen.getByRole('button',{name:'Crea soggetto'}));
    expect(api.create).not.toHaveBeenCalled();expect(screen.getByLabelText('Nome')).toHaveAttribute('aria-invalid','true');
    fireEvent.click(screen.getByRole('button',{name:'Elimina Mario Rossi'}));
    expect(await screen.findByText('Eliminazione fallita')).toHaveAttribute('role','alert');
    expect(screen.getByText('Mario Rossi')).toBeInTheDocument();
  });
});
"""

HTTP_TESTS = """// @vitest-environment node
import {expect,it,vi} from 'vitest';
import {createApiServer,createStore} from '../server.mjs';
import {createApi} from './api.js';
it('contratto HTTP reale: CRUD, filtro, validazione e assenza', async () => {
  const server=createApiServer(createStore());await new Promise(resolve => server.listen(0,'127.0.0.1',resolve));
  const base=`http://127.0.0.1:${server.address().port}/api/subjects`;const api=createApi(base);
  try {
    expect((await api.load(' ANNA ')).map(item=>item.name)).toEqual(['Anna Bianchi']);
    const item=await api.create(' Sara ');expect(item.name).toBe('Sara');
    const changed=await api.update(item.id,'Sara Neri');expect(changed.id).toBe(item.id);expect(changed.name).toBe('Sara Neri');
    await api.remove(item.id);expect(await api.load('Sara')).toEqual([]);
    await expect(api.create('  ')).rejects.toThrow('Nome obbligatorio');
    await expect(api.update(99,'Assente')).rejects.toThrow('Soggetto assente');
    const invalid=await fetch(base,{method:'POST',headers:{'Content-Type':'application/json'},body:'{'});expect(invalid.status).toBe(400);
    const direct=await fetch(base,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:'Altro'})});expect(direct.status).toBe(201);
  } finally {await new Promise(resolve => server.close(resolve));}
});
it('trasporto propaga rete e JSON invalidi, valida forma e inoltra signal', async () => {
  const signal=new AbortController().signal;
  const request=vi.fn(async () => ({ok:true,json:async () => [{id:1,name:'Anna'}]}));
  const api=createApi('/api/subjects',request);await api.load('Anna Bianchi',{signal});
  expect(request).toHaveBeenCalledWith('/api/subjects?query=Anna%20Bianchi',{signal});
  for(const transport of [async ()=>{throw Error('rete');},async()=>({ok:true,json:async()=>{throw Error('JSON');}}),async()=>({ok:true,json:async()=>[{id:'1',name:2}]})]) {
    await expect(createApi('/',transport).load()).rejects.toThrow();
  }
});
"""

API_STARTER = """import {useState} from 'react';
import {api as defaultApi} from './api.js';
import {useSubjects} from './useSubjects.js';
export default function App({api=defaultApi}) {
  const result=useSubjects(api,'');
  const [name,setName]=useState('');
  // TODO: integra ricerca, form, modifica, eliminazione, validazione e recupero dagli errori.
  return <main className="page"><h1>Archivio API</h1>
    <label htmlFor="name">Nome</label><input id="name" value={name} onChange={event=>setName(event.target.value)} />
    {result.status==='loading' && <p role="status">Caricamento…</p>}
  </main>;
}
"""

REACT_LABS = {
    "lab-react-list": {
        "starters": {"src/App.jsx": """import {useState} from 'react';
import {initialSubjects} from './fixtures.js';
export default function App({initialItems=initialSubjects}) {
  const [items,setItems]=useState(initialItems);
  const [query,setQuery]=useState('');
  // TODO: deriva la lista visibile; completa ricerca, conteggio, eliminazione e casi vuoti.
  return <main className="page"><h1>Archivio soggetti</h1><p>{items.length} soggetti iniziali</p></main>;
}
"""},
        "references": {"src/App.jsx": LIST_REFERENCE},
        "tests": {"src/App.test.jsx": LIST_TESTS},
        "notes": "Fixture, entry point, stile e configurazione sono forniti. Completa App.jsx: stato della query, trasformazione dei dati ed eventi. I quattro test verificano il DOM e l'immutabilità; nel browser prova anche Tab e ricerca con tastiera.",
    },
    "lab-react-form": {
        "starters": {"src/App.jsx": """import {useState} from 'react';
import {initialSubjects} from './fixtures.js';
export default function App({initialItems=initialSubjects}) {
  const [items,setItems]=useState(initialItems);
  // TODO: progetta stato del form e modifica per ID; valida nel submit.
  return <main className="page"><h1>Form soggetti</h1><ul>{items.map(item=><li key={item.id}>{item.name}</li>)}</ul></main>;
}
"""},
        "references": {"src/App.jsx": FORM_REFERENCE},
        "tests": {"src/App.test.jsx": FORM_TESTS},
        "notes": "La lista iniziale è fornita; costruisci form e interazioni a partire dai requisiti. Il componente App accetta initialItems per i casi isolati. I test verificano validazione, modifica, annullamento e input conservato; l'invio con Invio e il focus vanno provati nel browser.",
    },
    "lab-react-api": {
        "starters": {"src/App.jsx": API_STARTER, "src/useSubjects.js": "export function useSubjects(api,query) {\n  // TODO: caricamento, dipendenze, cleanup, stati e retry.\n  return {status:'loading',data:[],error:'',reload(){}};\n}\n"},
        "references": {"src/App.jsx": API_REFERENCE, "src/useSubjects.js": REMOTE_HOOK},
        "extra": {"src/api.js": API_CLIENT, "server.mjs": API_SERVER},
        "tests": {"src/App.test.jsx": API_TESTS, "src/api.test.js": HTTP_TESTS},
        "notes": "Server HTTP locale e trasporto sono già funzionanti. Completa il hook useSubjects e App. La prop api consente ai test di controllare gli esiti senza rete; api.test.js verifica separatamente un server HTTP reale su porta temporanea. Dopo i test avvia `npm run api` e `npm run dev` in due terminali: Vite inoltra /api alla porta 3001. Il server conserva i dati solo mentre resta acceso e non fornisce autenticazione.",
    },
}

FINAL_REFERENCE = API_REFERENCE.replace('Archivio API','Mini gestionale').replace(
    '<><p>{result.data.length} risultati</p>',
    '<><p>{result.data.length} risultati</p><p>Soggetti attivi: {result.data.filter(item => item.active).length}</p>')
FINAL_TESTS = TEST_HEADER + API_TEST_HELPERS + """it('riepilogo derivato cambia con ricerca e dati, senza una copia da sincronizzare', async () => {
  const api=memoryApi();render(<App api={api} />);await screen.findByText('Mario Rossi');
  expect(screen.getByText('Soggetti attivi: 1')).toBeInTheDocument();
  fireEvent.change(screen.getByLabelText('Cerca'),{target:{value:'Anna'}});
  await screen.findByText('Anna Bianchi');expect(screen.getByText('Soggetti attivi: 0')).toBeInTheDocument();
  expect(screen.queryByText('Mario Rossi')).not.toBeInTheDocument();
  fireEvent.change(screen.getByLabelText('Cerca'),{target:{value:''}});await screen.findByText('Mario Rossi');
  fireEvent.click(screen.getByRole('button',{name:'Elimina Mario Rossi'}));
  await waitFor(()=>expect(screen.queryByText('Mario Rossi')).not.toBeInTheDocument());
  await screen.findByText('Anna Bianchi');expect(screen.getByText('Soggetti attivi: 0')).toBeInTheDocument();
});
it('annullare la modifica non invia una PATCH', async () => {
  const api=memoryApi();render(<App api={api} />);await screen.findByText('Mario Rossi');
  fireEvent.click(screen.getByRole('button',{name:'Modifica Mario Rossi'}));
  fireEvent.change(screen.getByLabelText('Nome'),{target:{value:'Altro'}});
  fireEvent.click(screen.getByRole('button',{name:'Annulla modifica'}));
  expect(api.update).not.toHaveBeenCalled();expect(screen.getByText('Mario Rossi')).toBeInTheDocument();
});
"""
REACT_LABS["lab-final"] = {
    "starters": {"src/App.jsx": """import {api as defaultApi} from './api.js';
export default function App({api=defaultApi}) {
  // Costruisci componenti e flusso dal contratto e dai test; non è fornita la divisione della UI.
  return <main className="page"><h1>Mini gestionale</h1></main>;
}
"""},
    "references": {"src/App.jsx": FINAL_REFERENCE, "src/useSubjects.js": REMOTE_HOOK},
    "extra": {"src/api.js": API_CLIENT, "server.mjs": API_SERVER},
    "tests": {"src/App.test.jsx": API_TESTS, "src/final.test.jsx": FINAL_TESTS, "src/api.test.js": HTTP_TESTS},
    "notes": "Server, trasporto, fixture e test sono forniti; la divisione dei componenti e il flusso UI sono lavoro autonomo. App accetta api con load(query,{signal}), create(name), update(id,name) e remove(id). Per rendere riproducibili i test usa etichette Cerca/Nome, Crea soggetto/Salva modifica/Annulla modifica, Modifica <nome>/Elimina <nome>, messaggi Caricamento…/Nessun soggetto e un riepilogo 'Soggetti attivi: N' riferito ai risultati correnti. Puoi dividere liberamente il codice; il hook nella soluzione è una scelta possibile. Avvia API e Vite in due terminali. Il server è didattico, in memoria, senza auth o persistenza oltre il riavvio.",
}
