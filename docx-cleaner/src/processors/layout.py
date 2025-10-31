#!/usr/bin/env python3
"""
Processeur de mise en page et structure

Gère la reconstruction des paragraphes et l'application des styles.
"""

import re
from typing import List, Dict
from docx import Document
from docx.shared import Pt, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH


class LayoutProcessor:
    """Processeur de mise en page des documents"""

    def __init__(self, verbose: bool = False):
        """
        Initialise le processeur de mise en page

        Args:
            verbose: Mode verbeux pour le logging
        """
        self.verbose = verbose
        self.stats = {
            'paragraphs_split': 0,
            'styles_applied': 0,
        }

    def split_merged_paragraphs(self, text: str, min_paragraph_length: int = 50) -> List[str]:
        """
        Sépare les paragraphes fusionnés par l'OCR

        Args:
            text: Texte contenant des paragraphes fusionnés
            min_paragraph_length: Longueur minimale pour considérer une coupure

        Returns:
            Liste de paragraphes séparés
        """
        # Pattern : point/exclamation/interrogation + espaces + majuscule
        potential_breaks = list(re.finditer(
            r'([.!?])\s+([A-ZÀÉÈÊËÏÎÔÙŒÆ])',
            text
        ))

        if not potential_breaks:
            return [text]

        paragraphs = []
        last_pos = 0

        for match in potential_breaks:
            current_pos = match.start()

            # Vérifier si c'est une vraie coupure de paragraphe
            # Heuristique : au moins min_paragraph_length caractères depuis le début
            segment_length = current_pos - last_pos

            if segment_length >= min_paragraph_length:
                # Vérifier que ce n'est pas une abréviation (Mr., Dr., etc.)
                before_text = text[max(0, match.start() - 5):match.start()]
                if not re.search(r'\b(Mr|Dr|St|Mme|Mlle|etc)$', before_text, re.IGNORECASE):
                    # C'est probablement une vraie coupure
                    para = text[last_pos:match.end(1)].strip()
                    if para:
                        paragraphs.append(para)
                        self.stats['paragraphs_split'] += 1
                    last_pos = match.start(2)

        # Ajouter le dernier paragraphe
        final_para = text[last_pos:].strip()
        if final_para:
            paragraphs.append(final_para)

        if self.stats['paragraphs_split'] > 0 and self.verbose:
            print(f"  [PARAGRAPHES] {self.stats['paragraphs_split']} paragraphe(s) séparé(s)")

        return paragraphs if paragraphs else [text]

    def apply_professional_style(
        self,
        doc: Document,
        font_name: str = 'Times New Roman',
        font_size: int = 12,
        line_spacing: float = 1.15,
        first_line_indent: float = 1.27,  # cm
        justify: bool = True
    ):
        """
        Applique un style professionnel à tous les paragraphes

        Args:
            doc: Document python-docx
            font_name: Nom de la police
            font_size: Taille de la police (points)
            line_spacing: Interligne
            first_line_indent: Retrait première ligne (cm)
            justify: Justifier le texte
        """
        count = 0

        for para in doc.paragraphs:
            # Ignorer les paragraphes vides
            if not para.text.strip():
                continue

            # Vérifier si c'est un titre (heuristique)
            if self.is_likely_title(para.text):
                self.apply_title_style(para, font_name, font_size)
            else:
                self.apply_paragraph_style(
                    para,
                    font_name,
                    font_size,
                    line_spacing,
                    first_line_indent,
                    justify
                )

            count += 1

        self.stats['styles_applied'] += count

        if self.verbose:
            print(f"  [STYLES] Style appliqué à {count} paragraphe(s)")

    def apply_paragraph_style(
        self,
        paragraph,
        font_name: str,
        font_size: int,
        line_spacing: float,
        first_line_indent: float,
        justify: bool
    ):
        """
        Applique le style à un paragraphe

        Args:
            paragraph: Paragraphe python-docx
            font_name: Nom de la police
            font_size: Taille de la police
            line_spacing: Interligne
            first_line_indent: Retrait première ligne (cm)
            justify: Justifier le texte
        """
        # Alignement
        if justify:
            paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        else:
            paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT

        # Format paragraphe
        fmt = paragraph.paragraph_format
        fmt.first_line_indent = Cm(first_line_indent)
        fmt.line_spacing = line_spacing
        fmt.space_after = Pt(0)
        fmt.space_before = Pt(0)

        # Police
        for run in paragraph.runs:
            run.font.name = font_name
            run.font.size = Pt(font_size)

    def apply_title_style(self, paragraph, font_name: str, font_size: int):
        """
        Applique le style de titre

        Args:
            paragraph: Paragraphe python-docx
            font_name: Nom de la police
            font_size: Taille de la police
        """
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Format paragraphe
        fmt = paragraph.paragraph_format
        fmt.space_after = Pt(12)
        fmt.space_before = Pt(12)

        # Police (un peu plus grande et en gras)
        for run in paragraph.runs:
            run.font.name = font_name
            run.font.size = Pt(font_size + 2)
            run.font.bold = True

    def is_likely_title(self, text: str) -> bool:
        """
        Détermine si un texte est probablement un titre

        Args:
            text: Texte à analyser

        Returns:
            True si probablement un titre
        """
        text = text.strip()

        # Heuristiques pour détecter un titre :
        # 1. Moins de 100 caractères
        # 2. Pas de ponctuation finale (., !, ?)
        # 3. Première lettre majuscule ou tout en majuscules
        # 4. Pas trop de mots (moins de 15)

        if len(text) > 100:
            return False

        if text.endswith(('.', '!', '?')):
            return False

        word_count = len(text.split())
        if word_count > 15:
            return False

        # Vérifier capitalisation
        if not (text[0].isupper() or text.isupper()):
            return False

        return True

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
