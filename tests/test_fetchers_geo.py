"""Tests pour les fetchers GEO (Adresse et Commune)."""
import pytest
from pipeline.fetchers.adresse import AdresseFetcher
from pipeline.fetchers.commune import CommuneFetcher
from pipeline.models import GeocodingResult, CommuneInfo

class TestAdresseFetcher:
    """Tests pour le fetcher d'adresses (BAN)."""

    @pytest.fixture
    def fetcher(self):
        return AdresseFetcher()

    def test_fetch_one_valid_address(self, fetcher):
        result = fetcher.fetch_one("10 rue de Rivoli, Paris")
        assert isinstance(result, GeocodingResult)
        assert result.latitude is not None
        assert result.longitude is not None
        assert result.score > 0.5

    def test_fetch_one_invalid_address(self, fetcher):
        result = fetcher.fetch_one("xyzabc123456")
        assert result.score == 0 or result.latitude is None

    def test_fetch_one_empty_address(self, fetcher):
        result = fetcher.fetch_one("")
        assert result.score == 0
        assert result.latitude is None

class TestCommuneFetcher:
    """Tests pour le fetcher de communes (Geo API)."""

    @pytest.fixture
    def fetcher(self):
        return CommuneFetcher()

    def test_fetch_one_valid_commune(self, fetcher):
        result = fetcher.fetch_one("75104")  # code INSEE Paris 4e
        assert isinstance(result, CommuneInfo)
        assert result.citycode == "75104"
        assert result.nom.lower().startswith("paris")

    def test_fetch_one_invalid_commune(self, fetcher):
        result = fetcher.fetch_one("00000")
        assert result is None
