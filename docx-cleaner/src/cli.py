#!/usr/bin/env python3
"""
Interface en ligne de commande pour docx-cleaner
"""

import sys
import json
import click
from pathlib import Path
from datetime import datetime

from .cleaner import DocxCleaner


@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option(
    '-o', '--output',
    required=True,
    type=click.Path(),
    help='Fichier de sortie (.docx)'
)
@click.option(
    '--config',
    type=click.Path(exists=True),
    help='Fichier de configuration personnalisé (JSON)'
)
@click.option(
    '--preserve-footnotes',
    is_flag=True,
    help='Ne pas supprimer les appels de note'
)
@click.option(
    '--no-capitalization',
    is_flag=True,
    help='Désactiver la normalisation de la capitalisation'
)
@click.option(
    '-v', '--verbose',
    is_flag=True,
    help='Mode verbeux (affiche les détails)'
)
@click.option(
    '--dry-run',
    is_flag=True,
    help='Simulation sans écriture du fichier'
)
@click.option(
    '--report',
    type=click.Path(),
    help='Exporter le rapport au format JSON'
)
def clean(input_file, output, config, preserve_footnotes, no_capitalization, verbose, dry_run, report):
    """
    Nettoie un document DOCX issu d'OCR

    Applique les corrections typographiques, supprime les artefacts OCR,
    normalise la capitalisation et applique un style professionnel.

    Exemples:

        \b
        # Nettoyage simple
        docx-cleaner input.docx -o output.docx

        \b
        # Avec config personnalisée et mode verbeux
        docx-cleaner input.docx -o output.docx --config custom_config.json -v

        \b
        # Préserver les appels de note
        docx-cleaner input.docx -o output.docx --preserve-footnotes

        \b
        # Simulation (ne sauvegarde pas le fichier)
        docx-cleaner input.docx -o output.docx --dry-run -v
    """
    # Vérifier que le fichier d'entrée est bien un DOCX
    if not input_file.lower().endswith('.docx'):
        click.echo("❌ Erreur: Le fichier d'entrée doit être un fichier .docx", err=True)
        sys.exit(1)

    # Vérifier que le fichier de sortie a l'extension .docx
    if not output.lower().endswith('.docx'):
        click.echo("❌ Erreur: Le fichier de sortie doit avoir l'extension .docx", err=True)
        sys.exit(1)

    try:
        # Créer le nettoyeur
        cleaner = DocxCleaner(
            config_path=config,
            verbose=verbose,
            preserve_footnotes=preserve_footnotes,
            no_capitalization=no_capitalization
        )

        if dry_run:
            click.echo("🔍 Mode simulation activé (aucun fichier ne sera créé)")
            click.echo()

        # Nettoyer le document
        start_time = datetime.now()
        stats = cleaner.clean_document(input_file, output if not dry_run else '/tmp/dry_run.docx')
        end_time = datetime.now()

        processing_time = (end_time - start_time).total_seconds()

        # Afficher le résumé
        click.echo()
        click.echo("=" * 60)
        click.echo("📊 RAPPORT DE TRAITEMENT")
        click.echo("=" * 60)
        click.echo()
        click.echo(f"📄 Fichier d'entrée: {input_file}")
        if not dry_run:
            click.echo(f"📝 Fichier de sortie: {output}")
        click.echo(f"⏱️  Temps de traitement: {processing_time:.2f}s")
        click.echo()
        click.echo("📈 Statistiques:")
        click.echo(f"   Paragraphes: {stats['total_paragraphs']}")
        click.echo(f"   Mots: {stats['total_words']}")
        click.echo()
        click.echo("🔧 Corrections appliquées:")

        corrections = stats.get('corrections', {})
        for key, value in corrections.items():
            if value > 0:
                label = key.replace('_', ' ').title()
                click.echo(f"   {label}: {value}")

        click.echo()

        if dry_run:
            click.echo("⚠️  Mode simulation: Aucun fichier n'a été créé")
        else:
            click.echo(f"✅ Document nettoyé sauvegardé: {output}")

        click.echo()

        # Exporter le rapport si demandé
        if report:
            report_data = {
                **stats,
                'processing_time_seconds': processing_time,
                'processing_date': datetime.now().isoformat(),
                'dry_run': dry_run,
            }

            with open(report, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)

            click.echo(f"📄 Rapport exporté: {report}")
            click.echo()

        sys.exit(0)

    except FileNotFoundError as e:
        click.echo(f"❌ Fichier non trouvé: {e}", err=True)
        sys.exit(1)

    except PermissionError as e:
        click.echo(f"❌ Permission refusée: {e}", err=True)
        sys.exit(1)

    except Exception as e:
        click.echo(f"❌ Erreur inattendue: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def main():
    """Point d'entrée principal"""
    clean()


if __name__ == '__main__':
    main()
