"""Fetcher pour l'API geo.api.gouv.fr (communes)."""

from .base import BaseFetcher
from ..config import COMMUNE_CONFIG
from ..models import CommuneInfo


class CommuneFetcher(BaseFetcher):
    """Fetcher pour récupérer les informations d'une commune."""

    def __init__(self):
        super().__init__(COMMUNE_CONFIG)

    def fetch_one(self, item: str) -> CommuneInfo | None:
        """Récupère les infos d'une commune via son code INSEE."""
        if not item:
            return None

        data = self._make_request(
            endpoint=f"/communes/{item}"
        )

        # ✅ CAS COMMUNE INVALIDE (404)
        if data is None:
            return None # Commune non trouvée

        # ✅ CAS COMMUNE VALIDE
         # Retourne un objet CommuneInfo
        self.stats["items_fetched"] += 1

        return CommuneInfo(
            citycode=data["code"],
            nom=data["nom"],
            population=data.get("population", 0),
            code_departement=data["codeDepartement"],
            code_region=data["codeRegion"],
        )
