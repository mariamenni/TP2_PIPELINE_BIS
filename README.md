#🌍 TP2 Pipeline BIS – Exploration et Enrichissement GEO


##📖 Présentation du projet

Ce projet a pour objectif d’explorer et d’enrichir des données d’adresses françaises en combinant la puissance de deux APIs publiques et l'intelligence artificielle locale.

###Sources de données* 

📍 **API Adresse (Base Adresse Nationale - BAN)** : Géocodage, récupération de la latitude, longitude, code postal et ville.
* 🏙️ **Geo API Gouv (Communes)** : Enrichissement démographique (population, département, etc.).

###Fonctionnalités clés
Le pipeline est entièrement automatisé et réalise les tâches suivantes :

1. **Géocodage et enrichissement** des adresses.
2. **Transformation et nettoyage** (suppression des doublons, gestion des valeurs manquantes, normalisation).
3. **Analyse de la qualité** (complétude, détection d'anomalies, scoring).
4. **Visualisation** (cartes interactives, graphiques démographiques).
5. **Assistance IA** : Utilisation de **LLaMA 3.2** en local pour générer des recommandations et du code d’analyse.



##⚙️ Architecture du Pipeline
Le pipeline est conçu de manière **modulaire et reproductible**.

###1. Fetchers (`pipeline/fetchers`)
Modules responsables de la récupération des données. Ils héritent d'une classe `BaseFetcher` gérant les retries (Tenacity) et le rate limiting.

* `AdresseFetcher` : Interroge l'API BAN.
* `CommuneFetcher` : Interroge Geo API Gouv.

###2. Modèles de données (`pipeline/models.py`)
Utilisation de **Pydantic** pour garantir la structure des données :

* `GeocodingResult` & `CommuneInfo` : Données brutes des APIs.
* `EnrichedAddress` : Résultat final fusionné.
* `QualityMetrics` : Indicateurs de qualité du dataset.

###3. Enrichisseur (`pipeline/enricher.py`)
Le chef d'orchestre `GeoEnricher` coordonne les appels APIs et fusionne les résultats tout en maintenant des statistiques d'exécution.

###4. Transformation (`pipeline/transformer.py`)
Le `DataTransformer` assure la propreté des données :

* Nettoyage des textes (strip, lower).
* Imputation des valeurs manquantes (médiane, moyenne).
* Interaction avec LLaMA pour suggérer des transformations.

###5. Qualité & Stockage

**QualityAnalyzer** :
Calcule un score global (A, B, C) basé sur la complétude et la précision du géocodage.

**Storage** :
Sauvegarde en **JSON** (brut) et **Parquet** (optimisé pour l'analyse).

---

## 📂 Structure du projet

```text
tp2-exploration/
│
├── .venv/                  # Environnement virtuel Python
├── data/                   # Données
│   ├── raw/                # JSON bruts
│   ├── processed/          # Fichiers Parquet
│   └── reports/            # Rapports de qualité Markdown
├── notebooks/
│   ├── exploration.ipynb   # Analyses approfondies, cartes, IA
│   └── test.ipynb          # Tests rapides du pipeline
├── pipeline/               # Code source du pipeline
│   ├── fetchers/           # Modules d'appels API
│   ├── models.py           # Schémas de données
│   ├── main.py             # Point d'entrée
│   ├── transformer.py      # Nettoyage
│   ├── quality.py          # Analyse qualité
│   ├── storage.py          # I/O
│   ├── enricher.py         # Logique d'enrichissement
│   └── config.py           # Configuration
├── tests/                  # Tests unitaires (pytest)
├── main.py                 # Script d'exécution rapide
├── pyproject.toml          # Dépendances (uv/poetry)
└── README.md


##🛠️ Choix techniques| Domaine | Technologies | Justification |
| --- | --- | --- |
| **APIs** | API Adresse + Geo API | Combinaison stable pour obtenir précision géographique et contexte démographique. |
| **Core** | Python, Pandas | Standard de l'industrie pour la manipulation de données. |
| **Visu** | Plotly | Création de cartes et graphiques interactifs. |
| **IA** | LLaMA 3.2 (Local) | Génération de code et analyse sémantique sans envoi de données vers le cloud. |
| **Tests** | Pytest | Assurance qualité sur les fetchers et les transformations. |
| **Stockage** | Parquet | Format colonnaire compressé, idéal pour les performances d'analyse. |

---

##🚀 Installation et Exécution###
1. Cloner le projet
git clone <repo_url>
cd tp2-exploration


###2. Environnement virtuel
# Création
python -m venv .venv

# Activation
source .venv/bin/activate   # Linux/macOS
# ou
.venv\Scripts\activate      # Windows



###3. Installation des dépendances
Ce projet utilise `uv` pour la gestion des paquets.


uv add httpx pandas duckdb litellm python-dotenv tenacity tqdm pyarrow pydantic pytest
# ou via pip
pip install httpx pandas duckdb litellm python-dotenv tenacity tqdm pyarrow pydantic pytest



###4. Utilisation
Vous pouvez lancer le pipeline directement via le script Python :


from pipeline.main import run_pipeline_geo

addresses = [
    "10 Rue de Rivoli 75004 Paris",
    "5 Avenue des Champs Elysées 75008 Paris",
    "1 Place Bellecour 69002 Lyon"
]

# Lancement du pipeline avec verbose
stats = run_pipeline_geo(addresses, max_items=10, verbose=True)



Ou utiliser les **Notebooks Jupyter** :

jupyter notebook notebooks/exploration.ipynb
jupyter notebook notebooks/test.ipynb



##📊 Visualisations et Rapports
Les notebooks génèrent plusieurs types de visualisations :

* 🗺️ **Carte interactive** : Positionnement des adresses avec code couleur selon le score de confiance.
* 📊 **Démographie** : Histogramme de la population par commune identifiée.
* ⚠️ **Anomalies** : Mise en évidence des adresses avec un score de géocodage faible (<0.5) ou des doublons.



##✅ TestsLe projet est couvert par des tests unitaires assurant la robustesse du code (Fetchers, Transformer, Quality).

Pour lancer la suite de tests avec rapport de couverture :

pytest tests/ -v --cov=pipeline --cov-report=html



*Le rapport HTML sera disponible dans le dossier `htmlcov/'

##📝 Conclusion


Ce TP illustre la mise en place d'un pipeline de **Data Engineering moderne** :

1. Intégration d'APIs tierces.
2. Architecture propre (Separation of Concerns).
3. Utilisation de LLM locaux pour l'aide à l'analyse.
4. Focus sur la qualité de la donnée (Data Quality) et la visualisation.
