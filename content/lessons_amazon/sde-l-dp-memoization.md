# Dynamic Programming: recursion, memoization, tabulation

Dynamic programming nasce quando una ricorsione risolve più volte lo stesso sottoproblema. La prima domanda non è “quale tabella uso?”, ma “quale stato identifica una domanda la cui risposta può essere riutilizzata?”. Per Fibonacci, lo stato è `n`: la risposta dipende solo da `n-1` e `n-2`, non dal percorso di chiamate che ha portato fin lì.

La ricorsione diretta di `fib(5)` calcola `fib(3)` sia nel ramo di `fib(4)` sia come secondo figlio della radice. Una mappa conserva il risultato alla prima visita:

| Stato richiesto | Dipendenze | Risultato memorizzato |
| ---: | --- | ---: |
| `fib(2)` | `fib(1)+fib(0)` | 1 |
| `fib(3)` | `fib(2)+fib(1)` | 2 |
| `fib(4)` | `fib(3)+fib(2)` | 3 |
| `fib(5)` | `fib(4)+fib(3)` | 5 |

Alla seconda richiesta di `fib(3)`, si legge il valore 2 dalla cache invece di espandere altre chiamate.

Per mantenere equivalenti i risultati numerici degli esempi, consideriamo `0 <= n <= 92`: la risposta entra in un intero a 64 bit.

**Versione Python**

```python
def fibonacci(n):
    if n < 0:
        raise ValueError("n deve essere non negativo")
    memo = {0: 0, 1: 1}

    def solve(state):
        if state not in memo:
            memo[state] = solve(state - 1) + solve(state - 2)
        return memo[state]

    return solve(n)
```

**Versione C++**

```cpp
#include <stdexcept>
#include <vector>
using namespace std;

long long fibonacci(int n) {
    if (n < 0) {
        throw invalid_argument("n deve essere non negativo");
    }
    vector<long long> memo(n + 1, -1);
    memo[0] = 0;
    if (n >= 1) {
        memo[1] = 1;
    }

    auto solve = [&](auto&& self, int state) -> long long {
        if (memo[state] == -1) {
            memo[state] = self(self, state - 1) + self(self, state - 2);
        }
        return memo[state];
    };

    return solve(solve, n);
}
```

Gli stati da 0 a `n` vengono calcolati una sola volta; ciascuno fa lavoro costante, quindi il tempo è `O(n)`, la cache `O(n)` e lo stack ricorsivo può raggiungere `O(n)`. La tabulation usa lo stesso stato ma lo calcola dal basso: dopo aver trovato due valori, può conservarne soltanto gli ultimi due. Quale forma è più chiara dipende da quali stati servono davvero.

### Stesso schema, basi diverse

Climbing Stairs usa la stessa dipendenza dagli ultimi due stati, ma `ways(0)=1`: esiste un solo modo di restare al punto di partenza senza fare passi. Quindi `ways(1)=1`, `ways(2)=2`, `ways(3)=3`, `ways(4)=5`. Le basi fanno parte del significato del problema e non si copiano automaticamente da Fibonacci.

Coin Change cambia la transizione: per un importo `x` provi ciascuna moneta `c<=x` e confronti `1+dp[x-c]`. Il sentinel per uno stato irraggiungibile deve restare distinto da zero. Prima conta quanti stati esistono, poi quante transizioni prova ciascuno; così ricavi il tempo invece di ricordare una formula.

**Da ricordare.** La DP evita di risolvere più volte lo stesso stato; definizione dello stato, base e transizione vengono prima dell'ottimizzazione dello spazio. **Per praticare:** Contare i modi per salire le scale; Massimo bottino senza case adiacenti.