#!/usr/bin/env python3
"""
Script d'installation et vérification CrewAI pour La Chasse au Trésor
"""
import subprocess
import sys
from pathlib import Path


def check_python_version():
    """Vérifie la version Python"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ requis. Version actuelle:", sys.version)
        return False
    else:
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} compatible")
        return True


def install_dependencies():
    """Installe les dépendances CrewAI"""
    print("\n🔧 Installation des dépendances CrewAI...")
    
    try:
        # Lire requirements.txt
        requirements_file = Path(__file__).parent / "requirements.txt"
        
        if not requirements_file.exists():
            print("❌ Fichier requirements.txt introuvable")
            return False
        
        # Installer via pip
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dépendances installées avec succès!")
            return True
        else:
            print(f"❌ Erreur installation: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def test_crewai_import():
    """Test l'importation de CrewAI"""
    print("\n🧪 Test d'importation CrewAI...")
    
    try:
        import crewai
        from crewai import Agent, Task, Crew
        print(f"✅ CrewAI version {crewai.__version__} importé avec succès")
        return True
    except ImportError as e:
        print(f"❌ Impossible d'importer CrewAI: {e}")
        return False


def test_project_import():
    """Test l'importation du générateur CrewAI du projet"""
    print("\n🎯 Test du générateur projet...")
    
    try:
        # Ajouter le répertoire src au path
        src_path = Path(__file__).parent / "src"
        sys.path.insert(0, str(src_path))
        
        from crewai_generator import ChasseTresorCrewGenerator
        print("✅ Générateur CrewAI du projet importé avec succès")
        return True
    except ImportError as e:
        print(f"❌ Impossible d'importer le générateur: {e}")
        return False


def show_usage_examples():
    """Affiche des exemples d'utilisation"""
    print("\n" + "="*50)
    print("🚀 EXEMPLES D'UTILISATION CREWAI")
    print("="*50)
    print()
    print("1. Mode CrewAI dédié (recommandé):")
    print("   python -m src.main crewai --theme 'Les Mystères d'Égypte'")
    print()
    print("2. Mode interactif CrewAI:")
    print("   python -m src.main crewai")
    print()
    print("3. Commandes existantes avec CrewAI:")
    print("   python -m src.main create --crew")
    print("   python -m src.main generate --crew --theme 'Les Trésors de Petra'")
    print()
    print("4. Vérifier le statut du système:")
    print("   python -m src.main info")
    print()
    print("💡 Le mode CrewAI offre:")
    print("   • Génération 3-5x plus rapide")
    print("   • 6 agents spécialisés (Jacques Antoine, Philippe Gildas...)")
    print("   • Qualité narrative supérieure")
    print("   • Authenticité 'La Chasse au Trésor' garantie")


def main():
    """Fonction principale"""
    print("🎬 INSTALLATION CREWAI - LA CHASSE AU TRÉSOR")
    print("="*50)
    
    # Étapes de vérification et installation
    steps_ok = True
    
    # 1. Version Python
    if not check_python_version():
        steps_ok = False
    
    # 2. Installation dépendances
    if steps_ok:
        if not install_dependencies():
            steps_ok = False
    
    # 3. Test importation CrewAI
    if steps_ok:
        if not test_crewai_import():
            steps_ok = False
    
    # 4. Test importation projet
    if steps_ok:
        if not test_project_import():
            steps_ok = False
    
    # Résultat final
    print("\n" + "="*50)
    if steps_ok:
        print("🎉 INSTALLATION CREWAI RÉUSSIE!")
        print("="*50)
        show_usage_examples()
    else:
        print("❌ INSTALLATION ÉCHOUÉE")
        print("="*50)
        print("\n🔧 Solutions possibles:")
        print("1. Vérifiez votre connexion internet")
        print("2. Mettez à jour pip: python -m pip install --upgrade pip")
        print("3. Réessayez: python install_crewai.py")
        print("4. Installation manuelle: pip install crewai crewai-tools")


if __name__ == "__main__":
    main()