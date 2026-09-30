# Struttura e obiettivi dell'assessment

Un assessment online è una valutazione composta da una o più attività. La forma concreta dipende dal ruolo, dal paese e dalle istruzioni ricevute: la pagina ufficiale Amazon SDE per studenti e neolaureati invita a controllare l'email dell'assessment, che determina la struttura applicabile. Non dedurre durata, strumenti consentiti o ordine delle prove dal nome del ruolo o da un esempio trovato online.

Le attività possono misurare capacità diverse. In una domanda di coding il candidato riceve un contratto circoscritto: dato un input, deve produrre un output rispettando vincoli e casi limite. In un esercizio su repository il codice esiste già; occorre ricostruire il comportamento fra file, test e componenti prima di correggerlo. Work Style e Work Simulation presentano ancora un altro tipo di ragionamento: familiarità con affermazioni sul proprio modo di lavorare e decisioni in scenari, rispettivamente. Sapere che una di queste prove esiste non significa che sia inclusa in ogni assessment.

#### Un esempio per distinguere le attività

| Consegna ricevuta | Prima domanda da porsi | Evidenza di una risposta solida |
| --- | --- | --- |
| «Restituisci gli indici di due valori che sommano a `target`» | Che cosa significa “due” e che cosa restituire se non esistono? | La funzione rispetta il contratto anche con duplicati e input senza soluzione. |
| «Il test di `findOrder` fallisce in un progetto» | Quale test descrive il comportamento atteso e quale file produce il valore? | Una modifica circoscritta fa passare il caso senza rompere gli altri test. |
| «Scegli un'azione durante un disservizio» | Quale danno continua, quali prove mancano e chi può intervenire? | La motivazione distingue fatti, rischi e assunzioni. |

Le prime due consegne possono entrambe richiedere programmazione, ma il lavoro non è intercambiabile: la prima parte da un problema e una funzione da costruire; la seconda da un sistema e da un comportamento da rintracciare. Il terzo caso non ha una singola funzione corretta da implementare; si confrontano le conseguenze delle azioni nel contesto dato.

Le prove di pratica possono imporre timer o limitare assistenti per allenare una condizione specifica. Quel vincolo appartiene alla simulazione. Per un assessment reale si seguono le istruzioni mostrate nella piattaforma e nell'invito, comprese le regole sull'AI Assistant e sulle risorse esterne.

Per dettagli aggiornati, consulta la [pagina ufficiale Amazon sull'OA SDE](https://www.amazon.jobs/content/en/career-programs/university/sde) e poi verifica il tuo invito: le informazioni pubbliche descrivono il processo generale, non sostituiscono le istruzioni della prova assegnata.

### Esempio svolto: riconoscere che tipo di lavoro ti viene chiesto

Immagina di ricevere una di queste due richieste.

**Richiesta A — costruire una funzione.** «Dato un elenco di temperature, restituisci l'indice della prima temperatura almeno pari a 30.» Con `[18, 30, 27]`, controlli l'indice 0: `18` non basta; controlli l'indice 1: `30` soddisfa la condizione, quindi il risultato è 1. Qui il comportamento atteso viene dalla frase della consegna. Prima di scrivere codice, chiediti anche cosa restituire se nessuna temperatura raggiunge 30.

**Richiesta B — correggere un progetto.** Un test dice che `getTemperature("Milano")` dovrebbe restituire 30, ma riceve `null`. Il test dà il risultato atteso; il codice esistente mostra invece quello osservato. Il passo successivo è riprodurre il test e seguire il dato dalla route alla funzione che legge le temperature. Riscrivere una nuova ricerca prima di trovare dove il dato si perde rischia di correggere il posto sbagliato.

| Passo | Funzione nuova | Progetto esistente |
| --- | --- | --- |
| Prima fonte | Contratto scritto nella richiesta | Test, README e chiamanti |
| Prova piccola | `[18, 30, 27]` deve dare l'indice 1 | Il test nominato deve riprodurre `null` |
| Obiettivo | Implementare tutti i casi del contratto | Localizzare la causa e cambiare il punto responsabile |

Entrambi i lavori possono richiedere di programmare, ma il primo parte da una specifica e il secondo da un comportamento già presente. Durante una Work Simulation, invece, non c'è una funzione da implementare: devi motivare una decisione usando impatto, prove disponibili e persone da coinvolgere. Le istruzioni del tuo invito stabiliscono quali attività siano davvero previste.

**Da ricordare.** Prima identifica quale capacità e quale comportamento osservabile vengono richiesti; poi applica le regole della prova specifica. **Per praticare:** Simulazione completa · problema 40 + progetto 60; Errore nella rotta checkout.