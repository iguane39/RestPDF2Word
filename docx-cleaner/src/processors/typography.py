#!/usr/bin/env python3
"""
Processeur de corrections typographiques

Gère les ligatures, guillemets, apostrophes et ponctuation française.
"""

import re
from typing import Dict, Tuple


class TypographyProcessor:
    """Processeur pour les corrections typographiques françaises"""

    # Ligatures françaises
    LIGATURES = {
        'oe': 'œ',
        'Oe': 'Œ',
        'ae': 'æ',
        'Ae': 'Æ',
    }

    # Mots où les ligatures sont systématiques
    LIGATURE_WORDS = [
        'oeuvre', 'Oeuvre', 'oeuvres', 'Oeuvres',
        'oeil', 'Oeil', 'yeux',
        'coeur', 'Coeur', 'coeurs', 'Coeurs',
        'soeur', 'Soeur', 'soeurs', 'Soeurs',
        'boeuf', 'Boeuf', 'boeufs', 'Boeufs',
        'noeud', 'Noeud', 'noeuds', 'Noeuds',
        'voeu', 'Voeu', 'voeux', 'Voeux',
   ]

    def __init__(self, verbose: bool = False):
        """
        Initialise le processeur de typographie

        Args:
            verbose: Mode verbeux pour le logging
        """
        self.verbose = verbose
        self.stats = {
            'ligatures_fixed': 0,
            'quotes_fixed': 0,
            'apostrophes_fixed': 0,
            'punctuation_fixed': 0,
            'ellipsis_fixed': 0,
            'dashes_fixed': 0,
        }

    def process(self, text: str) -> str:
        """
        Applique toutes les corrections typographiques

        Args:
            text: Texte à corriger

        Returns:
            Texte corrigé
        """
        text = self.fix_ligatures(text)
        text = self.fix_quotes(text)
        text = self.fix_apostrophes(text)
        text = self.fix_punctuation(text)
        text = self.fix_ellipsis(text)
        text = self.fix_dashes(text)
        text = self.normalize_spaces(text)

        return text

    def fix_ligatures(self, text: str) -> str:
        """
        Restaure les ligatures françaises (œ, Œ, æ, Æ)

        Args:
            text: Texte à corriger

        Returns:
            Texte avec ligatures restaurées
        """
        original = text

        # Remplacement des mots complets (plus sûr)
        for word in self.LIGATURE_WORDS:
            pattern = r'\b' + word.replace('oe', r'[oO][eE]').replace('ae', r'[aA][eE]') + r'\b'
            ligature_word = word.replace('oe', 'œ').replace('Oe', 'Œ').replace('ae', 'æ').replace('Ae', 'Æ')

            if re.search(pattern, text, re.IGNORECASE):
                text = re.sub(pattern, ligature_word, text, flags=re.IGNORECASE)

        # Remplacement général plus prudent (avec contexte)
        # oeuvre, boeuf, etc.
        text = re.sub(r'\b([Oo])e([uû]vr|il|uf)', r'\1œ\2', text)

        # Compter les changements
        count = len(re.findall(r'[œŒæÆ]', text)) - len(re.findall(r'[œŒæÆ]', original))
        if count > 0:
            self.stats['ligatures_fixed'] += count
            if self.verbose:
                print(f"  [LIGATURES] {count} ligature(s) restaurée(s)")

        return text

    def fix_quotes(self, text: str) -> str:
        """
        Convertit les guillemets anglais en guillemets français

        Args:
            text: Texte à corriger

        Returns:
            Texte avec guillemets français
        """
        original_count = text.count('"')

        # Guillemets doubles : "texte" → « texte »
        # Pattern pour détecter les guillemets par paire
        text = re.sub(r'"([^"]+)"', r'« \1 »', text)

        # Guillemets simples internes (citation dans citation) : 'texte' → "texte"
        text = re.sub(r"'([^']+)'", r'"\1"', text)

        # Nettoyer les espaces multiples autour des guillemets
        text = re.sub(r'«\s+', '« ', text)
        text = re.sub(r'\s+»', ' »', text)

        new_count = text.count('«') + text.count('»')
        if new_count > 0:
            self.stats['quotes_fixed'] += new_count // 2
            if self.verbose:
                print(f"  [GUILLEMETS] {new_count // 2} paire(s) de guillemets corrigée(s)")

        return text

    def fix_apostrophes(self, text: str) -> str:
        """
        Remplace les apostrophes droites par des apostrophes typographiques

        Args:
            text: Texte à corriger

        Returns:
            Texte avec apostrophes typographiques
        """
        original_count = text.count("'")

        # Apostrophe droite → apostrophe typographique
        text = text.replace("'", "'")

        if original_count > 0:
            self.stats['apostrophes_fixed'] += original_count
            if self.verbose:
                print(f"  [APOSTROPHES] {original_count} apostrophe(s) corrigée(s)")

        return text

    def fix_punctuation(self, text: str) -> str:
        """
        Ajoute les espaces insécables avant :;!? selon les règles françaises

        Args:
            text: Texte à corriger

        Returns:
            Texte avec ponctuation correcte
        """
        count = 0

        # Espace insécable avant : ; ! ?
        # On utilise \u00A0 (espace insécable)

        # Deux-points
        if re.search(r'(\S):', text):
            text = re.sub(r'(\S)\s*:', r'\1\u00A0:', text)
            count += 1

        # Point-virgule
        if re.search(r'(\S);', text):
            text = re.sub(r'(\S)\s*;', r'\1\u00A0;', text)
            count += 1

        # Point d'exclamation
        if re.search(r'(\S)!', text):
            text = re.sub(r'(\S)\s*!', r'\1\u00A0!', text)
            count += 1

        # Point d'interrogation
        if re.search(r'(\S)\?', text):
            text = re.sub(r'(\S)\s*\?', r'\1\u00A0?', text)
            count += 1

        if count > 0:
            self.stats['punctuation_fixed'] += count
            if self.verbose:
                print(f"  [PONCTUATION] {count} règle(s) de ponctuation appliquée(s)")

        return text

    def fix_ellipsis(self, text: str) -> str:
        """
        Convertit les points de suspension ... en caractère unique …

        Args:
            text: Texte à corriger

        Returns:
            Texte avec points de suspension corrects
        """
        count = len(re.findall(r'\.\.\.', text))

        if count > 0:
            text = text.replace('...', '…')
            self.stats['ellipsis_fixed'] += count
            if self.verbose:
                print(f"  [ELLIPSE] {count} points de suspension corrigés")

        return text

    def fix_dashes(self, text: str) -> str:
        """
        Convertit les tirets simples en tirets cadratins pour les incises

        Args:
            text: Texte à corriger

        Returns:
            Texte avec tirets cadratins
        """
        count = 0

        # Tiret simple entouré d'espaces → tiret cadratin
        # Pattern : espace - espace
        if re.search(r'\s+-\s+', text):
            text = re.sub(r'\s+-\s+', ' — ', text)
            count = len(re.findall(r'—', text))

        if count > 0:
            self.stats['dashes_fixed'] += count
            if self.verbose:
                print(f"  [TIRETS] {count} tiret(s) cadratin(s) appliqué(s)")

        return text

    def normalize_spaces(self, text: str) -> str:
        """
        Normalise les espaces multiples en espaces simples

        Args:
            text: Texte à normaliser

        Returns:
            Texte normalisé
        """
        # Remplacer espaces multiples par un seul
        text = re.sub(r' {2,}', ' ', text)

        # Supprimer espaces en début/fin
        text = text.strip()

        return text

    def get_stats(self) -> Dict[str, int]:
        """
        Retourne les statistiques de traitement

        Returns:
            Dictionnaire des statistiques
        """
        return self.stats.copy()

    def reset_stats(self):
        """Réinitialise les statistiques"""
        for key in self.stats:
            self.stats[key] = 0
