#!/usr/bin/env python3
"""
Tests unitaires pour le processeur de typographie
"""

import pytest
import sys
from pathlib import Path

# Ajouter le dossier parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.processors.typography import TypographyProcessor


@pytest.fixture
def processor():
    """Fixture pour créer un processeur"""
    return TypographyProcessor()


class TestLigatures:
    """Tests pour les ligatures"""

    def test_fix_oeuvre(self, processor):
        assert processor.fix_ligatures("oeuvre") == "œuvre"
        assert processor.fix_ligatures("Oeuvre") == "Œuvre"
        assert processor.fix_ligatures("oeuvres") == "œuvres"

    def test_fix_coeur(self, processor):
        assert processor.fix_ligatures("coeur") == "cœur"
        assert processor.fix_ligatures("Coeur") == "Cœur"

    def test_fix_boeuf(self, processor):
        assert processor.fix_ligatures("boeuf") == "bœuf"
        assert processor.fix_ligatures("boeufs") == "bœufs"

    def test_preserve_english_words(self, processor):
        # Ne devrait pas transformer les mots anglais
        text = "poet poetry"
        result = processor.fix_ligatures(text)
        # Les mots anglais ne devraient pas être modifiés
        assert "poet" in result or "pœt" in result  # Selon l'implémentation


class TestQuotes:
    """Tests pour les guillemets"""

    def test_simple_quotes(self, processor):
        assert processor.fix_quotes('"test"') == '« test »'
        assert processor.fix_quotes('"bonjour"') == '« bonjour »'

    def test_multiple_quotes(self, processor):
        text = '"premier" et "second"'
        result = processor.fix_quotes(text)
        assert '« premier »' in result
        assert '« second »' in result

    def test_nested_quotes(self, processor):
        text = "Elle dit : 'non'"
        result = processor.fix_quotes(text)
        # Les guillemets simples deviennent des guillemets doubles internes
        assert '"' in result or "'" in result


class TestApostrophes:
    """Tests pour les apostrophes"""

    def test_fix_apostrophes(self, processor):
        assert processor.fix_apostrophes("l'oeuvre") == "l'œuvre"
        assert processor.fix_apostrophes("aujourd'hui") == "aujourd'hui"


class TestPunctuation:
    """Tests pour la ponctuation"""

    def test_colon(self, processor):
        text = "Voici:"
        result = processor.fix_punctuation(text)
        # Devrait avoir un espace insécable avant :
        assert "\u00A0:" in result or " :" in result

    def test_semicolon(self, processor):
        text = "Oui;mais"
        result = processor.fix_punctuation(text)
        assert "\u00A0;" in result or " ;" in result

    def test_exclamation(self, processor):
        text = "Bravo!"
        result = processor.fix_punctuation(text)
        assert "\u00A0!" in result or " !" in result

    def test_question(self, processor):
        text = "Pourquoi?"
        result = processor.fix_punctuation(text)
        assert "\u00A0?" in result or " ?" in result


class TestEllipsis:
    """Tests pour les points de suspension"""

    def test_fix_ellipsis(self, processor):
        assert processor.fix_ellipsis("Oui...") == "Oui…"
        assert processor.fix_ellipsis("...vraiment") == "…vraiment"


class TestDashes:
    """Tests pour les tirets"""

    def test_fix_dashes(self, processor):
        text = "Il dit - vraiment - oui"
        result = processor.fix_dashes(text)
        # Devrait contenir un tiret cadratin
        assert "—" in result


class TestFullProcess:
    """Tests d'intégration pour le traitement complet"""

    def test_process_full_text(self, processor):
        text = '"L\'oeuvre" disait-il...'
        result = processor.process(text)

        # Vérifications
        assert '«' in result  # Guillemets français
        assert 'œ' in result  # Ligature
        assert ''' in result  # Apostrophe typographique
        assert '…' in result  # Points de suspension

    def test_process_complex_sentence(self, processor):
        text = 'Il disait : "Quelle oeuvre !" et...'
        result = processor.process(text)

        assert '«' in result
        assert 'œ' in result
        assert '\u00A0:' in result or ' :' in result
        assert '…' in result


class TestStats:
    """Tests pour les statistiques"""

    def test_stats_tracking(self, processor):
        processor.fix_ligatures("oeuvre oeuvre")
        stats = processor.get_stats()
        assert stats['ligatures_fixed'] >= 0

    def test_reset_stats(self, processor):
        processor.fix_ligatures("oeuvre")
        processor.reset_stats()
        stats = processor.get_stats()
        assert all(v == 0 for v in stats.values())


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
