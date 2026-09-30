# Stack, Queue e Deque: scegliere l'ordine delle visite

Un editor incontra `(`, poi `[`, poi `]`, poi `)`. Per decidere se ogni chiusura corrisponde, basta ricordare le aperture non ancora chiuse. La più recente va controllata per prima: è la regola LIFO di uno stack. Un semplice conteggio non basta, perché `([)]` ha lo stesso numero di parentesi aperte e chiuse ma un ordine impossibile.

Scegliamo di salvare nello stack il carattere di chiusura atteso: leggendo `(` inseriamo `)`, leggendo `[` inseriamo `]`. Quando compare una chiusura, deve coincidere con la cima; dopo il controllo la rimuoviamo.

| Carattere letto | Stack dopo il passo (fondo → cima) | Conseguenza |
| --- | --- | --- |
| `(` | `)` | la prossima chiusura deve essere `)` |
| `[` | `)`, `]` (cima) | la prossima deve essere `]` |
| `]` | `)` | corrisponde alla cima; rimuovi `]` |
| `)` | `[]` | corrisponde alla cima; la stringa è valida |

**Versione Python**

```python
def valid_parentheses(text):
    closing_for = {"(": ")", "[": "]", "{": "}"}
    expected = []

    for char in text:
        if char in closing_for:
            expected.append(closing_for[char])
        elif not expected or expected.pop() != char:
            return False

    return not expected
```

**Versione C++**

```cpp
#include <stack>
#include <string>
using namespace std;

bool valid_parentheses(const string& text) {
    stack<char> expected;

    for (char ch : text) {
        if (ch == '(') {
            expected.push(')');
        } else if (ch == '[') {
            expected.push(']');
        } else if (ch == '{') {
            expected.push('}');
        } else {
            if (expected.empty() || expected.top() != ch) {
                return false;
            }
            expected.pop();
        }
    }

    return expected.empty();
}
```

Entrambe le funzioni assumono che l'input contenga soltanto parentesi; l'else tratta quindi ogni carattere rimanente come una chiusura. Ogni carattere entra o viene rimosso dallo stack al massimo una volta: `O(n)` tempo e fino a `O(n)` spazio, per un input composto solo da aperture annidate. Una queue conserva invece l'ordine FIFO: è adatta alla BFS, che completa la distanza `d` prima di espandere i nodi a distanza `d+1`.

### Dalla FIFO alle visite per livelli

Immagina gli archi `A→B`, `A→C`, `B→D`. Una BFS parte dalla coda `[A]`, visita A e accoda B e C: `[B,C]`. Estrae B e accoda D: `[C,D]`. Prima di D visita C, così tutte le distanze 1 sono trattate prima della distanza 2. In Python usa `collections.deque` e `popleft()`; in C++ `queue.front()` legge la testa e `queue.pop()` la rimuove.

Questa proprietà dà un cammino minimo solo se ogni arco costa lo stesso. Con pesi diversi, una coda FIFO non ordina per costo: occorre un algoritmo come Dijkstra.

**Da ricordare.** Stack = ultimo entrato, primo uscito; queue = primo entrato, primo uscito. La scelta codifica l'ordine corretto. **Per praticare:** Parentheses con tipi e ordine corretti.