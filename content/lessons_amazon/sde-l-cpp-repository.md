# Repository C++: header, source, classi e test

Un header dichiara quali nomi e tipi sono disponibili; un file `.cpp` contiene spesso l'implementazione. Se il compilatore dice “undefined reference”, la dichiarazione può esistere ma la definizione non entra nel link. Se segnala un tipo sconosciuto, controlla gli include prima di riscrivere la funzione.

Con CMake si individua il target compilato e i file che lo compongono. La diagnosi parte dall'errore più vicino al codice applicativo e dal numero di riga del progetto. Una modifica a una firma in header deve restare coerente con source e chiamanti.

Un'asserzione `EXPECT_EQ(expected, actual)` confronta valori; per una classe, chiediti se il contratto è osservabile tramite metodo pubblico. Un test che passa non giustifica una modifica ampia all'API. Mantieni lo stato privato e correggi la regola che produce il valore errato.

### Dichiarazione, definizione e target

In una repository piccola, `Inventory.h` può dichiarare `bool visibleActive(const Item&)`; `Inventory.cpp` definisce la regola e `InventoryTest.cpp` verifica il risultato. Se il test compila ma il linker segnala `undefined reference to visibleActive`, la dichiarazione esiste ma la definizione può mancare dal target CMake o avere una firma diversa. Riscrivere l'header senza controllare `add_executable` e `target_sources` rischia di spostare il problema.

Un percorso diagnostico è: leggi il nome del target nel `CMakeLists.txt`; segui l'include usato dal test; confronta firma, namespace e const qualificatori fra header e source; poi esegui il test mirato. Una modifica alla firma pubblica tocca anche ogni chiamante e amplia il rischio. Per correggere una regola di filtro, mantieni API e dati invariati e cambia solo l'implementazione responsabile.

Le assertion provano osservazioni pubbliche. Non rendere pubblico un campo privato per poterlo testare se esiste già un metodo che espone il contratto.

**Da ricordare.** Header, source, target e test devono concordare; localizza prima il livello del problema (compilazione, link o comportamento). **Per praticare:** Repository di esempio · C++; Inventario · indici e riferimenti in C++.