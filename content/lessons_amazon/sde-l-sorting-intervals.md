# Sorting e intervalli: ordinare per scoprire sovrapposizioni

Se ordini gli intervalli per inizio, quando leggi il prossimo sai che nessun intervallo futuro inizierà prima. Puoi quindi confrontarlo con il risultato appena costruito: se si sovrappone, estendi la fine; altrimenti aggiungi un nuovo intervallo. Il costo è dominato dall'ordinamento, `O(n log n)`.

Il dettaglio che decide i test è il confine: `[1, 3]` e `[3, 5]` si toccano. Il requisito può considerarli sovrapposti (`start <= end`) o separati (`start < end`). Non scegliere una delle due convenzioni senza leggerla nell'enunciato.

Un comparatore C++ deve definire un ordinamento coerente; Python `sort(key=...)` spesso basta. L'ordinamento muta l'input: se il contratto vieta la mutation, copia prima oppure costruisci una sequenza ordinata nuova.
