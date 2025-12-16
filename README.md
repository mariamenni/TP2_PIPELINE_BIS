TP2_PIPELINE_BIS – Exploration et Enrichissement GEO

1. Présentation du projet

Ce projet a pour objectif d’explorer et d’enrichir des données d’adresses françaises à l’aide de deux APIs :

API Adresse (Base Adresse Nationale - BAN) : pour géocoder les adresses et récupérer latitude, longitude, code postal et ville.

Geo API Gouv (Communes) : pour enrichir les adresses avec des informations complémentaires comme la population et le département.


Le pipeline effectue :

1. **Géocodage et enrichissement** des adresses.
2. **Transformation et nettoyage** des données :
   - Suppression des doublons,
   - Traitement des valeurs manquantes,
   - Normalisation des textes,
3. **Analyse de la qualité des données** (complétude, doublons, score de géocodage).
4. **Production de rapports et visualisations** (carte interactive, population par commune, anomalies).
5. **Utilisation de LLaMA 3.2 locale** pour générer des recommandations d’enrichissement et du code d’analyse automatisé.



## 2.1 Principe de fonctionnement du pipeline

Le pipeline est conçu **modulaire et reproductible**. Chaque composant a un rôle clair :

1. **Fetchers (pipeline/fetchers)**  
   - `AdresseFetcher` : interroge l’API Adresse pour géocoder chaque adresse.  
   - `CommuneFetcher` : interroge Geo API Gouv pour enrichir les adresses avec informations démographiques.  
   - Ces fetchers héritent de `BaseFetcher`, qui gère :
     - les requêtes HTTP avec retry automatique (Tenacity),
     - le rate limiting pour ne pas saturer les APIs,
     - les statistiques d’exécution (`requests_made`, `requests_failed`, `items_fetched`).

2. **Modèles de données (pipeline/models.py)**  
   - `GeocodingResult` : résultat d’une adresse géocodée.  
   - `CommuneInfo` : informations administratives d’une commune.  
   - `EnrichedAddress` : fusion des résultats des deux APIs, prêt pour analyse.  
   - `QualityMetrics` : métriques pour évaluer la qualité du dataset.

3. **Enrichisseur (pipeline/enricher.py)**  
   - `GeoEnricher` coordonne les fetchers pour enrichir les adresses :
     - Appelle `AdresseFetcher.fetch_one()` pour géocoder.
     - Appelle `CommuneFetcher.fetch_one()` pour récupérer infos communes.
     - Produit des objets `EnrichedAddress`.
     - Maintient des statistiques (`total_addresses`, `geocoded`, `enriched`, `failed`).

4. **Transformations et nettoyage (pipeline/transformer.py)**  
   - `DataTransformer` permet de nettoyer et enrichir le dataset :
     - Suppression des doublons,
     - Traitement des valeurs manquantes (`median`, `mean`, `unknown`),
     - Normalisation des colonnes texte (strip, lower),
     - Interaction avec LLaMA 3.2 pour proposer des transformations supplémentaires.

5. **Analyse de qualité (pipeline/quality.py)**  
   - `QualityAnalyzer` calcule :
     - Complétude (pourcentage de valeurs non nulles),
     - Doublons et leur proportion,
     - Taux de succès de géocodage et score moyen,
     - Génère un **grade global**  selon ces métriques.
   - Produit également un **rapport Markdown** pour visualiser la qualité du dataset.

6. **Stockage (pipeline/storage.py)**  
   - `save_raw_json()` : sauvegarde les données brutes en JSON.  
   - `save_parquet()` : sauvegarde les données traitées en Parquet pour analyses rapides.  
   - `load_parquet()` : recharge un fichier Parquet.



2.2 Structure du projet
tp2-exploration/
│
├─ .venv/                        # Environnement virtuel Python
├─ data/                          # Données brutes, traitées et rapports
│  ├─ raw/
│  ├─ processed/
│  └─ reports/
├─ notebooks/                     # Notebooks Jupyter
│  ├─ exploration.ipynb           # Exploration et analyses GEO
│  └─ test.ipynb                  # Tests et exécution du pipeline
├─ pipeline/                      # Modules Python du pipeline
│  ├─ fetchers/                   # Fetchers pour APIs
│  ├─ models.py                   # Modèles de données (GeocodingResult, EnrichedAddress)
│  ├─ main.py                     # Script principal du pipeline
│  ├─ transformer.py              # Nettoyage et transformations
│  ├─ quality.py                  # Analyse qualité
│  ├─ storage.py                  # Lecture/écriture de fichiers
│  ├─ enricher.py                 # Enrichissement GEO
│  └─ config.py                   # Configurations et constantes
├─ tests/                         # Tests unitaires avec pytest
├─ .gitignore
├─ pyproject.toml
├─ main.py
├─ README.md
└─ uv.lock

3. Choix techniques et justifications


| API d’enrichissement : API Adresse + Geo API Gouv           

Les deux APIs sont stables et fiables. L’API Adresse fournit un géocodage précis et rapide, et Geo API Gouv complète avec la population et le département. Cette combinaison permet un enrichissement pertinent et complet pour l’analyse. 


| Pipeline GEO  : Python, Pandas, Plotly, LLaMA       

Pandas pour la manipulation des données, Plotly pour visualisations interactives, et LLaMA pour recommandations et génération de code d’analyse. 


| Tests: pytest                               

 Permet de s’assurer du bon fonctionnement des fetchers, du DataTransformer et de la qualité du pipeline. 

| Stockage :              

JSON pour données brutes, Parquet pour données traitées 
Parquet est rapide et compressé, adapté aux analyses et visualisations. 

| Notebooks                 

exploration.ipynb, test.ipynb        
Séparation claire : `exploration` pour analyses et visualisations, `test` pour tester le pipeline et vérifier les résultats. 


4. Installation et exécution

Cloner le projet :

git clone <repo_url>
cd tp2-exploration


Créer et activer l’environnement virtuel :

python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows


Installer les dépendances :

uv add httpx pandas duckdb litellm python-dotenv tenacity tqdm pyarrow pydantic pytest


Exécuter le pipeline directement :

from pipeline.main import run_pipeline_geo

addresses = [
    "10 Rue de Rivoli 75004 Paris",
    "5 Avenue des Champs Elysées 75008 Paris",
    "1 Place Bellecour 69002 Lyon"
]

stats = run_pipeline_geo(addresses, max_items=10, verbose=True)


Ou ouvrir les notebooks pour l’exploration et le test :

jupyter notebook notebooks/exploration.ipynb
jupyter notebook notebooks/test.ipynb

5. Notebooks
exploration.ipynb:

Analyse et visualisation des données GEO.

Catégorisation du score (Faible, Moyen, Élevé).

Carte interactive des adresses selon leur score.

Visualisation de la population par commune.

Détection des anomalies et doublons.

Recommandations et génération de code d’analyse avec LLaMA 3.2 locale.



test.ipynb:

Test du pipeline GEO complet sur un petit jeu d’adresses.

Vérification de la qualité des données (A, B, C).

Génération de rapports.

Visualisation rapide du dataset enrichi.

Exécution des tests unitaires avec pytest.


6. Tests

Les tests unitaires couvrent :

Fetchers (Adresse et Commune)

DataTransformer (doublons, valeurs manquantes, normalisation)

QualityAnalyzer (calcul des métriques et génération de rapport)

Exemple d’exécution :

pytest tests/ -v --cov=pipeline --cov-report=html


Tous les tests passent, et un rapport de couverture HTML est généré dans htmlcov/.

7. Visualisations incluses

Carte interactive : latitude/longitude des adresses avec score de géocodage.

Population par commune : barres représentant la population totale par commune.

Analyse des anomalies : score faible (<0.5) ou doublons.


8. Conclusion

Ce projet illustre :

L’intégration de plusieurs APIs pour enrichir des données géographiques.

La conception d’un pipeline modulaire, testable et reproductible.

L’usage de LLaMA pour guider l’analyse et générer du code.

La production de visualisations interactives et de rapports de qualité.

L’utilisation des deux APIs permet d’assurer la fiabilité, la complétude et la pertinence des données pour toute analyse géographique et démographique.