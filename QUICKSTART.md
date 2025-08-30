# 🚀 Guide de Démarrage Rapide

## 1. Vérification de l'installation

```bash
# Tester les imports et fonctionnalités de base
python test_imports.py
```

Si tous les tests passent, vous pouvez continuer. Sinon :

```bash
# Installer les dépendances
pip install -r requirements.txt
```

## 2. Configuration de l'API OpenAI

```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer .env et ajouter votre clé API
# OPENAI_API_KEY=votre_cle_ici
```

## 3. Premier test (RECOMMANDÉ)

```bash
# Mode test : génère seulement 3 sections (rapide)
python -m src.main test
```

Cette commande va :
- Générer un livre de test avec 3 sections
- Le sauvegarder en JSON et Markdown
- Afficher un aperçu

## 4. Tests complets

```bash
# Test complet du système
python test_simple.py
```

## 5. Génération personnalisée

```bash
# Test avec thème personnalisé
python -m src.main test --theme "Les Pyramides de Gizeh" --sections 5

# Génération complète (95 sections - LENT)
python -m src.main generate --theme "Les Mystères d'Égypte"
```

## 6. Visualisation des résultats

Les fichiers sont sauvegardés dans :
- `output/books/` : Fichiers JSON
- `output/markdown/` : Fichiers Markdown

```bash
# Lister les livres générés
python -m src.main list-books

# Prévisualiser un livre
python -m src.main preview output/books/votre_livre.json
```

## 📊 Résolution des problèmes courants

### Erreur "OPENAI_API_KEY non configurée"
- Vérifiez que le fichier `.env` existe
- Vérifiez que `OPENAI_API_KEY=votre_cle` est défini
- Redémarrez le terminal après modification

### Erreur d'import
- Exécutez `pip install -r requirements.txt`
- Vérifiez que Python 3.10+ est utilisé

### Génération lente
- Utilisez le mode test : `python -m src.main test`
- Réduisez le nombre de sections : `--sections 2`

### Pas de clé OpenAI
- Le système fonctionne en mode "fallback" sans API
- Le contenu sera générique mais la structure sera correcte

## 🎯 Commandes Essentielles

```bash
# Test rapide
python -m src.main test

# Test avec paramètres
python -m src.main test --theme "Votre Thème" --sections 3

# Informations système
python -m src.main info

# Aide complète
python -m src.main --help
```

## ✅ Validation de Fonctionnement

Si vous voyez ces fichiers après `python -m src.main test` :
- `output/books/lachasseautresor_*.json`
- `output/markdown/lachasseautresor_*.md`

🎉 **Le système fonctionne parfaitement !**