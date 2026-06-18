# Projet fil rouge - Presidentielle 2027
# Analyse electorale pour La France Insoumise
# Application de data storytelling (Streamlit)

import os
import json
import warnings

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st

warnings.filterwarnings("ignore")

st.set_page_config(page_title="Présidentielle 2027", page_icon="🗳️", layout="wide")

DOSSIER = os.path.dirname(os.path.abspath(__file__))

# ── Palette aux couleurs de LFI (rouge sur thème sombre) ──────────────────
ACCENT = "#E2001A"        # rouge LFI (couleur principale UI)
ACCENT2 = "#FF5C45"       # rouge-corail (second ton, pour les dégradés)
LFI_C = "#E2001A"         # rouge LFI : on met LFI en avant avec cette couleur
GRIS = "#A99AA0"

# couleur par parti (LFI en rouge, les autres restent distincts pour la lisibilité)
COULEURS_PARTIS = {
    "Mélenchon": LFI_C, "LFI": LFI_C, "LFI (Aubry)": LFI_C,
    "Hollande": "#F472B6", "Hamon": "#F472B6", "Hidalgo": "#F472B6",
    "PS (Glucksmann)": "#F472B6", "PS_Glucksmann": "#F472B6",
    "Macron": "#FBBF24", "Renaissance (Hayer)": "#FBBF24", "Renaissance": "#FBBF24",
    "Bayrou": "#FCD34D",
    "Le Pen": "#38BDF8", "RN (Bardella)": "#38BDF8", "RN": "#38BDF8",
    "Zemmour": "#6366F1", "Reconquête (Maréchal)": "#6366F1", "Reconquete": "#6366F1",
    "Sarkozy": "#60A5FA", "Fillon": "#60A5FA", "Pécresse": "#60A5FA",
    "LR (Bellamy)": "#60A5FA", "LR": "#60A5FA",
    "Jadot": "#34D399", "Joly": "#34D399", "EELV (Toussaint)": "#34D399", "EELV": "#34D399",
    "Roussel": "#C084FC", "PCF (Léon)": "#C084FC", "PCF": "#C084FC",
}

# palette qualitative (pour les séries multi-régions) — démarre sur le rouge LFI
PALETTE = ["#E2001A", "#FF7A45", "#FBBF24", "#F472B6", "#34D399", "#38BDF8",
           "#FB6340", "#C084FC", "#FF9F1C", "#2DD4BF", "#F87171", "#60A5FA", "#FACC15"]

# alias et nuances de rouge LFI
ROUGE = LFI_C
ROUGE_FONCE = "#A4001A"
CORAIL_PALE = "rgba(226,0,26,0.28)"   # pour les "fonds" de barres


# ── Style : look "dashboard premium" sombre ───────────────────────────────
st.markdown("""
<style>
  .stApp { background:
      radial-gradient(1100px 550px at 85% -10%, rgba(226,0,26,0.07), transparent 60%),
      radial-gradient(900px 450px at -10% 5%, rgba(255,92,69,0.05), transparent 55%),
      #FFFFFF; }

  /* bandeau d'en-tête */
  .hero {
    background: linear-gradient(120deg, #A4001A 0%, #E2001A 50%, #FF5C45 100%);
    border-radius: 20px; padding: 1.6rem 2rem; margin-bottom: 1.2rem;
    box-shadow: 0 10px 30px rgba(226,0,26,0.28);
  }
  .hero .t { font-size: 2rem; font-weight: 900; color: white; letter-spacing: -0.5px; margin: 0; }
  .hero .s { font-size: 1rem; color: rgba(255,255,255,0.92); margin: 0.3rem 0 0; }

  /* titre de chapitre */
  .chapitre { margin: 0.3rem 0 0.2rem; border-left: 6px solid #E2001A; padding-left: 1rem; }
  .chapitre h1 { font-size: 2rem; font-weight: 900; margin: 0; color: #B0001A; }
  .chapitre p { font-size: 1.05rem; color: #6B6B7B; margin: 0.3rem 0 0; }

  /* encadré "à retenir" */
  .retenir {
    background: #FFF3F4;
    border: 1px solid rgba(226,0,26,0.20);
    border-left: 5px solid #E2001A;
    border-radius: 12px; padding: 1.1rem 1.3rem; margin: 1.4rem 0 0.5rem;
    box-shadow: 0 4px 16px rgba(226,0,26,0.08);
  }
  .retenir .titre { color: #B0001A; font-weight: 800; font-size: 0.85rem;
                    text-transform: uppercase; letter-spacing: 1px; }
  .retenir .texte { color: #2A2A38; font-size: 1.02rem; margin-top: 0.35rem; line-height: 1.5; }

  /* cartes chiffres */
  .kpi {
    background: #FFFFFF;
    border: 1px solid #EEE3E5;
    border-radius: 16px; padding: 1.1rem 0.6rem; text-align: center;
    box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    transition: transform 0.15s ease, border 0.15s ease;
  }
  .kpi:hover { transform: translateY(-3px); border-color: rgba(226,0,26,0.45); }
  .kpi .val { font-size: 2.1rem; font-weight: 900; line-height: 1; color: #E2001A; }
  .kpi .lbl { font-size: 0.8rem; color: #777; margin-top: 0.4rem; }

  /* onglets */
  .stTabs [data-baseweb="tab-list"] { gap: 0.3rem; }
  .stTabs [data-baseweb="tab"] {
    font-size: 0.98rem; font-weight: 600; padding: 0.55rem 1rem;
    border-radius: 12px 12px 0 0;
  }
  .stTabs [aria-selected="true"] {
    color: #E2001A !important;
    background: rgba(226,0,26,0.08) !important;
  }

  h2, h3, h4 { color: #1C1C28; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# DONNÉES NATIONALES (résultats officiels 1er tour - Ministère de l'Intérieur)
# ══════════════════════════════════════════════════════════════════════════
resultats = {
    2012: {"Hollande": 28.63, "Sarkozy": 27.18, "Le Pen": 17.90, "Mélenchon": 11.10,
           "Bayrou": 9.13, "Joly": 2.31, "Dupont-Aignan": 1.79, "Poutou": 1.15, "Arthaud": 0.56},
    2017: {"Macron": 24.01, "Le Pen": 21.30, "Fillon": 20.01, "Mélenchon": 19.58,
           "Hamon": 6.36, "Dupont-Aignan": 4.70, "Lassalle": 1.21, "Poutou": 1.09, "Arthaud": 0.64},
    2022: {"Macron": 27.85, "Le Pen": 23.15, "Mélenchon": 21.95, "Zemmour": 7.07,
           "Pécresse": 4.78, "Jadot": 4.63, "Lassalle": 3.13, "Roussel": 2.28,
           "Dupont-Aignan": 2.06, "Hidalgo": 1.75, "Poutou": 0.77, "Arthaud": 0.56},
}
melenchon = {2012: 11.10, 2017: 19.58, 2022: 21.95}
participation = {2012: 79.48, 2017: 77.77, 2022: 73.69}
sondage_2027 = {"Bardella (RN)": 32, "Bloc central": 17, "Mélenchon (LFI)": 16,
                "Glucksmann (PS)": 11, "Ciotti (LR)": 6, "Autres": 18}

CODES_METRO = ["11", "24", "27", "28", "32", "44", "52", "53", "75", "76", "84", "93", "94"]


# ══════════════════════════════════════════════════════════════════════════
# CHARGEMENT DES FICHIERS
# ══════════════════════════════════════════════════════════════════════════
@st.cache_data
def charger_donnees():
    frames = []
    clean = os.path.join(DOSSIER, "data_clean")
    sources = [
        ("elections_2012_clean.csv", 2012, "csv"),
        ("elections_2017_clean.xlsx", 2017, "xlsx"),
        ("elections_2022_clean.csv", 2022, "csv"),
    ]
    for fichier, annee, typ in sources:
        try:
            if typ == "csv":
                d = pd.read_csv(os.path.join(clean, fichier), sep=";", encoding="utf-8-sig")
            else:
                d = pd.read_excel(os.path.join(clean, fichier))
            frames.append(preparer(d, annee))
        except Exception:
            pass
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def preparer(df, annee):
    df = df.copy()
    df.columns = df.columns.str.strip()

    def trouver(mots, sauf=None):
        sauf = sauf or []
        for c in df.columns:
            cl = c.lower()
            if any(m in cl for m in mots) and not any(s in cl for s in sauf):
                return c
        return None

    col_code = trouver(["code"])
    col_region = trouver(["region", "libell", "nom"], sauf=["code", "etat", "saisie"])
    col_inscrits = trouver(["inscrit"])
    col_abst = trouver(["abstention"])
    col_exprimes = trouver(["exprim"])
    col_votants = trouver(["votant"])
    col_mel = trouver(["lench"], sauf=["%"])

    lignes = []
    for _, r in df.iterrows():
        region = str(r[col_region]).strip() if col_region else ""
        if region.lower() in ("nan", "", "total", "france", "region"):
            continue
        inscrits = pd.to_numeric(r.get(col_inscrits), errors="coerce") if col_inscrits else np.nan
        abst = pd.to_numeric(r.get(col_abst), errors="coerce") if col_abst else np.nan
        exprimes = pd.to_numeric(r.get(col_exprimes), errors="coerce") if col_exprimes else np.nan
        votants = pd.to_numeric(r.get(col_votants), errors="coerce") if col_votants else (inscrits - abst)
        mel = pd.to_numeric(r.get(col_mel), errors="coerce") if col_mel else np.nan
        pct_part = votants / inscrits * 100 if inscrits and votants else np.nan
        pct_mel = np.nan
        for c in df.columns:
            if "lench" in c.lower() and "%" in c.lower():
                pct_mel = pd.to_numeric(r[c], errors="coerce")
                break
        if pd.isna(pct_mel) and not pd.isna(mel) and exprimes:
            pct_mel = mel / exprimes * 100
        lignes.append({
            "annee": annee,
            "code": str(r[col_code]).strip() if col_code else "",
            "region": region,
            "inscrits": inscrits,
            "pct_melenchon": pct_mel,
            "pct_participation": pct_part,
            "pct_abstention": 100 - pct_part if pct_part else np.nan,
        })
    return pd.DataFrame(lignes)


@st.cache_data
def charger_europeennes():
    chemin = os.path.join(DOSSIER, "data_clean", "europeennes_2024_clean.csv")
    try:
        return pd.read_csv(chemin, sep=";", encoding="utf-8-sig")
    except Exception:
        return pd.DataFrame()


@st.cache_data
def charger_socio():
    chemin = os.path.join(DOSSIER, "data_clean", "socio_demographie_regions.csv")
    try:
        return pd.read_csv(chemin, sep=";", encoding="utf-8-sig")
    except Exception:
        return pd.DataFrame()


@st.cache_data
def charger_carte():
    chemin = os.path.join(DOSSIER, "regions_france.geojson")
    if os.path.exists(chemin):
        with open(chemin, encoding="utf-8") as f:
            return json.load(f)
    url = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions-version-simplifiee.geojson"
    try:
        import urllib3
        urllib3.disable_warnings()
        geo = requests.get(url, timeout=15, verify=False).json()
        with open(chemin, "w", encoding="utf-8") as f:
            json.dump(geo, f, ensure_ascii=False)
        return geo
    except Exception:
        return None


# ══════════════════════════════════════════════════════════════════════════
# HELPERS DE PRÉSENTATION
# ══════════════════════════════════════════════════════════════════════════
def titre_chapitre(titre, accroche):
    st.markdown(
        f'<div class="chapitre"><h1>{titre}</h1><p>{accroche}</p></div>',
        unsafe_allow_html=True,
    )
    st.write("")


def a_retenir(texte):
    st.markdown(
        f'<div class="retenir"><div class="titre">💡 À retenir</div>'
        f'<div class="texte">{texte}</div></div>',
        unsafe_allow_html=True,
    )


def carte_kpi(colonne, valeur, label):
    colonne.markdown(
        f'<div class="kpi"><div class="val">{valeur}</div>'
        f'<div class="lbl">{label}</div></div>',
        unsafe_allow_html=True,
    )


def style_graphe(fig, hauteur=380, titre=None):
    fig.update_layout(
        height=hauteur,
        title=titre,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="sans-serif", size=13, color="#2A2A38"),
        margin=dict(l=10, r=10, t=50 if titre else 20, b=10),
        title_font=dict(size=15, color="#1C1C28"),
        legend=dict(font=dict(color="#3A3A48")),
    )
    fig.update_xaxes(gridcolor="rgba(0,0,0,0.07)", zerolinecolor="rgba(0,0,0,0.15)")
    fig.update_yaxes(gridcolor="rgba(0,0,0,0.07)", zerolinecolor="rgba(0,0,0,0.15)")
    return fig


def couleurs_pour(noms):
    return [COULEURS_PARTIS.get(n, GRIS) for n in noms]


# ══════════════════════════════════════════════════════════════════════════
# CHAPITRE 1 — LE CONTEXTE
# ══════════════════════════════════════════════════════════════════════════
def chap_contexte():
    titre_chapitre(
        "La France Insoumise face à 2027",
        "Mission : comprendre si LFI peut atteindre le second tour de la présidentielle.",
    )

    col_txt, col_son = st.columns([3, 2])
    with col_txt:
        st.markdown(
            "Cette étude est réalisée pour **La France Insoumise**. La question est simple :\n\n"
            "> **Mélenchon (ou un candidat LFI) peut-il se qualifier au 2ᵉ tour en 2027 ?**\n\n"
            "Pour y répondre, on analyse les trois dernières présidentielles (2012, 2017, 2022), "
            "on regarde qui vote LFI, et on simule différents scénarios pour 2027."
        )
        st.markdown(
            "En juin 2026, les sondages placent **Mélenchon au coude-à-coude avec le bloc central** "
            "(héritiers de Macron) pour la 2ᵉ place, derrière Jordan Bardella (RN). "
            "La qualification se joue donc à quelques points."
        )
    with col_son:
        st.markdown("**Intentions de vote 2027** — sondage Odoxa, mai 2026")
        fig = px.pie(names=list(sondage_2027.keys()), values=list(sondage_2027.values()),
                     hole=0.55, color_discrete_sequence=["#38BDF8", "#60A5FA", LFI_C,
                                                         "#F472B6", "#A78BFA", "#475569"])
        fig.update_traces(textinfo="label+percent", textfont_size=12,
                          marker=dict(line=dict(color="#FFFFFF", width=2)))
        st.plotly_chart(style_graphe(fig, 300), width='stretch')
        st.caption(
            "Note méthodo : Macron ne peut pas se représenter (limite de deux mandats) "
            "et aucun successeur officiel n'a été désigné. Le « Bloc central » regroupe ici "
            "l'hypothèse d'un candidat unique du camp présidentiel (Philippe, Attal, Darmanin…). "
            "Ce chiffre est une projection, pas un résultat acquis."
        )

    st.write("")
    st.markdown("#### La progression de Mélenchon en 10 ans")
    c1, c2, c3, c4 = st.columns(4)
    carte_kpi(c1, "11 %", "2012 (Front de Gauche)")
    carte_kpi(c2, "20 %", "2017 (LFI)")
    carte_kpi(c3, "22 %", "2022 (LFI)")
    carte_kpi(c4, "~16 %", "Sondage 2026")

    a_retenir(
        "En 10 ans, Mélenchon est passé de <b>11 % à 22 %</b> (+10,9 points), la plus forte "
        "progression à gauche. Mais attention : les sondages à un an du scrutin sont peu fiables "
        "(en 2022, LFI était donné à 9 % et a fait 22 %). Le potentiel réel est sans doute plus haut."
    )


# ══════════════════════════════════════════════════════════════════════════
# CHAPITRE 2 — L'ASCENSION 2012-2022
# ══════════════════════════════════════════════════════════════════════════
def chap_ascension(df):
    titre_chapitre(
        "L'ascension : 2012 → 2022",
        "Comment LFI est devenue la première force de gauche en trois élections.",
    )

    # grande courbe de progression
    st.markdown("#### Une montée régulière, élection après élection")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[2012, 2017, 2022], y=[11.10, 19.58, 21.95],
        mode="lines+markers+text", line=dict(color=ROUGE, width=4),
        marker=dict(size=14, color=ROUGE), text=["11,1 %", "19,6 %", "22,0 %"],
        textposition="top center", textfont=dict(size=14, color=ROUGE_FONCE),
    ))
    fig.update_yaxes(range=[8, 26], title="% des voix (1er tour)")
    fig.update_xaxes(tickvals=[2012, 2017, 2022])
    st.plotly_chart(style_graphe(fig, 340), width='stretch')

    st.divider()

    # resultats d'une annee choisie
    st.markdown("#### Où se situe Mélenchon face aux autres candidats ?")
    annee = st.radio("Choisis une élection :", [2012, 2017, 2022],
                     horizontal=True, index=2, key="asc_annee")
    data = resultats[annee]
    df_res = pd.DataFrame({"Candidat": list(data.keys()), "Score": list(data.values())})
    df_res = df_res.sort_values("Score")
    fig2 = go.Figure(go.Bar(
        x=df_res["Score"], y=df_res["Candidat"], orientation="h",
        marker_color=couleurs_pour(df_res["Candidat"]),
        text=df_res["Score"], texttemplate="%{text} %", textposition="outside",
    ))
    fig2.update_xaxes(range=[0, 33], title="% des exprimés")
    st.plotly_chart(style_graphe(fig2, 420), width='stretch')

    rang = {2012: "4ᵉ", 2017: "4ᵉ", 2022: "3ᵉ"}[annee]
    ecart = {2012: "loin derrière", 2017: "à 1,7 pt du 2ᵉ tour", 2022: "à seulement 1,2 pt du 2ᵉ tour"}[annee]
    st.caption(f"En {annee}, Mélenchon finit **{rang}**, {ecart}.")

    st.divider()

    # evolution par region
    if not df.empty:
        st.markdown("#### La progression touche toutes les régions")
        df_mel = df[df["pct_melenchon"].notna() & df["code"].isin(CODES_METRO)]
        fig3 = px.line(df_mel, x="annee", y="pct_melenchon", color="region", markers=True,
                       color_discrete_sequence=PALETTE)
        fig3.update_traces(line_width=2)
        fig3.update_xaxes(tickvals=[2012, 2017, 2022], title="")
        fig3.update_yaxes(title="% Mélenchon")
        st.plotly_chart(style_graphe(fig3, 420), width='stretch')

    a_retenir(
        "Mélenchon passe de la 4ᵉ à la 3ᵉ place et talonne Le Pen en 2022 (1,2 point d'écart). "
        "La progression est <b>générale</b> : toutes les régions montent. LFI s'est imposée comme "
        "la principale force de gauche."
    )


# ══════════════════════════════════════════════════════════════════════════
# CHAPITRE 3 — LA CARTE
# ══════════════════════════════════════════════════════════════════════════
def chap_carte(df, geo):
    titre_chapitre(
        "La carte du vote LFI",
        "Où Mélenchon est-il fort, où doit-il progresser ?",
    )

    if df.empty or geo is None:
        st.warning("Carte indisponible (données ou fond de carte manquants).")
        return

    c1, c2 = st.columns([1, 2])
    annee = c1.selectbox("Année", [2012, 2017, 2022], index=2)
    indicateur = c2.radio("Indicateur", ["Score Mélenchon", "Participation", "Abstention"],
                          horizontal=True)
    colonne = {"Score Mélenchon": "pct_melenchon", "Participation": "pct_participation",
               "Abstention": "pct_abstention"}[indicateur]
    # échelles continues assorties au thème sombre
    ech_lfi = [[0, "#FFE3E3"], [0.5, "#E2001A"], [1, "#8B0012"]]
    ech_part = [[0, "#E3F2FD"], [0.5, "#1976D2"], [1, "#0D47A1"]]
    ech_abst = [[0, "#FFF3E0"], [0.5, "#FB8C00"], [1, "#E65100"]]
    echelle = (ech_lfi if indicateur == "Score Mélenchon"
               else ech_part if indicateur == "Participation" else ech_abst)

    df_an = df[df["annee"] == annee].copy()
    df_an["code"] = df_an["code"].astype(str).str.strip().str.zfill(2)
    df_an = df_an[df_an["code"].isin(CODES_METRO) & df_an[colonne].notna()]

    col_carte, col_class = st.columns([3, 2])
    with col_carte:
        fig = px.choropleth(df_an, geojson=geo, locations="code",
                            featureidkey="properties.code", color=colonne,
                            hover_name="region", color_continuous_scale=echelle)
        fig.update_geos(fitbounds="locations", visible=False, bgcolor="rgba(0,0,0,0)")
        fig.update_layout(height=480, margin=dict(l=0, r=0, t=10, b=0),
                          paper_bgcolor="rgba(0,0,0,0)", font_color="#2A2A38",
                          coloraxis_colorbar=dict(title=indicateur))
        st.plotly_chart(fig, width='stretch')
    with col_class:
        st.markdown(f"**Classement — {indicateur} ({annee})**")
        rang = df_an[["region", colonne]].sort_values(colonne, ascending=False).reset_index(drop=True)
        rang.index += 1
        rang.columns = ["Région", indicateur]
        rang[indicateur] = rang[indicateur].round(1).astype(str) + " %"
        st.dataframe(rang, width='stretch', height=440)

    if indicateur == "Score Mélenchon" and annee == 2022:
        a_retenir(
            "LFI est très forte en <b>Île-de-France (30 %)</b> et en <b>Occitanie</b>, "
            "plus faible en <b>Corse</b> et dans le <b>Grand Est</b>. "
            "Son fief, ce sont les grandes agglomérations et le sud."
        )
    else:
        a_retenir(
            "La carte se filtre par année et par indicateur. La participation baisse partout "
            "entre 2012 et 2022 — et l'abstention est la plus forte là où LFI pourrait gagner des voix."
        )


# ══════════════════════════════════════════════════════════════════════════
# CHAPITRE 4 — QUI VOTE LFI
# ══════════════════════════════════════════════════════════════════════════
def chap_electorat(df, socio):
    titre_chapitre(
        "Qui vote pour LFI ?",
        "Le portrait des électeurs de Mélenchon en 2022 (sondage Ipsos sortie des urnes).",
    )

    st.markdown("#### LFI, le parti des jeunes")
    ages = ["18-24", "25-34", "35-49", "50-59", "60-69", "70+"]
    score_age = [31, 34, 24, 18, 12, 9]
    fig = go.Figure(go.Bar(x=ages, y=score_age, marker_color=ROUGE,
                           text=score_age, texttemplate="%{text} %", textposition="outside"))
    fig.add_hline(y=22, line_dash="dash", line_color="rgba(0,0,0,0.4)",
                  annotation_text="moyenne nationale (22 %)", annotation_position="top right")
    fig.update_yaxes(range=[0, 42], title="% qui votent Mélenchon")
    st.plotly_chart(style_graphe(fig, 340), width='stretch')
    st.caption("Plus de **30 %** des moins de 35 ans votent Mélenchon — deux fois plus que les seniors.")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Par catégorie sociale")
        csp = ["Cadres", "Prof. interm.", "Employés", "Ouvriers", "Chômeurs"]
        score_csp = [27, 24, 23, 22, 30]
        fig2 = go.Figure(go.Bar(x=score_csp, y=csp, orientation="h", marker_color=ROUGE,
                                text=score_csp, texttemplate="%{text} %", textposition="outside"))
        fig2.update_xaxes(range=[0, 36])
        st.plotly_chart(style_graphe(fig2, 300), width='stretch')
        st.caption("Vote homogène, sauf un pic chez les **chômeurs (30 %)**.")
    with col2:
        st.markdown("#### Par type de commune")
        communes = ["Grandes villes", "Villes moyennes", "Petites villes", "Rural"]
        score_comm = [25, 22, 21, 20]
        fig3 = go.Figure(go.Bar(x=score_comm, y=communes, orientation="h",
                                marker_color=["#E2001A", "#F0334A", "#F76E7E", "#FBA9B3"],
                                text=score_comm, texttemplate="%{text} %", textposition="outside"))
        fig3.update_xaxes(range=[0, 30])
        st.plotly_chart(style_graphe(fig3, 300), width='stretch')
        st.caption("Plus fort dans les **grandes villes**, plus faible en **zone rurale**.")

    a_retenir(
        "L'électeur type LFI est <b>jeune, urbain, et populaire</b>. 54 % de l'électorat a moins "
        "de 35 ans. Le problème : ces profils (jeunes, quartiers populaires) sont aussi ceux qui "
        "s'abstiennent le plus. Mobiliser, c'est le nerf de la guerre."
    )

    # ── Croisement avec les données sociales (INSEE) ──────────────────────
    st.divider()
    st.markdown("#### Croisement avec les données sociales (INSEE)")
    st.write("On croise le score LFI 2022 par région avec deux indicateurs INSEE : "
             "le **niveau de vie médian** et le **taux de chômage**.")

    if df.empty or socio.empty:
        st.info("Données sociales indisponibles.")
        return

    df22 = df[(df["annee"] == 2022) & df["pct_melenchon"].notna()].copy()
    df22["code_num"] = pd.to_numeric(df22["code"], errors="coerce")
    m = socio.merge(df22[["code_num", "pct_melenchon"]],
                    left_on="Code_region", right_on="code_num", how="inner")

    if len(m) >= 3:
        import numpy as np
        col_a, col_b = st.columns(2)
        with col_a:
            fig = px.scatter(m, x="niveau_vie_median", y="pct_melenchon",
                             hover_name="Region", color_discrete_sequence=[LFI_C])
            z = np.polyfit(m["niveau_vie_median"], m["pct_melenchon"], 1)
            xs = np.linspace(m["niveau_vie_median"].min(), m["niveau_vie_median"].max(), 50)
            fig.add_trace(go.Scatter(x=xs, y=np.poly1d(z)(xs), mode="lines",
                                     line=dict(color=ACCENT2, dash="dash"), name="tendance"))
            fig.update_traces(marker=dict(size=11))
            fig.update_xaxes(title="Niveau de vie médian (€/mois)")
            fig.update_yaxes(title="Score LFI 2022 (%)")
            st.plotly_chart(style_graphe(fig, 330, "Niveau de vie vs vote LFI"), width='stretch')
        with col_b:
            fig2 = px.scatter(m, x="taux_chomage", y="pct_melenchon",
                              hover_name="Region", color_discrete_sequence=[LFI_C])
            fig2.update_traces(marker=dict(size=11))
            fig2.update_xaxes(title="Taux de chômage (%)")
            fig2.update_yaxes(title="Score LFI 2022 (%)")
            st.plotly_chart(style_graphe(fig2, 330, "Chômage vs vote LFI"), width='stretch')

        r_nv = np.corrcoef(m["niveau_vie_median"], m["pct_melenchon"])[0, 1]
        r_ch = np.corrcoef(m["taux_chomage"], m["pct_melenchon"])[0, 1]
        c1, c2 = st.columns(2)
        carte_kpi(c1, f"r = {r_nv:.2f}", "corrélation niveau de vie ↔ LFI (positive)")
        carte_kpi(c2, f"r = {r_ch:.2f}", "corrélation chômage ↔ LFI (faible)")

        a_retenir(
            "Surprise : au niveau régional, LFI est plus fort là où le <b>niveau de vie est élevé</b> "
            "(r ≈ 0,70), et <b>pas</b> corrélé au chômage. C'est l'<b>effet métropole</b> : les régions "
            "riches (Île-de-France, Auvergne-Rhône-Alpes) abritent les grandes villes, fiefs de LFI. "
            "⚠️ Cela ne veut pas dire que les riches votent LFI — au niveau individuel, LFI reste le "
            "vote des jeunes et des milieux populaires. C'est le « piège écologique » à connaître."
        )


# ══════════════════════════════════════════════════════════════════════════
# CHAPITRE 5 — LE SIGNAL 2024
# ══════════════════════════════════════════════════════════════════════════
def chap_europeennes(df_euro, geo):
    titre_chapitre(
        "Le signal des européennes 2024",
        "Le dernier scrutin national : un avertissement pour LFI.",
    )
    st.warning(
        "Une européenne se compare mal à une présidentielle (forte abstention, vote de liste). "
        "On la lit comme un **contexte récent**, pas comme une 4ᵉ présidentielle.",
        icon="⚠️",
    )

    if df_euro.empty:
        st.error("Fichier européennes 2024 introuvable.")
        return

    listes = ["RN", "Renaissance", "PS_Glucksmann", "LFI", "LR", "EELV", "Reconquete", "PCF"]
    noms = {"RN": "RN (Bardella)", "Renaissance": "Renaissance (Hayer)",
            "PS_Glucksmann": "PS (Glucksmann)", "LFI": "LFI (Aubry)", "LR": "LR (Bellamy)",
            "EELV": "EELV (Toussaint)", "Reconquete": "Reconquête (Maréchal)", "PCF": "PCF (Léon)"}
    exp = df_euro["Exprimes"].sum()
    nat = {noms[l]: round(df_euro[l].sum() / exp * 100, 1) for l in listes}
    nat = dict(sorted(nat.items(), key=lambda x: x[1]))

    st.markdown("#### Résultat national des européennes 2024")
    fig = go.Figure(go.Bar(
        x=list(nat.values()), y=list(nat.keys()), orientation="h",
        marker_color=couleurs_pour(nat.keys()),
        text=list(nat.values()), texttemplate="%{text} %", textposition="outside",
    ))
    fig.update_xaxes(range=[0, 36], title="% des exprimés")
    st.plotly_chart(style_graphe(fig, 380), width='stretch')

    c1, c2, c3 = st.columns(3)
    carte_kpi(c1, "9,9 %", "LFI (−12 pts vs présidentielle)")
    carte_kpi(c2, "13,8 %", "PS-Glucksmann (passe devant)")
    carte_kpi(c3, "31,4 %", "RN (large vainqueur)")

    st.write("")
    if geo is not None:
        st.markdown("#### Mais LFI garde ses bastions")
        df_c = df_euro.copy()
        df_c["code"] = df_c["Code_region"].astype(str).str.strip().str.zfill(2)
        df_c = df_c[df_c["code"].isin(CODES_METRO)]
        fig2 = px.choropleth(df_c, geojson=geo, locations="code",
                             featureidkey="properties.code", color="% LFI",
                             hover_name="Region",
                             color_continuous_scale=[[0, "#FFE3E3"], [0.5, "#E2001A"], [1, "#8B0012"]])
        fig2.update_geos(fitbounds="locations", visible=False, bgcolor="rgba(0,0,0,0)")
        fig2.update_layout(height=420, margin=dict(l=0, r=0, t=10, b=0),
                           paper_bgcolor="rgba(0,0,0,0)", font_color="#D7D9E8")
        st.plotly_chart(fig2, width='stretch')
        st.caption("Même aux européennes, LFI reste forte en **Île-de-France (18,6 %)** et en Outre-mer.")

    a_retenir(
        "Aux européennes, LFI chute à 9,9 % et se fait dépasser par le PS de Glucksmann (13,8 %). "
        "La gauche est <b>éclatée</b> et l'électorat LFI se démobilise hors présidentielle. "
        "Deux enjeux clés pour 2027 : <b>l'union</b> et <b>la mobilisation</b>."
    )


# ══════════════════════════════════════════════════════════════════════════
# CHAPITRE 6 — LE SIMULATEUR
# ══════════════════════════════════════════════════════════════════════════
def chap_simulateur(df, df_euro):
    titre_chapitre(
        "Simuler la présidentielle 2027",
        "Ajuste les paramètres et regarde le score projeté de LFI.",
    )

    lfi_euro_nat = 9.86
    reservoir_nat = round(21.95 - lfi_euro_nat, 1)

    st.markdown("#### Les leviers")
    col1, col2 = st.columns(2)
    with col1:
        union = st.selectbox("🤝 Union à gauche",
                             ["LFI seule", "LFI + PCF + EELV", "Union totale (PS inclus)"])
        part = st.slider("📊 Variation de la participation (%)", -8.0, 8.0, 2.0, 0.5)
        jeunes = st.slider("👥 Mobilisation des jeunes (%)", -15.0, 15.0, 5.0, 1.0)
    with col2:
        candidat = st.selectbox("🎙️ Candidat",
                                ["Mélenchon", "Nouveau candidat", "Candidat de compromis"])
        rn = st.slider("📉 Score estimé du RN (%)", 25.0, 40.0, 32.0, 0.5)
        sensibilite = st.slider("🎯 Calibrage par le réservoir 2024", 0.0, 1.0, 0.5, 0.1,
                                help="Utilise l'écart présidentielle/européennes 2024 pour calibrer "
                                     "l'impact de la mobilisation.")

    base = 21.95
    bonus_union = {"LFI seule": 0.0, "LFI + PCF + EELV": 2.8, "Union totale (PS inclus)": 6.5}[union]
    bonus_candidat = {"Mélenchon": 0.0, "Nouveau candidat": 1.5, "Candidat de compromis": -2.0}[candidat]
    mobilisation_brute = part * 0.4 + jeunes * 0.15
    coef_reservoir = 1 + sensibilite * (reservoir_nat / 12 - 1)
    effet_mobilisation = round(mobilisation_brute * coef_reservoir, 2)
    effet_vote_utile = max(0, (rn - 30) * 0.12)
    tendance = 1.5
    score = base + bonus_union + bonus_candidat + effet_mobilisation + effet_vote_utile + tendance
    score = round(max(10, min(score, 45)), 1)

    st.divider()

    # resultat
    col_score, col_detail = st.columns([2, 3])
    with col_score:
        couleur = "#2E7D32" if score >= 20 else "#F59E0B" if score >= 18 else ROUGE_FONCE
        st.markdown(
            f'<div class="kpi" style="padding:1.5rem 0.5rem;">'
            f'<div class="val" style="font-size:3rem;color:{couleur};">{score} %</div>'
            f'<div class="lbl">score projeté LFI au 1er tour 2027</div></div>',
            unsafe_allow_html=True,
        )
        st.write("")
        if score >= 20:
            qualifie, coul_q = "✅ Qualification probable", "#2E7D32"
        elif score >= 18:
            qualifie, coul_q = "⚠️ Qualification incertaine", "#F59E0B"
        else:
            qualifie, coul_q = "❌ Qualification improbable", ROUGE_FONCE
        st.markdown(f"<p style='text-align:center;font-size:1.2rem;font-weight:700;color:{coul_q};'>"
                    f"{qualifie}</p>", unsafe_allow_html=True)
        st.caption(f"vs 21,95 % en 2022 ({score - base:+.1f} pts) · seuil estimé ~18-20 % · "
                   f"entre 18 et 20 % la qualification reste incertaine")
    with col_detail:
        detail = {"Base 2022": base, "Tendance": tendance, "Union": bonus_union,
                  "Mobilisation": effet_mobilisation, "Vote utile": round(effet_vote_utile, 1),
                  "Candidat": bonus_candidat}
        coul = [ROUGE if v >= 0 else GRIS for v in detail.values()]
        fig = go.Figure(go.Bar(x=list(detail.keys()), y=list(detail.values()),
                               marker_color=coul, text=list(detail.values()),
                               texttemplate="%{text}", textposition="outside"))
        st.plotly_chart(style_graphe(fig, 320, "D'où vient ce score ? (en points)"),
                        width='stretch')

    st.info(
        f"**Le signal 2024** : aux européennes, LFI n'a fait que {lfi_euro_nat:.1f} % contre 22 % "
        f"à la présidentielle. Ces **{reservoir_nat} points** d'écart sont le réservoir d'électeurs "
        f"à remobiliser. Le curseur « calibrage » règle à quel point on s'appuie sur ce signal.",
        icon="🎯",
    )

    # projection regionale
    if not df.empty:
        st.markdown("#### Projection par région")
        df22 = df[(df["annee"] == 2022) & df["pct_melenchon"].notna() & df["code"].isin(CODES_METRO)].copy()
        reservoir_region = {}
        if not df_euro.empty:
            euro = df_euro.copy()
            euro["code"] = euro["Code_region"].astype(str).str.strip().str.zfill(2)
            serie = euro.set_index("code")["% LFI"]
            for _, r in df22.iterrows():
                e = serie.get(r["code"])
                if e is not None:
                    reservoir_region[r["code"]] = r["pct_melenchon"] - e
        res_moyen = (sum(reservoir_region.values()) / len(reservoir_region)
                     if reservoir_region else reservoir_nat)

        def projeter(row):
            fixe = bonus_union + bonus_candidat + effet_vote_utile + tendance
            res = reservoir_region.get(row["code"], res_moyen)
            coef = 1 + sensibilite * (res / res_moyen - 1) if res_moyen else 1
            return row["pct_melenchon"] + fixe + mobilisation_brute * coef

        df22["proj"] = df22.apply(projeter, axis=1).clip(8, 42).round(1)
        df22 = df22.sort_values("proj", ascending=True)
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(y=df22["region"], x=df22["pct_melenchon"], orientation="h",
                              name="2022 (réel)", marker_color=CORAIL_PALE))
        fig2.add_trace(go.Bar(y=df22["region"], x=(df22["proj"] - df22["pct_melenchon"]),
                              orientation="h", name="gain projeté 2027", marker_color=ACCENT))
        fig2.update_layout(barmode="stack", legend=dict(orientation="h", y=1.08))
        fig2.update_xaxes(title="% des exprimés")
        st.plotly_chart(style_graphe(fig2, 460), width='stretch')

    a_retenir(
        "Dans un scénario d'<b>union + mobilisation</b>, LFI dépasse facilement le seuil du 2ᵉ tour. "
        "Le levier le plus puissant est l'union à gauche (jusqu'à +6,5 pts). Sans union et sans "
        "mobilisation, la qualification redevient incertaine."
    )


# ══════════════════════════════════════════════════════════════════════════
# CHAPITRE 7 — LE VERDICT
# ══════════════════════════════════════════════════════════════════════════
def chap_verdict():
    titre_chapitre(
        "Le verdict",
        "LFI peut-elle gagner ? Trois conditions et trois scénarios.",
    )

    st.markdown("#### Les 3 leviers pour 2027")
    c1, c2, c3 = st.columns(3)
    c1.markdown("##### 🎯 Mobiliser")
    c1.write("Dans les quartiers populaires, l'abstention atteint 29 %. Ce sont des électeurs "
             "proches de LFI. **Potentiel : +3 à +5 pts.**")
    c2.markdown("##### 🤝 Unir la gauche")
    c2.write("En 2022, le reste de la gauche pesait ~9 pts hors LFI. Un accord en ramènerait une "
             "partie. **Potentiel : +3 à +6 pts.**")
    c3.markdown("##### 👥 Capter les jeunes")
    c3.write("Plus de 30 % des -35 ans votent LFI, mais ils s'abstiennent beaucoup. "
             "**Potentiel : +1 à +2 pts.**")

    st.divider()

    st.markdown("#### Trois scénarios")
    scen = pd.DataFrame({
        "Scénario": ["😟 Pessimiste", "🙂 Réaliste", "😀 Optimiste"],
        "Conditions": ["LFI seule, faible mobilisation",
                       "Union légère (PCF+EELV), mobilisation normale",
                       "Union totale, forte mobilisation jeunesse"],
        "Score estimé": ["~18 %", "~22-24 %", "~26-28 %"],
        "2ᵉ tour ?": ["Incertain", "Probable", "Très probable"],
    })
    st.table(scen)

    st.markdown(
        "<div style='background:linear-gradient(120deg,#A4001A 0%,#E2001A 50%,#FF5C45 100%);"
        "color:white;border-radius:18px;padding:1.8rem;text-align:center;margin-top:0.5rem;"
        "box-shadow:0 12px 40px rgba(226,0,26,0.40);'>"
        f"<div style='font-size:1.3rem;font-weight:800;'>En résumé</div>"
        f"<div style='font-size:1.05rem;margin-top:0.5rem;opacity:0.95;'>"
        f"Avec +10,9 pts en 10 ans, LFI a les moyens d'atteindre le 2ᵉ tour en 2027. "
        f"La clé tient en deux mots : <b>union</b> et <b>mobilisation</b>. "
        f"Et les sondages sous-estiment historiquement LFI.</div></div>",
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════
def main():
    df = charger_donnees()
    df_euro = charger_europeennes()
    socio = charger_socio()
    geo = charger_carte()

    # bandeau d'en-tête
    st.markdown(
        "<div class='hero'>"
        "<div class='t'>🗳️ Présidentielle 2027 — La France Insoumise</div>"
        "<div class='s'>Analyse électorale &amp; data storytelling · 2012 → 2027</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    onglets = st.tabs([
        "🎯 Contexte",
        "📈 L'ascension",
        "🗺️ La carte",
        "👥 Qui vote LFI",
        "🇪🇺 Signal 2024",
        "🔮 Simuler 2027",
        "✅ Le verdict",
    ])
    with onglets[0]:
        chap_contexte()
    with onglets[1]:
        chap_ascension(df)
    with onglets[2]:
        chap_carte(df, geo)
    with onglets[3]:
        chap_electorat(df, socio)
    with onglets[4]:
        chap_europeennes(df_euro, geo)
    with onglets[5]:
        chap_simulateur(df, df_euro)
    with onglets[6]:
        chap_verdict()

    st.write("")
    st.caption("Sources : Ministère de l'Intérieur (data.gouv.fr) · INSEE · Ipsos · Odoxa  —  "
               "Projet fil rouge B3 DATA IA")


if __name__ == "__main__":
    main()
