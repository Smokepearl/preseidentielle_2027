# Présidentielle 2027 - Analyse électorale LFI

Projet fil rouge - B3 DATA IA

## Le sujet

Analyser les résultats des présidentielles de 2012, 2017 et 2022 pour comprendre la
progression de La France Insoumise et estimer ses chances en 2027. Le rendu final est
une application Streamlit interactive avec un simulateur.

## Les fichiers

- `app_lfi_2027.py` : l'application Streamlit
- `analyse_electorale.ipynb` : notebook d'analyse des données (graphiques, comparaisons)
- `modelisation_2027.ipynb` : notebook de prédiction (régression + scénarios)
- `elections_2012_construction.ipynb` : construction du fichier 2012
- `construction_2017.ipynb` : construction du fichier 2017
- `construction_europeennes_2024.ipynb` : construction du fichier européennes 2024
- `construction_socio.ipynb` : construction du fichier de données sociales (INSEE)
- `data_brut/` : les données brutes téléchargées du Ministère de l'Intérieur
- `data_clean/` : les données nettoyées et prêtes à l'emploi
- `regions_france.geojson` : fond de carte des régions
- `DATASETS.md` : liste détaillée de tous les datasets et leurs sources

## Installation

```
pip install -r requirements.txt
```

## Lancer l'application

```
python -m streamlit run app_lfi_2027.py
```

L'app s'ouvre dans le navigateur (http://localhost:8501).

## Les pages de l'app

- Accueil : contexte, sondages, progression de Mélenchon
- Évolution 2012-2022 : résultats par année, par région, participation
- Carte des votes : carte de France colorée selon le score
- Électorat LFI : profil des électeurs (âge, CSP, commune)
- Européennes 2024 : le dernier scrutin national, contexte pour 2027
- Simulateur 2027 : on ajuste les paramètres et on voit le score projeté
- Conclusion : recommandations

## Sources

- Résultats : Ministère de l'Intérieur (data.gouv.fr)
- Participation et socio : INSEE
- Profil des électeurs : sondage Ipsos sortie des urnes 2022
- Sondages 2027 : Odoxa (mai 2026)

Le détail de chaque fichier de données et de sa source est dans `DATASETS.md`.

## Principaux résultats

- Mélenchon : 11 % en 2012, 19,6 % en 2017, 22 % en 2022 (+10,9 pts)
- 3e en 2022, à 1,2 point du 2e tour
- Électorat jeune et urbain
- Scénario réaliste 2027 : autour de 22-24 %
