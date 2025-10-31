# docx-cleaner - Nettoyeur de documents OCR

Un outil CLI Python pour transformer des documents DOCX issus d'OCR en documents professionnels fidèles à l'original.

## ✨ Fonctionnalités

### Corrections Typographiques
- ✅ Restauration des ligatures françaises (œ, Œ, æ, Æ)
- ✅ Conversion des guillemets anglais `"` en guillemets français `« »`
- ✅ Apostrophes typographiques `'` au lieu de `'`
- ✅ Espaces insécables avant `:`, `;`, `!`, `?`
- ✅ Tirets cadratins `—` pour les incises
- ✅ Points de suspension `…` au lieu de `...`

### Suppression des Artefacts OCR
- ✅ Suppression des en-têtes de page (ex: `6 ANNA KARÉNINE`)
- ✅ Suppression des faux appels de note (chiffres isolés avant ponctuation)
- ✅ Nettoyage des espaces multiples

### Normalisation de la Capitalisation
- ✅ Correction des mots entièrement en MAJUSCULES
- ✅ Gestion intelligente des noms propres russes avec diacritiques
- ✅ Dictionnaire personnalisable
- ✅ Préservation des acronymes (URSS, USA, etc.)

### Mise en Page Professionnelle
- ✅ Justification des paragraphes
- ✅ Retrait de première ligne (1.27 cm)
- ✅ Police Times New Roman 12pt
- ✅ Interligne 1.15
- ✅ Détection et style des titres

## 📋 Prérequis

- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)

## 🚀 Installation

### Installation depuis le code source

```bash
# Cloner le dépôt
cd docx-cleaner

# Créer un environnement virtuel (recommandé)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -e .

# Ou pour le développement
pip install -e ".[dev]"
```

## 📖 Utilisation

### Usage de base

```bash
# Nettoyage simple
docx-cleaner input.docx -o output.docx

# Avec mode verbeux
docx-cleaner input.docx -o output.docx -v

# Simulation (ne sauvegarde pas le fichier)
docx-cleaner input.docx -o output.docx --dry-run -v
```

### Options avancées

```bash
# Utiliser une configuration personnalisée
docx-cleaner input.docx -o output.docx --config custom_config.json

# Préserver les appels de note (ne pas les supprimer)
docx-cleaner input.docx -o output.docx --preserve-footnotes

# Désactiver la normalisation de la capitalisation
docx-cleaner input.docx -o output.docx --no-capitalization

# Exporter un rapport JSON
docx-cleaner input.docx -o output.docx --report rapport.json
```

### Usage en tant que module Python

```python
from src.cleaner import DocxCleaner

# Créer le nettoyeur
cleaner = DocxCleaner(
    config_path=None,  # Utiliser la config par défaut
    verbose=True,
    preserve_footnotes=False,
    no_capitalization=False
)

# Nettoyer un document
stats = cleaner.clean_document('input.docx', 'output.docx')

# Afficher les statistiques
print(f"Paragraphes: {stats['total_paragraphs']}")
print(f"Corrections: {stats['corrections']}")
```

## ⚙️ Configuration

### Structure des fichiers de configuration

Le projet inclut deux fichiers de configuration dans `src/config/`:

#### `proper_nouns.json` - Dictionnaire des noms propres

```json
{
  "russian_authors": {
    "DOSTOÏEVSKI": "Dostoïevski",
    "TCHEKHOV": "Tchékhov",
    "TOLSTOÏ": "Tolstoï"
  },
  "russian_places": {
    "MOSCOU": "Moscou",
    "SAINT-PÉTERSBOURG": "Saint-Pétersbourg"
  },
  "common_names": {
    "ANNA": "Anna",
    "KARÉNINE": "Karénine"
  },
  "acronyms": ["URSS", "USA", "ONU"]
}
```

#### `patterns.json` - Patterns regex personnalisables

```json
{
  "page_headers": [
    "\\d+\\s+ANNA KARÉNINE",
    "\\d+\\s+LÉON TOLSTOÏ"
  ],
  "false_footnotes": "\\s+(\\d+)\\s*([\\.,;:])"
}
```

### Configuration personnalisée

Créez votre propre fichier JSON et utilisez l'option `--config`:

```bash
docx-cleaner input.docx -o output.docx --config my_config.json
```

## 🧪 Tests

```bash
# Lancer tous les tests
pytest tests/ -v

# Avec couverture de code
pytest tests/ --cov=src --cov-report=html

# Tester un module spécifique
pytest tests/test_typography.py -v
```

## 📊 Exemple de sortie

```
📊 RAPPORT DE TRAITEMENT
============================================================

📄 Fichier d'entrée: anna_karenine_ocr.docx
📝 Fichier de sortie: anna_karenine_clean.docx
⏱️  Temps de traitement: 2.34s

📈 Statistiques:
   Paragraphes: 127
   Mots: 8543

🔧 Corrections appliquées:
   Ligatures Fixed: 34
   Quotes Fixed: 67
   Apostrophes Fixed: 89
   Punctuation Fixed: 156
   Ellipsis Fixed: 12
   Dashes Fixed: 23
   Page Headers Removed: 10
   False Footnotes Removed: 15
   Words Capitalized: 89
   Styles Applied: 127

✅ Document nettoyé sauvegardé: anna_karenine_clean.docx
```

## 🎯 Cas d'usage typiques

### Livre numérisé (OCR)

Document original (OCR) :
```
6 ANNA KARÉNINE

"L'OEUVRE de TOLSTOÏ 1 ." disait-il... C'est ainsi - vraiment - que
MOSCOU apparait.
```

Document nettoyé :
```
« L'œuvre de Tolstoï. » disait-il… C'est ainsi — vraiment — que
Moscou apparaît.
```

### Corrections appliquées
1. Suppression de l'en-tête "6 ANNA KARÉNINE"
2. Guillemets anglais → français avec espaces insécables
3. Ligature : OEUVRE → œuvre
4. Capitalisation : TOLSTOÏ → Tolstoï, MOSCOU → Moscou
5. Suppression du faux appel de note " 1"
6. Points de suspension : ... → …
7. Tiret cadratin : - → —
8. Ajustement des espaces

## 📁 Structure du projet

```
docx-cleaner/
├── src/
│   ├── __init__.py
│   ├── cli.py              # Interface CLI
│   ├── cleaner.py          # Classe principale
│   ├── processors/
│   │   ├── __init__.py
│   │   ├── typography.py   # Corrections typographiques
│   │   ├── artifact_remover.py  # Suppression artefacts OCR
│   │   ├── capitalization.py    # Normalisation capitalisation
│   │   └── layout.py       # Mise en page
│   └── config/
│       ├── proper_nouns.json    # Dictionnaire noms propres
│       └── patterns.json   # Patterns regex
├── tests/
│   ├── test_typography.py
│   ├── test_artifact_remover.py
│   └── fixtures/
├── pyproject.toml
├── README.md
└── .gitignore
```

## 🛠️ Développement

### Installer en mode développement

```bash
pip install -e ".[dev]"
```

### Formatter le code

```bash
black src/ tests/
```

### Linter

```bash
flake8 src/ tests/
```

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créez une branche (`git checkout -b feature/amelioration`)
3. Committez vos changements (`git commit -m 'Ajout fonctionnalité'`)
4. Push vers la branche (`git push origin feature/amelioration`)
5. Ouvrez une Pull Request

### Guidelines

- Suivre PEP 8
- Ajouter des tests pour toute nouvelle fonctionnalité
- Maintenir la couverture de tests > 80%
- Documenter les fonctions publiques (docstrings)

## 📝 Licence

MIT License - Voir le fichier LICENSE pour plus de détails.

## 🙏 Remerciements

- Projet développé pour nettoyer des documents OCR de littérature russe
- Inspiré par le besoin de préserver la typographie française correcte
- Utilise python-docx pour la manipulation des documents Word

## 📞 Support

Pour signaler un bug ou proposer une fonctionnalité :
- Ouvrir une issue sur GitHub
- Consulter la documentation dans `docs/`

---

**Développé avec ❤️ pour la préservation de la typographie française**
