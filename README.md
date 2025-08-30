# 🚁 La Chasse au Trésor - Générateur de Livres d'Aventure

Système basé sur CrewAI pour générer automatiquement des livres d'aventure interactifs "dont vous êtes le héros" inspirés de l'émission culte des années 80 "La Chasse au Trésor" avec Philippe de Dieuleveult.

## 📚 Description

Ce projet génère automatiquement des livres d'aventure interactifs "dont vous êtes le héros" inspirés de l'émission "La Chasse au Trésor" des années 80. Le système utilise l'IA pour créer des histoires authentiques avec :

- **Ton Philippe de Dieuleveult** : Enthousiasme et émerveillement authentique
- **Énigmes culturelles** : Basées sur l'histoire et la géographie
- **Format TV années 80** : Structure en épisodes avec suspense
- **Descriptions immersives** : Lieux exotiques et rencontres locales
- **Choix narratifs** : Embranchements multiples pour la rejouabilité

## 🚀 Installation

1. **Cloner le repository**
```bash
git clone https://github.com/nmarchand73/lachasseautresor.git
cd lachasseauxtresor
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer l'API OpenAI**
```bash
cp .env.example .env
# Éditer .env et ajouter votre clé OPENAI_API_KEY
```

## 📖 Utilisation

### Test rapide (recommandé)

```bash
# Test du système complet avec génération d'exemple
python test_clean.py
```

### Générer un livre

```bash
# Génération simple (format Markdown par défaut)
python -m src.main generate

# Génération avec thème spécifique
python -m src.main generate --theme "Les Mystères d'Égypte"

# Génération en format JSON
python -m src.main generate --format json

# Génération dans les deux formats
python -m src.main generate --format both

# Mode verbose pour voir les détails
python -m src.main generate -v
```

### Autres commandes disponibles

```bash
# Lister les livres générés
python -m src.main list-books

# Prévisualiser un livre Markdown
python -m src.main preview output/markdown/livre.md

# Nettoyer les anciens fichiers
python -m src.main clean

# Afficher l'aide
python -m src.main --help
```

## 📁 Structure du Projet

```
lachasseauxtresor/
├── src/
│   ├── simple_generator.py    # Générateur principal
│   ├── main.py               # CLI interface
│   └── utils/                # Utilitaires
│       ├── file_handler.py   # Gestion fichiers
│       └── json_formatter.py # Format JSON
├── output/                   # Livres générés
│   ├── books/               # Fichiers JSON
│   └── markdown/            # Fichiers Markdown
├── brief/                   # Documentation du projet
│   ├── concept.md           # Concept original
│   ├── PRD_*.md            # Spécifications
│   └── book_golden_bullets.json # Exemple format
├── test_*.py               # Scripts de test
├── CLAUDE.md              # Instructions pour Claude
├── QUICKSTART.md          # Guide rapide
└── requirements.txt       # Dépendances
```

## 📊 Formats de Sortie

Les livres peuvent être générés dans deux formats :

### Format Markdown (par défaut)
Structure organisée avec :
- Table des matières avec liens
- Sections numérotées avec titres
- Formatage lisible pour les humains
- Compatible avec les éditeurs Markdown

### Format Golden Bullets JSON  
Format technique avec :
- 95 paragraphes numérotés
- Sections spéciales (title, intro)
- 2-3 choix par paragraphe
- Longueur de 2000-2500 caractères par paragraphe

### Exemple de structure JSON

```json
{
  "id": "lachasseautresor_egypte",
  "title": "La Chasse au Trésor: Les Mystères d'Égypte",
  "content": {
    "title": { ... },
    "intro": { ... },
    "1": {
      "paragraph_number": 1,
      "text": "#01\n- Titre\nContenu...",
      "choices": [
        {
          "text": "Action\nAller au numéro #12",
          "destination": 12
        }
      ],
      "combat": null
    },
    ...
  }
}
```

## 🔧 Configuration

Éditer le fichier `.env` pour personnaliser :

```env
# Clé API OpenAI (optionnelle - fallback sans IA disponible)
OPENAI_API_KEY=your_key_here

# Modèle OpenAI
OPENAI_MODEL_NAME=gpt-4o-mini

# Paramètres de génération
TEMPERATURE=0.7
MAX_TOKENS=2000
```

## 🎯 Workflow de Génération

1. **Initialisation** : Configuration du thème et de la structure (95 paragraphes)
2. **Génération** : Création du contenu avec IA (ou fallback statique)
3. **Formatage** : Export en Markdown (lisible) et/ou JSON (Golden Bullets)
4. **Sauvegarde** : Fichiers horodatés dans output/

## ⚙️ État Actuel

**Version actuelle** : Système de génération fonctionnel avec :
- ✅ Interface CLI complète
- ✅ Générateur de contenu (avec/sans IA)
- ✅ Export Markdown et JSON
- ✅ Validation basique
- ✅ Tests automatisés
- 🚧 Integration CrewAI (en développement)

## 🧪 Tests

```bash
# Test complet du système nettoyé
python test_clean.py

# Tests des imports (optionnel)
python test_imports.py
```

## 📝 License

MIT License - Voir [LICENSE](LICENSE) pour plus de détails.

## 🙏 Crédits

Inspiré par l'émission "La Chasse au Trésor" (1981-1984) créée par Jacques Antoine et présentée par Philippe Gildas et Philippe de Dieuleveult.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📧 Contact

Pour toute question ou suggestion, ouvrez une issue sur GitHub.