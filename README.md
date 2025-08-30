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

### Générer un livre

```bash
# MODE TEST (RECOMMANDÉ POUR DÉBUTER) - Génère seulement 3 sections
python -m src.main test

# Test avec thème personnalisé et plus de sections
python -m src.main test --theme "Les Pyramides de Gizeh" --sections 5

# GÉNÉRATION COMPLÈTE (95 sections) - Plus lent
python -m src.main generate --theme "Les Mystères d'Égypte"

# Génération en format JSON uniquement
python -m src.main generate --format json

# Mode verbose pour voir les détails
python -m src.main generate -v
```

### Valider un livre existant

```bash
# Validation simple
python -m src.main validate output/books/monlivre.json

# Validation détaillée avec rapport
python -m src.main validate output/books/monlivre.json --detailed
```

### Autres commandes

```bash
# Test rapide du système complet (RECOMMANDÉ APRÈS INSTALLATION)
python test_clean.py

# Lister tous les livres générés
python -m src.main list-books

# Prévisualiser un livre en format Markdown
python -m src.main preview output/books/monlivre.json

# Nettoyer les anciens fichiers (>30 jours)
python -m src.main clean

# Afficher les informations système
python -m src.main info
```

## 📁 Structure du Projet

```
lachasseauxtresor/
├── src/
│   ├── simple_generator.py    # Générateur principal
│   ├── main.py               # CLI interface
│   └── utils/                # Utilitaires
│       ├── file_handler.py   # Gestion fichiers
│       ├── json_formatter.py # Format JSON
│       └── markdown_formatter.py # Format Markdown
├── output/                   # Livres générés
│   ├── books/               # Fichiers JSON
│   └── markdown/            # Fichiers Markdown
├── brief/                   # Documentation du projet
├── test_clean.py           # Tests système
├── QUICKSTART.md           # Guide rapide
└── requirements.txt        # Dépendances (simplifiées)
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
# Modèle OpenAI
OPENAI_MODEL_NAME=gpt-4-turbo-preview
TEMPERATURE=0.7
MAX_TOKENS=2000

# Configuration CrewAI
CREW_VERBOSE=true
CREW_MEMORY=true
CREW_MAX_ITER=50
```

## 🎯 Workflow de Génération

1. **Thème et Structure** : Sélection automatique du thème et nombre de sections
2. **Génération IA** : Création des sections avec OpenAI (fallback sans API)
3. **Formatage** : Export automatique en JSON et Markdown
4. **Validation** : Vérification basique de la structure

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