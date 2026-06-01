"""
Générateur de rapport HTML — Déciles & matrices de transition
Usage : python generate_rapport.py  →  rapport_deciles.html

Structure des données
---------------------
perimètres_deciles / perimètres_centiles :
    { "Nom périmètre": { "Nom modèle": DataFrame, ... }, ... }
    DataFrame : colonnes "Décile"/"Centile", "Individus", "Souscriptions", "Taux (%)"

tables_transition :
    { "Titre": DataFrame }   (index & colonnes = étiquettes déciles)

Mettre perimètres_centiles = None pour masquer le bouton décile/centile.
"""

import pandas as pd
from datetime import datetime

# ── Vos données ──────────────────────────────────────────────────────────────

perimètres_deciles = {
    "Global": {
        "Modèle A": pd.DataFrame({
            "Décile": [f"D{i}" for i in range(1,11)],
            "Individus":     [1200]*10,
            "Souscriptions": [48,72,96,120,144,168,192,216,240,264],
            "Taux (%)":      [4,6,8,10,12,14,16,18,20,22],
        }),
        "Modèle B": pd.DataFrame({
            "Décile": [f"D{i}" for i in range(1,11)],
            "Individus":     [1000]*10,
            "Souscriptions": [30,55,80,105,130,155,180,205,230,250],
            "Taux (%)":      [3,5.5,8,10.5,13,15.5,18,20.5,23,25],
        }),
    },
    "Périmètre 1": {
        "Modèle A": pd.DataFrame({
            "Décile": [f"D{i}" for i in range(1,11)],
            "Individus":     [600]*10,
            "Souscriptions": [20,34,48,62,76,90,104,118,132,146],
            "Taux (%)":      [3.3,5.7,8,10.3,12.7,15,17.3,19.7,22,24.3],
        }),
        "Modèle B": pd.DataFrame({
            "Décile": [f"D{i}" for i in range(1,11)],
            "Individus":     [500]*10,
            "Souscriptions": [15,28,41,54,67,80,93,106,119,132],
            "Taux (%)":      [3,5.6,8.2,10.8,13.4,16,18.6,21.2,23.8,26.4],
        }),
    },
    "Périmètre 2": {
        "Modèle A": pd.DataFrame({
            "Décile": [f"D{i}" for i in range(1,11)],
            "Individus":     [600]*10,
            "Souscriptions": [28,38,48,58,68,78,88,98,108,118],
            "Taux (%)":      [4.7,6.3,8,9.7,11.3,13,14.7,16.3,18,19.7],
        }),
        "Modèle B": pd.DataFrame({
            "Décile": [f"D{i}" for i in range(1,11)],
            "Individus":     [500]*10,
            "Souscriptions": [15,27,39,51,63,75,87,99,111,118],
            "Taux (%)":      [3,5.4,7.8,10.2,12.6,15,17.4,19.8,22.2,23.6],
        }),
    },
}

perimètres_centiles = None   # Remplacez par un dict identique pour activer le bouton

DL = [f"D{i}" for i in range(1,11)]
import numpy as np; np.random.seed(0)
tables_transition = {
    "Transition Modèle A → Modèle B": pd.DataFrame(
        (lambda m: m / m.sum(axis=1, keepdims=True) * 100)(
            np.random.dirichlet([2]*10, 10)
        ).round(1), index=DL, columns=DL),
    "Transition Modèle B → Modèle A": pd.DataFrame(
        (lambda m: m / m.sum(axis=1, keepdims=True) * 100)(
            np.random.dirichlet([2]*10, 10)
        ).round(1), index=DL, columns=DL),
}

# ── Rendu HTML ───────────────────────────────────────────────────────────────

def fmt(v):
    return f"{int(v):,}".replace(",", "\u202f")

def taux_cell(v, mx):
    pct = min(v / mx * 100, 100) if mx else 0
    return (f'<div class="taux-wrap"><span>{v:.1f}%</span>'
            f'<div class="bar-bg"><div class="bar-fg" style="width:{pct:.0f}%"></div></div></div>')

def heat(v, lo, hi):
    if hi == lo: return "heat-1"
    r = (v - lo) / (hi - lo)
    return "heat-3" if r >= .6 else "heat-2" if r >= .35 else "heat-1" if r >= .12 else "heat-0"

def one_table(df, title, col="Décile"):
    mx = df["Taux (%)"].max()
    rows = "".join(
        f"<tr><td>{r[col]}</td><td>{fmt(r['Individus'])}</td>"
        f"<td>{fmt(r['Souscriptions'])}</td><td>{taux_cell(r['Taux (%)'], mx)}</td></tr>"
        for _, r in df.iterrows()
    )
    return (f'<div class="table-block"><div class="table-title">{title}</div>'
            f'<div class="table-wrap"><table>'
            f'<thead><tr><th>{col}</th><th>Individus</th><th>Souscriptions</th><th>Taux (%)</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div></div>')

def perim_block(label, dec, cen):
    dv = f'<div class="decile-view"><div class="tables-grid">{"".join(one_table(df,n) for n,df in dec.items())}</div></div>'
    cv = (f'<div class="centile-view"><div class="tables-grid">{"".join(one_table(df,n,"Centile") for n,df in cen.items())}</div></div>'
          if cen else "")
    return (f'<div class="perimetre-block">'
            f'<div class="perimetre-header"><span class="perimetre-label">{label}</span><div class="perimetre-rule"></div></div>'
            f'{dv}{cv}</div>')

def transition_block(df, title):
    cols = list(df.columns)
    lo, hi = df.values.min(), df.values.max()
    th = "".join(f"<th>{c}</th>" for c in cols)
    rows = "".join(
        "<tr><td><strong>{}</strong></td>{}</tr>".format(
            idx, "".join(
                f'<td class="{"diag" if idx==c else heat(row[c],lo,hi)}">{row[c]:.1f}%</td>'
                for c in cols))
        for idx, row in df.iterrows()
    )
    return (f'<div class="table-block" style="margin-bottom:32px">'
            f'<div class="table-title">{title}</div><div class="table-wrap"><table>'
            f'<thead><tr><th>orig. / dest.</th>{th}</tr></thead>'
            f'<tbody>{rows}</tbody></table></div></div>')

def generate_report(perimètres_deciles, tables_transition,
                    perimètres_centiles=None,
                    output_path="rapport_deciles.html",
                    titre="Analyse par Déciles"):

    date_str = datetime.now().strftime("%d/%m/%Y %H:%M")
    has_cen = perimètres_centiles is not None

    toggle = (
        '<div class="toggle-group">'
        '<button class="toggle-btn active" data-mode="decile" onclick="switchView(\'decile\')">Déciles</button>'
        '<button class="toggle-btn" data-mode="centile" onclick="switchView(\'centile\')">10 derniers centiles</button>'
        '</div>'
    ) if has_cen else ""

    perims = "".join(
        perim_block(f"{i:02d} — {name}", dec, (perimètres_centiles or {}).get(name))
        for i, (name, dec) in enumerate(perimètres_deciles.items(), 1)
    )
    transitions = "".join(transition_block(df, name) for name, df in tables_transition.items())

    nb = f"{len(perimètres_deciles)} périmètre(s) · {len(next(iter(perimètres_deciles.values())))} modèle(s) · {len(tables_transition)} matrice(s)"

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{titre}</title>
  <link rel="stylesheet" href="rapport.css">
</head>
<body class="view-decile">
<header class="report-header">
  <h1>{titre}</h1>
  <div class="meta">Généré le {date_str}<br>{nb}</div>
</header>
<section class="section">
  <div class="distrib-toolbar">
    <span class="distrib-toolbar-title">Distribution</span>{toggle}
  </div>
  {perims}
</section>
<section class="section">
  <div class="section-header"><div class="section-title">Matrices de transition</div></div>
  {transitions}
</section>
<footer class="report-footer">
  <span>Rapport automatique — {titre}</span><span>{date_str}</span>
</footer>
<script>
  function switchView(m) {{
    document.body.className='view-'+m;
    document.querySelectorAll('.toggle-btn').forEach(b=>b.classList.toggle('active',b.dataset.mode===m));
  }}
</script>
</body></html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✓ Rapport généré : {output_path}")


if __name__ == "__main__":
    generate_report(
        perimètres_deciles=perimètres_deciles,
        perimètres_centiles=perimètres_centiles,
        tables_transition=tables_transition,
    )
