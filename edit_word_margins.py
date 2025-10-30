#!/usr/bin/env python3
"""
Script pour modifier les marges de documents Word

Ce script permet de modifier facilement les marges de documents Word (.docx)
en ligne de commande ou par lot.

Option A : Script standalone pour l'édition des marges
"""

import sys
import argparse
from pathlib import Path
from typing import Optional
from word_editor import WordEditor, modify_word_margins


def main():
    """Fonction principale pour l'utilisation en ligne de commande"""

    parser = argparse.ArgumentParser(
        description='Modifie les marges de documents Word (.docx)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:

  # Définir toutes les marges à 2.5 cm
  python edit_word_margins.py document.docx --all 2.5

  # Définir des marges spécifiques
  python edit_word_margins.py document.docx --top 3 --bottom 3 --left 2.5 --right 2.5

  # Avec un fichier de sortie différent
  python edit_word_margins.py input.docx -o output.docx --all 2.5

  # Utiliser des inches au lieu de cm
  python edit_word_margins.py document.docx --all 1 --unit inches

  # Modifier seulement la première section
  python edit_word_margins.py document.docx --all 2.5 --first-section-only

  # Afficher les marges actuelles
  python edit_word_margins.py document.docx --info

  # Modifier plusieurs fichiers dans un dossier
  python edit_word_margins.py -d ./documents --all 2.5
        """
    )

    parser.add_argument(
        'input',
        nargs='?',
        help='Fichier Word à modifier'
    )

    parser.add_argument(
        '-o', '--output',
        help='Fichier de sortie (par défaut: écrase le fichier d\'entrée)'
    )

    parser.add_argument(
        '-d', '--directory',
        help='Modifier tous les fichiers Word d\'un dossier'
    )

    parser.add_argument(
        '-od', '--output-directory',
        help='Dossier de sortie pour les modifications multiples'
    )

    parser.add_argument(
        '--all',
        type=float,
        metavar='MARGIN',
        help='Définir toutes les marges à la même valeur'
    )

    parser.add_argument(
        '--top',
        type=float,
        help='Marge supérieure'
    )

    parser.add_argument(
        '--bottom',
        type=float,
        help='Marge inférieure'
    )

    parser.add_argument(
        '--left',
        type=float,
        help='Marge gauche'
    )

    parser.add_argument(
        '--right',
        type=float,
        help='Marge droite'
    )

    parser.add_argument(
        '--unit',
        choices=['cm', 'inches', 'pt'],
        default='cm',
        help='Unité de mesure (défaut: cm)'
    )

    parser.add_argument(
        '--first-section-only',
        action='store_true',
        help='Appliquer seulement à la première section'
    )

    parser.add_argument(
        '--info',
        action='store_true',
        help='Afficher les informations sur le document (marges actuelles, etc.)'
    )

    parser.add_argument(
        '-r', '--recursive',
        action='store_true',
        help='Traiter récursivement les sous-dossiers'
    )

    args = parser.parse_args()

    # Mode information
    if args.info:
        if not args.input:
            print("❌ Erreur: Spécifiez un fichier avec --info")
            sys.exit(1)

        return show_document_info(args.input)

    # Mode dossier
    if args.directory:
        return process_directory(
            directory=args.directory,
            output_directory=args.output_directory,
            top=args.top,
            bottom=args.bottom,
            left=args.left,
            right=args.right,
            all_margins=args.all,
            unit=args.unit,
            all_sections=not args.first_section_only,
            recursive=args.recursive
        )

    # Mode fichier unique
    if args.input:
        return process_single_file(
            input_path=args.input,
            output_path=args.output,
            top=args.top,
            bottom=args.bottom,
            left=args.left,
            right=args.right,
            all_margins=args.all,
            unit=args.unit,
            all_sections=not args.first_section_only
        )

    # Aucun argument
    parser.print_help()
    sys.exit(1)


def process_single_file(
    input_path: str,
    output_path: Optional[str],
    top: Optional[float],
    bottom: Optional[float],
    left: Optional[float],
    right: Optional[float],
    all_margins: Optional[float],
    unit: str,
    all_sections: bool
) -> int:
    """
    Traite un seul fichier

    Returns:
        Code de sortie (0 = succès, 1 = erreur)
    """
    # Utiliser la valeur "all" si spécifiée
    if all_margins is not None:
        top = bottom = left = right = all_margins

    # Vérifier qu'au moins une marge est spécifiée
    if not any([top, bottom, left, right]):
        print("❌ Erreur: Spécifiez au moins une marge (--all, --top, --bottom, --left, --right)")
        return 1

    print(f"📄 Modification de: {input_path}")

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
            print(f"❌ Erreur: {result['message']}")
            return 1

        print(f"✅ {result['message']}")
        print(f"   Marges appliquées:")
        for side, value in result['margins'].items():
            print(f"   - {side.capitalize()}: {value}")

        # Sauvegarder
        if output_path is None:
            output_path = input_path
            print(f"💾 Sauvegarde dans le fichier original...")
        else:
            print(f"💾 Sauvegarde vers: {output_path}")

        save_result = editor.save(output_path)

        if save_result['success']:
            print(f"✅ Document sauvegardé avec succès")
            return 0
        else:
            print(f"❌ Erreur lors de la sauvegarde: {save_result['message']}")
            return 1

    except FileNotFoundError:
        print(f"❌ Fichier non trouvé: {input_path}")
        return 1

    except Exception as e:
        print(f"❌ Erreur inattendue: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


def process_directory(
    directory: str,
    output_directory: Optional[str],
    top: Optional[float],
    bottom: Optional[float],
    left: Optional[float],
    right: Optional[float],
    all_margins: Optional[float],
    unit: str,
    all_sections: bool,
    recursive: bool
) -> int:
    """
    Traite tous les fichiers Word d'un dossier

    Returns:
        Code de sortie (0 = succès, 1 = erreur)
    """
    # Utiliser la valeur "all" si spécifiée
    if all_margins is not None:
        top = bottom = left = right = all_margins

    # Vérifier qu'au moins une marge est spécifiée
    if not any([top, bottom, left, right]):
        print("❌ Erreur: Spécifiez au moins une marge (--all, --top, --bottom, --left, --right)")
        return 1

    dir_path = Path(directory)
    if not dir_path.exists():
        print(f"❌ Dossier non trouvé: {directory}")
        return 1

    # Créer le dossier de sortie si spécifié
    if output_directory:
        output_dir = Path(output_directory)
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = dir_path

    # Trouver tous les fichiers Word
    if recursive:
        docx_files = list(dir_path.rglob('*.docx'))
    else:
        docx_files = list(dir_path.glob('*.docx'))

    # Filtrer les fichiers temporaires de Word (commencent par ~$)
    docx_files = [f for f in docx_files if not f.name.startswith('~$')]

    if not docx_files:
        print(f"❌ Aucun fichier Word trouvé dans {directory}")
        return 1

    print(f"📚 {len(docx_files)} fichier(s) Word trouvé(s)")
    print("=" * 60)

    success_count = 0
    error_count = 0

    for i, docx_file in enumerate(docx_files, 1):
        print(f"\n[{i}/{len(docx_files)}] 📄 {docx_file.name}")

        # Construire le chemin de sortie
        relative_path = docx_file.relative_to(dir_path)
        output_path = output_dir / relative_path
        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            editor = WordEditor(str(docx_file))

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
                print(f"   ❌ {result['message']}")
                error_count += 1
                continue

            # Sauvegarder
            save_result = editor.save(str(output_path))

            if save_result['success']:
                print(f"   ✅ Modifié et sauvegardé")
                success_count += 1
            else:
                print(f"   ❌ Erreur lors de la sauvegarde: {save_result['message']}")
                error_count += 1

        except Exception as e:
            print(f"   ❌ Erreur: {str(e)}")
            error_count += 1

    print("\n" + "=" * 60)
    print(f"✅ {success_count}/{len(docx_files)} fichier(s) modifié(s) avec succès")
    if error_count > 0:
        print(f"❌ {error_count}/{len(docx_files)} erreur(s)")

    return 0 if success_count > 0 else 1


def show_document_info(input_path: str) -> int:
    """
    Affiche les informations sur un document

    Returns:
        Code de sortie (0 = succès, 1 = erreur)
    """
    try:
        editor = WordEditor(input_path)
        info = editor.get_document_info()

        if not info['success']:
            print(f"❌ Erreur: {info['message']}")
            return 1

        print("=" * 60)
        print(f"📄 Document: {info['document_path']}")
        print("=" * 60)
        print(f"Sections: {info['sections_count']}")
        print(f"Paragraphes: {info['paragraphs_count']}")
        print()

        for section in info['sections']:
            print(f"Section {section['index'] + 1}:")
            print(f"  Orientation: {section['orientation']}")
            print(f"  Taille: {section['page_width_cm']} x {section['page_height_cm']} cm")
            print(f"  Marges (cm):")
            print(f"    - Haut: {section['margins']['top_cm']} cm")
            print(f"    - Bas: {section['margins']['bottom_cm']} cm")
            print(f"    - Gauche: {section['margins']['left_cm']} cm")
            print(f"    - Droite: {section['margins']['right_cm']} cm")
            print()

        return 0

    except FileNotFoundError:
        print(f"❌ Fichier non trouvé: {input_path}")
        return 1

    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️ Opération annulée par l'utilisateur")
        sys.exit(130)
