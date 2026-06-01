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
import numpy as np
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

def _centiles(base_sous, base_ind, seed=0):
    rng = np.random.default_rng(seed)
    rows = [{"Centile": f"C{i}",
             "Individus": base_ind//10 + int(rng.integers(-20,20)),
             "Souscriptions": (s := int(base_sous*(1+(i-91)*.04)+rng.integers(0,5))),
             "Taux (%)": round(s/(base_ind//10)*100, 1)}
            for i in range(91,101)]
    return pd.DataFrame(rows)

perimètres_centiles = {
    "Global":      {"Modèle A": _centiles(264,1200,0), "Modèle B": _centiles(250,1000,1)},
    "Périmètre 1": {"Modèle A": _centiles(146, 600,2), "Modèle B": _centiles(132, 500,3)},
    "Périmètre 2": {"Modèle A": _centiles(118, 600,4), "Modèle B": _centiles(118, 500,5)},
}
# Mettez perimètres_centiles = None pour masquer le bouton

DL = [f"D{i}" for i in range(1, 11)]
np.random.seed(0)
tables_transition = {
    "Transition Modèle A → Modèle B": pd.DataFrame(
        (np.random.dirichlet([2]*10, 10) * 100).round(1), index=DL, columns=DL),
    "Transition Modèle B → Modèle A": pd.DataFrame(
        (np.random.dirichlet([2]*10, 10) * 100).round(1), index=DL, columns=DL),
}

# ── CSS ──────────────────────────────────────────────────────────────────────

CSS = """
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');
:root{--bg:#f9f9f7;--surface:#fff;--border:#e4e4e0;--border2:#d0d0cb;--text:#1a1a18;--muted:#888880;--accent:#2d6a4f;--accent-bg:#eef5f1;--mono:'IBM Plex Mono',monospace}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--bg);color:var(--text);font-family:'IBM Plex Sans',sans-serif;font-size:14px;line-height:1.6;padding:48px 40px 80px;max-width:1200px;margin:0 auto}
.report-header{border-bottom:2px solid var(--text);padding-bottom:20px;margin-bottom:48px;display:flex;justify-content:space-between;align-items:flex-end}
.report-header h1{font-size:1.6rem;font-weight:600;letter-spacing:-.02em}
.report-header .meta{font-family:var(--mono);font-size:.72rem;color:var(--muted);text-align:right;line-height:1.8}
.distrib-toolbar{position:sticky;top:0;z-index:10;background:var(--bg);display:flex;align-items:center;justify-content:space-between;padding:10px 0;border-bottom:1px solid var(--border)}
.distrib-toolbar-title{font-size:.7rem;font-family:var(--mono);font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.toggle-group{display:flex;border:1px solid var(--border2);border-radius:4px;overflow:hidden}
.toggle-btn{padding:5px 14px;background:var(--surface);color:var(--muted);border:none;cursor:pointer;font-family:var(--mono);font-size:.72rem;font-weight:500;letter-spacing:.05em;transition:background .15s,color .15s}
.toggle-btn:not(:last-child){border-right:1px solid var(--border2)}
.toggle-btn.active{background:var(--accent);color:#fff}
.section{margin-bottom:52px}
.section-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;padding-bottom:10px;border-bottom:1px solid var(--border)}
.section-title{font-size:.7rem;font-family:var(--mono);font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.perimetre-block{margin-bottom:40px}
.perimetre-header{display:flex;align-items:center;gap:10px;margin:28px 0 16px}
.perimetre-label{font-size:.75rem;font-family:var(--mono);font-weight:500;letter-spacing:.08em;text-transform:uppercase;color:var(--text)}
.perimetre-rule{flex:1;height:1px;background:var(--border)}
.tables-grid{display:grid;gap:20px;grid-template-columns:repeat(auto-fit,minmax(340px,1fr))}
.table-title{font-size:.82rem;font-weight:600;color:var(--text);margin-bottom:8px}
.table-wrap{border:1px solid var(--border2);border-radius:4px;overflow-x:auto;background:var(--surface)}
table{width:100%;border-collapse:collapse;font-size:.8rem}
thead tr{background:#f2f2ef;border-bottom:1px solid var(--border2)}
thead th{padding:9px 14px;text-align:right;font-family:var(--mono);font-size:.68rem;font-weight:500;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);white-space:nowrap}
thead th:first-child{text-align:left}
tbody tr{border-bottom:1px solid var(--border)}
tbody tr:last-child{border-bottom:none}
tbody tr:hover{background:#f6f6f3}
tbody td{padding:8px 14px;text-align:right;font-family:var(--mono);color:var(--text);white-space:nowrap}
tbody td:first-child{text-align:left;font-weight:500}
.taux-wrap{display:flex;align-items:center;justify-content:flex-end;gap:8px}
.bar-bg{width:56px;height:5px;background:#e8e8e4;border-radius:99px;flex-shrink:0}
.bar-fg{height:100%;border-radius:99px;background:var(--accent)}
.diag{background:var(--accent-bg)!important;color:var(--accent)!important;font-weight:600}
.heat-3{color:#1a1a18}.heat-2{color:#555550}.heat-1{color:#999994}.heat-0{color:#ccccca}
body.view-decile .centile-view{display:none}
body.view-centile .decile-view{display:none}
.report-footer{margin-top:64px;padding-top:16px;border-top:1px solid var(--border);font-family:var(--mono);font-size:.7rem;color:var(--muted);display:flex;justify-content:space-between}
"""

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
  <style>{CSS}</style>
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
