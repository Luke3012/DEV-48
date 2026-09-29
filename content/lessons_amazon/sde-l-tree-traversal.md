# Alberi binari: preorder, inorder, postorder e livelli

Preorder visita nodo, sinistra, destra; inorder visita sinistra, nodo, destra; postorder visita i figli prima del nodo. Su un BST, inorder restituisce valori in ordine crescente. Il nome è un promemoria dell'istante in cui elabori il nodo rispetto alle chiamate ai figli.

La visita per livelli usa una queue. Memorizza la dimensione della coda prima di iniziare il livello: così elabori esattamente i nodi già presenti, senza includere quelli appena aggiunti. Un albero vuoto è un input normale, non un'eccezione.

In C++ un puntatore `const TreeNode*` rende esplicito che la visita legge l'albero; in Python il nodo può essere una piccola classe con `left` e `right`. Prima di copiare una ricorsione, definisci il valore restituito da ciascun sottoalbero.
