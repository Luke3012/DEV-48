# Usare l'AI Assistant come supporto al debugging

Le funzioni dell'assistente HackerRank dipendono dal tipo di domanda e dalla configurazione dell'assessment. La documentazione Candidate Support descrive modalità Guarded e Unguarded; alcune viste consentono domande sui file, altre anche agenti che modificano il progetto. Prima di usarlo, leggi l'interfaccia e le istruzioni dell'invito.

Una domanda buona restringe il problema senza chiedere la soluzione intera: «Spiegami il flusso da questa route al service senza modificare il codice». Puoi aggiungere `@README.md` per dare contesto: «Quale requisito qui descrive il comportamento atteso?». Se il test mostra expected X e actual Y, chiedi quali componenti collegano input e output.

Il giudizio sul fix resta indipendente dall'assistente: il processo comprende lettura del requisito, esame dei file, esecuzione dei test, formulazione di un'ipotesi, richiesta di chiarimenti circoscritti, valutazione della risposta e verifica del cambiamento minimo. Una spiegazione convincente non costituisce una prova; lo sono i test e il contratto del repository.

### Chiedere un aiuto che si possa controllare

Prima di usare un assistente, verifica se è abilitato e quali modalità mostra l'interfaccia: HackerRank descrive modalità Guarded e Unguarded, ma il test setter configura le funzioni disponibili. Per esempio, con un test che riceve una Promise invece di un array, una domanda circoscritta è: «Indica il percorso fra questa route e il service e spiega quale valore viene restituito in ciascun punto; non modificare file». La risposta propone una pista, non dimostra che la causa sia quella.

Controlla la pista leggendo i file e rilanciando il test. Se l'assistente suggerisce `await`, verifica se il chiamante e il service condividono davvero il contratto asincrono; applicare una modifica senza capirla può spostare l'errore. Le indicazioni HackerRank attuali dicono che le interazioni sono visibili al valutatore e che l'assistente non è presente in ogni prova; seguono comunque le istruzioni specifiche del test. Consulta la [guida ufficiale sull'AI Assistant in tests](https://candidatesupport.hackerrank.com/articles/7634558376-ai-assistant-in-tests) perché interfaccia e capacità possono cambiare.

**Da ricordare.** Chiedi contesto o un piano verificabile, poi giudica la risposta con codice, contratto e test indipendenti. **Per praticare:** Repository asincrona · Promise e controller; Debugging di un progetto · stato delle spedizioni.