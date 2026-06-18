# Questions probables à l'oral — Réponses prêtes

Préparation soutenance · Projet Présidentielle 2027 (LFI) · B3 DATA IA

---

## 1. Questions sur Streamlit

**Q : Pourquoi avoir choisi Streamlit (et pas Dash ou Power BI) ?**
Le brief imposait Streamlit ou Dash. On a pris Streamlit car c'est plus rapide à développer
(tout en Python, pas de HTML/callbacks comme Dash), et il est très adapté au data storytelling.
Power BI aurait été hors brief (no-code, pas de vrai code Python).

**Q : Comment fonctionne Streamlit techniquement ?**
À chaque interaction de l'utilisateur (clic, curseur), Streamlit **réexécute tout le script
de haut en bas**. C'est simple mais ça peut être lourd, donc on optimise avec le cache.

**Q : C'est quoi `@st.cache_data` que vous utilisez ?**
C'est un décorateur qui **met en cache le résultat d'une fonction**. On l'a mis sur nos
fonctions de chargement (`charger_donnees`, `charger_carte`...). Comme ça, les fichiers ne sont
lus qu'une seule fois, pas à chaque clic. Ça rend l'app beaucoup plus rapide.

**Q : Comment marche la navigation entre vos pages ?**
On utilise `st.tabs()` : 7 onglets, un par chapitre du récit. Chaque onglet appelle une
fonction (`chap_contexte`, `chap_carte`...). On a choisi un récit guidé pour le côté storytelling.

**Q : Comment le simulateur recalcule en direct ?**
Les curseurs (`st.slider`) renvoient une valeur. Quand on les bouge, Streamlit réexécute le
script, recalcule le score avec la nouvelle valeur, et réaffiche le graphique. Tout est
recalculé instantanément côté serveur.

**Q : L'app est-elle déployée en ligne ?**
Non, déploiement **local** (`streamlit run`), comme demandé dans le brief. On pourrait la
déployer gratuitement sur Streamlit Community Cloud comme évolution.

**Q : Comment gérez-vous la carte de France ?**
On utilise un fichier **GeoJSON** des régions (contours géographiques) + `plotly.choropleth`.
On a stocké le GeoJSON en local car le réseau de l'école bloquait le téléchargement (problème
de certificat SSL).

**Q : Pourquoi Plotly et pas Matplotlib pour l'app ?**
Plotly est **interactif** (survol, zoom, infobulles) — parfait pour une app web. Matplotlib,
on l'a gardé pour les notebooks d'analyse (graphiques statiques).

---

## 2. Questions sur les données

**Q : D'où viennent vos données ?**
Résultats électoraux : **Ministère de l'Intérieur** via data.gouv.fr (2012, 2017, 2022 +
européennes 2024). Données sociales : **INSEE** (chômage, niveau de vie). Profil des électeurs :
sondage **Ipsos** sortie des urnes. Sondages 2027 : **Odoxa**.

**Q : Comment avez-vous nettoyé les données ?**
On a séparé `data_brut/` (fichiers officiels téléchargés) et `data_clean/` (fichiers traités).
Un notebook de construction par scrutin documente le nettoyage. On a standardisé les colonnes
pour que les 3 années soient comparables.

**Q : Quelle a été la plus grosse difficulté sur les données ?**
Trois choses :
1. En 2012 il y avait **22 anciennes régions** → on les a agrégées vers les 13 actuelles (réforme 2015).
2. Le format ministère est « large » (un candidat = 7 colonnes répétées) → parsing par position.
3. On a détecté qu'un fichier était **mal nommé** (« 2017_bureaux » contenait en fait du 2022).

**Q : Pourquoi par région et pas par commune ou département ?**
Choix de lisibilité pour le storytelling (13 régions = carte claire). Les données par commune
existent mais c'est beaucoup plus lourd. C'est une évolution possible du projet.

---

## 3. Questions sur le modèle / simulateur

**Q : Votre modèle prédit-il vraiment le résultat de 2027 ?**
Non, et on l'assume. C'est une **projection de tendance + des scénarios**, pas une prédiction
fiable. Avec seulement 3 élections (3 points), on ne peut pas faire de vraie prédiction
statistique. On explore des hypothèses, on ne prédit pas l'avenir.

**Q : Pourquoi une simple régression linéaire ?**
Avec 3 points de données, un modèle complexe (random forest, etc.) sur-apprendrait. La
régression linéaire donne une tendance simple et honnête. On a aussi testé un Random Forest
dans le notebook, mais surtout pour la pédagogie (feature importance).

**Q : D'où viennent les coefficients de votre simulateur ?**
Ce sont des **hypothèses calibrées** à partir de l'analyse (ex : +0,4 pt de LFI par +1 % de
participation, +6,5 pts pour une union totale). Ce ne sont pas des valeurs « exactes » : le
simulateur sert à **explorer des scénarios**, pas à donner un chiffre garanti. On l'assume.

**Q : C'est quoi le « signal de mobilisation 2024 » ?**
L'écart entre le score LFI à la présidentielle 2022 (22 %) et aux européennes 2024 (9,9 %) =
~12 points. C'est le réservoir d'électeurs « intermittents ». On l'utilise pour **calibrer**
l'effet de la mobilisation dans le simulateur, sans mélanger les deux types de scrutin dans le
modèle (une européenne ne se compare pas à une présidentielle).

**Q : Pourquoi ne pas avoir mis les européennes dans la régression ?**
Justement parce qu'une européenne et une présidentielle ne sont pas comparables (abstention,
vote différent). Les mélanger fausserait la tendance. On les utilise comme **indicateur** à côté.

---

## 4. Questions sur l'analyse / interprétation

**Q : Votre croisement montre que LFI est fort dans les régions riches. Les riches votent LFI ?**
Non, c'est un piège ! Au niveau **régional**, LFI est corrélé au niveau de vie élevé (r=0,70)
à cause de l'**effet métropole** : les régions riches (Île-de-France, Auvergne-Rhône-Alpes)
contiennent les grandes villes, fiefs de LFI. Au niveau **individuel**, LFI reste le vote des
jeunes et des milieux populaires. C'est le « piège écologique » : on ne déduit pas l'individuel
de l'agrégé.

**Q : Le projet est « mandaté par LFI ». Est-ce objectif ?**
Les données et les méthodes sont neutres et sourcées. L'angle LFI définit la **problématique**
(« LFI peut-elle se qualifier ? »), pas les résultats. On présente aussi les limites et les
scénarios pessimistes, donc ce n'est pas un travail de propagande.

**Q : Quelle est votre conclusion ?**
LFI a progressé de +10,9 pts en 10 ans et était à 1,2 pt du 2ᵉ tour en 2022. Sa qualification
en 2027 dépend de deux leviers : **l'union à gauche** et **la mobilisation**. C'est jouable,
mais pas garanti.

---

## 5. Questions sur l'organisation / le code

**Q : Comment est organisé votre code ?**
- `app_lfi_2027.py` : l'application (fonctions de chargement + une fonction par chapitre)
- des notebooks séparés pour la construction des données, l'analyse et la modélisation
- `data_brut/` et `data_clean/` pour les données
- `README.md` et `DATASETS.md` pour la documentation

**Q : Comment avez-vous réparti le travail à deux ?**
(À adapter à votre cas réel) On s'est réparti par blocs : collecte/nettoyage, analyse,
modélisation, app, design, doc — avec des points de mise en commun réguliers.

**Q : Avez-vous utilisé Git ?**
(Répondre selon votre cas. Si oui : versioning du code. Si non : assumer et dire que c'est une
bonne pratique à ajouter.)

**Q : Comment relance-t-on votre application ?**
`pip install -r requirements.txt` puis `python -m streamlit run app_lfi_2027.py`. On a aussi un
fichier `lancer_app.bat` pour lancer en double-clic.

---

## 6. Réflexes pour bien répondre

- **Assumer les limites** (modèle simple, coefficients estimés) : ça montre de la maturité.
- **Distinguer** « prédiction » et « scénario / exploration ».
- Si tu ne sais pas : « Bonne question, c'est une piste qu'on n'a pas creusée, mais on ferait
  comme ça... » — ne jamais inventer.
- Toujours relier au **brief** : collecte, nettoyage, analyse, modèle, app, déploiement local.
