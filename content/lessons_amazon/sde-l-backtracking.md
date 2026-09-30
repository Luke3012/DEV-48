# Backtracking: esplorare scelte e annullarle bene

Il backtracking visita un albero di decisioni e mantiene il percorso corrente. Ogni scelta aggiunta vale soltanto per il ramo che la sta esplorando: al ritorno dalla ricorsione la rimuovi, così il ramo seguente parte dallo stato giusto.

Per generare stringhe binarie di lunghezza 2, a ogni posizione scegli `0` oppure `1`. Il percorso produce, in ordine, `00`, `01`, `10`, `11`. Dopo aver salvato `00`, la scelta finale `0` viene tolta prima di provare `1`; dopo aver completato entrambi i rami, si torna alla prima posizione.

**Versione Python**

```python
def binary_strings(length):
    if length < 0:
        raise ValueError("length deve essere non negativa")
    results = []
    current = []

    def build(position):
        if position == length:
            results.append("".join(current))
            return

        for bit in ("0", "1"):
            current.append(bit)
            build(position + 1)
            current.pop()

    build(0)
    return results
```

**Versione C++**

```cpp
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;

void build_binary_strings(int length, int position, string& current, vector<string>& results) {
    if (position == length) {
        results.push_back(current);
        return;
    }

    const char choices[2] = {'0', '1'};
    for (char bit : choices) {
        current.push_back(bit);
        build_binary_strings(length, position + 1, current, results);
        current.pop_back();
    }
}

vector<string> binary_strings(int length) {
    vector<string> results;
    string current;
    if (length < 0) {
        throw invalid_argument("length deve essere non negativa");
    }
    build_binary_strings(length, 0, current, results);
    return results;
}
```

Il percorso `current` viene passato per riferimento in C++ e mutato sul posto; `results.push_back(current)` ne salva una copia alla foglia. Se `length=0`, il caso base salva una stringa vuota. Ci sono `2^n` foglie e ogni risposta contiene `n` caratteri, quindi materializzare l'output richiede `O(n·2^n)` tempo e memoria; lo stato temporaneo e lo stack usano `O(n)`.

Lo stesso albero include/esclude descrive i sottoinsiemi. Per le permutazioni occorre anche impedire di scegliere di nuovo un indice già usato; per Combination Sum il riuso può invece essere consentito. Il costo può essere esponenziale, quindi cerca una regola sicura per potare un ramo prima di esplorare i suoi discendenti.

### Un albero di scelte con stato ripristinato

Per i valori `[1,2]`, ogni livello decide se includere il prossimo valore. Dal percorso vuoto `[]`, includi 1 e salva `[1]`; includi 2 e salva `[1,2]`; togli 2 tornando a `[1]`, poi togli 1 tornando a `[]`. Il ramo che salta 1 e include 2 salva `[2]`; quello che salta entrambi salva `[]`. Se aggiungi una scelta, dopo la chiamata ricorsiva esegui il passo inverso. Quando registri una risposta, copia `path`: salvare sempre lo stesso riferimento fa apparire tutte le risposte uguali all'ultimo stato.

Per n valori distinti ci sono `2^n` sottoinsiemi; materializzarli richiede già O(n·2^n) tempo e memoria di output. Le permutazioni sono n!, e una singola copia costa O(n). La potatura riduce i rami esplorati soltanto se il vincolo lo giustifica: con candidati positivi, un totale oltre il target non può tornare valido; con valori negativi quell'arresto può essere scorretto.

Per Combination Sum il valore scelto può riapparire, quindi la ricorsione riparte dallo stesso indice; per subsets si passa al successivo. Questa differenza evita rispettivamente di vietare un riuso permesso o di generare permutazioni duplicate.

**Da ricordare.** Ogni ramo rappresenta una scelta, il caso base salva una risposta e il ripristino garantisce che i rami restino indipendenti. **Per praticare:** Generare tutti i sottoinsiemi; Ordinare tutti gli ordini possibili; Combinazioni che raggiungono il target.