# Trie: parole, prefissi e ricerche con wildcard

Un dizionario hash risponde bene a «questa parola intera esiste?», ma una ricerca per prefisso può richiedere di provare molte chiavi. Una trie condivide invece i percorsi iniziali delle parole. Inseriamo `cat`, `car` e `dog`: il prefisso `ca` compare una volta nella struttura, mentre i rami finali distinguono `t` e `r`.

```text
root
├─ c
│  └─ a
│     ├─ t*  (cat è una parola)
│     └─ r*  (car è una parola)
└─ d
   └─ o
      └─ g*  (dog è una parola)
```

Ogni nodo rappresenta un prefisso raggiunto; ogni arco aggiunge un carattere. L'asterisco non è un arco: indica un flag `terminal` che dice che il percorso completo è stato inserito come parola. Così `search("ca")` è falso mentre `starts_with("ca")` è vero. Senza il flag, il nodo `ca` non ci direbbe se `ca` è una parola autonoma.

Per inserire `cat`, parti dalla radice e crea soltanto i nodi mancanti `c`, `a`, `t`; marca l'ultimo come terminale. Per cercare una parola segui ogni carattere: un arco assente significa subito “non trovata”; arrivare all'ultimo nodo non basta, serve anche `terminal`. Per cercare un prefisso è sufficiente arrivare al nodo finale, anche se non è terminale. Una parola vuota, se ammessa dal contratto, termina già alla radice.

Se la parola ha lunghezza `L`, inserimento e lookup visitano al massimo `L` archi, quindi costano `O(L)`; lo spazio dipende dai nodi creati e può arrivare alla somma delle lunghezze delle parole. Una hash map può avere una ricerca esatta più semplice e memoria inferiore quando quasi nessun prefisso viene condiviso: una trie è utile quando prefix lookup o wildcard sono davvero richiesti.

Nella ricerca con wildcard `.` un arco non rappresenta un carattere noto: bisogna provare i figli disponibili. Per `c.t`, dopo `c` si esplorano i rami possibili al posto del punto e si accetta soltanto un percorso terminale. Questa scelta crea un albero di ricerca e usa backtracking; non si applica al lookup esatto. Word Search II combina infine la trie con una DFS sulla griglia e resta un approfondimento Extra/Hard.

### Seguire un prefisso condiviso

Inserendo `cat` e poi `car`, il percorso `c → a` viene riutilizzato; solo gli ultimi archi divergono. Il nodo `ca` non è automaticamente una parola: un flag terminale permette di rispondere `starts_with("ca") == True` e `search("ca") == False`.

Con una wildcard `.` non conosci l'arco da seguire. Se il pattern è `c.t`, dopo `c` provi i figli del nodo e prosegui di un carattere per ciascun ramo. Il backtracking si ferma appena trova una parola terminale; una corrispondenza parziale non basta.

Una griglia Word Search II usa la stessa idea su due dimensioni: dalla cella corrente la DFS segue soltanto il ramo della lettera adiacente, marca la cella per non riutilizzarla e ripristina la griglia quando torna indietro. Quando una parola viene trovata, il nodo terminale può essere disattivato per non restituire duplicati; i rami senza parole restanti si possono potare.

Le query esatte e di prefisso costano O(L) per stringa lunga L. Wildcard e ricerca su griglia possono esplorare più rami; la Trie condivide prefissi e consente pruning, ma non elimina il caso peggiore.

**Da ricordare.** Ogni nodo descrive un prefisso; il flag terminale distingue una parola completa da un percorso ancora estendibile. **Per praticare:** Implementare ricerca di parole e prefissi con una Trie; Cercare parole con caratteri wildcard; Trovare parole su una griglia senza riusare celle.