#!/usr/bin/env python3
"""
Exemples d'utilisation des fonctionnalités d'ajustement de marges

Ce script montre comment utiliser les nouvelles fonctionnalités:
- Option A: Édition standalone des marges de documents Word existants
- Option B: Pipeline complet PDF → Word avec ajustement automatique des marges
"""

import os
from pdf_to_word import PDFToWordConverter
from word_editor import WordEditor, modify_word_margins


def exemple_option_a_simple():
    """Option A - Exemple 1: Édition simple des marges d'un document Word"""
    print("=" * 70)
    print("OPTION A - EXEMPLE 1: Édition simple des marges")
    print("=" * 70)
    print()

    # Supposons qu'on a un document Word existant
    doc_path = "mon_document.docx"

    print(f"📄 Document: {doc_path}")
    print("🎯 Objectif: Définir toutes les marges à 2.5 cm\n")

    # Méthode 1: Utiliser la classe WordEditor
    print("Méthode 1: Avec WordEditor")
    editor = WordEditor(doc_path)

    # Afficher les marges actuelles
    info = editor.get_margins(section_index=0)
    if info['success']:
        print(f"📏 Marges actuelles:")
        margins = info['margins']
        print(f"   Haut: {margins['top_cm']} cm")
        print(f"   Bas: {margins['bottom_cm']} cm")
        print(f"   Gauche: {margins['left_cm']} cm")
        print(f"   Droite: {margins['right_cm']} cm\n")

    # Définir des marges uniformes à 2.5 cm
    result = editor.set_uniform_margins(margin=2.5, unit='cm')

    if result['success']:
        print(f"✅ {result['message']}")
        editor.save()
        print("💾 Document sauvegardé\n")

    # Méthode 2: Utiliser la fonction utilitaire
    print("Méthode 2: Avec fonction utilitaire")
    result = modify_word_margins(
        input_path=doc_path,
        output_path="mon_document_2.5cm.docx",
        top=2.5,
        bottom=2.5,
        left=2.5,
        right=2.5,
        unit='cm'
    )

    if result['success']:
        print(f"✅ {result['message']}")
        print(f"📁 Fichier créé: {result['output_file']}\n")


def exemple_option_a_marges_specifiques():
    """Option A - Exemple 2: Marges spécifiques différentes"""
    print("=" * 70)
    print("OPTION A - EXEMPLE 2: Marges spécifiques différentes")
    print("=" * 70)
    print()

    doc_path = "rapport.docx"

    print(f"📄 Document: {doc_path}")
    print("🎯 Objectif: Marges haut/bas 3cm, gauche/droite 2cm\n")

    editor = WordEditor(doc_path)

    result = editor.set_margins(
        top=3,
        bottom=3,
        left=2,
        right=2,
        unit='cm'
    )

    if result['success']:
        print(f"✅ {result['message']}")
        print("📐 Marges appliquées:")
        for side, value in result['margins'].items():
            print(f"   - {side.capitalize()}: {value}")

        editor.save()
        print("\n💾 Document sauvegardé")


def exemple_option_a_informations():
    """Option A - Exemple 3: Obtenir des informations sur un document"""
    print("\n" + "=" * 70)
    print("OPTION A - EXEMPLE 3: Informations sur un document")
    print("=" * 70)
    print()

    doc_path = "mon_document.docx"

    editor = WordEditor(doc_path)
    info = editor.get_document_info()

    if info['success']:
        print(f"📄 Document: {info['document_path']}")
        print(f"📑 Sections: {info['sections_count']}")
        print(f"📝 Paragraphes: {info['paragraphs_count']}\n")

        for section in info['sections']:
            print(f"Section {section['index'] + 1}:")
            print(f"  📐 Orientation: {section['orientation']}")
            print(f"  📏 Taille: {section['page_width_cm']} x {section['page_height_cm']} cm")
            print(f"  📏 Marges:")
            print(f"     Haut: {section['margins']['top_cm']} cm")
            print(f"     Bas: {section['margins']['bottom_cm']} cm")
            print(f"     Gauche: {section['margins']['left_cm']} cm")
            print(f"     Droite: {section['margins']['right_cm']} cm")
            print()


def exemple_option_b_simple():
    """Option B - Exemple 1: Conversion PDF → Word avec ajustement automatique"""
    print("=" * 70)
    print("OPTION B - EXEMPLE 1: Pipeline complet (PDF → Word + marges)")
    print("=" * 70)
    print()

    api_key = os.environ.get('PDFREST_API_KEY')
    if not api_key:
        print("⚠️ PDFREST_API_KEY non définie, exemple ignoré")
        return

    print("📄 Fichier: rapport.pdf")
    print("🎯 Objectif: Convertir en Word avec marges à 2.5 cm automatiquement\n")

    converter = PDFToWordConverter(api_key)

    result = converter.convert_pdf_to_word(
        pdf_path="rapport.pdf",
        output_path="rapport.docx",
        adjust_margins=True,
        margin_top=2.5,
        margin_bottom=2.5,
        margin_left=2.5,
        margin_right=2.5,
        margin_unit='cm'
    )

    if result['success']:
        print(f"✅ Conversion réussie!")
        print(f"📁 Fichier créé: {result['output_file']}")
        if result.get('margins_adjusted'):
            print(f"📐 Marges ajustées à 2.5 cm sur tous les côtés")
        print()


def exemple_option_b_batch():
    """Option B - Exemple 2: Conversion par lot avec ajustement des marges"""
    print("=" * 70)
    print("OPTION B - EXEMPLE 2: Conversion par lot avec ajustement")
    print("=" * 70)
    print()

    api_key = os.environ.get('PDFREST_API_KEY')
    if not api_key:
        print("⚠️ PDFREST_API_KEY non définie, exemple ignoré")
        return

    print("📂 Dossier: ./mes_pdfs")
    print("🎯 Objectif: Convertir tous les PDFs avec marges à 2.5 cm\n")

    converter = PDFToWordConverter(api_key)

    results = converter.convert_multiple_pdfs(
        pdf_directory="./mes_pdfs",
        output_directory="./mes_words",
        recursive=True,
        adjust_margins=True,
        margin_top=2.5,
        margin_bottom=2.5,
        margin_left=2.5,
        margin_right=2.5,
        margin_unit='cm'
    )

    if results['success']:
        print(f"✅ {results['message']}")
        print(f"\n📊 Détails:")
        for item in results['results']:
            status = "✅" if item['success'] else "❌"
            margins_status = "📐" if item.get('margins_adjusted') else ""
            print(f"  {status} {margins_status} {item['input_file']}")


def exemple_option_b_marges_personnalisees():
    """Option B - Exemple 3: Marges personnalisées pendant la conversion"""
    print("\n" + "=" * 70)
    print("OPTION B - EXEMPLE 3: Marges personnalisées")
    print("=" * 70)
    print()

    api_key = os.environ.get('PDFREST_API_KEY')
    if not api_key:
        print("⚠️ PDFREST_API_KEY non définie, exemple ignoré")
        return

    print("📄 Fichier: document_legal.pdf")
    print("🎯 Objectif: Marges conformes aux normes (1 inch = 2.54 cm)\n")

    converter = PDFToWordConverter(api_key)

    result = converter.convert_pdf_to_word(
        pdf_path="document_legal.pdf",
        output_path="document_legal.docx",
        adjust_margins=True,
        margin_top=1,
        margin_bottom=1,
        margin_left=1,
        margin_right=1,
        margin_unit='inches'  # Utiliser des inches
    )

    if result['success']:
        print(f"✅ Conversion réussie!")
        print(f"📁 Fichier créé: {result['output_file']}")
        if result.get('margins_adjusted'):
            print(f"📐 Marges ajustées à 1 inch (2.54 cm) sur tous les côtés")


def exemple_comparaison_options():
    """Comparaison des deux options"""
    print("\n" + "=" * 70)
    print("COMPARAISON: Option A vs Option B")
    print("=" * 70)
    print()

    print("📋 Option A - Édition standalone des marges")
    print("   ✅ Pour documents Word existants")
    print("   ✅ Modification rapide sans conversion")
    print("   ✅ Support de plusieurs fichiers")
    print("   ✅ Affichage d'informations sur les documents")
    print("   📝 Utilisation: python edit_word_margins.py document.docx --all 2.5")
    print()

    print("📋 Option B - Pipeline complet (PDF → Word + marges)")
    print("   ✅ Conversion ET ajustement en une seule étape")
    print("   ✅ Automatisation complète")
    print("   ✅ Pas besoin de script séparé")
    print("   ✅ Idéal pour workflows automatisés")
    print("   📝 Utilisation: python pdf_to_word.py input.pdf --margins 2.5")
    print()

    print("💡 Conseil: Utilisez Option A pour documents Word existants,")
    print("           Option B pour convertir des PDFs avec marges spécifiques")


def main():
    """Fonction principale"""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 12 + "EXEMPLES: AJUSTEMENT DES MARGES" + " " * 24 + "║")
    print("╚" + "═" * 68 + "╝")
    print()

    print("Choisissez un exemple:")
    print()
    print("Option A - Édition standalone:")
    print("  1. Édition simple des marges (2.5 cm)")
    print("  2. Marges spécifiques différentes")
    print("  3. Afficher les informations d'un document")
    print()
    print("Option B - Pipeline complet:")
    print("  4. Conversion PDF → Word avec marges")
    print("  5. Conversion par lot avec marges")
    print("  6. Marges personnalisées (inches)")
    print()
    print("  7. Comparaison Option A vs Option B")
    print("  8. Tous les exemples")
    print("  0. Quitter")
    print()

    try:
        choix = input("Votre choix (0-8): ").strip()

        if choix == "1":
            exemple_option_a_simple()
        elif choix == "2":
            exemple_option_a_marges_specifiques()
        elif choix == "3":
            exemple_option_a_informations()
        elif choix == "4":
            exemple_option_b_simple()
        elif choix == "5":
            exemple_option_b_batch()
        elif choix == "6":
            exemple_option_b_marges_personnalisees()
        elif choix == "7":
            exemple_comparaison_options()
        elif choix == "8":
            print("\n🚀 Exécution de tous les exemples...")
            exemple_option_a_simple()
            exemple_option_a_marges_specifiques()
            exemple_option_a_informations()
            exemple_option_b_simple()
            exemple_option_b_batch()
            exemple_option_b_marges_personnalisees()
            exemple_comparaison_options()
        elif choix == "0":
            print("👋 Au revoir!")
        else:
            print("❌ Choix invalide")

        print("\n" + "=" * 70)
        print("Fin des exemples")
        print("=" * 70 + "\n")

    except KeyboardInterrupt:
        print("\n\n👋 Au revoir!")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")


if __name__ == '__main__':
    main()
