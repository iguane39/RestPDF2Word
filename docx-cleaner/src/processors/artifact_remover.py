#!/usr/bin/env python3
"""
Processeur de suppression des artefacts OCR

Supprime les en-têtes de page, faux appels de note, etc.
"""

import re
from typing import List, Dict


class ArtifactRemover:
    """Supprime les artefacts OCR des documents"""

    def __init__(self, page_header_patterns: List[str] = None, verbose: bool = False):
        """
        Initialise le suppresseur d'artefacts

        Args:
            page_header_patterns: Liste de patterns regex pour les en-têtes
            verbose: Mode verbeux pour le logging
        """
        self.page_header_patterns = page_header_patterns or []
        self.verbose = verbose
        self.stats = {
            'page_headers_removed': 0,
            'false_footnotes_removed': 0,
        }

    def process(self, text: str, preserve_footnotes: bool = False) -> str:
        """
        Applique toutes les suppressions d'artefacts

        Args:
            text: Texte à nettoyer
            preserve_footnotes: Si True, ne supprime pas les appels de note

        Returns:
            Texte nettoyé
        """
        text = self.remove_page_headers(text)

        if not preserve_footnotes:
            text = self.remove_false_footnotes(text)

        return text

    def remove_page_headers(self, text: str) -> str:
        """
        Supprime les en-têtes de page (numéros + titre)

        Args:
            text: Texte contenant des en-têtes

        Returns:
            Texte sans en-têtes
        """
        count = 0

        for pattern in self.page_header_patterns:
            matches = list(re.finditer(pattern, text, flags=re.IGNORECASE))
            count += len(matches)

            # Supprimer toutes les occurrences
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)

        # Nettoyer les espaces multiples résultants
        text = re.sub(r'\n{3,}', '\n\n', text)  # Max 2 sauts de ligne
        text = re.sub(r' {2,}', ' ', text)      # Max 1 espace

        if count > 0:
            self.stats['page_headers_removed'] += count
            if self.verbose:
                print(f"  [EN-TÊTES] {count} en-tête(s) de page supprimé(s)")

        return text

    def remove_false_footnotes(self, text: str) -> str:
        """
        Supprime les faux appels de note (chiffres isolés avant ponctuation)

        Exemples:
            "Tolstoï 1 ." → "Tolstoï."
            "phrase 2 ," → "phrase,"

        Args:
            text: Texte contenant des faux appels de note

        Returns:
            Texte sans faux appels de note
        """
        # Pattern : espace + chiffre + espace optionnel + ponctuation
        pattern = r'\s+(\d+)\s*([.,;:])'

        # Compter les occurrences avant suppression
        matches = list(re.finditer(pattern, text))
        count = 0

        # Pour chaque match, vérifier si c'est vraiment un faux appel
        for match in matches:
            number = match.group(1)
            punct = match.group(2)

            # Heuristique : si le chiffre est <= 99, c'est probablement un faux appel
            # Les vrais numéros (années, quantités) sont généralement > 99 ou en contexte
            if int(number) <= 99:
                count += 1

        # Remplacer par juste la ponctuation
        text = re.sub(pattern, r'\2', text)

        if count > 0:
            self.stats['false_footnotes_removed'] += count
            if self.verbose:
                print(f"  [FAUX APPELS] {count} faux appel(s) de note supprimé(s)")

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
