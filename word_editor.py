#!/usr/bin/env python3
"""
Module d'édition de documents Word

Ce module fournit des fonctionnalités pour modifier des documents Word (.docx)
telles que l'ajustement des marges, de l'orientation, de la taille de page, etc.
"""

from pathlib import Path
from typing import Optional, Dict, Any, Tuple
from docx import Document
from docx.shared import Cm, Inches, Pt
from docx.enum.section import WD_ORIENT


class WordEditor:
    """Éditeur de documents Word avec support des modifications de mise en page"""

    def __init__(self, document_path: Optional[str] = None):
        """
        Initialise l'éditeur Word

        Args:
            document_path: Chemin vers le document Word existant (optionnel)
        """
        if document_path:
            self.doc = Document(document_path)
            self.doc_path = Path(document_path)
        else:
            self.doc = Document()
            self.doc_path = None

    def set_margins(
        self,
        top: Optional[float] = None,
        bottom: Optional[float] = None,
        left: Optional[float] = None,
        right: Optional[float] = None,
        unit: str = 'cm',
        all_sections: bool = True
    ) -> Dict[str, Any]:
        """
        Définit les marges du document

        Args:
            top: Marge supérieure
            bottom: Marge inférieure
            left: Marge gauche
            right: Marge droite
            unit: Unité de mesure ('cm', 'inches', 'pt')
            all_sections: Appliquer à toutes les sections (True) ou seulement la première (False)

        Returns:
            Dict avec les résultats de l'opération
        """
        if not any([top, bottom, left, right]):
            return {
                'success': False,
                'message': 'Au moins une marge doit être spécifiée'
            }

        # Convertir les valeurs selon l'unité
        unit_converter = {
            'cm': Cm,
            'inches': Inches,
            'pt': Pt
        }

        if unit not in unit_converter:
            return {
                'success': False,
                'message': f'Unité non supportée: {unit}. Utilisez "cm", "inches" ou "pt"'
            }

        converter = unit_converter[unit]
        sections = self.doc.sections if all_sections else [self.doc.sections[0]]
        sections_modified = 0

        for section in sections:
            if top is not None:
                section.top_margin = converter(top)
            if bottom is not None:
                section.bottom_margin = converter(bottom)
            if left is not None:
                section.left_margin = converter(left)
            if right is not None:
                section.right_margin = converter(right)
            sections_modified += 1

        return {
            'success': True,
            'message': f'Marges modifiées pour {sections_modified} section(s)',
            'sections_modified': sections_modified,
            'margins': {
                'top': f'{top} {unit}' if top else 'inchangée',
                'bottom': f'{bottom} {unit}' if bottom else 'inchangée',
                'left': f'{left} {unit}' if left else 'inchangée',
                'right': f'{right} {unit}' if right else 'inchangée'
            }
        }

    def set_uniform_margins(
        self,
        margin: float,
        unit: str = 'cm',
        all_sections: bool = True
    ) -> Dict[str, Any]:
        """
        Définit des marges uniformes pour tous les côtés

        Args:
            margin: Valeur de la marge pour tous les côtés
            unit: Unité de mesure ('cm', 'inches', 'pt')
            all_sections: Appliquer à toutes les sections

        Returns:
            Dict avec les résultats de l'opération
        """
        return self.set_margins(
            top=margin,
            bottom=margin,
            left=margin,
            right=margin,
            unit=unit,
            all_sections=all_sections
        )

    def get_margins(self, section_index: int = 0) -> Dict[str, Any]:
        """
        Récupère les marges actuelles d'une section

        Args:
            section_index: Index de la section (0 par défaut)

        Returns:
            Dict avec les marges en cm
        """
        if section_index >= len(self.doc.sections):
            return {
                'success': False,
                'message': f'Section {section_index} n\'existe pas'
            }

        section = self.doc.sections[section_index]

        # Convertir de EMU (English Metric Units) vers cm
        # 1 cm = 360000 EMU
        return {
            'success': True,
            'section': section_index,
            'margins': {
                'top_cm': round(section.top_margin.cm, 2),
                'bottom_cm': round(section.bottom_margin.cm, 2),
                'left_cm': round(section.left_margin.cm, 2),
                'right_cm': round(section.right_margin.cm, 2),
                'top_inches': round(section.top_margin.inches, 2),
                'bottom_inches': round(section.bottom_margin.inches, 2),
                'left_inches': round(section.left_margin.inches, 2),
                'right_inches': round(section.right_margin.inches, 2)
            }
        }

    def set_orientation(
        self,
        orientation: str,
        all_sections: bool = True
    ) -> Dict[str, Any]:
        """
        Définit l'orientation du document

        Args:
            orientation: 'portrait' ou 'landscape'
            all_sections: Appliquer à toutes les sections

        Returns:
            Dict avec les résultats de l'opération
        """
        orientation_map = {
            'portrait': WD_ORIENT.PORTRAIT,
            'landscape': WD_ORIENT.LANDSCAPE
        }

        if orientation.lower() not in orientation_map:
            return {
                'success': False,
                'message': f'Orientation non supportée: {orientation}. Utilisez "portrait" ou "landscape"'
            }

        sections = self.doc.sections if all_sections else [self.doc.sections[0]]
        sections_modified = 0

        for section in sections:
            section.orientation = orientation_map[orientation.lower()]

            # Inverser largeur et hauteur si nécessaire
            if orientation.lower() == 'landscape':
                section.page_width, section.page_height = section.page_height, section.page_width

            sections_modified += 1

        return {
            'success': True,
            'message': f'Orientation définie à "{orientation}" pour {sections_modified} section(s)',
            'sections_modified': sections_modified
        }

    def set_page_size(
        self,
        width: float,
        height: float,
        unit: str = 'cm',
        all_sections: bool = True
    ) -> Dict[str, Any]:
        """
        Définit la taille de la page

        Args:
            width: Largeur de la page
            height: Hauteur de la page
            unit: Unité de mesure ('cm', 'inches', 'pt')
            all_sections: Appliquer à toutes les sections

        Returns:
            Dict avec les résultats de l'opération
        """
        unit_converter = {
            'cm': Cm,
            'inches': Inches,
            'pt': Pt
        }

        if unit not in unit_converter:
            return {
                'success': False,
                'message': f'Unité non supportée: {unit}'
            }

        converter = unit_converter[unit]
        sections = self.doc.sections if all_sections else [self.doc.sections[0]]
        sections_modified = 0

        for section in sections:
            section.page_width = converter(width)
            section.page_height = converter(height)
            sections_modified += 1

        return {
            'success': True,
            'message': f'Taille de page définie à {width}x{height} {unit} pour {sections_modified} section(s)',
            'sections_modified': sections_modified
        }

    def save(self, output_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Sauvegarde le document

        Args:
            output_path: Chemin de sortie (optionnel, utilise le chemin original par défaut)

        Returns:
            Dict avec les résultats de l'opération
        """
        if output_path is None:
            if self.doc_path is None:
                return {
                    'success': False,
                    'message': 'Aucun chemin de sortie spécifié'
                }
            output_path = self.doc_path
        else:
            output_path = Path(output_path)

        try:
            self.doc.save(str(output_path))
            return {
                'success': True,
                'message': 'Document sauvegardé avec succès',
                'output_path': str(output_path)
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la sauvegarde: {str(e)}'
            }

    def get_document_info(self) -> Dict[str, Any]:
        """
        Récupère des informations sur le document

        Returns:
            Dict avec les informations du document
        """
        sections_info = []

        for i, section in enumerate(self.doc.sections):
            sections_info.append({
                'index': i,
                'orientation': 'landscape' if section.orientation == WD_ORIENT.LANDSCAPE else 'portrait',
                'page_width_cm': round(section.page_width.cm, 2),
                'page_height_cm': round(section.page_height.cm, 2),
                'margins': {
                    'top_cm': round(section.top_margin.cm, 2),
                    'bottom_cm': round(section.bottom_margin.cm, 2),
                    'left_cm': round(section.left_margin.cm, 2),
                    'right_cm': round(section.right_margin.cm, 2)
                }
            })

        return {
            'success': True,
            'document_path': str(self.doc_path) if self.doc_path else 'Nouveau document',
            'sections_count': len(self.doc.sections),
            'paragraphs_count': len(self.doc.paragraphs),
            'sections': sections_info
        }


def modify_word_margins(
    input_path: str,
    output_path: Optional[str] = None,
    top: Optional[float] = None,
    bottom: Optional[float] = None,
    left: Optional[float] = None,
    right: Optional[float] = None,
    unit: str = 'cm',
    all_sections: bool = True
) -> Dict[str, Any]:
    """
    Fonction utilitaire pour modifier rapidement les marges d'un document

    Args:
        input_path: Chemin du document Word d'entrée
        output_path: Chemin du document de sortie (optionnel)
        top: Marge supérieure
        bottom: Marge inférieure
        left: Marge gauche
        right: Marge droite
        unit: Unité de mesure ('cm', 'inches', 'pt')
        all_sections: Appliquer à toutes les sections

    Returns:
        Dict avec les résultats de l'opération
    """
    try:
        editor = WordEditor(input_path)

        # Modifier les marges
        result = editor.set_margins(
            top=top,
            bottom=bottom,
            left=left,
            right=right,
            unit=unit,
            all_sections=all_sections
        )

        if not result['success']:
            return result

        # Sauvegarder
        if output_path is None:
            output_path = input_path

        save_result = editor.save(output_path)

        if save_result['success']:
            return {
                'success': True,
                'message': f'Marges modifiées et document sauvegardé',
                'input_file': input_path,
                'output_file': output_path,
                'margins': result['margins']
            }
        else:
            return save_result

    except FileNotFoundError:
        return {
            'success': False,
            'message': f'Fichier non trouvé: {input_path}'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Erreur: {str(e)}'
        }


def modify_word_margins_uniform(
    input_path: str,
    margin: float,
    output_path: Optional[str] = None,
    unit: str = 'cm',
    all_sections: bool = True
) -> Dict[str, Any]:
    """
    Fonction utilitaire pour définir des marges uniformes

    Args:
        input_path: Chemin du document Word d'entrée
        margin: Valeur de la marge pour tous les côtés
        output_path: Chemin du document de sortie (optionnel)
        unit: Unité de mesure ('cm', 'inches', 'pt')
        all_sections: Appliquer à toutes les sections

    Returns:
        Dict avec les résultats de l'opération
    """
    return modify_word_margins(
        input_path=input_path,
        output_path=output_path,
        top=margin,
        bottom=margin,
        left=margin,
        right=margin,
        unit=unit,
        all_sections=all_sections
    )
