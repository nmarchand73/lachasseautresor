#!/usr/bin/env python3
"""
Test du système nettoyé
"""

import sys
from pathlib import Path

def test_clean_system():
    """Test du système nettoyé"""
    print("🧹 TEST DU SYSTÈME NETTOYÉ")
    print("=" * 40)
    
    try:
        # Add src to path
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        
        # Test imports minimaux
        from src.simple_generator import SimpleChasseTresorGenerator
        print("✅ Import générateur OK")
        
        # Test initialisation
        generator = SimpleChasseTresorGenerator()
        print("✅ Initialisation OK")
        
        # Test génération basique
        print("\n📝 Test génération basique...")
        book_data = generator.generate_test_book("Test Clean", 2)
        
        # Vérifications basiques
        assert "id" in book_data
        assert "title" in book_data
        assert "content" in book_data
        assert book_data["total_sections"] == 2
        
        content = book_data["content"]
        assert "title" in content
        assert "intro" in content
        assert "1" in content
        assert "2" in content
        
        print("✅ Structure du livre OK")
        
        # Test sauvegarde
        print("\n💾 Test sauvegarde...")
        saved_files = generator.save_to_files(book_data, "output")
        
        assert "json" in saved_files
        assert "markdown" in saved_files
        
        # Vérifier que les fichiers existent
        for fmt, filepath in saved_files.items():
            if not Path(filepath).exists():
                raise FileNotFoundError(f"Fichier {fmt} non trouvé: {filepath}")
        
        print("✅ Sauvegarde OK")
        
        # Test du contenu Markdown
        with open(saved_files["markdown"], 'r', encoding='utf-8') as f:
            md_content = f.read()
            
        assert "# Story Content" in md_content
        assert "## Table of Contents" in md_content
        assert "## Section 1:" in md_content
        assert "## Section 2:" in md_content
        
        print("✅ Format Markdown OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cli_imports():
    """Test des imports du CLI"""
    print("\n🖥️ TEST IMPORTS CLI")
    print("=" * 20)
    
    try:
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        
        # Test imports CLI
        import click
        from rich.console import Console
        from rich.progress import Progress
        print("✅ Imports CLI OK")
        
        # Test import main (sans exécution)
        from src import main
        print("✅ Import main OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur imports CLI: {e}")
        return False

def test_file_structure():
    """Test de la structure des fichiers"""
    print("\n📁 TEST STRUCTURE FICHIERS")
    print("=" * 27)
    
    required_files = [
        "src/simple_generator.py",
        "src/main.py", 
        "src/__init__.py",
        "src/utils/__init__.py",
        "src/utils/file_handler.py",
        "requirements.txt",
        "README.md",
        "QUICKSTART.md"
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print(f"\n❌ Fichiers manquants:")
        for file_path in missing_files:
            print(f"  • {file_path}")
        return False
    
    print("\n✅ Structure complète OK")
    return True

if __name__ == "__main__":
    print("🎯 LA CHASSE AU TRÉSOR - Test Système Nettoyé")
    print("=" * 50)
    
    tests = [
        ("Structure des fichiers", test_file_structure),
        ("Imports CLI", test_cli_imports),
        ("Système complet", test_clean_system)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*10} {test_name} {'='*10}")
        if test_func():
            passed += 1
            print(f"✅ {test_name} : RÉUSSI")
        else:
            print(f"❌ {test_name} : ÉCHOUÉ")
    
    print("\n" + "="*50)
    print(f"📊 Résultats finaux: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Système nettoyé et fonctionnel !")
        
        print("\n🚀 Commandes disponibles:")
        print("  python -m src.main test                    # Test rapide")
        print("  python -m src.main generate --sections 5   # 5 sections")
        print("  python -m src.main validate output/books/livre.json")
        print("  python -m src.main list-books")
        print("  python -m src.main info")
        
        sys.exit(0)
    else:
        print("❌ Le système nécessite des corrections")
        sys.exit(1)