# Nuovo Control Flow: @if, @else, @for e @switch

## In parole semplici

L'obiettivo di questa lezione è confrontare il Control Flow integrato (`@if`, `@for`, `@switch`) con le direttive strutturali più datate.

Il Control Flow integrato (`@if`, `@for`, `@switch`) è disponibile da Angular 17. Usa blocchi leggibili nel template e non richiede CommonModule per queste istruzioni; l'effetto sulle prestazioni dipende dall'applicazione e dal lavoro svolto.

### Nel percorso

Da conoscere: [Introduzione a signal() e aggiornamento stato con set() e update()](net-05-01-introduzione-a-signal-e-aggiornamen.md); [Valori derivati intelligenti con computed()](net-05-02-valori-derivati-intelligenti-con-co.md).

Il modello TypeScript prepara i dati; il template decide che cosa mostrare. Nel laboratorio Catalogo Standalone con Control Flow verifica lista, stato vuoto e selezione nel DOM: il conteggio corretto nell'esercizio breve da solo non dimostra che il template funzioni.

## Le parole da riconoscere

- `@if`
- `@else`
- `@for`
- `track`
- `@empty`
- `@switch`
- `@case`
- `nuovo control flow`

## Anatomia e Sintassi del Codice

### Sintassi del Nuovo Control Flow nei Template:

#### 1. Condizionale `@if / @else`:
```html
@if (isLoggedIn()) {
  <p>Benvenuto, {{ username() }}!</p>
} @else {
  <button (click)="login()">Accedi</button>
}
```

#### 2. Ciclo `@for` (con `track` obbligatorio e `@empty`):
```html
<ul>
  @for (user of users(); track user.id) {
    <li>{{ user.name }}</li>
  } @empty {
    <li>Nessun utente registrato.</li>
  }
</ul>
```
> `track` è obbligatorio e descrive come associare gli elementi della lista alle viste. Usa un identificatore stabile se gli elementi possono cambiare o riordinarsi; `track $index` è adatto soprattutto a liste statiche. Questo aiuta Angular a riutilizzare le viste correttamente, senza garantire un numero minimo di aggiornamenti in ogni situazione.

### Scegliere una vista con `@switch`
```html
@switch (status) {
  @case ('loading') { <p role="status">Caricamento…</p> }
  @case ('error') { <p role="alert">Caricamento fallito</p> }
  @default { <p>Pronto</p> }
}
```
`status` è una proprietà della classe del componente, per esempio `status = 'loading'`. Se diventa un Signal, nel template leggilo con `status()`. Ogni caso mostra la propria vista; non serve `break`.

## Un esempio concreto

```html
@if (users().length > 0) {
  @for (user of users(); track user.id) {
    <div>{{ user.name }}</div>
  }
} @else {
  <p>Lista vuota</p>
}
```

### Seguilo passo per passo

1. La condizione `users().length > 0` sceglie quale blocco del template mostrare.
2. Se la lista contiene utenti, `@for` crea una riga per ciascuno; `track user.id` associa ogni riga a una chiave stabile.
3. Se la lista è vuota, il blocco `@else` mostra `Lista vuota`. Con tre utenti, la vista produce tre `<div>`.
4. Prova una lista vuota e poi cambia un nome mantenendo lo stesso id. Il contenuto cambia, mentre l'identità stabile aiuta Angular a riutilizzare la riga appropriata.

## Pattern Guida per gli Esercizi

La pratica breve isola una regola e non avvia l'applicazione Angular. Prova la consegna con gli aiuti chiusi e usa l’esempio della lezione per ricostruire i passaggi che ti mancano. Nel laboratorio del modulo verifica anche il comportamento del framework.

```typescript
export class UserListManager {
    users = signal<{ id: number; name: string }[]>([]);
    addUser(id: number, name: string) {
        this.users.update(list => [...list, { id, name }]);
    }
}
```

## Dove ci si confonde spesso

- Dimenticare la clausola `track` in `@for` (provoca errore del compilatore Angular)
- usare `track $index` quando gli elementi hanno un ID stabile.

## Domanda di verifica

> Perché la clausola `track` è obbligatoria nel nuovo blocco `@for`?
