# Binary Search classica: dimezzare uno spazio ordinato

La ricerca binaria è corta solo dopo avere stabilito l'invariante. Con l'intervallo chiuso `[left, right]`, calcola il medio e conserva la metà che può ancora contenere il valore. Quando `left > right`, non è rimasto alcun candidato.

Su `[1, 3, 5, 8, 12]`, la ricerca di `8` inizia dal valore medio `5`: i tre valori a sinistra vengono esclusi e resta `[8, 12]`. Il nuovo valore medio è `8`, che individua l'indice cercato. A ogni confronto si elimina metà dei candidati; l'ordinamento dell'array rende valido questo taglio.

In C++ scrivere `left + (right - left) / 2` evita l'overflow della somma quando i bordi sono grandi. Con `vector::size()` fai attenzione ai tipi unsigned e al caso vuoto. In Python gli interi non traboccano, ma l'off-by-one resta.

L'array ordinato non è un dettaglio decorativo: la decisione «vai a sinistra» scarta elementi perché sai come sono ordinati. Se manca l'ordine, cerca una proprietà monotona diversa o usa un'altra struttura.
