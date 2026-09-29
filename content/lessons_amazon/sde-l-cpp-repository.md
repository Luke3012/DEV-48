# Repository C++: header, source, classi e test

Un header dichiara quali nomi e tipi sono disponibili; un file `.cpp` contiene spesso l'implementazione. Se il compilatore dice “undefined reference”, la dichiarazione può esistere ma la definizione non entra nel link. Se segnala un tipo sconosciuto, controlla gli include prima di riscrivere la funzione.

Con CMake individua il target compilato e i file che lo compongono. Parti dall'errore più vicino al tuo codice e leggi il numero di riga del progetto. Una modifica a una firma in header deve restare coerente con source e chiamanti.

Un'asserzione `EXPECT_EQ(expected, actual)` confronta valori; per una classe, chiediti se il contratto è osservabile tramite metodo pubblico. Un test che passa non giustifica una modifica ampia all'API. Mantieni lo stato privato e correggi la regola che produce il valore errato.
