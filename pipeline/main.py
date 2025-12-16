#!/usr/bin/env python3
"""Script principal du pipeline GEO."""
import argparse
from datetime import datetime
import pandas as pd

from .enricher import GeoEnricher
from .transformer import DataTransformer
from .quality import QualityAnalyzer
from .storage import save_raw_json, save_parquet
from .config import MAX_ITEMS


def run_pipeline_geo(
    addresses: list[str],
    max_items: int = MAX_ITEMS,
    skip_enrichment: bool = False,
    verbose: bool = True
) -> dict:
    stats = {"start_time": datetime.now()}
    
    print("="*60)
    print("🚀 PIPELINE GEO")
    print("="*60)
    
    # === ÉTAPE 1 : Enrichissement GEO ===
    if not skip_enrichment:
        print("\n🌍 ÉTAPE 1 : Enrichissement (géocodage + commune)")
        enricher = GeoEnricher()
        enriched_list = enricher.enrich_addresses(addresses[:max_items])
        stats["enricher"] = enricher.get_stats()
    else:
        print("⏭️ ÉTAPE 1 : Enrichissement ignoré")
        enriched_list = []
    
    if not enriched_list:
        print("❌ Aucun résultat enrichi. Arrêt.")
        return {"error": "No enriched data"}
    
    save_raw_json([e.dict() for e in enriched_list], "geo_enriched_raw")
    
    # === ÉTAPE 2 : Transformation ===
    print("\n🔧 ÉTAPE 2 : Transformation et nettoyage")
    df = pd.DataFrame([e.dict() for e in enriched_list])
    
    transformer = DataTransformer(df)
    df_clean = (
        transformer
        .remove_duplicates(subset=["address"])
        .handle_missing_values(numeric_strategy='median', text_strategy='unknown')
        .normalize_text_columns(["city", "commune"])
        .get_result()
    )
    
    stats["transformer"] = {"transformations": transformer.transformations_applied}
    
    # === ÉTAPE 3 : Qualité ===
    print("\n📊 ÉTAPE 3 : Analyse de qualité")
    analyzer = QualityAnalyzer(df_clean)
    metrics = analyzer.analyze()
    
    print(f"   Note: {metrics.quality_grade}")
    print(f"   Complétude: {metrics.completeness_score*100:.1f}%")
    print(f"   Doublons: {metrics.duplicates_pct:.1f}%")
    
    analyzer.generate_report("geo_dataset")
    stats["quality"] = metrics.dict()
    
    # === ÉTAPE 4 : Stockage final ===
    print("\n💾 ÉTAPE 4 : Stockage final")
    output_path = save_parquet(df_clean, "geo_dataset")
    stats["output_path"] = str(output_path)
    
    stats["end_time"] = datetime.now()
    stats["duration_seconds"] = (stats["end_time"] - stats["start_time"]).seconds
    
    print("\n" + "="*60)
    print("✅ PIPELINE GEO TERMINÉ")
    print("="*60)
    print(f"Durée: {stats['duration_seconds']}s")
    print(f"Adresses enrichies: {len(df_clean)}")
    print(f"Qualité: {metrics.quality_grade}")
    print(f"Fichier: {output_path}")
    
    return stats
