"""
Main entry point for La Chasse au Trésor book generator
"""
import click
import os
import sys
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
from src.utils import FileHandler

# Load environment variables
load_dotenv()

# Initialize Rich console
console = Console()


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
  [cyan]1.[/cyan] 🧪 Test rapide (3-5 paragraphes) - Pour découvrir rapidement
  [cyan]2.[/cyan] 🏃 Aventure courte (10-20 paragraphes) - Lecture d'1 heure  
  [cyan]3.[/cyan] 📖 Aventure standard (30-50 paragraphes) - Format équilibré
  [cyan]4.[/cyan] 📚 Livre complet (95 paragraphes) - Format Golden Bullets authentique
  [cyan]5.[/cyan] 🎯 Nombre personnalisé
""")
    
    length_options = {
        1: ("Test rapide", 5),
        2: ("Aventure courte", 15),
        3: ("Aventure standard", 35),
        4: ("Livre complet", 95),
        5: ("Personnalisé", None)
    }
    
    while True:
        try:
            length_choice = IntPrompt.ask("Choisissez la longueur (1-5)", default=2)
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
    
    # Mode de génération
    console.print(f"\n[bold yellow]⚡ ÉTAPE 4 : Mode de génération[/bold yellow]")
    is_test = sections <= 10
    
    if is_test:
        console.print("[yellow]Mode test automatiquement sélectionné (≤10 paragraphes)[/yellow]")
    else:
        use_test = Confirm.ask(
            "Utiliser le mode test pour une génération plus rapide ?",
            default=False
        )
        is_test = use_test
    
    # Résumé final
    console.print(Panel.fit(
        f"[bold green]🎯 CONFIGURATION TERMINÉE[/bold green]\n\n"
        f"[cyan]Destination :[/cyan] {selected_country}\n"
        f"[cyan]Thème :[/cyan] {selected_theme}\n"  
        f"[cyan]Paragraphes :[/cyan] {sections}\n"
        f"[cyan]Mode :[/cyan] {'Test (rapide)' if is_test else 'Standard (détaillé)'}",
        border_style="green"
    ))
    
    if not Confirm.ask("\n[yellow]Confirmer et commencer la génération ?[/yellow]", default=True):
        console.print("[red]❌ Génération annulée[/red]")
        return None
    
    return {
        "country": selected_country,
        "theme": selected_theme,
        "sections": sections,
        "test_mode": is_test
    }


@click.group()
def cli():
    """
    🎯 LA CHASSE AU TRÉSOR - Générateur de Livres d'Aventure
    
    Système basé sur CrewAI pour générer des livres d'aventure interactifs
    inspirés de l'émission culte des années 80.
    """
    pass


@cli.command()
@click.option('--output', '-o', default='output', help='Répertoire de sortie')
def create(output: str):
    """
    Mode interactif : créer un livre d'aventure personnalisé
    """
    console.print(Panel.fit(
        "[bold magenta]🎭 CRÉATION INTERACTIVE[/bold magenta]\n"
        "[white]Bienvenue dans l'aventure de La Chasse au Trésor ![/white]",
        border_style="magenta"
    ))
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        console.print("[bold red]❌ Erreur: OPENAI_API_KEY non configurée[/bold red]")
        console.print("Veuillez configurer votre clé API dans le fichier .env")
        return 1
    
    # Collecte interactive des informations
    adventure_info = collect_adventure_info()
    if not adventure_info:
        return 0
    
    try:
        generator = SimpleChasseTresorGenerator()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task(
                f"[green]Génération de {adventure_info['sections']} paragraphes...", 
                total=None
            )
            
            # Générer le livre avec les paramètres interactifs
            book_data = generator.generate_test_book(
                adventure_info['theme'], 
                adventure_info['sections']
            )
            
            # Ajouter les informations de pays dans les métadonnées
            book_data['country'] = adventure_info['country']
            book_data['generation_mode'] = 'Test rapide' if adventure_info['test_mode'] else 'Standard'
            
            saved_files = generator.save_to_files(book_data, output)
            progress.update(task, completed=100)
        
        # Affichage des résultats
        console.print(f"\n[bold green]✅ Livre d'aventure créé avec succès ![/bold green]")
        
        table = Table(title="📚 Votre Livre d'Aventure", border_style="green")
        table.add_column("Propriété", style="cyan")
        table.add_column("Valeur", style="yellow")
        
        table.add_row("Destination", adventure_info['country'])
        table.add_row("Thème", adventure_info['theme'])
        table.add_row("Paragraphes", str(adventure_info['sections']))
        table.add_row("Mode", adventure_info.get('generation_mode', 'Standard'))
        table.add_row("ID", book_data["id"])
        
        for fmt, filepath in saved_files.items():
            table.add_row(f"Fichier {fmt.upper()}", Path(filepath).name)
        
        console.print(table)
        console.print(f"\n[green]📁 Fichiers sauvegardés dans: {output}/[/green]")
        
        # Offrir la possibilité de créer un autre livre
        if Confirm.ask("\n[cyan]Créer un autre livre d'aventure ?[/cyan]", default=False):
            return create.callback(output)
        
    except Exception as e:
        console.print(f"[bold red]❌ Erreur: {str(e)}[/bold red]")
        return 1
    
    return 0


@cli.command()
@click.option(
    '--theme',
    '-t',
    help='Thème pour l\'aventure (mode interactif si non spécifié)'
)
@click.option(
    '--sections',
    '-s',
    type=click.IntRange(1, 200),
    help='Nombre de sections/paragraphes (3=test rapide, 95=Golden Bullets standard, 200=maximum)'
)
@click.option(
    '--output',
    '-o',
    default='output',
    help='Répertoire de sortie'
)
@click.option(
    '--interactive',
    '-i',
    is_flag=True,
    help='Activer le mode interactif pour choisir thème et pays'
)
def generate(theme: str, sections: int, output: str, interactive: bool):
    """
    Générer un livre d'aventure avec nombre de paragraphes personnalisable
    """
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
    
    # Affichage du mode en fonction du nombre de sections
    if sections <= 5:
        mode = "🧪 MODE TEST"
        color = "yellow"
        advice = "Parfait pour des tests rapides"
    elif sections <= 20:
        mode = "🏃 MODE COURT"
        color = "blue" 
        advice = "Livre d'aventure court et dynamique"
    elif sections <= 95:
        mode = "📖 MODE STANDARD"
        color = "green"
        advice = "Livre d'aventure de taille moyenne"
    else:
        mode = "📚 MODE GOLDEN BULLETS"
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
        generator = SimpleChasseTresorGenerator()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task(f"[green]Génération de {sections} sections...", total=None)
            
            book_data = generator.generate_test_book(theme, sections)
            saved_files = generator.save_to_files(book_data, output)
            
            progress.update(task, completed=100)
        
        console.print(f"\n[bold green]✅ Livre de {sections} paragraphes généré ![/bold green]")
        
        # Display results
        table = Table(title="📚 Livre Généré", border_style="green")
        table.add_column("Propriété", style="cyan")
        table.add_column("Valeur", style="yellow")
        
        table.add_row("Destination", country if 'country' in locals() else "Non spécifiée")
        table.add_row("Thème", theme)
        table.add_row("Paragraphes", str(sections))
        table.add_row("ID", book_data["id"])
        
        for fmt, filepath in saved_files.items():
            table.add_row(f"Fichier {fmt.upper()}", Path(filepath).name)
        
        console.print(table)
        console.print(f"\n[green]📁 Fichiers sauvegardés dans: {output}/[/green]")
        
    except Exception as e:
        console.print(f"[bold red]❌ Erreur: {str(e)}[/bold red]")
        return 1
    
    return 0


@cli.command()
@click.argument('filepath', type=click.Path(exists=True))
def validate(filepath: str):
    """
    Valider un livre généré (validation basique)
    """
    console.print(Panel.fit(
        "[bold cyan]🔍 VALIDATION DE LIVRE[/bold cyan]",
        border_style="cyan"
    ))
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            book_data = json.load(f)
        
        title = book_data.get('title', 'Titre inconnu')
        sections = book_data.get('total_sections', 0)
        content = book_data.get('content', {})
        
        console.print(f"[green]📖 Livre: {title}[/green]")
        console.print(f"[green]📊 Sections déclarées: {sections}[/green]")
        
        # Basic validation
        issues = []
        
        # Check structure
        if 'title' not in content:
            issues.append("Section 'title' manquante")
        if 'intro' not in content:
            issues.append("Section 'intro' manquante")
        
        # Count actual sections
        actual_sections = len([k for k in content.keys() if k.isdigit()])
        if actual_sections != sections:
            issues.append(f"Sections réelles ({actual_sections}) != déclarées ({sections})")
        
        # Check format
        for key, section in content.items():
            if key.isdigit():
                if 'text' not in section:
                    issues.append(f"Section {key}: texte manquant")
                if 'choices' not in section:
                    issues.append(f"Section {key}: choix manquants")
        
        # Results
        if issues:
            console.print(f"\n[yellow]⚠️ {len(issues)} problème(s) détecté(s):[/yellow]")
            for issue in issues:
                console.print(f"  • {issue}")
        else:
            console.print("\n[green]✅ Livre valide - Aucun problème détecté[/green]")
        
        console.print(f"\n[cyan]📊 Résumé:[/cyan]")
        console.print(f"  • Titre: {title}")
        console.print(f"  • Sections: {actual_sections}")
        console.print(f"  • Fichier: {Path(filepath).name}")
        
    except Exception as e:
        console.print(f"[bold red]❌ Erreur: {str(e)}[/bold red]")
        return 1
    
    return 0


@cli.command()
@click.option('--dir', '-d', default='output', help='Répertoire des livres')
def list_books(dir: str):
    """
    Lister tous les livres générés
    """
    console.print(Panel.fit(
        "[bold cyan]📚 LIVRES GÉNÉRÉS[/bold cyan]",
        border_style="cyan"
    ))
    
    try:
        file_handler = FileHandler(dir)
        books = file_handler.list_books()
        
        if not books:
            console.print("[yellow]Aucun livre trouvé[/yellow]")
            return
        
        table = Table(title=f"Livres dans {dir}/books", border_style="cyan")
        table.add_column("#", style="dim")
        table.add_column("Fichier", style="cyan")
        table.add_column("Taille", style="yellow")
        table.add_column("Créé le", style="green")
        
        for i, book in enumerate(books, 1):
            table.add_row(
                str(i),
                book["filename"],
                book["size"],
                book["created"]
            )
        
        console.print(table)
        console.print(f"\n[green]Total: {len(books)} livre(s)[/green]")
    
    except Exception as e:
        console.print(f"[bold red]❌ Erreur: {str(e)}[/bold red]")
        return 1
    
    return 0


@cli.command()
@click.option('--days', '-d', default=30, help='Nombre de jours à conserver')
@click.option('--dir', default='output', help='Répertoire à nettoyer')
@click.confirmation_option(prompt='Êtes-vous sûr de vouloir nettoyer les anciens fichiers?')
def clean(days: int, dir: str):
    """
    Nettoyer les anciens fichiers générés
    """
    console.print(Panel.fit(
        "[bold yellow]🗑️ NETTOYAGE[/bold yellow]",
        border_style="yellow"
    ))
    
    try:
        file_handler = FileHandler(dir)
        deleted = file_handler.clean_old_files(days)
        
        if deleted > 0:
            console.print(f"[green]✅ {deleted} fichier(s) supprimé(s)[/green]")
        else:
            console.print("[yellow]Aucun fichier à supprimer[/yellow]")
    
    except Exception as e:
        console.print(f"[bold red]❌ Erreur: {str(e)}[/bold red]")
        return 1
    
    return 0


@cli.command()
@click.option(
    '--theme',
    '-t',
    default="Les Mystères d'Égypte",
    help='Thème pour le test (défaut: "Les Mystères d\'Égypte")'
)
@click.option(
    '--sections',
    '-s',
    default=3,
    type=click.IntRange(1, 50),
    help='Nombre de sections/paragraphes à générer pour le test (défaut: 3, max recommandé: 10)'
)
@click.option(
    '--output',
    '-o',
    default='output',
    help='Répertoire de sortie'
)
def test(theme: str, sections: int, output: str):
    """
    Mode test : génère un livre d'aventure simplifié avec peu de sections
    """
    console.print(Panel.fit(
        "[bold green]🧪 MODE TEST[/bold green]\n"
        "[yellow]Génération simplifiée pour tests rapides[/yellow]",
        border_style="green"
    ))
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        console.print("[bold red]❌ Erreur: OPENAI_API_KEY non configurée[/bold red]")
        console.print("Veuillez configurer votre clé API dans le fichier .env")
        return
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            task = progress.add_task(f"[green]Génération de {sections} sections...", total=None)
            
            # Initialize simple generator
            generator = SimpleChasseTresorGenerator()
            
            # Generate test book
            book_data = generator.generate_test_book(theme, sections)
            
            # Save to files
            saved_files = generator.save_to_files(book_data, output)
            
            progress.update(task, completed=100)
        
        # Display results
        console.print("\n[bold green]✅ Génération de test terminée ![/bold green]")
        
        table = Table(title="📚 Livre de Test Généré", border_style="green")
        table.add_column("Propriété", style="cyan")
        table.add_column("Valeur", style="yellow")
        
        table.add_row("Thème", theme)
        table.add_row("Sections générées", str(sections))
        table.add_row("Mode", "Test (simplifié)")
        
        for fmt, filepath in saved_files.items():
            table.add_row(f"Fichier {fmt.upper()}", Path(filepath).name)
        
        console.print(table)
        
        # Show preview of markdown if available
        if "markdown" in saved_files:
            console.print(f"\n[green]📄 Aperçu du fichier Markdown:[/green]")
            with open(saved_files["markdown"], 'r', encoding='utf-8') as f:
                content = f.read()
                preview = content[:1000] + "..." if len(content) > 1000 else content
            console.print(f"[dim]{preview}[/dim]")
        
        console.print(f"\n[green]📁 Fichiers sauvegardés dans: {output}/[/green]")
        
    except Exception as e:
        console.print(f"[bold red]❌ Erreur lors de la génération de test: {str(e)}[/bold red]")
        console.print_exception()
        return 1
    
    return 0


@cli.command()
@click.argument('filepath', type=click.Path(exists=True))
@click.option('--sections', '-s', default=3, help='Nombre de sections à afficher (défaut: 3)')
def preview(filepath: str, sections: int):
    """
    Prévisualiser un livre en format Markdown
    """
    console.print(Panel.fit(
        "[bold cyan]👁️ PRÉVISUALISATION MARKDOWN[/bold cyan]",
        border_style="cyan"
    ))
    
    try:
        # Load the book (format simplifié - pas de JSON)
        console.print("[yellow]📝 Fonction de prévisualisation temporairement désactivée[/yellow]")
        console.print(f"[cyan]📄 Fichier à prévisualiser: {Path(filepath).name}[/cyan]")
        return 0
        
        # Simple preview
        title = book_data.get('title', 'Titre inconnu')
        total_sections = book_data.get('total_sections', 0)
        content = book_data.get('content', {})
        
        console.print(f"[green]📖 {title}[/green]")
        console.print(f"[cyan]📊 Sections: {total_sections}[/cyan]\n")
        
        # Show intro
        if 'intro' in content:
            console.print("[bold yellow]## Introduction[/bold yellow]")
            intro_text = content['intro'].get('text', '')[:500]
            console.print(f"{intro_text}...\n")
        
        # Show first sections
        console.print(f"[bold yellow]## Premières {min(sections, total_sections)} sections:[/bold yellow]")
        for i in range(1, min(sections + 1, total_sections + 1)):
            if str(i) in content:
                section = content[str(i)]
                text = section.get('text', '')
                
                # Extract title
                lines = text.split('\n')
                title_line = "Section inconnue"
                for line in lines:
                    if line.startswith('- '):
                        title_line = line[2:].strip()
                        break
                
                console.print(f"[cyan]Section {i}: {title_line}[/cyan]")
                
                # Show first 200 chars
                preview_text = text[:200].replace('\n', ' ') + "..."
                console.print(f"[dim]{preview_text}[/dim]\n")
        
        console.print(f"[dim]Prévisualisation limitée. Fichier complet: {Path(filepath).name}[/dim]")
        
    except Exception as e:
        console.print(f"[bold red]❌ Erreur lors de la prévisualisation: {str(e)}[/bold red]")
        return 1
    
    return 0


@cli.command()
def info():
    """
    Afficher les informations sur le système
    """
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


if __name__ == "__main__":
    cli()