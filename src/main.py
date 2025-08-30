"""
Main entry point for La Chasse au Trésor book generator
"""
import click
import os
import sys
import signal
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm, IntPrompt
from rich import print as rprint
import json
from typing import Optional, Dict, Any

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.simple_generator import SimpleChasseTresorGenerator

# Load environment variables
load_dotenv()

# Initialize Rich console
console = Console()

# Import CrewAI generator with fallback
try:
    from src.crewai_generator_v2 import ChasseTresorCrewGeneratorV2 as ChasseTresorCrewGenerator
    CREWAI_AVAILABLE = True
except ImportError as e:
    CREWAI_AVAILABLE = False
    # Silent fallback - will be shown in info command

# Global flag for handling interruption
interrupted = False

def signal_handler(signum, frame):
    """Handle CTRL+C interruption"""
    global interrupted
    interrupted = True
    console.print("\n[yellow]⚠️ Interruption détectée... Arrêt en cours...[/yellow]")
    raise KeyboardInterrupt("Processus interrompu par l'utilisateur")

# Set up signal handler for CTRL+C
signal.signal(signal.SIGINT, signal_handler)


def collect_adventure_info() -> Dict[str, Any]:
    """
    Collecte interactivement les informations sur l'aventure
    """
    console.print(Panel.fit(
        "[bold cyan]🎯 CONFIGURATION DE L'AVENTURE[/bold cyan]\n"
        "[yellow]Créons ensemble votre livre d'aventure personnalisé![/yellow]",
        border_style="cyan"
    ))
    
    # Suggestions de thèmes par région
    theme_suggestions = {
        "Égypte": ["Les Mystères des Pyramides", "Les Secrets du Nil", "Les Trésors de Pharaon"],
        "France": ["Les Châteaux de la Loire", "Les Mystères du Mont-Saint-Michel", "Les Secrets de Versailles"],
        "Grèce": ["Les Mystères de l'Olympe", "Les Secrets de Delphes", "L'Atlantide Retrouvée"],
        "Pérou": ["Les Trésors des Incas", "Le Mystère de Machu Picchu", "L'Or du Pérou"],
        "Égypte antique": ["Les Mystères d'Égypte", "Les Pharaons Perdus", "Les Gardiens du Sphinx"],
        "Cambodge": ["Les Secrets d'Angkor", "Les Temples Perdus", "L'Empire Khmer"],
        "Jordanie": ["Les Trésors de Petra", "Les Mystères Nabatéens", "La Cité Rose"],
        "Tibet": ["Les Monastères Secrets", "Le Toit du Monde", "Les Sages de l'Himalaya"],
        "Autre": []
    }
    
    console.print("\n[bold yellow]📍 ÉTAPE 1 : Choisissez votre destination[/bold yellow]")
    countries = list(theme_suggestions.keys())
    
    console.print("\nDestinations disponibles :")
    for i, country in enumerate(countries, 1):
        if country != "Autre":
            console.print(f"  [cyan]{i}.[/cyan] {country}")
        else:
            console.print(f"  [cyan]{i}.[/cyan] Autre destination (à préciser)")
    
    while True:
        try:
            choice = IntPrompt.ask(
                f"\nChoisissez votre destination (1-{len(countries)})",
                default=1
            )
            if 1 <= choice <= len(countries):
                selected_country = countries[choice - 1]
                break
            else:
                console.print("[red]❌ Choix invalide. Veuillez réessayer.[/red]")
        except:
            console.print("[red]❌ Veuillez entrer un numéro valide.[/red]")
    
    # Si "Autre", demander le pays
    if selected_country == "Autre":
        selected_country = Prompt.ask(
            "[yellow]Précisez votre destination",
            default="Mystérieuse contrée lointaine"
        )
    
    console.print(f"\n[green]✅ Destination sélectionnée : {selected_country}[/green]")
    
    # Choix du thème
    console.print(f"\n[bold yellow]🎭 ÉTAPE 2 : Choisissez votre thème d'aventure[/bold yellow]")
    
    original_country = selected_country if selected_country in theme_suggestions else "Autre"
    suggestions = theme_suggestions.get(original_country, [])
    
    if suggestions:
        console.print(f"\nThèmes suggérés pour {selected_country} :")
        for i, theme in enumerate(suggestions, 1):
            console.print(f"  [cyan]{i}.[/cyan] {theme}")
        console.print(f"  [cyan]{len(suggestions)+1}.[/cyan] Thème personnalisé")
        
        while True:
            try:
                theme_choice = IntPrompt.ask(
                    f"\nChoisissez un thème (1-{len(suggestions)+1})",
                    default=1
                )
                if 1 <= theme_choice <= len(suggestions):
                    selected_theme = suggestions[theme_choice - 1]
                    break
                elif theme_choice == len(suggestions) + 1:
                    selected_theme = Prompt.ask(
                        "[yellow]Précisez votre thème personnalisé",
                        default=f"Les Mystères de {selected_country}"
                    )
                    break
                else:
                    console.print("[red]❌ Choix invalide. Veuillez réessayer.[/red]")
            except:
                console.print("[red]❌ Veuillez entrer un numéro valide.[/red]")
    else:
        selected_theme = Prompt.ask(
            f"[yellow]Quel thème pour votre aventure en {selected_country} ?",
            default=f"Les Mystères de {selected_country}"
        )
    
    console.print(f"[green]✅ Thème sélectionné : {selected_theme}[/green]")
    
    # Choix du nombre de paragraphes
    console.print(f"\n[bold yellow]📖 ÉTAPE 3 : Longueur de votre livre[/bold yellow]")
    console.print("""
Modes disponibles :
  [cyan]1.[/cyan] 🏃 Aventure courte (10-20 paragraphes) - Lecture d'1 heure  
  [cyan]2.[/cyan] 📖 Aventure standard (30-50 paragraphes) - Format équilibré
  [cyan]3.[/cyan] 📚 Livre complet (95 paragraphes) - Format Golden Bullets authentique
  [cyan]4.[/cyan] 🎯 Nombre personnalisé
""")
    
    length_options = {
        1: ("Aventure courte", 15),
        2: ("Aventure standard", 35),
        3: ("Livre complet", 95),
        4: ("Personnalisé", None)
    }
    
    while True:
        try:
            length_choice = IntPrompt.ask("Choisissez la longueur (1-4)", default=2)
            if length_choice in length_options:
                length_name, sections = length_options[length_choice]
                if sections is None:
                    sections = IntPrompt.ask(
                        "Nombre de paragraphes souhaité (1-200)",
                        default=30
                    )
                    if not 1 <= sections <= 200:
                        console.print("[red]❌ Le nombre doit être entre 1 et 200.[/red]")
                        continue
                    length_name = f"Personnalisé ({sections} paragraphes)"
                break
            else:
                console.print("[red]❌ Choix invalide. Veuillez réessayer.[/red]")
        except:
            console.print("[red]❌ Veuillez entrer un numéro valide.[/red]")
    
    console.print(f"[green]✅ Longueur sélectionnée : {length_name}[/green]")
    
    
    # Résumé final
    console.print(Panel.fit(
        f"[bold green]🎯 CONFIGURATION TERMINÉE[/bold green]\n\n"
        f"[cyan]Destination :[/cyan] {selected_country}\n"
        f"[cyan]Thème :[/cyan] {selected_theme}\n"  
        f"[cyan]Paragraphes :[/cyan] {sections}\n"
        f"[cyan]Mode :[/cyan] Standard",
        border_style="green"
    ))
    
    if not Confirm.ask("\n[yellow]Confirmer et commencer la génération ?[/yellow]", default=True):
        console.print("[red]❌ Génération annulée[/red]")
        return None
    
    return {
        "country": selected_country,
        "theme": selected_theme,
        "sections": sections
    }


@click.group()
def cli():
    """
    🎯 LA CHASSE AU TRÉSOR - Adventure Book Generator
    
    Generate interactive adventure books inspired by the 1980s French TV show.
    
    Examples:
      python -m src.main generate -t "Egyptian Mysteries" -s 10
      python -m src.main generate --crew --interactive
      python -m src.main info
    """
    pass


# Commande create supprimée - fonctionnalité intégrée dans generate


@cli.command()
@click.option('-t', '--theme', help='Adventure theme (interactive if not specified)')
@click.option('-s', '--sections', type=click.IntRange(1, 200), help='Number of sections (3=quick, 95=standard, 200=max)')
@click.option('-o', '--output', default='output', help='Output directory')
@click.option('-i', '--interactive', is_flag=True, help='Interactive mode for theme selection')
@click.option('-c', '--crew', is_flag=True, help='Use CrewAI multi-agent system (better quality)')
def generate(theme: str, sections: int, output: str, interactive: bool, crew: bool):
    """Generate an adventure book with customizable sections"""
    # Si mode interactif demandé ou si pas de thème fourni, utiliser le questionnaire
    if interactive or not theme:
        adventure_info = collect_adventure_info()
        if not adventure_info:
            return 0
        
        theme = adventure_info['theme']
        sections = adventure_info['sections'] if not sections else sections
        country = adventure_info['country']
    else:
        # Valeurs par défaut si non interactif
        if not sections:
            sections = 95
        country = "Destination mystérieuse"
    
    # Vérification et affichage du mode
    if crew and not CREWAI_AVAILABLE:
        console.print("[red]❌ Mode CrewAI demandé mais non disponible[/red]")
        console.print("[yellow]Installez: pip install crewai crewai-tools[/yellow]")
        crew = False
    
    # Affichage du mode en fonction du nombre de sections et du système
    generation_system = "🤖 CrewAI Multi-Agents" if crew else "🔧 Générateur Simple"
    
    if sections <= 20:
        mode = f"🏃 MODE COURT ({generation_system})"
        color = "blue" if not crew else "cyan"
        advice = "Livre d'aventure court et dynamique"
    elif sections <= 95:
        mode = f"📖 MODE STANDARD ({generation_system})"
        color = "green" if not crew else "cyan"
        advice = "Livre d'aventure de taille moyenne"
    else:
        mode = f"📚 MODE GOLDEN BULLETS ({generation_system})"
        color = "cyan"
        advice = "Format officiel avec 95+ paragraphes"
    
    if not interactive and theme:
        console.print(Panel.fit(
            f"[bold {color}]{mode}[/bold {color}]\n"
            f"[white]{advice}[/white]\n"
            f"[yellow]{sections} paragraphes à générer[/yellow]",
            border_style=color
        ))
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        console.print("[bold red]❌ Erreur: OPENAI_API_KEY non configurée[/bold red]")
        console.print("Veuillez configurer votre clé API dans le fichier .env")
        return 1
    
    try:
        # Choisir le générateur selon le mode
        if crew and CREWAI_AVAILABLE:
            console.print(f"[cyan]🤖 Initialisation du système CrewAI...[/cyan]")
            generator = ChasseTresorCrewGenerator()
            generation_mode = "CrewAI Multi-Agents"
        else:
            generator = SimpleChasseTresorGenerator()
            generation_mode = "Générateur Simple"
        
        # Génération selon le type de générateur
        if crew and CREWAI_AVAILABLE:
            # Mode CrewAI : Progress intégré dans le générateur
            book_data = generator.generate_book(theme, sections)
        else:
            # Mode Simple : Progress externe
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task(f"[green]Génération de {sections} sections...", total=None)
                book_data = generator.generate_book(theme, sections)
                progress.update(task, completed=100)
        
        # Sauvegarde commune
        saved_files = generator.save_to_files(book_data, output)
        
        console.print(f"\n[bold green]✅ Livre de {sections} paragraphes généré ![/bold green]")
        
        # Display results
        table = Table(title="📚 Livre Généré", border_style="green")
        table.add_column("Propriété", style="cyan")
        table.add_column("Valeur", style="yellow")
        
        table.add_row("Destination", country if 'country' in locals() else "Non spécifiée")
        table.add_row("Thème", theme)
        table.add_row("Paragraphes", str(sections))
        table.add_row("Mode Génération", generation_mode)
        table.add_row("ID", book_data["id"])
        
        for fmt, filepath in saved_files.items():
            table.add_row(f"Fichier {fmt.upper()}", Path(filepath).name)
        
        console.print(table)
        console.print(f"\n[green]📁 Fichiers sauvegardés dans: {output}/[/green]")
        
    except KeyboardInterrupt:
        console.print(f"\n[yellow]⏹️ Génération annulée par l'utilisateur[/yellow]")
        return 0
    except Exception as e:
        console.print(f"[bold red]❌ Erreur: {str(e)}[/bold red]")
        return 1
    
    return 0


# Commande crewai supprimée - fonctionnalité intégrée dans generate avec flag --crew


# Commandes de gestion des livres supprimées - fonctionnalité inutile


@cli.command()
def info():
    """Show system information and configuration"""
    console.print(Panel.fit(
        "[bold cyan]ℹ️ INFORMATIONS SYSTÈME[/bold cyan]",
        border_style="cyan"
    ))
    
    table = Table(border_style="cyan")
    table.add_column("Paramètre", style="cyan")
    table.add_column("Valeur", style="yellow")
    
    # Check environment
    api_key = os.getenv("OPENAI_API_KEY")
    table.add_row("API Key OpenAI", "✅ Configurée" if api_key else "❌ Non configurée")
    table.add_row("Modèle", os.getenv("OPENAI_MODEL_NAME", "gpt-4-turbo-preview"))
    table.add_row("Température", os.getenv("TEMPERATURE", "0.7"))
    table.add_row("Max Tokens", os.getenv("MAX_TOKENS", "2000"))
    
    # CrewAI settings
    table.add_row("CrewAI Disponible", "✅ Oui" if CREWAI_AVAILABLE else "❌ Non (pip install crewai)")
    if CREWAI_AVAILABLE:
        table.add_row("CrewAI Verbose", os.getenv("CREW_VERBOSE", "true"))
        table.add_row("CrewAI Memory", os.getenv("CREW_MEMORY", "true"))
        table.add_row("CrewAI Max Iter", os.getenv("CREW_MAX_ITER", "50"))
    
    # Output settings
    table.add_row("Répertoire de sortie", os.getenv("OUTPUT_DIR", "output"))
    
    console.print(table)
    
    # Instructions
    if not api_key:
        console.print("\n[yellow]⚠️ Pour configurer votre clé API:[/yellow]")
        console.print("1. Copiez .env.example vers .env")
        console.print("2. Ajoutez votre clé OpenAI dans OPENAI_API_KEY")
        console.print("3. Relancez la commande")
    
    if not CREWAI_AVAILABLE:
        console.print("\n[cyan]🤖 Pour activer CrewAI (recommandé):[/cyan]")
        console.print("1. pip install crewai crewai-tools")
        console.print("2. Utilisez: python -m src.main generate --crew")
        console.print("3. Ou ajoutez --crew à vos commandes")
        console.print("\n[green]✨ Avantages CrewAI:[/green]")
        console.print("• Génération 3-5x plus rapide")
        console.print("• Qualité narrative supérieure")
        console.print("• 6 agents spécialisés (Jacques Antoine, Philippe Gildas...)")
        console.print("• Authenticité 'La Chasse au Trésor' garantie")


if __name__ == "__main__":
    cli()