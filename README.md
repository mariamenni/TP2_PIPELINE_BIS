
```markdown
# 🌍 TP2 Pipeline BIS – Exploration et Enrichissement GEO

## 📖 1. Présentation du projet

Ce projet a pour objectif d’explorer et d’enrichir des données d’adresses françaises à l’aide de deux APIs et d'un modèle d'IA local.

### Sources de données
* 📍 **API Adresse (Base Adresse Nationale - BAN)** : Géocodage, récupération latitude/longitude, code postal et ville.
* 🏙️ **Geo API Gouv (Communes)** : Enrichissement démographique (population, département).

### Fonctionnalités du pipeline
1.  **Géocodage et enrichissement** des adresses.
2.  **Transformation et nettoyage** : suppression des doublons, gestion des valeurs manquantes, normalisation.
3.  **Analyse de la qualité** : complétude, doublons, score de géocodage.
4.  **Visualisation** : carte interactive, population par commune, anomalies.
5.  **Intelligence Artificielle** : Utilisation de **LLaMA 3.2** locale pour générer des recommandations et du code d’analyse.

---

## ⚙️ 2.1 Principe de fonctionnement du pipeline

Le pipeline est conçu **modulaire et reproductible**. Chaque composant a un rôle clair :

1.  **Fetchers (`pipeline/fetchers`)**
    * `AdresseFetcher` : Interroge l’API Adresse (BAN).
    * `CommuneFetcher` : Interroge Geo API Gouv.
    * *BaseFetcher* : Gère les requêtes HTTP, le retry automatique (Tenacity) et le rate limiting.

2.  **Modèles de données (`pipeline/models.py`)**
    * `GeocodingResult` : Résultat brut du géocodage.
    * `CommuneInfo` : Données administratives.
    * `EnrichedAddress` : Objet fusionné prêt pour l'analyse.

3.  **Enrichisseur (`pipeline/enricher.py`)**
    * `GeoEnricher` coordonne les fetchers. Il géocode, récupère les infos communes et produit les objets enrichis.

4.  **Transformations (`pipeline/transformer.py`)**
    * Nettoyage des données (strip, lower).
    * Traitement des valeurs manquantes (médiane, moyenne).
    * Interaction avec LLaMA pour des transformations avancées.

5.  **Analyse de qualité (`pipeline/quality.py`)**
    * Calcul de la complétude et des scores.
    * Génération d'un **grade global** (A, B, C) et d'un rapport Markdown.

6.  **Stockage (`pipeline/storage.py`)**
    * Sauvegarde en **JSON** (données brutes) et **Parquet** (données traitées pour performance).

---

## 📂 2.2 Structure du projet

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

```

---

##🛠️ 3. Choix techniques| Composant | Technologie | Justification |
| --- | --- | --- |
| **Données** | API Adresse + Geo API | Fiabilité et complémentarité (Géo + Démographie). |
| **Pipeline** | Python, Pandas | Standard pour la manipulation de données. |
| **Visu** | Plotly | Graphiques et cartes interactives. |
| **IA** | LLaMA 3.2 (Local) | Analyse sémantique et génération de code sans fuite de données. |
| **Stockage** | Parquet | Format compressé et rapide pour la lecture/écriture. |
| **Tests** | Pytest | Assure la robustesse des fetchers et transformations. |

---

##🚀 4. Installation et exécution

###Cloner le projet```
git clone <repo_url>
cd tp2-exploration

```

###Environnement virtuel```
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# ou
.venv\Scripts\activate      # Windows

```

###Installation des dépendances```

uv add httpx pandas duckdb litellm python-dotenv tenacity tqdm pyarrow pydantic pytest

```

###Exécution du pipelineVia le script principal :

```python
from pipeline.main import run_pipeline_geo

addresses = [
    "10 Rue de Rivoli 75004 Paris",
    "5 Avenue des Champs Elysées 75008 Paris",
    "1 Place Bellecour 69002 Lyon"
]

stats = run_pipeline_geo(addresses, max_items=10, verbose=True)

```

Ou via les notebooks :

* `jupyter notebook notebooks/exploration.ipynb`
* `jupyter notebook notebooks/test.ipynb`

---

##📊 5. Visualisations incluses*

**Carte interactive** : Latitude/longitude des adresses avec indicateur couleur du score de confiance.
* **Population** : Graphique en barres de la population par commune.
* **Anomalies** : Détection visuelle des adresses à score faible (<0.5) ou des doublons.

---

##✅ 6. Tests

Les tests unitaires couvrent l'intégralité du pipeline (Fetchers, Transformer, Quality).

Pour lancer les tests avec un rapport de couverture :

```bash
pytest tests/ -v --cov=pipeline --cov-report=html

```

Un rapport HTML sera généré dans le dossier `htmlcov/`.

---

##📝 7. Conclusion

Ce projet illustre l’intégration de plusieurs APIs pour enrichir des données géographiques au sein d'un pipeline modulaire et testable. L’usage de **LLaMA** apporte une couche d'intelligence pour guider l’analyse, tandis que le format **Parquet** et les visualisations **Plotly** assurent performance et lisibilité.

```

```
