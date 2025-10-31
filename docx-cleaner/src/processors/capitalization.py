#!/usr/bin/env python3
"""
Processeur de normalisation de la capitalisation

Gère les noms propres, notamment les noms russes avec diacritiques.
"""

import re
from typing import Dict, List, Set


class CapitalizationProcessor:
    """Normalise la capitalisation des mots"""

    def __init__(
        self,
        proper_nouns: Dict[str, Dict[str, str]] = None,
        acronyms: List[str] = None,
        verbose: bool = False
    ):
        """
        Initialise le processeur de capitalisation

        Args:
            proper_nouns: Dictionnaire de noms propres (par catégorie)
            acronyms: Liste d'acronymes à préserver
            verbose: Mode verbeux pour le logging
        """
        self.proper_nouns = proper_nouns or {}
        self.acronyms = set(acronyms or [])
        self.verbose = verbose
        self.stats = {
            'words_capitalized': 0,
        }

        # Créer un index plat de tous les noms propres
        self.nouns_index = {}
        for category, nouns in self.proper_nouns.items():
            self.nouns_index.update(nouns)

    def process(self, text: str) -> str:
        """
        Normalise la capitalisation du texte

        Args:
            text: Texte à normaliser

        Returns:
            Texte avec capitalisation normalisée
        """
        # Traiter mot par mot
        words = re.findall(r'\b\w+\b|\W+', text)
        result = []
        count = 0

        is_sentence_start = True

        for i, token in enumerate(words):
            # Si ce n'est pas un mot, garder tel quel
            if not re.match(r'\w+', token):
                result.append(token)
                # Détecter fin de phrase
                if re.match(r'[.!?]', token):
                    is_sentence_start = True
                continue

            # Normaliser le mot
            normalized = self.normalize_word(token, is_sentence_start)

            if normalized != token:
                count += 1

            result.append(normalized)

            # Reset sentence start après le premier mot
            if token.strip():
                is_sentence_start = False

        if count > 0:
            self.stats['words_capitalized'] += count
            if self.verbose:
                print(f"  [CAPITALISATION] {count} mot(s) normalisé(s)")

        return ''.join(result)

    def normalize_word(self, word: str, is_sentence_start: bool = False) -> str:
        """
        Normalise la capitalisation d'un seul mot

        Args:
            word: Mot à normaliser
            is_sentence_start: True si le mot est en début de phrase

        Returns:
            Mot normalisé
        """
        # Ne toucher que les mots entièrement en majuscules (> 1 caractère)
        if not (word.isupper() and len(word) > 1):
            return word

        # Vérifier si c'est un acronyme connu
        if word in self.acronyms:
            return word

        # Chercher dans le dictionnaire de noms propres
        if word.upper() in self.nouns_index:
            return self.nouns_index[word.upper()]

        # Règle par défaut : capitalize en début de phrase, sinon minuscules
        if is_sentence_start:
            return word.capitalize()
        else:
            # Les noms propres commencent par une majuscule même au milieu
            # Heuristique : si > 3 lettres, probablement un nom propre
            if len(word) >= 4:
                return word.capitalize()
            else:
                return word.lower()

    def add_proper_noun(self, uppercase: str, correct: str, category: str = 'custom'):
        """
        Ajoute un nom propre au dictionnaire

        Args:
            uppercase: Version majuscules
            correct: Version correcte
            category: Catégorie du nom
        """
        if category not in self.proper_nouns:
            self.proper_nouns[category] = {}

        self.proper_nouns[category][uppercase] = correct
        self.nouns_index[uppercase] = correct

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
