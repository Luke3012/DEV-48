# Monotonic Stack: conservare candidati ancora utili

Per ogni valore vogliamo il primo valore strettamente più grande che compare alla sua destra. Provare tutti i successori per ciascuna posizione confronta fino a `O(n²)` coppie. Invece conserviamo nello stack gli indici a cui non abbiamo ancora assegnato una risposta. I valori corrispondenti restano decrescenti: quando arriva un valore maggiore, risolve gli indici più piccoli che attendono in cima.

Con `[2,1,3]`, i primi due indici restano in attesa; quando arriva 3, esso è il successore maggiore di entrambi. L'ultimo indice non troverà una risposta:

| Indice letto | Valore | Indici in attesa dopo il passo | Risposte determinate |
| ---: | ---: | --- | --- |
| 0 | 2 | `[0:2]` | nessuna |
| 1 | 1 | `[0:2,1:1]` | nessuna |
| 2 | 3 | `[2:3]` | `answer[1]=3`, `answer[0]=3` |
| fine | — | `[2:3]` | `[3,3,-1]` nell'ordine degli indici |

**Versione Python**

```python
def next_greater_values(values):
    answer = [-1] * len(values)
    waiting = []

    for index, value in enumerate(values):
        while waiting and value > values[waiting[-1]]:
            previous = waiting.pop()
            answer[previous] = value
        waiting.append(index)

    return answer
```

**Versione C++**

```cpp
#include <vector>
using namespace std;

vector<int> next_greater_values(const vector<int>& values) {
    vector<int> answer(values.size(), -1);
    vector<int> waiting;

    for (int index = 0; index < static_cast<int>(values.size()); ++index) {
        while (!waiting.empty() && values[index] > values[waiting.back()]) {
            const int previous = waiting.back();
            waiting.pop_back();
            answer[previous] = values[index];
        }
        waiting.push_back(index);
    }

    return answer;
}
```

Il valore `-1` iniziale significa che non esiste un successore maggiore. Ogni indice entra nello stack una volta e ne esce al massimo una; il ciclo interno può fare più operazioni in un passo, ma il totale dei push e pop resta `O(n)`. Lo spazio ausiliario è `O(n)`. Se la consegna chiedesse “maggiore o uguale”, il confronto stretto `>` andrebbe cambiato; con valori uguali, la scelta cambia il risultato.

### Un rettangolo che aspetta il proprio confine

Nell'istogramma `[2,1,2]`, l'indice 0 di altezza 2 non può estendersi oltre l'indice 1: lì compare una barra più bassa. Quando l'indice 1 viene rimosso, la barra di altezza 1 ha trovato il proprio confine destro; il nuovo indice in cima allo stack determina il confine sinistro. La larghezza è `right-left`, quindi la barra bassa forma un rettangolo di area `1·3=3`.

Una sentinella finale di altezza 0 forza a chiudere le barre rimaste. Le altezze uguali richiedono una condizione coerente: usando `<` o `<=` cambia quale copia resta come candidato, perciò prova anche istogrammi piatti e una singola barra.

**Da ricordare.** Lo stack monotono elimina un candidato solo quando il nuovo elemento ne determina la risposta o lo rende inutile. **Per praticare:** Attesa fino a una giornata più calda; Rettangolo massimo in un istogramma.