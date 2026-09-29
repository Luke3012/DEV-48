# Monotonic Stack: conservare candidati ancora utili

Per ogni giorno, vuoi sapere il prossimo giorno più caldo. Il doppio ciclo visita tutte le coppie. Uno stack monotono conserva gli indici ancora in attesa: quando arriva una temperatura più alta, risolve i giorni più freddi in cima. Gli indici che restano non hanno ancora trovato risposta.

Ogni indice entra una volta ed esce una volta, quindi il lavoro totale è `O(n)` anche se un singolo elemento può attivare più pop. È un caso in cui “niente cicli annidati” non è la prova della complessità: conta quante volte ogni elemento attraversa lo stack.

Prima di partire, decidi se vuoi il successivo strettamente maggiore o maggiore/uguale. Cambia la condizione di pop. Se il testo chiede distanza, salva gli indici; se vuole solo il valore, può bastare salvare i valori.
