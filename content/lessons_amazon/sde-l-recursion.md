# Ricorsione: caso base, progresso e costo dello stack

Una funzione ricorsiva delega una parte più piccola del problema a una nuova chiamata. Per iniziare, sommiamo gli interi da 1 a `n`: quando `n=0` la somma restante è zero; quando `n>0`, la risposta è `n` più la somma da 1 a `n-1`. Il numero diminuisce a ogni chiamata, quindi prima o poi raggiunge il caso base.

Con `sum_to(3)`, le chiamate scendono `3 → 2 → 1 → 0`. La chiamata con 0 restituisce 0; poi i frame sospesi rispondono `1+0=1`, `2+1=3`, `3+3=6`. Ogni frame conserva il proprio `n` mentre aspetta il risultato più piccolo.

**Versione Python**

```python
def sum_to(n):
    if n < 0:
        raise ValueError("n deve essere non negativo")
    if n == 0:
        return 0
    return n + sum_to(n - 1)
```

**Versione C++**

```cpp
#include <stdexcept>

long long sum_to(int n) {
    if (n < 0) {
        throw std::invalid_argument("n deve essere non negativo");
    }
    if (n == 0) {
        return 0;
    }
    return n + sum_to(n - 1);
}
```

Il caso `n=0` risponde senza altre chiamate; `n<0` non progredirebbe verso la base, quindi il contratto lo rifiuta. Per un valore non negativo vengono create `n+1` chiamate: tempo e stack sono `O(n)`. La ricorsione non rende il calcolo automaticamente più veloce: per questa somma esiste una formula diretta, ma l'esempio isola la struttura dei casi base e del ritorno.

### Profondità delle chiamate e lavoro ripetuto

La profondità dello stack misura quante chiamate restano sospese contemporaneamente; il numero totale di chiamate può essere molto più grande. Fibonacci ingenuo crea un albero di chiamate: `F(5)` chiede `F(4)` e `F(3)`, mentre `F(4)` chiede ancora `F(3)`. Il valore dello stesso stato viene ricalcolato. Una memoization può salvare i risultati soltanto quando le chiamate condividono sottoproblemi; la lezione seguente separa stato, transizione e cache.

Per un albero, il caso base `None → 0` si combina con i risultati dei figli: la profondità è uno più la maggiore profondità dei sottoalberi. Questa forma postorder generalizza la somma ricorsiva del capitolo. La visita fa `O(n)` chiamate, ma la memoria resta `O(h)`; una catena di `n` nodi può raggiungere profondità `n` anche se il lavoro totale è lineare.

**Da ricordare.** Definisci prima che cosa restituisce ogni chiamata, qual è la base e come il problema diventa più piccolo. **Per praticare:** Profondità massima di un albero.