# Work Simulation: scegliere un'azione e spiegare il compromesso

Ogni scenario propone azioni che potrebbero sembrare ragionevoli a prima vista. Prima di ordinarle, chiediti quale informazione manca, quale danno potrebbe continuare mentre indaghi e chi deve sapere cosa. A volte la risposta forte unisce una misura immediata reversibile e una verifica più profonda.

Ordina le opzioni dalla più alla meno efficace; una classifica formativa confronta i rischi descritti, non pretende di conoscere una chiave ufficiale Amazon. Il debrief spiega quale rischio ogni scelta riduce e quale lascia aperto. Se la tua classifica differisce, cerca l'assunzione diversa: gravità, tempo, autorità, impatto o qualità dei dati.

Gli scenari sono originali e ispirati a decisioni quotidiane SDE: release, incidenti, review, requisiti incompleti, colleghi, test instabili, rollback e debito tecnico. Non sono domande reali né materiali riservati.

### Confrontare azioni plausibili

Scenario di esempio: dopo un rilascio, un webhook consegna alcuni eventi duplicati. Un rollback immediato può fermare i duplicati ma annullare anche una correzione indipendente; esaminare due payload identici può isolare la causa ma lascia aperto l'impatto; disattivare temporaneamente soltanto il consumer coinvolto può contenere il danno, ma richiede sapere come recuperare gli eventi sospesi. La scelta dipende da volume, reversibilità, dati persi e responsabilità disponibili.

Per ogni opzione chiediti: quale effetto immediato produce, quale informazione raccoglie, che rischio crea e chi deve essere coinvolto? Un'azione può essere utile dopo una mitigazione anche se non è la prima mossa. Esplicita le assunzioni che potrebbero cambiare l'ordine.

Le classifiche e i debrief di questo materiale sono giudizi formativi sulle conseguenze descritte, non chiavi ufficiali Amazon. Se una scelta diversa presuppone gravità o vincoli differenti, nomina quel dato invece di cercare una lettera da memorizzare.

**Da ricordare.** Valuta prima l'impatto che continua, poi reversibilità, qualità delle prove e coordinamento; il contesto può cambiare l'ordine delle azioni. **Per praticare:** Errore nella rotta checkout; Rollback o patch.