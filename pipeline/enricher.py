"""Module d'enrichissement croisé GEO."""

from typing import List
from tqdm import tqdm

from .fetchers.adresse import AdresseFetcher
from .fetchers.commune import CommuneFetcher
from .models import GeocodingResult, EnrichedAddress


class GeoEnricher:
    """Enrichit des adresses via géocodage + données communes."""

    def __init__(self):
        self.geocoder = AdresseFetcher()
        self.commune_fetcher = CommuneFetcher()
        self.stats = {
            "total_addresses": 0,
            "geocoded": 0,
            "enriched": 0,
            "failed": 0,
        }

    # ==========================================================
    # Géocodage + enrichissement
    # ==========================================================

    def enrich_addresses(self, addresses: List[str]) -> List[EnrichedAddress]:
        """Enrichit une liste d'adresses avec géocodage et infos communes."""
        enriched_results = []

        for address in tqdm(addresses, desc="Enrichissement GEO"):
            self.stats["total_addresses"] += 1

            geo: GeocodingResult = self.geocoder.fetch_one(address)

            if not geo or not geo.is_valid:
                self.stats["failed"] += 1
                continue

            self.stats["geocoded"] += 1

            commune = self.commune_fetcher.fetch_one(geo.citycode)

            if not commune:
                self.stats["failed"] += 1
                continue

            # Fusion des données géocodées et commune
            enriched_results.append(
                EnrichedAddress(
                    address=geo.label,
                    latitude=geo.latitude,
                    longitude=geo.longitude,
                    score=geo.score,
                    city=geo.city,
                    postcode=geo.postcode,
                    citycode=geo.citycode,
                    commune=commune.nom,
                    population=commune.population,
                )
            )

            self.stats["enriched"] += 1

        return enriched_results

    # ==========================================================
    # Statistiques
    # ==========================================================

    def get_stats(self) -> dict:
        """Retourne les statistiques d'enrichissement."""
        return {
            **self.stats,
            "geocoder_stats": self.geocoder.get_stats(),
            "commune_stats": self.commune_fetcher.get_stats(),
            "success_rate": (
                self.stats["enriched"] / self.stats["total_addresses"] * 100
                if self.stats["total_addresses"] > 0
                else 0
            ),
        }
