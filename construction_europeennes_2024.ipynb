{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "intro",
   "metadata": {},
   "source": [
    "# Construction du dataset Européennes 2024\n",
    "\n",
    "En bonus des trois présidentielles, on ajoute les **européennes du 9 juin 2024**, qui sont\n",
    "le scrutin national le plus récent. C'est utile pour le contexte 2027 : on y voit la montée\n",
    "du RN, la percée de Glucksmann (PS) et le recul de LFI par rapport à la présidentielle.\n",
    "\n",
    "⚠️ Attention : une européenne se compare mal à une présidentielle (abstention bien plus forte,\n",
    "vote plus protestataire). À utiliser comme **contexte récent**, pas comme une 4e présidentielle.\n",
    "\n",
    "Source : Ministère de l'Intérieur via data.gouv.fr (résultats par région).\n",
    "Le fichier brut a un format \"large\" : 16 colonnes communes puis 38 listes, chacune sur 8 colonnes."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "code",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import os\n",
    "import warnings\n",
    "warnings.filterwarnings('ignore')\n",
    "\n",
    "os.makedirs('data_clean', exist_ok=True)\n",
    "\n",
    "# lecture sans en-tête (on traite par position de colonne)\n",
    "raw = pd.read_excel('data_brut/europeennes_2024_regions_raw.xlsx', header=None)\n",
    "data = raw.iloc[1:].copy()   # on enlève la ligne d'en-tête\n",
    "print('Brut :', raw.shape, '— 18 régions, 38 listes')"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "md2",
   "metadata": {},
   "source": [
    "## Colonnes communes et listes principales\n",
    "\n",
    "On garde les 8 plus grosses listes, repérées par leur numéro de panneau."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "extract",
   "metadata": {},
   "outputs": [],
   "source": [
    "# colonnes communes (par position)\n",
    "df = pd.DataFrame()\n",
    "df['Code_region'] = data[0].values\n",
    "df['Region'] = data[1].values\n",
    "df['Inscrits'] = pd.to_numeric(data[2], errors='coerce').values\n",
    "df['Votants'] = pd.to_numeric(data[3], errors='coerce').values\n",
    "df['Abstentions'] = pd.to_numeric(data[5], errors='coerce').values\n",
    "df['Exprimes'] = pd.to_numeric(data[7], errors='coerce').values\n",
    "\n",
    "# liste principale -> numéro de panneau (chaque liste = bloc de 8 colonnes à partir de la 16)\n",
    "listes = {\n",
    "    'RN': 5,            # Bardella - La France revient\n",
    "    'Renaissance': 11,  # Hayer - Besoin d'Europe\n",
    "    'PS_Glucksmann': 27,# Glucksmann - Réveiller l'Europe\n",
    "    'LFI': 4,           # Aubry - LFI\n",
    "    'LR': 18,           # Bellamy\n",
    "    'EELV': 6,          # Toussaint - Europe Écologie\n",
    "    'Reconquete': 3,    # Maréchal\n",
    "    'PCF': 33,          # Léon - Gauche unie\n",
    "}\n",
    "for nom, panneau in listes.items():\n",
    "    base = 16 + (panneau - 1) * 8\n",
    "    df[nom] = pd.to_numeric(data[base + 4], errors='coerce').values   # +4 = colonne Voix\n",
    "\n",
    "# pourcentages\n",
    "for nom in listes:\n",
    "    df[f'% {nom}'] = (df[nom] / df['Exprimes'] * 100).round(2)\n",
    "df['% Participation'] = (df['Votants'] / df['Inscrits'] * 100).round(2)\n",
    "\n",
    "print(df[['Region', '% RN', '% LFI', '% PS_Glucksmann', '% Renaissance']].to_string(index=False))"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "md3",
   "metadata": {},
   "source": [
    "## Vérification et export"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "export",
   "metadata": {},
   "outputs": [],
   "source": [
    "# totaux nationaux (vérification vs résultats officiels)\n",
    "exp = df['Exprimes'].sum()\n",
    "print(f\"LFI national  : {df['LFI'].sum()/exp*100:.2f} %  (officiel 9,89 %)\")\n",
    "print(f\"RN national   : {df['RN'].sum()/exp*100:.2f} %  (officiel 31,37 %)\")\n",
    "print(f\"PS national   : {df['PS_Glucksmann'].sum()/exp*100:.2f} %  (officiel 13,83 %)\")\n",
    "\n",
    "df.to_csv('data_clean/europeennes_2024_clean.csv', sep=';', index=False, encoding='utf-8-sig')\n",
    "print('\\n✅ Exporté : data_clean/europeennes_2024_clean.csv', df.shape)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
  "language_info": {"name": "python", "version": "3.11"}
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
