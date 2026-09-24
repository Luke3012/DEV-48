# Nuovo Control Flow: @if, @else, @for e @switch

## In parole semplici

L'obiettivo di questa lezione è confrontare il Control Flow integrato (`@if`, `@for`, `@switch`) con le direttive strutturali più datate.

Il Control Flow integrato (`@if`, `@for`, `@switch`) è disponibile da Angular 17. Usa blocchi leggibili nel template e non richiede CommonModule per queste istruzioni; l'effetto sulle prestazioni dipende dall'applicazione e dal lavoro svolto.

### Prima di iniziare

Non dare per scontato di conoscere i termini elencati sotto: la spiegazione li introduce nel contesto. Se un termine resta poco chiaro, consulta il glossario e torna all'esempio.

## Le parole da riconoscere

- `@if`
- `@else`
- `@for`
- `track`
- `@empty`
- `@switch`
- `@case`
- `nuovo control flow`

Non serve imparare questi termini a memoria. Concentrati inizialmente su **`@if`, `@else`** e cerca di osservarli all'interno del codice e degli esercizi pratici.

## Anatomia e Sintassi del Codice

Leggi la spiegazione prima del codice. Quando compare una parola nuova, cerca il suo ruolo qui e prova a riconoscerla nell'esempio.

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
    <p>Nessun utente registrato.</p>
  }
</ul>
```
> `track` è obbligatorio e descrive come associare gli elementi della lista alle viste. Usa un identificatore stabile se gli elementi possono cambiare o riordinarsi; `track $index` è adatto soprattutto a liste statiche. Questo aiuta Angular a riutilizzare le viste correttamente, senza garantire un numero minimo di aggiornamenti in ogni situazione.

## Un esempio concreto

Questo è un esempio o un estratto minimo. Potrebbe dipendere da import, classi o configurazioni dichiarate altrove; il blocco mostra la parte pertinente al concetto.

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

La traccia seguente mostra un modo di applicare il concetto. Confrontala con il prompt e adatta i passaggi ai casi richiesti; potrebbe mostrare soltanto la parte centrale:

```typescript
export class UserListManager {
    users = signal<{ id: number; name: string }[]>([]);
    addUser(id: number, name: string) {
        this.users.update(list => [...list, { id, name }]);
    }
}
```

Prima di iniziare, prova a indicare che cosa ricevi, quale risultato ti aspetti e un caso limite. Poi affronta un passaggio alla volta e usa i controlli disponibili per verificare la consegna.

## Dove ci si confonde spesso

- Dimenticare la clausola `track` in `@for` (provoca errore del compilatore Angular)
- usare `track $index` quando gli elementi hanno un ID stabile.

Se qualcosa non funziona al primo tentativo, leggi il primo errore del compilatore o del test. Controlla una cosa alla volta: sintassi, tipo restituito, poi caso limite.

## Controllo rapido

- Riesco a spiegare il concetto principale con parole mie senza leggere?
- So identificare input, output e almeno un caso limite o di errore?
- Saprei applicare questa feature all'interno di un componente o di un'API reale?

## Domanda di verifica

> Perché la clausola `track` è obbligatoria nel nuovo blocco `@for`?

Prova a formulare una risposta chiara: prima definisci la regola generale, poi porta un esempio pratico, e infine cita un errore comune da evitare.

## Prima di andare avanti

Se una parte rimane poco chiara, torna al primo passaggio e spiega che cosa entra e che cosa esce dal codice. Passa all'esercizio quando riesci a prevedere almeno il caso normale e un caso limite.
