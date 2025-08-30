"""
JSON Formatter for Golden Bullets format - Version simplifiée
"""
import json
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime


class JSONFormatter:
    """Formats book data into Golden Bullets JSON format"""
    
    @staticmethod
    def format_paragraph_text(number: int, title: str, content: str) -> str:
        """
        Format paragraph text with proper numbering and title
        
        Args:
            number: Paragraph number (1-95)
            title: Paragraph title
            content: Paragraph content
            
        Returns:
            Formatted text string
        """
        return f"#{number:02d}\n- {title}\n{content}"
    
    @staticmethod
    def create_title_paragraph() -> Dict[str, Any]:
        """Create the title paragraph"""
        return {
            "paragraph_number": "title",
            "text": "La Chasse au Trésor\nUn livre dont vous êtes le Héros\nGénéré par CrewAI",
            "choices": [],
            "combat": None
        }
    
    @staticmethod
    def create_intro_paragraph(theme: str) -> Dict[str, Any]:
        """
        Create the introduction paragraph
        
        Args:
            theme: The adventure theme
            
        Returns:
            Intro paragraph dict
        """
        intro_text = f"""Paris, Studio de Télévision

Le générique mythique de "La Chasse au Trésor" résonne dans le studio. Philippe Gildas ajuste ses lunettes et se tourne vers vous avec un sourire bienveillant.

— Bonjour et bienvenue dans cette nouvelle aventure de La Chasse au Trésor ! Aujourd'hui, notre thème est : {theme}. Philippe de Dieuleveult est déjà en route dans son hélicoptère, prêt à relever les défis que nous allons lui soumettre.

Il vous tend une enveloppe cachetée.

— Voici la première énigme. Trois trésors vous attendent aux quatre coins du monde. Chaque découverte vous rapprochera de la victoire finale. Mais attention, le temps presse et les mauvais choix peuvent vous faire perdre de précieuses minutes !

La voix enthousiaste de Philippe de Dieuleveult grésille dans le haut-parleur :

— Allô Paris ? Je suis prêt ! L'hélicoptère est en vol stationnaire. J'attends vos instructions !

Philippe Gildas ouvre l'enveloppe et commence à lire...

L'aventure peut commencer !"""
        
        return {
            "paragraph_number": "intro",
            "text": intro_text,
            "choices": [
                {
                    "text": "Commencer l'aventure",
                    "destination": 1
                }
            ],
            "combat": None
        }
    
    @staticmethod
    def format_choice(action: str, destination: int) -> Dict[str, Any]:
        """
        Format a choice properly
        
        Args:
            action: The action description
            destination: Target paragraph number
            
        Returns:
            Formatted choice dict
        """
        if destination < 10:
            dest_text = f"Aller au numéro #0{destination}"
        else:
            dest_text = f"Aller au numéro #{destination}"
            
        # Alternate between "Aller" and "Continuer"
        if destination % 2 == 0:
            dest_text = dest_text.replace("Aller", "Continuer")
        
        return {
            "text": f"{action}\n{dest_text}",
            "destination": destination
        }
    
    @staticmethod
    def save_book_json(book_data: Dict[str, Any], output_dir: str = "output") -> str:
        """
        Save book data to JSON file
        
        Args:
            book_data: Book data dictionary
            output_dir: Output directory path
            
        Returns:
            Path to saved file
        """
        # Create output directory if it doesn't exist
        output_path = Path(output_dir)
        books_dir = output_path / "books"
        books_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        book_id = book_data.get("id", "unknown")
        filename = f"{book_id}_{timestamp}.json"
        filepath = books_dir / filename
        
        # Save JSON
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(book_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Book saved to: {filepath}")
        
        return str(filepath)
    
    @staticmethod
    def load_book_json(filepath: str) -> Dict[str, Any]:
        """
        Load book from JSON file
        
        Args:
            filepath: Path to JSON file
            
        Returns:
            Book data dictionary
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)