# Dai primi due minuti a una soluzione verificabile

Quando il cronometro parte, la tentazione è digitare subito. Fai invece un esempio piccolo con le mani. Per una lista `[4, 1, 7]` e una ricerca del valore `1`, scrivi quale risultato deve uscire e cosa succede se la lista è vuota. Una domanda fatta ora costa pochi secondi; una supposizione errata può costarti l'intero tentativo.

Poi scegli la versione più semplice che rispetta il contratto e misurane il costo. Se la prima idea confronta ogni coppia, con `n` elementi esegue circa `n²` confronti. Non è un difetto se `n` è piccolo; diventa un problema quando il vincolo arriva a decine di migliaia. Solo a quel punto cerca l'informazione che manca: una mappa, un ordinamento, una finestra mantenuta tra un passo e il successivo.

Mentre implementi, tieni un'invariante in una frase. Durante una scansione può essere: «tutti gli elementi prima dell'indice corrente sono già stati controllati». In un altro pattern potresti dire: «la mappa contiene i dati già attraversati e il valore associato ha questo significato preciso». Dopo ogni cambiamento, verifica un caso che avrebbe fatto fallire la versione precedente. Se il codice non va, riduci l'input e formula una causa precisa; cambiare tre righe insieme cancella le prove.

Un ritmo realistico per 40 minuti è: chiarimento e casi, 4–6 minuti; scelta e implementazione, circa 25; test manuali e rifinitura, il tempo restante. Se una strada è bloccata, conserva la soluzione parziale e prova un'alternativa con costo chiaro.

### Esempio svolto: trasformare una frase in una scansione

Richiesta: «Restituisci l'indice del primo valore strettamente maggiore di `limite`; se non esiste, restituisci `-1`.» Usiamo `values = [2, 7, 1, 9]` e `limite = 5`.

| Indice | Valore | Domanda | Decisione |
| ---: | ---: | --- | --- |
| 0 | 2 | `2 > 5`? | No, passa al successivo |
| 1 | 7 | `7 > 5`? | Sì, restituisci 1 e fermati |

Il risultato è 1: non serve esaminare il 9, perché la parola «primo» impone di fermarsi alla prima corrispondenza. Una scansione possibile è:

```text
per ogni indice i da sinistra a destra:
    se values[i] > limite:
        restituisci i
restituisci -1
```

Proviamo ora due casi che possono smentire una soluzione frettolosa: con `[5, 4]` la risposta è `-1` perché la condizione è strettamente maggiore, non maggiore o uguale; con `[]` la scansione non entra nel ciclo e restituisce comunque `-1`. Il ragionamento resta lo stesso anche quando cambi algoritmo: traduci le parole importanti in confronti precisi, poi segui un input fino al risultato.

### Dal controllo a mano a una funzione

La richiesta precedente si traduce in quattro decisioni: scorrere da sinistra, confrontare con `> 5`, restituire subito il primo indice e usare `-1` se il ciclo finisce. Ecco la stessa idea in entrambe le lingue:

**Versione Python**

```python
def first_above(values, limit):
    for index, value in enumerate(values):
        if value > limit:
            return index
    return -1
```

**Versione C++**

```cpp
#include <vector>

int first_above(const std::vector<int>& values, int limit) {
    for (int index = 0; index < static_cast<int>(values.size()); ++index) {
        if (values[index] > limit) {
            return index;
        }
    }
    return -1;
}
```

Su `[2, 7, 1, 9]`, `enumerate` produce `(0, 2)`, poi `(1, 7)`: il secondo valore supera 5 e la funzione termina con 1. Il `9` non viene letto. Su `[5, 4]` nessun valore supera strettamente il limite, quindi si raggiunge `return -1`; su `[]` il ciclo non parte e la stessa risposta resta valida. La funzione è corretta perché ogni indice precedente a quello restituito è già stato controllato e non soddisfa la condizione.

**Da ricordare.** Un'invariante descrive che cosa è già stato dimostrato dopo ogni passo; i test cercano di falsificarla. **Per praticare:** Due valori che completano il target; Rilevare un duplicato senza ordinare.