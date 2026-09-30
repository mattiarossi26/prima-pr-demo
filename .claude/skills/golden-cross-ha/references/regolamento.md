# GOLDEN CROSS HA Strategy - Regolamento completo

Fonte: "MASTERCLASS ABTG - GOLDEN CROSS HA Strategy", documento didattico-operativo v1.0 (1 luglio 2026).
Uso formativo: non è consulenza finanziaria.

## Indice
1. Ruoli degli indicatori
2. Timeframe, mercati e sessioni
3. Setup Long (15 condizioni)
4. Setup Short (15 condizioni)
5. Regola delle tre Heiken Ashi
6. Filtro ADX e DI
7. Ingresso e distanza dalle medie
8. Stop, target, gestione, uscita
9. Regole di non ingresso
10. Classificazione A/B/C
11. Money management
12. Checklist pre-ingresso
13. Checklist post-trade
14. Diario operativo
15. Soglie numeriche usate dallo script
16. Glossario

## 1. Ruoli degli indicatori

- **EMA 9** (veloce): trigger dinamico, riferimento per l'ingresso su pullback, misura l'accelerazione.
- **EMA 21** (intermedia): conferma del trigger, supporto/resistenza dinamica, riferimento per stop o trailing.
- **EMA 50** (filtro direzionale): sopra → long; sotto → short; prezzo che la attraversa continuamente → no trade o massima prudenza.
- **Heiken Ashi**: filtro di conferma, non segnale isolato. Continuità direzionale, perdita/rafforzamento del momentum, gestione dell'uscita.
- **ADX**: forza, non direzione. < 15 debole (evitare), 15-20 incerto, > 20 operativo, > 25 trend forte.
- **DI+ / DI-**: DI+ > DI- pressione rialzista; DI- > DI+ pressione ribassista.

## 2. Timeframe, mercati e sessioni

| Operatività | Timeframe | Nota |
|---|---|---|
| Intraday veloce | M5 / M15 | Più segnali, più rumore: selezione severa |
| Intraday ordinaria | M15 / M30 | Compromesso tra reattività e pulizia |
| Swing | H1 / H4 | Meno segnali, generalmente più puliti |

Strumenti adatti: liquidi e direzionali (DAX, Nasdaq, S&P 500, Dow Jones, major Forex, oro, petrolio, indici maggiori).
Da evitare: spread elevato, bassa liquidità, comportamento erratico.

| Mercato | Fasce operative |
|---|---|
| Indici europei | Apertura europea, prima parte della mattina, ripartenze direzionali, apertura USA |
| Indici americani | Pre-market operativo, apertura Wall Street, prima parte della sessione USA |
| Forex | Sessione europea, sovrapposizione Europa/USA, prime ore americane |
| Da evitare | Mercato lento, fine sessione, pre-news ad alto impatto, congestioni strette |

## 3. Setup Long

Configurazione ideale: **Prezzo > EMA 9 > EMA 21 > EMA 50**, medie inclinate verso l'alto, tre HA rialziste senza stoppino inferiore, **ADX > 25 e DI+ > DI-**.

1. Il prezzo è sopra la EMA 50.
2. La EMA 50 è inclinata verso l'alto o almeno non ribassista.
3. EMA 9 incrocia sopra EMA 21.
4. EMA 9 ed EMA 21 sono inclinate verso l'alto.
5. Le medie sono ordinate o in chiaro processo di allineamento rialzista.
6. Almeno tre candele Heiken Ashi rialziste consecutive.
7. Le HA non presentano stoppino inferiore significativo.
8. Il corpo delle HA è stabile o crescente.
9. ADX > 20, preferibilmente > 25.
10. ADX crescente o almeno stabile.
11. DI+ > DI-.
12. Il prezzo non è eccessivamente distante da EMA 9 o EMA 21.
13. C'è spazio tecnico fino alla prima resistenza utile.
14. Lo stop loss è posizionabile in modo tecnico.
15. R:R almeno 1:1, preferibilmente 1:1,5 o 1:2.

## 4. Setup Short

Configurazione ideale: **Prezzo < EMA 9 < EMA 21 < EMA 50**, medie inclinate verso il basso, tre HA ribassiste senza stoppino superiore, **ADX > 25 e DI- > DI+**.

1. Il prezzo è sotto la EMA 50.
2. La EMA 50 è inclinata verso il basso o almeno non rialzista.
3. EMA 9 incrocia sotto EMA 21.
4. EMA 9 ed EMA 21 sono inclinate verso il basso.
5. Le medie sono ordinate o in chiaro processo di allineamento ribassista.
6. Almeno tre candele Heiken Ashi ribassiste consecutive.
7. Le HA non presentano stoppino superiore significativo.
8. Il corpo delle HA è stabile o crescente.
9. ADX > 20, preferibilmente > 25.
10. ADX crescente o almeno stabile.
11. DI- > DI+.
12. Il prezzo non è eccessivamente distante da EMA 9 o EMA 21.
13. C'è spazio tecnico fino al primo supporto utile.
14. Lo stop loss è posizionabile in modo tecnico.
15. R:R almeno 1:1, preferibilmente 1:1,5 o 1:2.

## 5. Regola delle tre Heiken Ashi

| Direzione | Condizione richiesta | Da scartare |
|---|---|---|
| Long | 3 HA rialziste consecutive, senza stoppino inferiore significativo, corpo stabile o crescente | Corpi in riduzione, stoppini inferiori evidenti, alternanza di colore |
| Short | 3 HA ribassiste consecutive, senza stoppino superiore significativo, corpo stabile o crescente | Corpi in riduzione, stoppini superiori evidenti, alternanza di colore |

Se la terza HA conferma ma chiude troppo lontano dalle medie, il setup può essere corretto ma l'ingresso è tardivo: si attende il pullback.

## 6. Filtro ADX e DI

| ADX | Interpretazione | Decisione |
|---|---|---|
| < 15 | Debole o laterale | No trade |
| 15-20 | Forza incerta | Solo setup molto pulito, preferibile attendere |
| > 20 | Trend operativo | Setup valutabile |
| > 25 | Trend forte | Condizione preferibile |
| > 35/40 | Trend molto forte | Attenzione a non inseguire un movimento esteso |

Long: ADX > 20/25, crescente o stabile, DI+ sopra DI-. Short: ADX > 20/25, crescente o stabile, DI- sopra DI+.

## 7. Ingresso e distanza dalle medie

| Modalità | Quando | Rischio principale |
|---|---|---|
| Diretto | Alla chiusura della terza HA valida, prezzo ancora vicino a EMA 9/21 | Pullback immediato dopo l'ingresso |
| Su pullback | Dopo setup valido, attendendo il ritorno verso EMA 9 o EMA 21 | Il mercato può non tornare e il trade si perde |

Regola ABTG: prezzo vicino alle medie → posso entrare sulla conferma; lontano → attendo il pullback; se il pullback non arriva, il trade non si forza.

- Ingresso preferibile entro **0,5 ATR da EMA 9**.
- Ingresso accettabile entro **1 ATR da EMA 21**.
- Oltre 1 ATR da EMA 21 → segnale tardivo.
- Terza HA molto ampia → valutare attesa del pullback.

## 8. Stop, target, gestione, uscita

**Stop** (definito prima dell'ingresso, dove il setup perde validità, non dove fa comodo per la size):
- Long: sotto ultimo minimo significativo, sotto EMA 21, sotto candela di conferma o distanza tecnica ATR.
- Short: sopra ultimo massimo significativo, sopra EMA 21, sopra candela di conferma o distanza tecnica ATR.

**Target** (definito prima dell'ingresso): minimo 1:1, preferibile 1:1,5, ideale 1:2. Riferimenti tecnici: supporti, resistenze, massimi/minimi relativi, pivot, aree di volume, estensioni.

**Gestione dinamica**:
- A 1R valutare stop a pareggio, parziale o protezione dietro EMA 21.
- In trend forte mantenere finché HA, ADX e medie restano coerenti.
- In perdita di momentum valutare uscita parziale o totale.

**Uscita**:

| Scenario | Uscita tecnica | Note |
|---|---|---|
| Long | TP raggiunto, chiusura sotto EMA 21, EMA 9 sotto EMA 21, cambio colore HA, resistenza importante | Valutare calo marcato di ADX o forte stoppino superiore |
| Short | TP raggiunto, chiusura sopra EMA 21, EMA 9 sopra EMA 21, cambio colore HA, supporto importante | Valutare calo marcato di ADX o forte stoppino inferiore |

Regola di protezione: quando il mercato smette di mostrare continuità, la posizione non si difende per orgoglio.

## 9. Regole di non ingresso

1. EMA 9, EMA 21 ed EMA 50 intrecciate.
2. EMA 50 piatta e prezzo che la attraversa ripetutamente.
3. Incrocio dentro una congestione.
4. ADX sotto 15.
5. ADX tra 15 e 20 senza forte conferma tecnica.
6. DI+ e DI- non confermano la direzione.
7. Le HA alternano colore.
8. Le tre HA hanno corpo in riduzione.
9. Stoppino contrario significativo.
10. Prezzo troppo distante da EMA 21.
11. Movimento già arrivato su supporto o resistenza.
12. R:R inferiore a 1:1.
13. Stop tecnico troppo ampio.
14. News ad alto impatto imminenti.
15. Mercato privo di liquidità.
16. Trader emotivamente alterato o in cerca di recupero di una perdita.

## 10. Classificazione del setup

| Classe | Caratteristiche | Decisione |
|---|---|---|
| A | EMA ordinate, trend chiaro, 3 HA forti, ADX > 25, DI coerenti, spazio tecnico, R:R ≥ 1:1,5 | Preferibile |
| B | Condizioni principali rispettate, ADX > 20, R:R ≥ 1:1, qualche imperfezione ma nessuna invalidazione forte | Tradabile con prudenza |
| C | EMA piatte o intrecciate, ADX debole, HA poco convincenti, prezzo lontano o target vicino | Da scartare |

## 11. Money management

| Fase | Rischio per trade | Nota |
|---|---|---|
| Test / Demo | 0,5% | Verificare esecuzione e disciplina |
| Ordinaria | 1% | Gestione continuativa |
| Setup A qualificato | max 1,5% | Solo con storico e disciplina consolidati |
| Limite massimo | mai oltre 2% | Salvo esperienza elevata e piano validato |

- Max 2 trade al giorno sullo stesso strumento; max 3 trade complessivi al giorno.
- Stop operativo dopo 2 perdite consecutive; stop giornaliero consigliato a -2R o -3R.
- Non aumentare la size dopo una perdita. La size dipende dal rischio tecnico, non dalla convinzione.
- Size = (capitale × rischio %) / distanza stop (in unità di prezzo × valore per punto).

## 12. Checklist pre-ingresso

| # | Controllo | Esito |
|---|---|---|
| 1 | Il prezzo è coerente con EMA 50? | ☐ Sì ☐ No |
| 2 | La EMA 50 è coerente con la direzione del trade? | ☐ Sì ☐ No |
| 3 | EMA 9 ha incrociato EMA 21? | ☐ Sì ☐ No |
| 4 | EMA 9 ed EMA 21 sono inclinate nella direzione corretta? | ☐ Sì ☐ No |
| 5 | Le medie sono ordinate o si stanno allineando? | ☐ Sì ☐ No |
| 6 | Almeno tre HA consecutive nella direzione del trade? | ☐ Sì ☐ No |
| 7 | HA senza stoppino contrario significativo? | ☐ Sì ☐ No |
| 8 | Corpo delle HA stabile o crescente? | ☐ Sì ☐ No |
| 9 | ADX sopra 20, meglio sopra 25? | ☐ Sì ☐ No |
| 10 | DI+ e DI- confermano la direzione? | ☐ Sì ☐ No |
| 11 | Prezzo vicino a EMA 9 o EMA 21? | ☐ Sì ☐ No |
| 12 | Spazio tecnico fino al primo target? | ☐ Sì ☐ No |
| 13 | Stop loss tecnico e sostenibile? | ☐ Sì ☐ No |
| 14 | R:R almeno 1:1? | ☐ Sì ☐ No |
| 15 | Nessuna news imminente o forte rischio evento? | ☐ Sì ☐ No |
| 16 | Sto entrando per regola e non per impulso? | ☐ Sì ☐ No |

## 13. Checklist post-trade

| # | Controllo |
|---|---|
| 1 | Ho rispettato tutte le condizioni di ingresso? |
| 2 | Lo stop era tecnico o adattato alla size? |
| 3 | Il target era realistico? |
| 4 | Ho gestito la posizione secondo piano? |
| 5 | Ho anticipato o rincorso il prezzo? |
| 6 | Ho rispettato il limite di rischio giornaliero? |
| 7 | Il trade era Setup A, B o C? |
| 8 | Quale errore devo evitare nel prossimo trade? |

## 14. Diario operativo

Ogni operazione va registrata: serve a verificare disciplina, qualità del setup e ripetibilità, non solo P&L.

| Categoria | Dati da registrare | Obiettivo |
|---|---|---|
| Identificazione | Data, strumento, timeframe, direzione, orario di ingresso | Contestualizzare il trade |
| Setup | EMA 50, incrocio EMA 9/21, qualità HA, ADX, DI+ / DI- | Misurare coerenza tecnica |
| Rischio | Prezzo ingresso, stop, target, size, rischio %, R:R | Verificare sostenibilità |
| Gestione | Parziali, stop a pareggio, trailing, motivazione uscita | Valutare disciplina esecutiva |
| Revisione | Screenshot, risultato in R, errore, nota psicologica, classe setup | Miglioramento continuo |

Modello di riga (CSV):

```
data,strumento,tf,direzione,ora_ingresso,ema50,incrocio,qualita_ha,adx,di_plus,di_minus,ingresso,stop,target,size,rischio_pct,rr,parziali,uscita_motivo,risultato_R,classe,errore,nota_psicologica
```

## 15. Soglie numeriche usate dallo script

Il documento esprime alcune regole in modo qualitativo. `scripts/analyze.py` le traduce così
(tutte modificabili da riga di comando):

| Regola qualitativa | Traduzione | Opzione |
|---|---|---|
| Media "inclinata" | EMA oggi vs EMA di N barre fa (N=3) | `--slope-bars` |
| EMA 50 "piatta" | variazione su N barre < 0,1 ATR | - |
| Incrocio "recente" | entro le ultime 10 barre | `--cross-lookback` |
| Stoppino contrario "significativo" | > 15% del range della HA | `--wick-pct` |
| Corpo "stabile o crescente" | ogni corpo ≥ 85% del precedente | `--body-ratio` |
| ADX "crescente o stabile" | ADX ≥ 97% del valore di N barre fa | - |
| Prezzo che "attraversa ripetutamente" EMA 50 | ≥ 3 attraversamenti nelle ultime 20 barre | - |
| "Ultimo minimo/massimo significativo" | ultimo frattale a 2 barre nelle ultime 20 (altrimenti min/max della finestra) | `--swing-bars` |
| Stop di default | ultimo minimo/massimo significativo ± 0,1 ATR | `--stop` |
| Stop "troppo ampio" | oltre 2 ATR | - |
| Terza HA "molto ampia" | corpo > 1 ATR | - |

## 16. Glossario

- **EMA**: media mobile esponenziale, più sensibile ai prezzi recenti.
- **Golden Cross operativo**: EMA 9 sopra EMA 21, validato dai filtri.
- **Death Cross operativo**: EMA 9 sotto EMA 21, validato dai filtri.
- **Heiken Ashi**: candele mediate che mostrano la continuità del movimento filtrando il rumore.
  HA_close = (O+H+L+C)/4; HA_open = (HA_open prec + HA_close prec)/2; HA_high = max(H, HA_open, HA_close); HA_low = min(L, HA_open, HA_close).
- **ADX**: forza del trend, non direzione.
- **DI+ / DI-**: componenti direzionali dell'ADX.
- **ATR**: volatilità; misura distanza, stop eccessivi, ingresso tardivo.
- **R**: unità di rischio. Se rischio 100 €, +1R = +100 €.
