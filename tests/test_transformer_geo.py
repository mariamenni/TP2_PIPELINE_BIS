"""Tests pour le DataTransformer GEO."""
import pytest
import pandas as pd
from pipeline.transformer import DataTransformer

class TestDataTransformer:
    """Tests pour DataTransformer."""

    @pytest.fixture
    def sample_df(self):
        return pd.DataFrame({
            'address': ['Addr 1', 'Addr 2', 'Addr 1'],
            'city': ['Paris', None, 'Paris'],
            'score': [0.9, None, 0.9],
            'latitude': [48.85, None, 48.85],
            'longitude': [2.35, None, 2.35],
        })

    def test_remove_duplicates(self, sample_df):
        transformer = DataTransformer(sample_df)
        df = transformer.remove_duplicates(subset=['address']).get_result()
        assert len(df) == 2
        assert df['address'].nunique() == 2

    def test_handle_missing_values(self, sample_df):
        transformer = DataTransformer(sample_df)
        df = transformer.handle_missing_values(numeric_strategy='median', text_strategy='unknown').get_result()
        assert df['score'].isnull().sum() == 0
        assert df['latitude'].isnull().sum() == 0
        assert df['city'].isnull().sum() == 0

    def test_normalize_text_columns(self, sample_df):
        transformer = DataTransformer(sample_df)
        df = transformer.normalize_text_columns(['city']).get_result()
        assert all(isinstance(c, str) for c in df['city'])
        assert all(c == c.strip().lower() or c == 'unknown' for c in df['city'])
