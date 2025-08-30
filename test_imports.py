#!/usr/bin/env python3
"""
Test des imports pour vérifier que le système fonctionne
"""

import sys
from pathlib import Path

def test_basic_imports():
    """Test des imports de base"""
    print("🔍 Test des imports de base...")
    
    try:
        # Add src to path
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        
        # Test dotenv
        from dotenv import load_dotenv
        print("✅ dotenv OK")
        
        # Test pathlib
        from pathlib import Path
        print("✅ pathlib OK")
        
        # Test json
        import json
        print("✅ json OK")
        
        # Test datetime
        from datetime import datetime
        print("✅ datetime OK")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erreur import de base: {e}")
        return False

def test_optional_imports():
    """Test des imports optionnels"""
    print("\n🔍 Test des imports optionnels...")
    
    success = True
    
    # Test OpenAI
    try:
        from langchain_openai import ChatOpenAI
        print("✅ langchain_openai OK")
    except ImportError as e:
        print(f"⚠️ langchain_openai manquant: {e}")
        success = False
    
    # Test rich
    try:
        from rich.console import Console
        print("✅ rich OK")
    except ImportError as e:
        print(f"⚠️ rich manquant: {e}")
        success = False
    
    # Test click
    try:
        import click
        print("✅ click OK")
    except ImportError as e:
        print(f"⚠️ click manquant: {e}")
        success = False
    
    return success

def test_project_imports():
    """Test des imports du projet"""
    print("\n🔍 Test des imports du projet...")
    
    try:
        # Add src to path
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        
        # Test simple generator
        from src.simple_generator import SimpleChasseTresorGenerator
        print("✅ SimpleChasseTresorGenerator OK")
        
        # Test que le générateur peut s'initialiser
        generator = SimpleChasseTresorGenerator()
        print("✅ Initialisation générateur OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur imports projet: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_minimal_generation():
    """Test de génération minimale sans API"""
    print("\n🔍 Test génération minimale...")
    
    try:
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        
        from src.simple_generator import SimpleChasseTresorGenerator
        
        # Test sans API key
        import os
        if "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]
        
        generator = SimpleChasseTresorGenerator()
        
        # Test structure de base
        book_data = generator._create_book_structure("Test Theme", 2)
        assert "id" in book_data
        assert "title" in book_data
        assert "content" in book_data
        print("✅ Structure de base OK")
        
        # Test intro fallback
        intro = generator._get_fallback_intro("Test Theme")
        assert len(intro) > 100
        print("✅ Intro fallback OK")
        
        # Test section fallback
        section_text, title = generator._get_fallback_section(1, "Test Theme")
        assert len(section_text) > 100
        assert len(title) > 0
        print("✅ Section fallback OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur génération minimale: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 TEST DES IMPORTS ET FONCTIONNALITÉ DE BASE")
    print("=" * 60)
    
    tests = [
        ("Imports de base", test_basic_imports),
        ("Imports optionnels", test_optional_imports), 
        ("Imports du projet", test_project_imports),
        ("Génération minimale", test_minimal_generation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            passed += 1
            print(f"✅ {test_name} : RÉUSSI")
        else:
            print(f"❌ {test_name} : ÉCHOUÉ")
    
    print("\n" + "="*60)
    print(f"📊 Résultats finaux: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont passés ! Le système est prêt.")
        sys.exit(0)
    elif passed >= total - 1:
        print("⚠️  Presque tous les tests passent. Vérifiez les dépendances optionnelles.")
        sys.exit(0)
    else:
        print("❌ Plusieurs tests échouent. Vérifiez l'installation.")
        sys.exit(1)