#!/usr/bin/env python3
"""
Exemple d'utilisation du convertisseur PDF vers Word

Ce script montre différentes façons d'utiliser le module pdf_to_word
"""

import os
from pdf_to_word import PDFToWordConverter


def exemple_simple():
    """Exemple 1 : Conversion simple d'un fichier"""
    print("=" * 60)
    print("EXEMPLE 1 : Conversion simple")
    print("=" * 60)

    # Obtenir la clé API depuis les variables d'environnement
    api_key = os.environ.get('PDFREST_API_KEY')

    if not api_key:
        print("❌ Définissez la variable PDFREST_API_KEY")
        return

    # Créer le convertisseur
    converter = PDFToWordConverter(api_key)

    # Convertir un fichier
    result = converter.convert_pdf_to_word(
        pdf_path="mon_document.pdf",
        output_path="mon_document.docx"
    )

    # Vérifier le résultat
    if result['success']:
        print(f"\n✅ Succès!")
        print(f"   Fichier créé: {result['output_file']}")
        print(f"   Message: {result['message']}")
    else:
        print(f"\n❌ Échec!")
        print(f"   Message: {result['message']}")


def exemple_conversion_multiple():
    """Exemple 2 : Conversion multiple de fichiers"""
    print("\n" + "=" * 60)
    print("EXEMPLE 2 : Conversion multiple")
    print("=" * 60)

    api_key = os.environ.get('PDFREST_API_KEY')

    if not api_key:
        print("❌ Définissez la variable PDFREST_API_KEY")
        return

    converter = PDFToWordConverter(api_key)

    # Convertir tous les PDFs d'un dossier
    results = converter.convert_multiple_pdfs(
        pdf_directory="./mes_pdfs",
        output_directory="./mes_words",
        recursive=True  # Inclure les sous-dossiers
    )

    # Afficher les résultats
    print(f"\n📊 Résumé: {results['message']}")
    print("\nDétails:")

    for item in results['results']:
        status = "✅" if item['success'] else "❌"
        print(f"{status} {item['input_file']}")
        if item['success']:
            print(f"   → {item['output_file']}")
        else:
            print(f"   → Erreur: {item['message']}")


def exemple_avec_gestion_erreurs():
    """Exemple 3 : Gestion avancée des erreurs"""
    print("\n" + "=" * 60)
    print("EXEMPLE 3 : Gestion des erreurs")
    print("=" * 60)

    api_key = os.environ.get('PDFREST_API_KEY')

    if not api_key:
        print("❌ Définissez la variable PDFREST_API_KEY")
        return

    converter = PDFToWordConverter(api_key)

    fichiers_a_convertir = [
        "document1.pdf",
        "document2.pdf",
        "document_qui_nexiste_pas.pdf",
        "document3.pdf"
    ]

    successes = []
    failures = []

    for pdf_file in fichiers_a_convertir:
        try:
            result = converter.convert_pdf_to_word(
                pdf_path=pdf_file,
                timeout=120  # Timeout de 2 minutes
            )

            if result['success']:
                successes.append({
                    'input': pdf_file,
                    'output': result['output_file']
                })
                print(f"✅ {pdf_file} → {result['output_file']}")
            else:
                failures.append({
                    'input': pdf_file,
                    'error': result['message']
                })
                print(f"❌ {pdf_file} : {result['message']}")

        except FileNotFoundError as e:
            failures.append({
                'input': pdf_file,
                'error': str(e)
            })
            print(f"⚠️ {pdf_file} : Fichier introuvable")

        except Exception as e:
            failures.append({
                'input': pdf_file,
                'error': str(e)
            })
            print(f"💥 {pdf_file} : Erreur inattendue - {e}")

    # Résumé
    print("\n" + "-" * 60)
    print(f"Succès: {len(successes)}/{len(fichiers_a_convertir)}")
    print(f"Échecs: {len(failures)}/{len(fichiers_a_convertir)}")

    if failures:
        print("\n⚠️ Fichiers en échec:")
        for failure in failures:
            print(f"   - {failure['input']}: {failure['error']}")


def exemple_integration_workflow():
    """Exemple 4 : Intégration dans un workflow"""
    print("\n" + "=" * 60)
    print("EXEMPLE 4 : Workflow automatisé")
    print("=" * 60)

    api_key = os.environ.get('PDFREST_API_KEY')

    if not api_key:
        print("❌ Définissez la variable PDFREST_API_KEY")
        return

    import time
    from pathlib import Path

    converter = PDFToWordConverter(api_key)

    # Simuler un workflow où on traite des PDFs au fur et à mesure
    input_dir = Path("./input_pdfs")
    output_dir = Path("./output_words")
    processed_dir = Path("./processed_pdfs")

    # Créer les dossiers s'ils n'existent pas
    output_dir.mkdir(exist_ok=True)
    processed_dir.mkdir(exist_ok=True)

    print(f"👀 Surveillance du dossier: {input_dir}")
    print("   Appuyez sur Ctrl+C pour arrêter\n")

    try:
        while True:
            # Chercher les nouveaux PDFs
            pdf_files = list(input_dir.glob("*.pdf")) if input_dir.exists() else []

            if pdf_files:
                print(f"📥 {len(pdf_files)} fichier(s) trouvé(s)")

                for pdf_file in pdf_files:
                    print(f"\n🔄 Traitement de: {pdf_file.name}")

                    # Convertir
                    output_path = output_dir / pdf_file.with_suffix('.docx').name
                    result = converter.convert_pdf_to_word(
                        str(pdf_file),
                        str(output_path)
                    )

                    if result['success']:
                        # Déplacer le PDF traité
                        processed_path = processed_dir / pdf_file.name
                        pdf_file.rename(processed_path)
                        print(f"✅ Traité et déplacé vers: {processed_path}")
                    else:
                        print(f"❌ Échec: {result['message']}")

            else:
                print("⏳ En attente de fichiers...", end='\r')

            # Attendre avant de vérifier à nouveau
            time.sleep(5)

    except KeyboardInterrupt:
        print("\n\n⚠️ Arrêt du workflow")


def main():
    """Fonction principale pour exécuter les exemples"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "EXEMPLES D'UTILISATION PDF → WORD" + " " * 14 + "║")
    print("╚" + "═" * 58 + "╝")

    # Vérifier la clé API
    if not os.environ.get('PDFREST_API_KEY'):
        print("\n⚠️ ATTENTION: Variable PDFREST_API_KEY non définie")
        print("   Définissez-la avant d'exécuter les exemples:")
        print("   export PDFREST_API_KEY='votre_clé_api'\n")

    # Menu
    print("\nChoisissez un exemple:")
    print("1. Conversion simple d'un fichier")
    print("2. Conversion multiple (dossier)")
    print("3. Gestion avancée des erreurs")
    print("4. Workflow automatisé (surveillance)")
    print("5. Tous les exemples (1-3)")
    print("0. Quitter")

    try:
        choix = input("\nVotre choix (0-5): ").strip()

        if choix == "1":
            exemple_simple()
        elif choix == "2":
            exemple_conversion_multiple()
        elif choix == "3":
            exemple_avec_gestion_erreurs()
        elif choix == "4":
            exemple_integration_workflow()
        elif choix == "5":
            exemple_simple()
            exemple_conversion_multiple()
            exemple_avec_gestion_erreurs()
        elif choix == "0":
            print("👋 Au revoir!")
        else:
            print("❌ Choix invalide")

        print("\n" + "=" * 60)
        print("Fin des exemples")
        print("=" * 60 + "\n")

    except KeyboardInterrupt:
        print("\n\n👋 Au revoir!")


if __name__ == '__main__':
    main()
