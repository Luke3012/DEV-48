# BST, profondità e antenati: usare la struttura dichiarata

In un BST, ogni valore nel sottoalbero sinistro è minore della radice e ogni valore a destra è maggiore, se il contratto non ammette duplicati. La proprietà globale permette di cercare un elemento seguendo un solo cammino: ogni confronto elimina un sottoalbero intero.

Nell'albero con radice 10, figlio destro 15 e figlio sinistro di 15 pari a 12, cercare 12 porta prima a destra di 10, poi a sinistra di 15. Se cerchi 6, vai a sinistra verso 5 e poi a destra; arrivare a un figlio nullo dimostra che il valore non è presente.

**Versione Python**

```python
class TreeNode:
    def __init__(self, value=0, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def contains_bst(root, target):
    current = root
    while current is not None:
        if current.value == target:
            return True
        if target < current.value:
            current = current.left
        else:
            current = current.right
    return False
```

**Versione C++**

```cpp
struct TreeNode {
    int value;
    TreeNode* left;
    TreeNode* right;
};

bool contains_bst(const TreeNode* root, int target) {
    const TreeNode* current = root;
    while (current != nullptr) {
        if (current->value == target) {
            return true;
        }
        if (target < current->value) {
            current = current->left;
        } else {
            current = current->right;
        }
    }
    return false;
}
```

La ricerca costa `O(h)` tempo e `O(1)` spazio, con `h` pari alla lunghezza del cammino percorso. Un BST bilanciato ha altezza logaritmica; un albero inclinato può richiedere `O(n)`. L'ordinamento dei valori non garantisce da solo che l'albero sia bilanciato.

### I limiti arrivano dagli antenati

La radice 10 ha figlio destro 15 e il nodo 6 come figlio sinistro di 15. Ogni coppia padre-figlio sembra ordinata localmente, ma 6 viola il limite ereditato dalla radice: tutto il sottoalbero destro di 10 deve contenere valori maggiori di 10. Una visita porta quindi due limiti: per 15 il limite inferiore diventa 10; 6 non è strettamente maggiore di quel limite.

Con duplicati, il contratto deve stabilire dove possano stare; la validazione corrente richiede valori strettamente compresi e non ammette duplicati. Per LCA dei valori 4 e 7 in un BST con radice 5, uno va a sinistra e l'altro a destra: 5 è il primo punto in cui i percorsi si separano. Se entrambi fossero 4 e 7 a sinistra, si proseguirebbe a sinistra.

Entrambi gli algoritmi seguono al massimo un cammino di altezza h: O(h) tempo. La validazione visita ogni nodo, O(n), con O(h) stack. Un albero sbilanciato può avere h=n; non assumere automaticamente h=log n.

### Il k-esimo elemento segue l'inorder

In un BST l'inorder visita prima i valori minori del sottoalbero sinistro, poi il nodo, poi i maggiori del destro. Su radice 5, ramo sinistro 3 con figli 2 e 4, la visita comincia `2,3,4,5`; il terzo valore è 4. Una pila esplicita conserva i nodi in attesa e permette di fermarsi appena hai estratto il k-esimo, senza attraversare necessariamente tutto l'albero.

**Da ricordare.** Usa la proprietà globale del BST passando limiti e non soltanto confrontando un nodo coi figli immediati. **Per praticare:** Convalidare l'ordine globale di un BST; Lowest common ancestor in un BST; K-esimo valore più piccolo in un BST.