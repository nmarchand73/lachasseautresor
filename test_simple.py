#!/usr/bin/env python3
"""
Script de test simple pour La Chasse au Trésor
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.simple_generator import SimpleChasseTresorGenerator
from dotenv import load_dotenv

def test_simple_generation():
    """Test de génération simple"""
    print("🧪 Test de génération simple")
    print("=" * 40)
    
    # Load environment
    load_dotenv()
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Erreur: OPENAI_API_KEY non configurée")
        print("Veuillez configurer votre clé API dans le fichier .env")
        return False
    
    try:
        # Initialize generator
        generator = SimpleChasseTresorGenerator()
        
        # Generate test book with 3 sections
        print("📝 Génération d'un livre de test avec 3 sections...")
        book_data = generator.generate_test_book("Les Mystères d'Égypte", 3)
        
        # Save files
        print("💾 Sauvegarde des fichiers...")
        saved_files = generator.save_to_files(book_data, "output")
        
        # Display results
        print("\n✅ Test réussi !")
        print("📊 Résultats :")
        print(f"   - Titre : {book_data['title']}")
        print(f"   - Sections : {book_data['total_sections']}")
        print(f"   - ID : {book_data['id']}")
        
        for fmt, path in saved_files.items():
            print(f"   - Fichier {fmt.upper()} : {Path(path).name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test : {e}")
        import traceback
        traceback.print_exc()
        return False

def test_without_openai():
    """Test sans appel OpenAI (mode fallback)"""
    print("\n🧪 Test mode fallback (sans OpenAI)")
    print("=" * 40)
    
    # Remove API key temporarily
    original_key = os.environ.get("OPENAI_API_KEY")
    if "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"]
    
    try:
        generator = SimpleChasseTresorGenerator()
        
        print("📝 Génération avec mode fallback...")
        book_data = generator.generate_test_book("Test Sans API", 2)
        
        print("💾 Sauvegarde...")
        saved_files = generator.save_to_files(book_data, "output")
        
        print("\n✅ Test fallback réussi !")
        print(f"   - Titre : {book_data['title']}")
        print(f"   - Sections : {book_data['total_sections']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test fallback : {e}")
        return False
    
    finally:
        # Restore API key
        if original_key:
            os.environ["OPENAI_API_KEY"] = original_key

if __name__ == "__main__":
    print("🎯 LA CHASSE AU TRÉSOR - Tests")
    print("=" * 50)
    
    success_count = 0
    total_tests = 2
    
    # Test 1: Simple generation
    if test_simple_generation():
        success_count += 1
    
    # Test 2: Fallback mode
    if test_without_openai():
        success_count += 1
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📊 Résultats : {success_count}/{total_tests} tests réussis")
    
    if success_count == total_tests:
        print("🎉 Tous les tests ont réussi !")
        sys.exit(0)
    else:
        print("⚠️  Certains tests ont échoué")
        sys.exit(1)