# Alberi binari: preorder, inorder, postorder e livelli

Preorder elabora il nodo prima dei figli, inorder fra il figlio sinistro e il destro, postorder dopo entrambi. Su un BST, inorder restituisce i valori crescenti perché ogni nodo è maggiore di tutto il sottoalbero sinistro e minore di quello destro.

Per l'albero `1` con figli `2` e `3`, e figli `4` e `5` sotto `2`, le visite differiscono:

| Ordine | Sequenza |
| --- | --- |
| Preorder: nodo, sinistra, destra | `1,2,4,5,3` |
| Inorder: sinistra, nodo, destra | `4,2,5,1,3` |
| Postorder: sinistra, destra, nodo | `4,5,2,3,1` |
| Per livelli, con una queue | `1,2,3,4,5` |

Con una visita postorder puoi anche calcolare una proprietà composta dai figli. Come primo esempio, somma il valore del nodo ai totali dei due sottoalberi. Questa funzione visita entrambi i rami, riceve i loro risultati e combina le risposte soltanto al ritorno.

**Versione Python**

```python
class TreeNode:
    def __init__(self, value=0, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def sum_tree(node):
    if node is None:
        return 0
    left_total = sum_tree(node.left)
    right_total = sum_tree(node.right)
    return node.value + left_total + right_total
```

**Versione C++**

```cpp
#include <algorithm>

struct TreeNode {
    int value;
    TreeNode* left;
    TreeNode* right;
};

int sum_tree(const TreeNode* node) {
    if (node == nullptr) {
        return 0;
    }

    const int left_total = sum_tree(node->left);
    const int right_total = sum_tree(node->right);
    return node->value + left_total + right_total;
}
```

Il valore nullo è l'identità della somma: aggiungerlo non cambia il risultato. La funzione visita ogni nodo una volta (`O(n)` tempo) e conserva `O(h)` chiamate; un albero vuoto restituisce zero. Nelle esercitazioni di diametro e massimo cammino, il risultato restituito dai figli non basta da solo: occorre anche aggiornare un massimo globale con una combinazione che il genitore non può usare direttamente.

### Separare i livelli durante la BFS

Per visita per livelli, la coda iniziale contiene la radice 1. Dopo averla estratta, accoda 2 e 3. Salva `level_size=2`, poi processa esattamente questi due nodi e accoda 4 e 5. Senza quel limite, i nodi appena accodati finirebbero nel risultato dello stesso livello.

Maximum Path Sum usa un'altra combinazione postorder. Con radice `-10`, figlio sinistro `9` e ramo destro `20` con figli `15` e `7`, il nodo 20 riceve guadagni 15 e 7: il cammino che lo attraversa vale 42, mentre verso il genitore può restituire un solo ramo, `20+15=35`. Alla radice il cammino che passa da lì vale `-10+9+35=34`, quindi il massimo globale resta 42.

I guadagni negativi si sostituiscono con zero quando li si aggiunge a un cammino più grande. Il massimo globale va però inizializzato dal primo nodo, non da zero: con soli valori negativi la risposta è il nodo meno negativo, non il cammino vuoto.

### Dal percorso ricorsivo alla visita per livelli

Invertire un albero significa scambiare i figli di ogni nodo; confrontare due alberi richiede che valori e posizione dei figli coincidano. Per cercare un sottoalbero prova ogni nodo come possibile radice e confronta l'intera struttura: trovare il valore della radice da solo non basta.

Per raggruppare i livelli usa una coda. Con radice 3 e figli 9 e 20, la coda parte da `[3]`: consumi una sola voce, raccogli `[3]` e accodi 9 e 20; la dimensione iniziale della coda delimita il livello successivo `[9,20]`. Non consumare i figli appena accodati nel livello corrente.

Per ricostruire l'albero da preorder e inorder, il primo valore preorder è la radice. La sua posizione in inorder separa il sottoalbero sinistro dal destro. Con preorder `[3,9,20,15,7]` e inorder `[9,3,15,20,7]`, 3 divide `[9]` da `[20,15,7]`; ricorri sui due intervalli. Una mappa delle posizioni evita di riscanalizzare inorder a ogni passo.

Una serializzazione deve distinguere i figli mancanti dalla fine dei token. In BFS, `1,#,2` descrive una radice con solo figlio destro; senza `#`, il 2 potrebbe essere interpretato come figlio sinistro. Definisci un formato preciso e fai il round trip serializza → deserializza → serializza.

**Da ricordare.** Preorder, inorder, postorder e BFS differiscono per il momento in cui elaborano un nodo; il dato richiesto decide l'ordine. **Per praticare:** Diametro di un albero binario; Massima somma di un cammino in un albero; Invertire un albero binario; Confrontare due alberi; Verificare se un albero contiene un sottoalbero; Visitare un albero per livelli; Ricostruire un albero da preorder e inorder; Serializzare e ricostruire un albero.