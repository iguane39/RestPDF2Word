#!/usr/bin/env python3
"""
Classe principale de nettoyage de documents DOCX

Orchestre tous les processeurs pour nettoyer un document OCR.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from docx import Document

from .processors.typography import TypographyProcessor
from .processors.artifact_remover import ArtifactRemover
from .processors.capitalization import CapitalizationProcessor
from .processors.layout import LayoutProcessor


class DocxCleaner:
    """Classe principale pour nettoyer des documents DOCX issus d'OCR"""

    def __init__(
        self,
        config_path: Optional[str] = None,
        verbose: bool = False,
        preserve_footnotes: bool = False,
        no_capitalization: bool = False
    ):
        """
        Initialise le nettoyeur de documents

        Args:
            config_path: Chemin vers fichier de config JSON personnalisé
            verbose: Mode verbeux
            preserve_footnotes: Préserver les appels de note
            no_capitalization: Désactiver la normalisation de capitalisation
        """
        self.verbose = verbose
        self.preserve_footnotes = preserve_footnotes
        self.no_capitalization = no_capitalization

        # Charger la configuration
        self.config = self._load_config(config_path)

        # Initialiser les processeurs
        self.typography = TypographyProcessor(verbose=verbose)

        self.artifact_remover = ArtifactRemover(
            page_header_patterns=self.config.get('patterns', {}).get('page_headers', []),
            verbose=verbose
        )

        proper_nouns = self.config.get('proper_nouns', {})
        acronyms = proper_nouns.get('acronyms', [])

        self.capitalization = CapitalizationProcessor(
            proper_nouns=proper_nouns,
            acronyms=acronyms,
            verbose=verbose
        )

        self.layout = LayoutProcessor(verbose=verbose)

    def _load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Charge la configuration depuis un fichier JSON

        Args:
            config_path: Chemin vers le fichier de config

        Returns:
            Dictionnaire de configuration
        """
        config = {}

        # Chemin par défaut
        if config_path is None:
            default_config_dir = Path(__file__).parent / 'config'
        else:
            default_config_dir = Path(config_path).parent

        # Charger proper_nouns.json
        proper_nouns_path = default_config_dir / 'proper_nouns.json'
        if proper_nouns_path.exists():
            with open(proper_nouns_path, 'r', encoding='utf-8') as f:
                config['proper_nouns'] = json.load(f)

        # Charger patterns.json
        patterns_path = default_config_dir / 'patterns.json'
        if patterns_path.exists():
            with open(patterns_path, 'r', encoding='utf-8') as f:
                config['patterns'] = json.load(f)

        # Si config personnalisée spécifiée, la charger et merger
        if config_path and Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                custom_config = json.load(f)
                # Merger avec la config par défaut
                config.update(custom_config)

        return config

    def clean_document(
        self,
        input_path: str,
        output_path: str
    ) -> Dict[str, Any]:
        """
        Nettoie un document DOCX

        Args:
            input_path: Chemin du document d'entrée
            output_path: Chemin du document de sortie

        Returns:
            Dictionnaire avec les statistiques de traitement
        """
        if self.verbose:
            print(f"\n📄 Nettoyage de: {input_path}")
            print(f"📝 Sortie vers: {output_path}")
            print()

        # Charger le document
        doc = Document(input_path)

        # Statistiques globales
        total_stats = {
            'input_file': input_path,
            'output_file': output_path,
            'total_paragraphs': len(doc.paragraphs),
            'total_words': sum(len(p.text.split()) for p in doc.paragraphs),
        }

        # Traiter chaque paragraphe
        for para in doc.paragraphs:
            if not para.text.strip():
                continue

            if self.verbose:
                print(f"  Traitement du paragraphe: {para.text[:60]}...")

            # 1. Suppression des artefacts OCR
            cleaned_text = self.artifact_remover.process(
                para.text,
                preserve_footnotes=self.preserve_footnotes
            )

            # 2. Corrections typographiques
            cleaned_text = self.typography.process(cleaned_text)

            # 3. Normalisation de la capitalisation
            if not self.no_capitalization:
                cleaned_text = self.capitalization.process(cleaned_text)

            # Mettre à jour le texte du paragraphe
            para.text = cleaned_text

        if self.verbose:
            print("\n📐 Application du style professionnel...")

        # 4. Application du style professionnel
        self.layout.apply_professional_style(doc)

        # Sauvegarder le document
        doc.save(output_path)

        if self.verbose:
            print(f"\n✅ Document nettoyé sauvegardé: {output_path}\n")

        # Compiler les statistiques
        total_stats['corrections'] = {
            **self.typography.get_stats(),
            **self.artifact_remover.get_stats(),
            **self.capitalization.get_stats(),
            **self.layout.get_stats(),
        }

        return total_stats

    def get_all_stats(self) -> Dict[str, int]:
        """
        Récupère toutes les statistiques de tous les processeurs

        Returns:
            Dictionnaire combiné des statistiques
        """
        return {
            **self.typography.get_stats(),
            **self.artifact_remover.get_stats(),
            **self.capitalization.get_stats(),
            **self.layout.get_stats(),
        }

    def reset_all_stats(self):
        """Réinitialise toutes les statistiques"""
        self.typography.reset_stats()
        self.artifact_remover.reset_stats()
        self.capitalization.reset_stats()
        self.layout.reset_stats()
