# RestPDF2Word - Convertisseur PDF vers Word

Un outil Python simple et puissant pour convertir des fichiers PDF en documents Word (.docx) **100% éditables** en utilisant l'API [pdfRest.com](https://pdfrest.com).

## ✨ Caractéristiques

### Conversion PDF → Word
- ✅ **Conversion fidèle à 99%** : Préserve les polices, le formatage (gras, italique), les couleurs et la mise en page
- ✅ **Documents éditables** : Produit de vrais fichiers Word avec du texte sélectionnable et modifiable (pas d'images)
- ✅ **Simple d'utilisation** : Interface en ligne de commande intuitive
- ✅ **Conversion par lot** : Convertit plusieurs PDFs en une seule commande
- ✅ **Gestion des erreurs** : Suivi détaillé et gestion robuste des erreurs
- ✅ **Support récursif** : Traite les sous-dossiers automatiquement

### Édition de documents Word
- ✅ **Ajustement automatique des marges** : Modifie les marges pendant ou après la conversion
- ✅ **Pipeline complet** : Convertit PDF → Word avec ajustement automatique des marges
- ✅ **Script standalone** : Éditeur de marges indépendant pour documents Word existants
- ✅ **Modification par lot** : Ajuste les marges de plusieurs documents en une seule commande
- ✅ **Unités flexibles** : Support de cm, inches et points

## 📋 Prérequis

- Python 3.7 ou supérieur
- Une clé API pdfRest (gratuite ou payante selon vos besoins)

### Obtenir une clé API

1. Créez un compte sur [pdfRest.com](https://pdfrest.com)
2. Accédez à votre tableau de bord
3. Copiez votre clé API

## 🚀 Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/votre-username/RestPDF2Word.git
cd RestPDF2Word
```

### 2. Créer un environnement virtuel (recommandé)

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer la clé API

**Option A : Fichier .env (recommandé)**

```bash
cp .env.example .env
# Éditez .env et ajoutez votre clé API
```

Contenu de `.env` :
```
PDFREST_API_KEY=votre_clé_api_ici
```

**Option B : Variable d'environnement**

```bash
# Linux/Mac
export PDFREST_API_KEY="votre_clé_api_ici"

# Windows
set PDFREST_API_KEY=votre_clé_api_ici
```

**Option C : Argument en ligne de commande**

```bash
python pdf_to_word.py input.pdf --api-key votre_clé_api_ici
```

## 📖 Utilisation

### Conversion d'un fichier unique

```bash
# Conversion simple (sortie automatique: input.docx)
python pdf_to_word.py mon_document.pdf

# Spécifier le fichier de sortie
python pdf_to_word.py mon_document.pdf -o resultat.docx

# Avec timeout personnalisé (en secondes)
python pdf_to_word.py mon_document.pdf --timeout 600
```

### Conversion multiple (dossier)

```bash
# Convertir tous les PDFs d'un dossier
python pdf_to_word.py -d ./mes_pdfs

# Sauvegarder dans un dossier spécifique
python pdf_to_word.py -d ./mes_pdfs -od ./mes_words

# Conversion récursive (inclut les sous-dossiers)
python pdf_to_word.py -d ./mes_pdfs -od ./mes_words --recursive
```

### Conversion avec ajustement automatique des marges (Pipeline complet)

```bash
# Convertir et ajuster toutes les marges à 2.5 cm
python pdf_to_word.py input.pdf --margins 2.5

# Convertir avec des marges spécifiques
python pdf_to_word.py input.pdf --margin-top 3 --margin-bottom 3 --margin-left 2.5 --margin-right 2.5

# Utiliser des inches au lieu de cm
python pdf_to_word.py input.pdf --margins 1 --margin-unit inches

# Conversion multiple avec ajustement des marges
python pdf_to_word.py -d ./mes_pdfs -od ./mes_words --margins 2.5
```

### Édition des marges de documents Word existants

```bash
# Modifier toutes les marges à 2.5 cm
python edit_word_margins.py document.docx --all 2.5

# Modifier des marges spécifiques
python edit_word_margins.py document.docx --top 3 --bottom 3 --left 2.5 --right 2.5

# Avec un fichier de sortie différent
python edit_word_margins.py input.docx -o output.docx --all 2.5

# Modifier plusieurs fichiers dans un dossier
python edit_word_margins.py -d ./documents --all 2.5

# Afficher les marges actuelles d'un document
python edit_word_margins.py document.docx --info
```

### Utilisation en tant que module Python

```python
from pdf_to_word import PDFToWordConverter
from word_editor import WordEditor

# Initialiser le convertisseur
converter = PDFToWordConverter(api_key="votre_clé_api")

# Convertir un fichier
result = converter.convert_pdf_to_word(
    pdf_path="input.pdf",
    output_path="output.docx"
)

if result['success']:
    print(f"✅ Fichier créé: {result['output_file']}")
else:
    print(f"❌ Erreur: {result['message']}")

# Convertir avec ajustement automatique des marges (Pipeline complet)
result = converter.convert_pdf_to_word(
    pdf_path="input.pdf",
    output_path="output.docx",
    adjust_margins=True,
    margin_top=2.5,
    margin_bottom=2.5,
    margin_left=2.5,
    margin_right=2.5,
    margin_unit='cm'
)

# Convertir plusieurs fichiers avec ajustement des marges
results = converter.convert_multiple_pdfs(
    pdf_directory="./pdfs",
    output_directory="./words",
    recursive=True,
    adjust_margins=True,
    margin_top=2.5,
    margin_bottom=2.5,
    margin_left=2.5,
    margin_right=2.5
)

print(f"Conversions réussies: {results['message']}")

# Éditer les marges d'un document Word existant
editor = WordEditor("document.docx")
editor.set_margins(top=2.5, bottom=2.5, left=2.5, right=2.5, unit='cm')
editor.save()
```

## 🎯 Exemples

### Exemple 1 : Conversion simple

```bash
$ python pdf_to_word.py rapport_annuel.pdf

📄 Conversion de: rapport_annuel.pdf
📝 Sortie vers: rapport_annuel.docx
🔄 Envoi du fichier à l'API pdfRest...
✅ Conversion réussie!
💾 Fichier sauvegardé: rapport_annuel.docx
```

### Exemple 2 : Conversion par lot

```bash
$ python pdf_to_word.py -d ./documents -od ./documents_word

📚 5 fichier(s) PDF trouvé(s)
==================================================

[1/5] 📄 Conversion de: doc1.pdf
📝 Sortie vers: documents_word/doc1.docx
✅ Conversion réussie!

[2/5] 📄 Conversion de: doc2.pdf
📝 Sortie vers: documents_word/doc2.docx
✅ Conversion réussie!

...

==================================================
✅ 5/5 conversion(s) réussie(s)
```

## 🔧 Options complètes

### pdf_to_word.py - Convertisseur PDF vers Word

```
usage: pdf_to_word.py [-h] [-o OUTPUT] [-d DIRECTORY] [-od OUTPUT_DIRECTORY]
                      [-r] [--api-key API_KEY] [--timeout TIMEOUT]
                      [--margins SIZE] [--margin-top MARGIN_TOP]
                      [--margin-bottom MARGIN_BOTTOM] [--margin-left MARGIN_LEFT]
                      [--margin-right MARGIN_RIGHT] [--margin-unit {cm,inches,pt}]
                      [input]

positional arguments:
  input                 Fichier PDF à convertir

optional arguments:
  -h, --help            Afficher ce message d'aide
  -o OUTPUT, --output OUTPUT
                        Chemin du fichier Word de sortie
  -d DIRECTORY, --directory DIRECTORY
                        Convertir tous les PDFs d'un dossier
  -od OUTPUT_DIRECTORY, --output-directory OUTPUT_DIRECTORY
                        Dossier de sortie pour les conversions multiples
  -r, --recursive       Chercher récursivement dans les sous-dossiers
  --api-key API_KEY     Clé API pdfRest
  --timeout TIMEOUT     Timeout en secondes (défaut: 300)
  --margins SIZE        Définir toutes les marges à la même valeur
  --margin-top          Marge supérieure
  --margin-bottom       Marge inférieure
  --margin-left         Marge gauche
  --margin-right        Marge droite
  --margin-unit         Unité des marges: cm, inches ou pt (défaut: cm)
```

### edit_word_margins.py - Éditeur de marges Word

```
usage: edit_word_margins.py [-h] [-o OUTPUT] [-d DIRECTORY] [-od OUTPUT_DIRECTORY]
                            [--all MARGIN] [--top TOP] [--bottom BOTTOM]
                            [--left LEFT] [--right RIGHT] [--unit {cm,inches,pt}]
                            [--first-section-only] [--info] [-r]
                            [input]

positional arguments:
  input                 Fichier Word à modifier

optional arguments:
  -h, --help            Afficher ce message d'aide
  -o OUTPUT, --output OUTPUT
                        Fichier de sortie
  -d DIRECTORY, --directory DIRECTORY
                        Modifier tous les fichiers Word d'un dossier
  -od OUTPUT_DIRECTORY, --output-directory OUTPUT_DIRECTORY
                        Dossier de sortie
  --all MARGIN          Définir toutes les marges à la même valeur
  --top TOP             Marge supérieure
  --bottom BOTTOM       Marge inférieure
  --left LEFT           Marge gauche
  --right RIGHT         Marge droite
  --unit {cm,inches,pt} Unité de mesure (défaut: cm)
  --first-section-only  Appliquer seulement à la première section
  --info                Afficher les informations sur le document
  -r, --recursive       Traiter récursivement les sous-dossiers
```

## 📊 Qualité de conversion

L'API pdfRest préserve :

- ✅ **Texte** : 100% éditable, sélectionnable et recherchable
- ✅ **Polices** : Conservées (si disponibles) ou substituées intelligemment
- ✅ **Formatage** : Gras, italique, souligné, barré
- ✅ **Couleurs** : Texte et arrière-plans
- ✅ **Mise en page** : Colonnes, tableaux, listes
- ✅ **Images** : Intégrées dans le document
- ✅ **Liens** : Hyperlinks préservés

## ❓ Dépannage

### Erreur : "La clé API est requise"

Assurez-vous d'avoir défini la variable d'environnement `PDFREST_API_KEY` ou utilisez l'option `--api-key`.

### Erreur HTTP 401 (Unauthorized)

Votre clé API est invalide ou expirée. Vérifiez sur [pdfRest.com](https://pdfrest.com).

### Erreur HTTP 429 (Too Many Requests)

Vous avez dépassé votre quota. Attendez quelques instants ou améliorez votre plan.

### Timeout

Pour les gros fichiers, augmentez le timeout :

```bash
python pdf_to_word.py gros_fichier.pdf --timeout 600
```

### Qualité de conversion insuffisante

L'API pdfRest offre généralement 95-99% de fidélité. Pour des cas complexes :

- Vérifiez que le PDF source est de bonne qualité
- Les PDFs scannés nécessitent l'OCR (non inclus dans cette API)
- Contactez le support pdfRest pour des améliorations

## 🔐 Sécurité

- ⚠️ **Ne commitez JAMAIS votre fichier `.env`** contenant la clé API
- ⚠️ Le fichier `.env` est déjà dans `.gitignore`
- ⚠️ Utilisez des variables d'environnement en production

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amelioration`)
3. Commit vos changements (`git commit -m 'Ajout d'une fonctionnalité'`)
4. Push vers la branche (`git push origin feature/amelioration`)
5. Ouvrir une Pull Request

## 📞 Support

- Documentation API : [docs.pdfrest.com](https://docs.pdfrest.com)
- Support pdfRest : [pdfrest.com/support](https://pdfrest.com/support)
- Issues GitHub : [github.com/votre-username/RestPDF2Word/issues](https://github.com/votre-username/RestPDF2Word/issues)

## 🙏 Remerciements

- [pdfRest.com](https://pdfrest.com) pour leur excellente API
- La communauté Python

---

**Fait avec ❤️ pour simplifier la conversion PDF → Word**
