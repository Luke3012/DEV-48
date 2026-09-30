# Nuovo Control Flow: @if, @else, @for e @switch

Una lista della dashboard può essere in caricamento, vuota, pronta o in errore. Il componente possiede questi dati e il template decide quale struttura DOM mostrare in ciascuno stato.

### Nel percorso

Da conoscere: [Introduzione a signal() e aggiornamento stato con set() e update()](net-05-01-introduzione-a-signal-e-aggiornamen.md); [Valori derivati intelligenti con computed()](net-05-02-valori-derivati-intelligenti-con-co.md).

Il modello TypeScript prepara i dati; il template decide che cosa mostrare. Nel laboratorio Catalogo Standalone con Control Flow verifica lista, stato vuoto e selezione nel DOM: il conteggio corretto nell'esercizio breve da solo non dimostra che il template funzioni.

## La vista che vogliamo costruire

### Dati del componente e identità delle righe
```typescript
type User = { id: number; name: string };
users = signal<User[]>([]);
status = signal<'loading' | 'ready' | 'error'>('loading');
```

```html
@switch (status()) {
  @case ('loading') { <p role="status">Caricamento utenti…</p> }
  @case ('error') { <p role="alert">Non è stato possibile caricare gli utenti.</p> }
  @default {
    <ul>
      @for (user of users(); track user.id) {
        <li>{{ user.name }}</li>
      } @empty {
        <li>Nessun utente trovato.</li>
      }
    </ul>
  }
}
```

`@if`/`@else` e `@switch` scelgono quale ramo esiste; `@for` ripete un blocco. In una lista modificabile `track user.id` è la chiave con cui Angular associa una vista già esistente all'utente che la rappresenta. Se un utente viene rinominato mantenendo l'id, la riga corrispondente resta la stessa; se cambia l'ordine, Angular può collegare ogni riga alla persona corretta. `track $index` descrive la posizione e di solito non è adatto quando gli elementi si inseriscono, rimuovono o riordinano.

## Segui il dato fino al DOM

```html
@for (user of users(); track user.id) {
  <li>{{ user.name }}</li>
} @empty {
  <li>Nessun utente trovato.</li>
}
```

### Dal modello alla schermata

1. Con `status() === 'loading'`, il template mostra l'indicatore e non crea la lista.
2. Quando lo stato diventa `ready`, Angular valuta `users()`. Con `[]` entra in `@empty`; con tre utenti crea tre `<li>`.
3. La chiave `user.id` collega ogni riga alla stessa entità. Se arriva una nuova lista con un nome aggiornato ma ID invariati, Angular può aggiornare il contenuto della riga corrispondente invece di scambiare le identità per posizione.
4. Imposta `status` su `error`, poi prova una lista vuota e una lista riordinata. Verifica nel DOM quale ramo è visibile e quali chiavi restano stabili.

Il mini-esercizio verifica la trasformazione della lista; il laboratorio controlla lista, stato vuoto, selezione ed elementi DOM effettivamente renderizzati.

## Che cosa deve conoscere il template?

- Dimenticare la clausola `track` in `@for` (provoca errore del compilatore Angular)
- usare `track $index` quando gli elementi hanno un ID stabile.

> **Che cosa collega classe e vista?** Perché la clausola `track` è obbligatoria nel nuovo blocco `@for`?
