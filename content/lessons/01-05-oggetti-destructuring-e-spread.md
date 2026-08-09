# Oggetti, destructuring e spread

## In parole semplici

L'obiettivo di questa lezione è leggere e creare copie aggiornate di strutture dati applicative.

Destructuring rende espliciti i campi che stai leggendo; spread aiuta a creare una copia con alcuni campi aggiornati. Ricorda però che la copia è superficiale: gli oggetti annidati restano condivisi se non li copi a loro volta.

### Perché è utile

In JavaScript è utile seguire i valori uno alla volta: che tipo hanno, dove vengono creati e che cosa restituisce ogni espressione. Se sai prevedere questi passaggi, scrivere il codice diventa molto meno meccanico.

## Le parole da riconoscere

- `proprietà`
- `destructuring`
- `spread`
- `optional chaining`
- `nullish coalescing`
- `copia superficiale`

Non serve imparare questo elenco a memoria. Per iniziare, concentrati su **proprietà, destructuring, spread** e cerca di usarli mentre descrivi l'esempio qui sotto.

## Un esempio concreto

```text
const updated = { ...user, profile: { ...user.profile, city: 'Milano' } };
const city = updated.profile?.city ?? 'N/D';
```

Segui il valore dall'ingresso fino al `return`. Chiediti che cosa cambierebbe con un valore vuoto, mancante o di tipo inatteso.

Adesso copri l'esempio e prova a ricostruirne la parte essenziale. Non deve essere identico: deve conservare lo stesso comportamento. Quando ci riesci, prova un caso normale e un caso limite.

## Dove ci si confonde spesso

- Credere che spread faccia una copia profonda
- Modificare oggetti condivisi

Se qualcosa non funziona, evita di cambiare più righe a caso. Riproduci il problema con l'input più piccolo possibile, formula un'ipotesi e verifica una sola modifica per volta.

## Controllo rapido

- Riesco a spiegarlo senza leggere la pagina?
- So indicare input, risultato e almeno un caso limite?
- Riesco a riscrivere l'esempio partendo da un file vuoto?
- So dire come verificherei che funziona?

## Domanda di verifica

> Perché {...obj} non è sempre una copia completamente indipendente?

Prova a rispondere senza rileggere: prima la regola, poi un esempio. Se ti manca un termine, descrivi il comportamento con parole semplici invece di fermarti.

## Prima di andare avanti

Chiudi la pagina per un minuto e ripeti tre cose: che problema risolve questo argomento, quale errore vuoi evitare e quale esempio useresti per spiegarlo. Se una delle tre non viene, riapri soltanto la sezione che ti serve.
