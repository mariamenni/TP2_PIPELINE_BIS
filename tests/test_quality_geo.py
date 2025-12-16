"""Tests pour QualityAnalyzer GEO."""
import pytest
import pandas as pd
from pipeline.quality import QualityAnalyzer

class TestQualityAnalyzer:

    @pytest.fixture
    def sample_df(self):
        return pd.DataFrame({
            'address': ['Addr 1', 'Addr 2', 'Addr 3'],
            'city': ['paris', 'lyon', 'marseille'],
            'score': [0.9, 0.7, 0.95],
            'latitude': [48.85, 45.75, 43.3],
            'longitude': [2.35, 4.83, 5.37],
        })

    def test_quality_metrics(self, sample_df):
        analyzer = QualityAnalyzer(sample_df)
        metrics = analyzer.analyze()
        assert metrics.total_records == 3
        assert metrics.valid_records == 3
        assert metrics.quality_grade in ['A', 'B', 'C', 'D', 'F']
        assert metrics.is_acceptable is True
