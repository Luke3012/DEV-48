# Linked List: cambiare collegamenti senza perdere la lista

Una lista collegata è una catena di nodi; ciascun nodo conserva un valore e un riferimento al successivo. Il nodo iniziale è `head`, la fine è indicata da `None` o `nullptr`. A differenza di un array non puoi saltare direttamente al nodo 20: devi seguire i collegamenti, perciò l'accesso all'indice `k` costa `O(k)`. Se hai già il riferimento al nodo giusto, invece, cambiare un link costa `O(1)`.

Supponi di avere `A → C` e un nodo nuovo `B` da inserire dopo A. Prima fai puntare B al successore di A, poi aggiorni il link di A:

| Passo | `A.next` | `B.next` | Catena raggiungibile da A |
| ---: | --- | --- | --- |
| iniziale | C | `None` | `A → C` |
| collega B al successore | C | C | `A → C` e `B → C` |
| collega A a B | B | C | `A → B → C` |

L'ordine evita di perdere C. Se prima sovrascrivessi `A.next` con B, non sapresti più quale nodo assegnare a `B.next`.

**Versione Python**

```python
class ListNode:
    def __init__(self, value=0, next_node=None):
        self.value = value
        self.next = next_node


def insert_after(previous, node):
    node.next = previous.next
    previous.next = node
```

**Versione C++**

```cpp
struct ListNode {
    int value;
    ListNode* next;
};

void insert_after(ListNode* previous, ListNode* node) {
    node->next = previous->next;
    previous->next = node;
}
```

La funzione presuppone che `previous` e `node` siano validi e che `node` non faccia già parte della catena. Una volta raggiunto `previous`, l'inserimento costa `O(1)` tempo e spazio: la lista non viene ricopiata.

L'inversione generalizza la stessa cautela: per ogni nodo salvi il collegamento originale al successore prima di riscriverlo verso il predecessore. Nella fusione di due liste ordinate colleghi la testa minore e avanzi solo la lista da cui proviene. Per cercare un ciclo, `slow` avanza di uno e `fast` di due; se la catena termina, `fast` o `fast.next` diventa nullo, altrimenti i due possono incontrarsi.

### Come ragionare su un ciclo e su una fusione

In `1→2→3→4→2`, il nodo 4 torna al 2. Partendo entrambi da 1, dopo un passo `slow=2, fast=3`; dopo il successivo `slow=3, fast=2`; al terzo `slow=4, fast=4`. La visita incontra un nodo già attraversato senza memorizzare l'intera catena. Se la lista finisse, il controllo di `fast` e `fast.next` impedirebbe di oltrepassare `None`/`nullptr`.

Per fondere `k` liste ordinate, un min-heap conserva una sola testa per lista: estrai la più piccola, collegala al risultato e inserisci il suo successore. Con `N` nodi, il tempo è `O(N log k)` e lo heap usa `O(k)` spazio. Una LRU aggiunge invece una mappa chiave→nodo e due link per spostare un nodo noto in testa in `O(1)`; le sentinelle semplificano le operazioni ai bordi.

**Da ricordare.** I collegamenti sono riferimenti modificabili: conserva il prossimo nodo prima di riscriverli e usa una mappa solo quando serve accesso diretto. **Per praticare:** Invertire una lista collegata; Rilevare un ciclo nei collegamenti; Cache LRU con capacità limitata.