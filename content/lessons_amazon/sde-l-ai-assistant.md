# Usare l'AI Assistant come supporto al debugging

Le funzioni dell'assistente HackerRank dipendono dal tipo di domanda e dalla configurazione dell'assessment. La documentazione Candidate Support descrive modalità Guarded e Unguarded; alcune viste consentono domande sui file, altre anche agenti che modificano il progetto. Prima di usarlo, leggi l'interfaccia e le istruzioni dell'invito.

Una domanda buona restringe il problema senza chiedere la soluzione intera: «Spiegami il flusso da questa route al service senza modificare il codice». Puoi aggiungere `@README.md` per dare contesto: «Quale requisito qui descrive il comportamento atteso?». Se il test mostra expected X e actual Y, chiedi quali componenti collegano input e output.

Il giudizio sul fix resta indipendente dall'assistente: il processo comprende lettura del requisito, esame dei file, esecuzione dei test, formulazione di un'ipotesi, richiesta di chiarimenti circoscritti, valutazione della risposta e verifica del cambiamento minimo. Una spiegazione convincente non costituisce una prova; lo sono i test e il contratto del repository.
