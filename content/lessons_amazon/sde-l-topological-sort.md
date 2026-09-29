# Topological Sort e cicli: dipendenze prima dei dipendenti

Un ordinamento topologico esiste soltanto in un grafo diretto aciclico. Con l'algoritmo di Kahn, metti in coda i nodi con indegree zero; quando ne rimuovi uno, diminuisci l'indegree dei vicini. Se alla fine hai estratto meno di `V` nodi, una parte è rimasta bloccata da un ciclo.

Con gli archi `A → C`, `B → C`, `C → D`, la coda iniziale contiene `A` e `B`. Dopo averli rimossi, `C` scende a indegree zero; soltanto dopo `C` può entrare `D`. Aggiungere anche `D → A` crea un ciclo: Kahn lascia nodi nella coda d'attesa e l'estrazione finale è incompleta.

L'ordine d'inserimento nella queue può cambiare tra soluzioni valide. Se il test confronta una risposta esatta, il requisito deve chiedere un ordine deterministico; altrimenti controlla le precedenze, non una singola sequenza arbitraria.

Per un task di corsi, rappresenta l'arco come `prerequisito → corso`. Invertire la direzione spesso supera esempi con una sola dipendenza e fallisce su catene di tre nodi.
