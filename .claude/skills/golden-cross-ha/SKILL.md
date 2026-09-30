---
name: golden-cross-ha
description: Analizza e valuta setup di trading secondo la GOLDEN CROSS HA Strategy (Masterclass ABTG) - EMA 9/21/50, Heiken Ashi, ADX e DI+/DI-, con filtro rischio/rendimento. Usala quando l'utente chiede di valutare un grafico, uno strumento o un segnale con questa strategia, di verificare un incrocio EMA 9/21, di classificare un setup (A/B/C), di calcolare stop, target e size, di compilare la checklist pre-ingresso o post-trade, o di registrare un trade nel diario operativo. Trigger anche su "golden cross", "death cross", "tre Heiken Ashi", "setup ABTG".
---

# GOLDEN CROSS HA Strategy

> "L'incrocio delle medie non è il segnale: è solo l'inizio dell'analisi."

Strategia trend-following filtrata: l'incrocio EMA 9 / EMA 21 **attiva l'osservazione**, non l'ingresso.
Il trade diventa operativo solo quando **trend, trigger, momentum, forza e rischio** sono tutti coerenti.

| Pilastro | Ruolo |
|---|---|
| EMA 50 | Contesto: sopra solo long, sotto solo short |
| EMA 9 / EMA 21 | Trigger: incrocio rialzista o ribassista |
| Heiken Ashi | Momentum: almeno 3 candele piene, senza stoppino contrario |
| ADX | Forza del trend, filtra le fasi laterali |
| DI+ / DI- | Quale pressione direzionale prevale |
| Rischio/Rendimento | Se il segnale tecnico è anche un trade sostenibile |

Il regolamento completo (checklist, tabelle, diario) è in `references/regolamento.md`: leggilo quando
serve il dettaglio di una regola o un modulo da compilare.

## Come procedere

### 1. Raccogli i dati

Serve almeno uno di questi:
- **Dati OHLC** (CSV con colonne `date/time, open, high, low, close`, almeno ~100 barre): usa lo script
  `scripts/analyze.py` per calcolare gli indicatori e valutare le regole in modo oggettivo.
- **Valori letti dal grafico** dall'utente (EMA, ADX, DI, ATR, colore/stoppini delle ultime HA, livelli
  di supporto/resistenza): valuta tu la checklist a mano.
- **Screenshot** del grafico: leggi quello che è visibile e chiedi i valori che mancano (ADX, DI, ATR),
  invece di inventarli.

Chiedi sempre, se non noti: strumento, timeframe, prossimo supporto/resistenza utile, news ad alto impatto
imminenti, capitale e rischio % per trade (se serve la size).

```bash
python3 .claude/skills/golden-cross-ha/scripts/analyze.py dati.csv \
    [--target 18650] [--capital 10000 --risk-pct 1] [--json]
```

Lo script usa solo la libreria standard. Calcola EMA 9/21/50, Heiken Ashi, ADX/DI+/DI- (Wilder, 14) e
ATR (14) e valuta l'ultima barra chiusa. Le regole qualitative del documento sono tradotte in soglie
numeriche (vedi `--help` e la sezione "Soglie" di `references/regolamento.md`): trattale come un
**primo filtro**, non come verdetto finale. Spazio tecnico verso S/R, news, liquidità e stato
emotivo restano giudizi da verificare con l'utente.

### 2. Valuta le 6 fasi in sequenza

Ogni fase deve essere superata prima della successiva. Se una fallisce, fermati e spiega perché.

| Fase | Domanda | Condizione |
|---|---|---|
| 1. Contesto | Prezzo coerente con EMA 50? | Long solo sopra EMA 50 (non ribassista); short solo sotto (non rialzista) |
| 2. Trigger | EMA 9 incrocia EMA 21? | Incrocio recente nella direzione del trade |
| 3. Allineamento | Medie ordinate e inclinate? | Long: Prezzo > EMA 9 > EMA 21 > EMA 50, inclinate su. Short: l'opposto |
| 4. Momentum | Le HA confermano? | ≥ 3 HA consecutive nella direzione, senza stoppino contrario significativo, corpo stabile o crescente |
| 5. Forza | ADX conferma? | ADX > 20 (meglio > 25), crescente o stabile; DI+ > DI- (long) o DI- > DI+ (short) |
| 6. Tradeability | R:R accettabile? | Stop tecnico, spazio fino al target, R:R ≥ 1:1 (meglio 1:1,5 o 1:2) |

**Lettura ADX:** < 15 no trade · 15-20 incerto (solo setup molto pulito, meglio attendere) ·
> 20 operativo · > 25 preferibile · > 35/40 attenzione a non inseguire un movimento esteso.

### 3. Controlla le regole di non ingresso

Anche con le 6 fasi superate, **nessun ingresso** se vale una di queste:
EMA intrecciate · EMA 50 piatta attraversata ripetutamente · incrocio dentro congestione ·
ADX < 15 · ADX 15-20 senza forte conferma · DI non coerenti · HA che alternano colore ·
corpi HA in riduzione · stoppino contrario significativo · prezzo troppo lontano da EMA 21 ·
movimento già su S/R · R:R < 1:1 · stop tecnico troppo ampio · news ad alto impatto imminenti ·
mercato illiquido · trader emotivamente alterato o in cerca di recupero.

### 4. Scegli la modalità di ingresso

- **Distanza dalle medie** (ATR 14): preferibile entro 0,5 ATR da EMA 9; accettabile entro 1 ATR da
  EMA 21; oltre 1 ATR da EMA 21 = ingresso tardivo.
- **Ingresso diretto**: alla chiusura della terza HA valida, se il prezzo è ancora vicino a EMA 9/21.
- **Ingresso su pullback**: se il prezzo è lontano o la terza HA è molto ampia, attendi il ritorno verso
  EMA 9 o EMA 21. Se il pullback non arriva, **il trade non si forza**.

### 5. Definisci stop, target e size, prima dell'ingresso

- **Stop long**: sotto l'ultimo minimo significativo, sotto EMA 21, sotto la candela di conferma o a
  distanza ATR. **Short**: specularmente sopra. Lo stop va dove il setup perde validità, non dove "fa
  comodo" alla size.
- **Target**: minimo 1R, preferibile 1,5R, ideale 2R, verificato contro il primo S/R, pivot, area di
  volume o estensione. Se il livello tecnico è più vicino di 1R → no trade.
- **Size** = (capitale × rischio %) / distanza stop. Rischio: demo 0,5% · ordinario 1% · Setup A con
  storico consolidato max 1,5% · mai oltre 2%.
- **Limiti giornalieri**: max 2 trade per strumento, max 3 totali, stop dopo 2 perdite consecutive,
  stop giornaliero a -2R/-3R, mai aumentare la size dopo una perdita.

### 6. Classifica il setup

- **A**: EMA ordinate, trend chiaro, 3 HA forti, ADX > 25, DI coerenti, spazio tecnico, R:R ≥ 1:1,5 → preferibile.
- **B**: condizioni principali rispettate, ADX > 20, R:R ≥ 1:1, qualche imperfezione ma nessuna
  invalidazione forte → tradabile con prudenza.
- **C**: EMA piatte/intrecciate, ADX debole, HA poco convincenti, prezzo lontano o target vicino → da scartare.

## Gestione e uscita (posizione aperta)

- A **1R**: valuta stop a pareggio, parziale o protezione dietro EMA 21.
- In trend forte mantieni finché HA, ADX e medie restano coerenti.
- **Uscita long**: TP raggiunto, chiusura sotto EMA 21, EMA 9 sotto EMA 21, cambio colore HA,
  resistenza importante; valuta anche calo marcato di ADX o forte stoppino superiore.
- **Uscita short**: specularmente (chiusura sopra EMA 21, EMA 9 sopra EMA 21, cambio colore HA,
  supporto importante, calo ADX, forte stoppino inferiore).
- La posizione non si difende per orgoglio: la gestione segue il setup, non l'aspettativa.

## Formato della risposta

Per una valutazione di setup rispondi con questa struttura:

```
Strumento / TF: <...>        Direzione valutata: LONG | SHORT | nessuna
Verdetto: OPERATIVO (Setup A|B) | ATTENDERE PULLBACK | NO TRADE (Setup C)

Fasi
1. Contesto       ✅/❌  <valori e motivo>
2. Trigger        ✅/❌
3. Allineamento   ✅/❌
4. Momentum HA    ✅/❌
5. Forza ADX/DI   ✅/❌
6. Tradeability   ✅/❌/❓ (se mancano dati)

Regole di non ingresso violate: <elenco o "nessuna">
Da verificare manualmente: <S/R, news, liquidità, ...>

Piano (solo se operativo)
Ingresso: diretto a <..> | pullback verso EMA 9/21 (<..>)
Stop: <..> (<motivazione tecnica>)   Target: <..> (R:R <..>)
Size: <..> (rischio <..>% = <..>)
Gestione: <regola a 1R, condizioni di uscita>
```

Sii esplicito quando un dato manca: segna ❓ e chiedilo, non assumere un valore favorevole.
Per checklist post-trade e diario operativo usa i moduli in `references/regolamento.md`.

## Principi da rispettare sempre

- Non operiamo l'incrocio: operiamo la conferma del momentum dopo l'incrocio.
- Non rincorro il prezzo, non anticipo il segnale, non forzo il trade.
- La strategia è robusta soprattutto grazie ai trade che decide di non fare: un "NO TRADE" motivato è
  una risposta corretta e utile.
- Chiudi ogni valutazione ricordando che il contenuto è didattico, non è consulenza finanziaria, e che la
  strategia va testata su storico, demo e forward test prima di usare capitale reale.
