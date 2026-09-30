# Errori e validazione

## In parole semplici

Prima di iniziare, ripassa [Valori, tipi e confronti](01-01-valori-tipi-e-confronti.md) e [Funzioni e responsabilità](01-03-funzioni-e-responsabilita.md).

Rifiutare input invalidi e distinguere errore previsto da bug di programmazione.

Validare significa rifiutare presto un dato che non rispetta il contratto. Un errore utile dice che cosa non va e lascia al livello corretto la scelta tra mostrare un messaggio, riprovare o interrompere l'operazione.

La conversione non basta a rendere valido un input: `Number('')` è zero e `Number('abc')` è NaN. Decidi prima il contratto. L'esempio accetta numeri e stringhe numeriche non vuote, rifiuta booleani e assenze, poi controlla che il risultato sia finito e non negativo. La UI potrà trasformare un errore previsto in un messaggio utile.

## Le parole da riconoscere

`throw`; `Error`; `try/catch`; `validazione`; `guard clause`; `messaggio utile`

## Un esempio concreto

```javascript
function parseAge(value) {
  if ((typeof value !== 'number' && typeof value !== 'string') ||
      (typeof value === 'string' && value.trim() === '')) {
    throw new Error('Età mancante o non numerica');
  }
  const age = Number(value);
  if (!Number.isFinite(age) || age < 0) throw new Error('Età non valida');
  return age;
}
try { console.log(parseAge('abc')); }
catch (error) { console.log(error.message); }
```

`throw` interrompe il percorso normale e risale fino a un catch. Il catch non deve fingere un successo: un errore di parsing non è l'età zero. Quando il contratto permette un risultato assente può essere adatto `null`; quando l'input viola il contratto, un errore distingue il fallimento da un risultato valido.

## Prova tu

Implementa la validazione per non negativi e prova zero, stringa numerica, negativo, Infinity, testo e stringa vuota. Scrivi quale caso distingue una funzione corretta da una che restituisce sempre zero.

## Dove ci si confonde spesso

- Catturare tutto e ignorare l'errore
- Mostrare dettagli sensibili all'utente

## Domanda di verifica

> Quando è corretto lanciare un errore invece di restituire null?

Confronta la tua spiegazione con la flashcard dedicata alla domanda.
