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
from rich import print as rprint
import json
from typing import Optional

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.simple_generator import SimpleChasseTresorGenerator
from src.utils import FileHandler

# Load environment variables
load_dotenv()

# Initialize Rich console
console = Console()


@click.group()
def cli():
    """
    🎯 LA CHASSE AU TRÉSOR - Générateur de Livres d'Aventure
    
    Système basé sur CrewAI pour générer des livres d'aventure interactifs
    inspirés de l'émission culte des années 80.
    """
    pass


@cli.command()
@click.option(
    '--theme',
    '-t',
    default="Les Mystères d'Égypte", 
    help='Thème pour l\'aventure'
)
@click.option(
    '--sections',
    '-s',
    default=95,
    help='Nombre de sections (3 pour test rapide, 95 pour livre complet)'
)
@click.option(
    '--output',
    '-o',
    default='output',
    help='Répertoire de sortie'
)
def generate(theme: str, sections: int, output: str):
    """
    Générer un livre d'aventure (utilisez 'test' pour un livre rapide)
    """
    if sections <= 10:
        console.print("[yellow]💡 Pour un test rapide, utilisez plutôt: python -m src.main test[/yellow]")
    
    console.print(Panel.fit(
        f"[bold cyan]🚁 GÉNÉRATION DE LIVRE[/bold cyan]\n"
        f"[yellow]{sections} sections à générer[/yellow]",
        border_style="cyan"
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
        
        console.print(f"\n[bold green]✅ Livre de {sections} sections généré ![/bold green]")
        
        # Display results
        table = Table(title="📚 Livre Généré", border_style="green")
        table.add_column("Propriété", style="cyan")
        table.add_column("Valeur", style="yellow")
        
        table.add_row("Thème", theme)
        table.add_row("Sections", str(sections))
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
    help='Nombre de sections à générer (défaut: 3)'
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