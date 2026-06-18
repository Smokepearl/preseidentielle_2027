# Datasets du projet

Tous les fichiers de données sont rangés en deux dossiers :

- `data_brut/` : les fichiers téléchargés tels quels (avant nettoyage)
- `data_clean/` : les fichiers après nettoyage / fusion / standardisation

Le geojson des régions (`regions_france.geojson`) est gardé à la racine car c'est un
fichier technique (fond de carte), pas un résultat électoral.

---

## 1. Données brutes (`data_brut/`)

Fichiers officiels du Ministère de l'Intérieur, récupérés sur data.gouv.fr. On ne les
modifie pas, ils servent de point de départ.

| Fichier | Année | Contenu | Source |
|---------|-------|---------|--------|
| `presidentielle_2012_raw.xls` | 2012 | Résultats 1er tour, anciennes régions (22 régions d'avant la réforme 2015) | [data.gouv.fr - présidentielle 2012](https://www.data.gouv.fr/api/1/datasets/r/adac47aa-6436-47aa-b1c0-f35882187970) |
| `presidentielle_2017_raw.xlsx` | 2017 | Résultats 1er tour par bureau de vote, métropole (11 candidats) | [data.gouv.fr - données élections](https://www.data.gouv.fr/pages/donnees-des-elections) |
| `presidentielle_2022_bureaux_raw.xlsx` | 2022 | Résultats 1er tour par bureau de vote, France entière (12 candidats) | [data.gouv.fr - présidentielle 2022](https://www.data.gouv.fr/datasets/election-presidentielle-des-10-et-24-avril-2022-resultats-definitifs-du-1er-tour) |
| `presidentielle_2022_regions_raw.xlsx` | 2022 | Résultats 1er tour par région (format ministère) | [data.gouv.fr - présidentielle 2022](https://www.data.gouv.fr/datasets/election-presidentielle-des-10-et-24-avril-2022-resultats-definitifs-du-1er-tour) |
| `europeennes_2024_regions_raw.xlsx` | 2024 | Résultats européennes par région (38 listes) | [data.gouv.fr - européennes 2024](https://www.data.gouv.fr/datasets/resultats-des-elections-europeennes-du-9-juin-2024) |

> Note : le fichier par bureau 2022 était à l'origine mal nommé (`resultats_2017_bureaux.xlsx`)
> alors qu'il contient en réalité les candidats de 2022 (Zemmour, Jadot, Pécresse...). Il a
> été renommé correctement.

---

## 2. Données nettoyées (`data_clean/`)

Fichiers obtenus après traitement (sélection des colonnes, agrégation des régions, calcul
des pourcentages). Les trois fichiers ont la même structure pour pouvoir comparer les années.

| Fichier | Année | Contenu | Construit par |
|---------|-------|---------|---------------|
| `elections_2012_clean.csv` / `.xlsx` | 2012 | Résultats par région (13 régions + Outre-mer) | `elections_2012_construction.ipynb` |
| `elections_2017_clean.xlsx` | 2017 | Résultats par région | `construction_2017.ipynb` |
| `elections_2022_clean.csv` | 2022 | Résultats par région (utilisé par l'app) | à partir de `presidentielle_2022_regions_raw.xlsx` |
| `europeennes_2024_clean.csv` | 2024 | Européennes par région, 8 listes principales + % | `construction_europeennes_2024.ipynb` |
| `socio_demographie_regions.csv` | 2021-2022 | Données sociales par région : taux de chômage + niveau de vie médian | `construction_socio.ipynb` |

---

## 3. Fichier de référence (racine)

| Fichier | Contenu | Source |
|---------|---------|--------|
| `regions_france.geojson` | Contours des 13 régions métropolitaines (fond de carte) | [github.com/gregoiredavid/france-geojson](https://github.com/gregoiredavid/france-geojson) |

---

## Sources des données sociales (`socio_demographie_regions.csv`)

- **Taux de chômage par région (2022)** : [INSEE — Chômage dans les régions](https://www.insee.fr/fr/statistiques/7456887)
- **Niveau de vie médian par région (Filosofi 2021)** : [INSEE](https://www.insee.fr/fr/statistiques/7941411) / [Observatoire des inégalités](https://www.inegalites.fr/Les-inegalites-de-revenus-selon-les-regions)

## Chiffres saisis directement dans l'app (pas dans un fichier)

Onglet « Qui vote LFI » (profil sociologique national) :

- **Profil des électeurs (âge, CSP, commune)** : sondage Ipsos / Sopra Steria, sortie des urnes 1er tour 2022
- **Sondages 2027** : Odoxa (mai 2026)

---

## Scrutins couverts

Le projet couvre les **trois dernières présidentielles : 2012, 2017, 2022** (comme demandé
dans le brief), plus les **européennes de 2024** ajoutées en bonus comme contexte récent
(scrutin national le plus proche de 2027). Les européennes sont à interpréter avec prudence :
forte abstention et vote différent d'une présidentielle, donc elles servent de repère de
contexte, pas de 4e présidentielle.
