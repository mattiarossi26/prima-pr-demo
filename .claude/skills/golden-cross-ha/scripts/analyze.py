#!/usr/bin/env python3
"""Valuta l'ultima barra di una serie OHLC secondo la GOLDEN CROSS HA Strategy.

Calcola EMA 9/21/50, Heiken Ashi, ADX/DI+/DI- e ATR (Wilder, 14) e controlla le
6 fasi del metodo (contesto, trigger, allineamento, momentum, forza, tradeability)
più le regole di non ingresso verificabili dai prezzi. Usa solo la libreria standard.

Esempio:
    python3 analyze.py dax_m15.csv --target 18650 --capital 10000 --risk-pct 1
"""

import argparse
import csv
import json
import sys

PASS, WARN, FAIL, MANUAL = "pass", "warn", "fail", "manual"
ICON = {PASS: "✅", WARN: "⚠️ ", FAIL: "❌", MANUAL: "❓"}


# ---------------------------------------------------------------- dati

def load_ohlc(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        sample = f.read(4096)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        except csv.Error:
            dialect = csv.excel
        reader = csv.DictReader(f, dialect=dialect)
        cols = {c.strip().lower(): c for c in reader.fieldnames or []}
        missing = [c for c in ("open", "high", "low", "close") if c not in cols]
        if missing:
            sys.exit(f"Colonne mancanti nel CSV: {', '.join(missing)} (trovate: {list(cols)})")
        time_col = next((cols[c] for c in ("datetime", "date", "time", "timestamp") if c in cols), None)
        rows = []
        for r in reader:
            try:
                o, h, l, c = (float(r[cols[k]].replace(",", ".")) for k in ("open", "high", "low", "close"))
            except (ValueError, AttributeError):
                continue
            rows.append({"t": r[time_col] if time_col else str(len(rows)), "o": o, "h": h, "l": l, "c": c})
    return rows


# ---------------------------------------------------------- indicatori

def ema(values, n):
    out = [None] * len(values)
    if len(values) < n:
        return out
    out[n - 1] = sum(values[:n]) / n
    k = 2 / (n + 1)
    for i in range(n, len(values)):
        out[i] = values[i] * k + out[i - 1] * (1 - k)
    return out


def wilder(values, n):
    """Smoothing di Wilder su una serie che parte dall'indice 1."""
    out = [None] * len(values)
    if len(values) <= n:
        return out
    out[n] = sum(values[1:n + 1]) / n
    for i in range(n + 1, len(values)):
        out[i] = (out[i - 1] * (n - 1) + values[i]) / n
    return out


def adx_atr(rows, n=14):
    size = len(rows)
    tr, pdm, mdm = [0.0] * size, [0.0] * size, [0.0] * size
    for i in range(1, size):
        h, l, pc = rows[i]["h"], rows[i]["l"], rows[i - 1]["c"]
        tr[i] = max(h - l, abs(h - pc), abs(l - pc))
        up, down = h - rows[i - 1]["h"], rows[i - 1]["l"] - l
        pdm[i] = up if up > down and up > 0 else 0.0
        mdm[i] = down if down > up and down > 0 else 0.0
    atr, spdm, smdm = wilder(tr, n), wilder(pdm, n), wilder(mdm, n)
    dip, dim, dx = [None] * size, [None] * size, [None] * size
    for i in range(size):
        if atr[i]:
            dip[i] = 100 * spdm[i] / atr[i]
            dim[i] = 100 * smdm[i] / atr[i]
            s = dip[i] + dim[i]
            dx[i] = 100 * abs(dip[i] - dim[i]) / s if s else 0.0
    adx = [None] * size
    first = next((i for i, v in enumerate(dx) if v is not None), None)
    if first is not None and size >= first + n:
        adx[first + n - 1] = sum(dx[first:first + n]) / n
        for i in range(first + n, size):
            adx[i] = (adx[i - 1] * (n - 1) + dx[i]) / n
    return atr, adx, dip, dim


def heiken_ashi(rows):
    ha = []
    for i, r in enumerate(rows):
        c = (r["o"] + r["h"] + r["l"] + r["c"]) / 4
        o = (r["o"] + r["c"]) / 2 if i == 0 else (ha[-1]["o"] + ha[-1]["c"]) / 2
        ha.append({"o": o, "c": c, "h": max(r["h"], o, c), "l": min(r["l"], o, c)})
    return ha


# ------------------------------------------------------------- analisi

def fmt(x, d=2):
    return "n/d" if x is None else f"{x:.{d}f}"


def last_pivot(rows, i, side, lookback):
    """Ultimo minimo (long) o massimo (short) significativo: frattale a 2 barre per lato.

    Se nelle ultime `lookback` barre non c'è un frattale, usa l'estremo della finestra.
    """
    key = "l" if side > 0 else "h"
    better = (lambda x, y: x < y) if side > 0 else (lambda x, y: x > y)
    for j in range(i - 2, i - lookback, -1):
        v = rows[j][key]
        if all(better(v, rows[k][key]) for k in (j - 2, j - 1, j + 1, j + 2)):
            return v
    window = [r[key] for r in rows[i - lookback + 1:i + 1]]
    return min(window) if side > 0 else max(window)


def analyze(rows, a):
    if len(rows) < 60:
        sys.exit(f"Servono almeno 60 barre (meglio 100+), trovate {len(rows)}.")
    closes = [r["c"] for r in rows]
    e9, e21, e50 = ema(closes, 9), ema(closes, 21), ema(closes, 50)
    atr, adx, dip, dim = adx_atr(rows)
    ha = heiken_ashi(rows)
    i = len(rows) - 1
    s = a.slope_bars
    last = rows[i]
    close, A = last["c"], atr[i]
    if None in (e50[i], e50[i - s], adx[i], adx[i - s], A):
        sys.exit("Storico insufficiente per calcolare EMA 50 / ADX: servono più barre.")

    slope = {k: (v[i] - v[i - s]) for k, v in (("ema9", e9), ("ema21", e21), ("ema50", e50))}
    flat = 0.1 * A  # EMA 50 "piatta": variazione su s barre inferiore a 0,1 ATR

    if close > e50[i]:
        side = 1
    elif close < e50[i]:
        side = -1
    else:
        side = 0
    name = {1: "LONG", -1: "SHORT", 0: "nessuna"}[side]

    checks = []

    def add(phase, label, status, detail):
        checks.append({"fase": phase, "controllo": label, "esito": status, "dettaglio": detail})

    # Fase 1 - Contesto
    ctx_ok = side != 0
    add(1, "Prezzo coerente con EMA 50", PASS if ctx_ok else FAIL,
        f"close {fmt(close)} vs EMA50 {fmt(e50[i])}")
    ema50_ok = side != 0 and slope["ema50"] * side >= -flat
    add(1, "EMA 50 non contraria alla direzione", PASS if ema50_ok else FAIL,
        f"pendenza EMA50 su {s} barre: {fmt(slope['ema50'])} (soglia piatta ±{fmt(flat)})")

    # Fase 2 - Trigger
    crosses = []
    for j in range(i - a.cross_lookback + 1, i + 1):
        d0, d1 = e9[j - 1] - e21[j - 1], e9[j] - e21[j]
        if d0 <= 0 < d1:
            crosses.append((j, 1))
        elif d0 >= 0 > d1:
            crosses.append((j, -1))
    same = [c for c in crosses if c[1] == side]
    currently = (e9[i] - e21[i]) * side > 0
    if same and currently:
        add(2, "Incrocio EMA 9 / EMA 21", PASS, f"incrocio {i - same[-1][0]} barre fa, EMA9 {fmt(e9[i])} / EMA21 {fmt(e21[i])}")
    elif currently:
        add(2, "Incrocio EMA 9 / EMA 21", WARN,
            f"EMA9 già dal lato giusto ma nessun incrocio nelle ultime {a.cross_lookback} barre: setup in corso, non nuovo trigger")
    else:
        add(2, "Incrocio EMA 9 / EMA 21", FAIL, f"EMA9 {fmt(e9[i])} non dal lato {name} di EMA21 {fmt(e21[i])}")

    # Fase 3 - Allineamento
    ordered = side != 0 and (close - e9[i]) * side > 0 and (e9[i] - e21[i]) * side > 0 and (e21[i] - e50[i]) * side > 0
    add(3, "Medie ordinate (Prezzo/EMA9/EMA21/EMA50)", PASS if ordered else (WARN if currently else FAIL),
        "ordine completo" if ordered else "ordine non completo: al massimo 'in allineamento'")
    tilt = side != 0 and slope["ema9"] * side > 0 and slope["ema21"] * side > 0
    add(3, "EMA 9 ed EMA 21 inclinate nella direzione", PASS if tilt else FAIL,
        f"pendenze EMA9 {fmt(slope['ema9'])}, EMA21 {fmt(slope['ema21'])}")

    # Fase 4 - Momentum Heiken Ashi
    last3 = ha[i - 2:i + 1]
    colors = [1 if h["c"] > h["o"] else -1 if h["c"] < h["o"] else 0 for h in last3]
    color_ok = side != 0 and all(c == side for c in colors)
    add(4, "Tre HA consecutive nella direzione", PASS if color_ok else FAIL,
        "colori ultime 3 HA: " + " ".join({1: "verde", -1: "rossa", 0: "doji"}[c] for c in colors))
    wicks = []
    for h in last3:
        rng = h["h"] - h["l"] or 1e-12
        opp = (min(h["o"], h["c"]) - h["l"]) if side >= 0 else (h["h"] - max(h["o"], h["c"]))
        wicks.append(opp / rng)
    wick_ok = all(w <= a.wick_pct for w in wicks)
    add(4, "Nessuno stoppino contrario significativo", PASS if wick_ok else FAIL,
        "stoppino contrario / range: " + ", ".join(f"{w:.0%}" for w in wicks) + f" (max {a.wick_pct:.0%})")
    bodies = [abs(h["c"] - h["o"]) for h in last3]
    body_ok = all(bodies[k] >= a.body_ratio * bodies[k - 1] for k in (1, 2))
    add(4, "Corpo HA stabile o crescente", PASS if body_ok else FAIL,
        "corpi: " + ", ".join(fmt(b) for b in bodies))
    big_third = bodies[2] > A
    if big_third:
        add(4, "Terza HA molto ampia", WARN, f"corpo {fmt(bodies[2])} > 1 ATR ({fmt(A)}): valutare attesa pullback")

    # Fase 5 - Forza ADX / DI
    x = adx[i]
    if x < 15:
        st, txt = FAIL, "mercato debole/laterale: no trade"
    elif x < 20:
        st, txt = WARN, "forza incerta: solo setup molto pulito, preferibile attendere"
    elif x <= 25:
        st, txt = PASS, "trend operativo"
    else:
        st, txt = PASS, "trend forte (preferibile)"
    add(5, "ADX > 20 (meglio > 25)", st, f"ADX {fmt(x)}: {txt}")
    if x > 35:
        add(5, "ADX molto alto", WARN, "trend molto forte: attenzione a non inseguire un movimento già esteso")
    rising = x >= 0.97 * adx[i - s]
    add(5, "ADX crescente o stabile", PASS if rising else WARN,
        f"ADX {fmt(adx[i - s])} → {fmt(x)} in {s} barre")
    di_ok = side != 0 and (dip[i] - dim[i]) * side > 0
    add(5, "DI coerenti con la direzione", PASS if di_ok else FAIL,
        f"DI+ {fmt(dip[i])} / DI- {fmt(dim[i])}")

    # Distanza dalle medie
    d9, d21 = abs(close - e9[i]) / A, abs(close - e21[i]) / A
    if d9 <= 0.5:
        dist, dist_txt = PASS, "ingresso diretto preferibile (≤ 0,5 ATR da EMA 9)"
    elif d21 <= 1:
        dist, dist_txt = PASS, "ingresso accettabile (≤ 1 ATR da EMA 21)"
    else:
        dist, dist_txt = WARN, "segnale tardivo (> 1 ATR da EMA 21): attendere pullback verso EMA 9/21"
    add(6, "Distanza dalle medie", dist, f"{d9:.2f} ATR da EMA9, {d21:.2f} ATR da EMA21: {dist_txt}")

    # Regole di non ingresso verificabili dai prezzi
    x50 = sum(1 for j in range(i - 19, i + 1) if (closes[j] - e50[j]) * (closes[j - 1] - e50[j - 1]) < 0)
    chop50 = x50 >= 3 and abs(slope["ema50"]) < flat
    add(0, "EMA 50 piatta e attraversata ripetutamente", FAIL if chop50 else (WARN if x50 >= 3 else PASS),
        f"{x50} attraversamenti di EMA50 nelle ultime 20 barre")
    add(0, "Incrocio dentro congestione (EMA 9/21 intrecciate)", FAIL if len(crosses) >= 2 else PASS,
        f"{len(crosses)} incroci EMA9/21 nelle ultime {a.cross_lookback} barre")

    # Fase 6 - Stop, target, R:R, size
    plan = {"ingresso": close}
    if side:
        swing = last_pivot(rows, i, side, a.swing_bars)
        candidates = {
            "ultimo minimo/massimo significativo": swing,
            "EMA 21": e21[i],
            "candela di conferma": last["l"] if side > 0 else last["h"],
            "1,5 ATR": close - side * 1.5 * A,
        }
        plan["stop_candidati"] = {k: round(v, 5) for k, v in candidates.items()}
        stop = a.stop if a.stop is not None else swing - side * 0.1 * A
        plan["stop"] = stop
        plan["stop_origine"] = "--stop" if a.stop is not None else "ultimo swing - 0,1 ATR"
        risk = (close - stop) * side
        if risk <= 0:
            add(6, "Stop tecnico", FAIL, f"stop {fmt(stop)} dal lato sbagliato del prezzo")
        else:
            plan["rischio_punti"] = risk
            plan["livelli_R"] = {f"{m}R": round(close + side * m * risk, 5) for m in (1, 1.5, 2)}
            add(6, "Stop tecnico non troppo ampio", PASS if risk <= 2 * A else WARN,
                f"distanza stop {fmt(risk)} = {risk / A:.2f} ATR")
            if a.target is not None:
                rr = (a.target - close) * side / risk
                plan["target"], plan["rr"] = a.target, rr
                add(6, "Rapporto rischio/rendimento ≥ 1:1", PASS if rr >= 1 else FAIL,
                    f"target {fmt(a.target)} → R:R 1:{rr:.2f}" + (" (preferibile)" if rr >= 1.5 else ""))
            else:
                add(6, "Rapporto rischio/rendimento ≥ 1:1", MANUAL,
                    "nessun --target: verifica che il primo S/R sia oltre 1R "
                    f"({fmt(plan['livelli_R']['1R'])}), meglio 1,5R ({fmt(plan['livelli_R']['1.5R'])})")
            if a.capital and a.risk_pct:
                money = a.capital * a.risk_pct / 100
                plan["rischio_denaro"] = money
                plan["size"] = money / (risk * a.point_value)
                if a.risk_pct > 2:
                    add(6, "Rischio per trade", FAIL, f"{a.risk_pct}% supera il limite massimo del 2%")
    add(6, "Spazio tecnico fino a S/R, news, liquidità", MANUAL,
        "non verificabile dai soli prezzi: controlla livelli, calendario macro e sessione")

    # Classificazione
    hard_fail = any(c["esito"] == FAIL for c in checks)
    late = dist == WARN or big_third
    rr = plan.get("rr")
    if hard_fail or side == 0:
        grade, verdict = "C", "NO TRADE"
    elif x > 25 and ordered and color_ok and wick_ok and body_ok and all(
            c["esito"] != WARN for c in checks if c["fase"] in (0, 2, 3, 5)) and (rr is None or rr >= 1.5):
        grade = "A" if rr is not None else "A (da confermare con R:R ≥ 1:1,5)"
        verdict = "ATTENDERE PULLBACK" if late else "OPERATIVO"
    else:
        grade = "B"
        verdict = "ATTENDERE PULLBACK" if late else "OPERATIVO CON PRUDENZA"

    return {
        "barra": last["t"], "direzione": name, "verdetto": verdict, "classe": grade,
        "indicatori": {"close": close, "ema9": e9[i], "ema21": e21[i], "ema50": e50[i],
                       "adx": x, "di_plus": dip[i], "di_minus": dim[i], "atr": A},
        "controlli": checks, "piano": plan,
    }


def print_report(res):
    ind = res["indicatori"]
    print(f"Barra: {res['barra']}   Direzione valutata: {res['direzione']}")
    print(f"Verdetto: {res['verdetto']}   Classe setup: {res['classe']}\n")
    print(f"Close {fmt(ind['close'])} | EMA9 {fmt(ind['ema9'])} | EMA21 {fmt(ind['ema21'])} | EMA50 {fmt(ind['ema50'])}")
    print(f"ADX {fmt(ind['adx'])} | DI+ {fmt(ind['di_plus'])} | DI- {fmt(ind['di_minus'])} | ATR {fmt(ind['atr'])}\n")
    titles = {1: "1. Contesto", 2: "2. Trigger", 3: "3. Allineamento", 4: "4. Momentum HA",
              5: "5. Forza ADX/DI", 6: "6. Tradeability", 0: "Regole di non ingresso"}
    for phase in (1, 2, 3, 4, 5, 6, 0):
        group = [c for c in res["controlli"] if c["fase"] == phase]
        if not group:
            continue
        print(titles[phase])
        for c in group:
            print(f"  {ICON[c['esito']]} {c['controllo']}: {c['dettaglio']}")
    p = res["piano"]
    if "stop" in p:
        print("\nPiano")
        print(f"  Ingresso: {fmt(p['ingresso'])}   Stop: {fmt(p['stop'])} ({p['stop_origine']})")
        print("  Stop alternativi: " + ", ".join(f"{k} {fmt(v)}" for k, v in p["stop_candidati"].items()))
        if "livelli_R" in p:
            print("  Livelli: " + ", ".join(f"{k} {fmt(v)}" for k, v in p["livelli_R"].items()))
        if "rr" in p:
            print(f"  Target: {fmt(p['target'])}   R:R 1:{p['rr']:.2f}")
        if "size" in p:
            print(f"  Rischio: {fmt(p['rischio_denaro'])}   Size: {fmt(p['size'], 4)}")
    print("\nUso didattico: non è consulenza finanziaria. Testa su storico, demo e forward test.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv", help="file CSV con colonne open, high, low, close (e opzionale date/time)")
    ap.add_argument("--exclude-last", action="store_true", help="scarta l'ultima riga se è una barra ancora aperta")
    ap.add_argument("--target", type=float, help="livello di target tecnico (primo S/R utile)")
    ap.add_argument("--stop", type=float, help="stop tecnico scelto (default: ultimo swing ± 0,1 ATR)")
    ap.add_argument("--capital", type=float, help="capitale del conto, per la size")
    ap.add_argument("--risk-pct", type=float, help="rischio %% per trade (0,5 demo, 1 ordinario, max 2)")
    ap.add_argument("--point-value", type=float, default=1.0, help="valore monetario di 1 punto per unità di size")
    ap.add_argument("--slope-bars", type=int, default=3, help="barre per misurare l'inclinazione (default 3)")
    ap.add_argument("--cross-lookback", type=int, default=10, help="barre entro cui l'incrocio è recente (default 10)")
    ap.add_argument("--wick-pct", type=float, default=0.15, help="stoppino contrario max come frazione del range HA")
    ap.add_argument("--body-ratio", type=float, default=0.85, help="corpo HA minimo rispetto al precedente")
    ap.add_argument("--swing-bars", type=int, default=20, help="barre in cui cercare l'ultimo minimo/massimo significativo")
    ap.add_argument("--json", action="store_true", help="output JSON")
    a = ap.parse_args()

    rows = load_ohlc(a.csv)
    if a.exclude_last:
        rows = rows[:-1]
    res = analyze(rows, a)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print_report(res)


if __name__ == "__main__":
    main()
