#!/usr/bin/env python3
"""
PDF to Word Converter using pdfRest API

Ce script convertit des fichiers PDF en documents Word (.docx) éditables
en utilisant l'API pdfRest.com, tout en préservant le formatage original
(polices, gras, italique, mise en page).
"""

import os
import sys
import time
import requests
from pathlib import Path
from typing import Optional, Dict, Any


class PDFToWordConverter:
    """Convertisseur PDF vers Word utilisant l'API pdfRest"""

    API_BASE_URL = "https://api.pdfrest.com"
    PDF_TO_WORD_ENDPOINT = "/word"

    def __init__(self, api_key: str):
        """
        Initialise le convertisseur avec une clé API

        Args:
            api_key: Clé API pdfRest (obtenue sur https://pdfrest.com)
        """
        if not api_key:
            raise ValueError("La clé API est requise")

        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Api-Key": self.api_key
        })

    def convert_pdf_to_word(
        self,
        pdf_path: str,
        output_path: Optional[str] = None,
        timeout: int = 300
    ) -> Dict[str, Any]:
        """
        Convertit un fichier PDF en document Word éditable

        Args:
            pdf_path: Chemin vers le fichier PDF source
            output_path: Chemin de sortie pour le fichier DOCX (optionnel)
            timeout: Temps maximum d'attente en secondes (défaut: 300s)

        Returns:
            Dict contenant les informations sur la conversion:
            - success: bool
            - output_file: str (chemin du fichier DOCX créé)
            - message: str
            - details: Dict (détails de la réponse API)

        Raises:
            FileNotFoundError: Si le fichier PDF n'existe pas
            requests.exceptions.RequestException: En cas d'erreur réseau
        """
        # Vérification du fichier PDF
        pdf_file = Path(pdf_path)
        if not pdf_file.exists():
            raise FileNotFoundError(f"Le fichier PDF n'existe pas: {pdf_path}")

        if not pdf_file.suffix.lower() == '.pdf':
            raise ValueError(f"Le fichier doit être un PDF: {pdf_path}")

        # Définir le chemin de sortie
        if output_path is None:
            output_path = pdf_file.with_suffix('.docx')
        else:
            output_path = Path(output_path)

        print(f"📄 Conversion de: {pdf_file.name}")
        print(f"📝 Sortie vers: {output_path.name}")
        print(f"🔄 Envoi du fichier à l'API pdfRest...")

        try:
            # Préparer la requête multipart/form-data
            with open(pdf_file, 'rb') as f:
                files = {
                    'file': (pdf_file.name, f, 'application/pdf')
                }

                # Paramètres supplémentaires (optionnels)
                data = {
                    'output': 'docx'  # Format de sortie
                }

                # Appel API
                url = f"{self.API_BASE_URL}{self.PDF_TO_WORD_ENDPOINT}"
                response = self.session.post(
                    url,
                    files=files,
                    data=data,
                    timeout=timeout
                )

            # Vérifier la réponse
            response.raise_for_status()

            # Gérer différents types de réponse
            content_type = response.headers.get('Content-Type', '')

            if 'application/json' in content_type:
                # Réponse JSON avec URL de téléchargement
                result = response.json()
                print(f"✅ Conversion réussie!")
                print(f"📥 Téléchargement du fichier Word...")

                # Télécharger le fichier résultant
                if 'outputUrl' in result:
                    download_url = result['outputUrl']
                    self._download_file(download_url, output_path)

                    return {
                        'success': True,
                        'output_file': str(output_path),
                        'message': 'Conversion réussie',
                        'details': result
                    }
                else:
                    return {
                        'success': False,
                        'output_file': None,
                        'message': 'URL de téléchargement non trouvée dans la réponse',
                        'details': result
                    }

            elif 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' in content_type:
                # Réponse directe avec le fichier DOCX
                with open(output_path, 'wb') as f:
                    f.write(response.content)

                print(f"✅ Conversion réussie!")
                print(f"💾 Fichier sauvegardé: {output_path}")

                return {
                    'success': True,
                    'output_file': str(output_path),
                    'message': 'Conversion et téléchargement réussis',
                    'details': {
                        'file_size': len(response.content),
                        'content_type': content_type
                    }
                }

            else:
                return {
                    'success': False,
                    'output_file': None,
                    'message': f'Type de contenu inattendu: {content_type}',
                    'details': {'content_type': content_type}
                }

        except requests.exceptions.HTTPError as e:
            error_message = f"Erreur HTTP {e.response.status_code}"
            try:
                error_details = e.response.json()
                error_message += f": {error_details}"
            except:
                error_message += f": {e.response.text[:200]}"

            print(f"❌ {error_message}")

            return {
                'success': False,
                'output_file': None,
                'message': error_message,
                'details': {'status_code': e.response.status_code}
            }

        except requests.exceptions.Timeout:
            error_message = f"Timeout: La conversion a dépassé {timeout} secondes"
            print(f"⏱️ {error_message}")

            return {
                'success': False,
                'output_file': None,
                'message': error_message,
                'details': {}
            }

        except requests.exceptions.RequestException as e:
            error_message = f"Erreur réseau: {str(e)}"
            print(f"🌐 {error_message}")

            return {
                'success': False,
                'output_file': None,
                'message': error_message,
                'details': {}
            }

    def _download_file(self, url: str, output_path: Path, chunk_size: int = 8192):
        """
        Télécharge un fichier depuis une URL

        Args:
            url: URL du fichier à télécharger
            output_path: Chemin de destination
            chunk_size: Taille des blocs de téléchargement
        """
        response = self.session.get(url, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0

        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)

                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\r📥 Téléchargement: {percent:.1f}%", end='', flush=True)

        if total_size > 0:
            print()  # Nouvelle ligne après la progression

        print(f"💾 Fichier sauvegardé: {output_path}")

    def convert_multiple_pdfs(
        self,
        pdf_directory: str,
        output_directory: Optional[str] = None,
        recursive: bool = False
    ) -> Dict[str, Any]:
        """
        Convertit plusieurs fichiers PDF en Word

        Args:
            pdf_directory: Dossier contenant les PDFs
            output_directory: Dossier de sortie (optionnel)
            recursive: Chercher récursivement dans les sous-dossiers

        Returns:
            Dict avec les résultats de toutes les conversions
        """
        pdf_dir = Path(pdf_directory)
        if not pdf_dir.exists():
            raise FileNotFoundError(f"Le dossier n'existe pas: {pdf_directory}")

        # Créer le dossier de sortie si spécifié
        if output_directory:
            output_dir = Path(output_directory)
            output_dir.mkdir(parents=True, exist_ok=True)
        else:
            output_dir = pdf_dir

        # Trouver tous les fichiers PDF
        if recursive:
            pdf_files = list(pdf_dir.rglob('*.pdf'))
        else:
            pdf_files = list(pdf_dir.glob('*.pdf'))

        if not pdf_files:
            return {
                'success': False,
                'message': f'Aucun fichier PDF trouvé dans {pdf_directory}',
                'results': []
            }

        print(f"📚 {len(pdf_files)} fichier(s) PDF trouvé(s)")
        print("="*50)

        results = []
        for i, pdf_file in enumerate(pdf_files, 1):
            print(f"\n[{i}/{len(pdf_files)}] ", end='')

            # Construire le chemin de sortie
            relative_path = pdf_file.relative_to(pdf_dir)
            output_path = output_dir / relative_path.with_suffix('.docx')
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Convertir
            result = self.convert_pdf_to_word(str(pdf_file), str(output_path))
            results.append({
                'input_file': str(pdf_file),
                **result
            })

            # Pause entre les requêtes pour ne pas surcharger l'API
            if i < len(pdf_files):
                time.sleep(1)

        print("\n" + "="*50)

        success_count = sum(1 for r in results if r['success'])
        print(f"✅ {success_count}/{len(pdf_files)} conversion(s) réussie(s)")

        return {
            'success': success_count > 0,
            'message': f'{success_count}/{len(pdf_files)} conversions réussies',
            'results': results
        }


def main():
    """Fonction principale pour utilisation en ligne de commande"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Convertit des fichiers PDF en documents Word éditables',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:

  # Convertir un seul PDF
  python pdf_to_word.py input.pdf

  # Convertir avec un nom de sortie spécifique
  python pdf_to_word.py input.pdf -o output.docx

  # Convertir tous les PDFs d'un dossier
  python pdf_to_word.py -d ./pdfs -od ./words

  # Utiliser une clé API spécifique
  python pdf_to_word.py input.pdf --api-key YOUR_API_KEY
        """
    )

    parser.add_argument(
        'input',
        nargs='?',
        help='Fichier PDF à convertir'
    )

    parser.add_argument(
        '-o', '--output',
        help='Chemin du fichier Word de sortie'
    )

    parser.add_argument(
        '-d', '--directory',
        help='Convertir tous les PDFs d\'un dossier'
    )

    parser.add_argument(
        '-od', '--output-directory',
        help='Dossier de sortie pour les conversions multiples'
    )

    parser.add_argument(
        '-r', '--recursive',
        action='store_true',
        help='Chercher récursivement dans les sous-dossiers'
    )

    parser.add_argument(
        '--api-key',
        help='Clé API pdfRest (ou utiliser la variable d\'environnement PDFREST_API_KEY)'
    )

    parser.add_argument(
        '--timeout',
        type=int,
        default=300,
        help='Timeout en secondes (défaut: 300)'
    )

    args = parser.parse_args()

    # Obtenir la clé API
    api_key = args.api_key or os.environ.get('PDFREST_API_KEY')

    if not api_key:
        print("❌ Erreur: Clé API requise")
        print("   Définissez la variable d'environnement PDFREST_API_KEY")
        print("   ou utilisez l'option --api-key")
        print("\n   Obtenez votre clé API sur: https://pdfrest.com")
        sys.exit(1)

    # Créer le convertisseur
    converter = PDFToWordConverter(api_key)

    try:
        # Mode dossier
        if args.directory:
            result = converter.convert_multiple_pdfs(
                args.directory,
                args.output_directory,
                args.recursive
            )
            sys.exit(0 if result['success'] else 1)

        # Mode fichier unique
        elif args.input:
            result = converter.convert_pdf_to_word(
                args.input,
                args.output,
                args.timeout
            )
            sys.exit(0 if result['success'] else 1)

        else:
            parser.print_help()
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n⚠️ Conversion annulée par l'utilisateur")
        sys.exit(130)

    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
