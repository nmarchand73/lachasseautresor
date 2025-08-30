"""
File handler for La Chasse au Trésor
"""
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import shutil


class FileHandler:
    """Handle file operations for book generation"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        self.books_dir = self.output_dir / "books"
        self.reports_dir = self.output_dir / "reports"
        self.backups_dir = self.output_dir / "backups"
        
        for dir_path in [self.books_dir, self.reports_dir, self.backups_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def save_book(self, book_data: Dict[str, Any], book_id: str, format: str = "both") -> Dict[str, str]:
        """
        Save book to file(s) in specified format(s)
        
        Args:
            book_data: Book data dictionary
            book_id: Unique book identifier
            format: Format to save ("json", "markdown", or "both")
            
        Returns:
            Dictionary with paths to saved files
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        saved_files = {}
        
        if format in ["json", "both"]:
            # Save JSON file
            json_filename = f"{book_id}_{timestamp}.json"
            json_filepath = self.books_dir / json_filename
            
            with open(json_filepath, 'w', encoding='utf-8') as f:
                json.dump(book_data, f, ensure_ascii=False, indent=2)
            
            saved_files["json"] = str(json_filepath)
            print(f"📚 JSON book saved: {json_filepath}")
        
        if format in ["markdown", "both"]:
            # Save Markdown file - conversion simplifiée 
            try:
                from src.simple_generator import SimpleChasseTresorGenerator
                generator = SimpleChasseTresorGenerator()
                markdown_content = generator._convert_to_markdown(book_data)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                book_id = book_data.get("id", "unknown")
                markdown_filename = f"{book_id}_{timestamp}.md"
                
                markdown_dir = self.output_dir / "markdown"
                markdown_dir.mkdir(parents=True, exist_ok=True)
                markdown_path = markdown_dir / markdown_filename
                
                with open(markdown_path, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
                
                saved_files["markdown"] = str(markdown_path)
                print(f"📝 Markdown book saved: {markdown_path}")
                
            except Exception as e:
                print(f"⚠️ Could not save Markdown: {e}")
        
        return saved_files
    
    def save_validation_report(self, report: Dict[str, Any], book_id: str) -> str:
        """
        Save validation report
        
        Args:
            report: Validation report dictionary
            book_id: Book identifier
            
        Returns:
            Path to saved report
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{book_id}_validation_{timestamp}.json"
        filepath = self.reports_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        # Also create a human-readable report
        readable_report = self._format_readable_report(report)
        txt_filepath = filepath.with_suffix('.txt')
        
        with open(txt_filepath, 'w', encoding='utf-8') as f:
            f.write(readable_report)
        
        print(f"📊 Validation report saved: {txt_filepath}")
        return str(txt_filepath)
    
    def create_backup(self, filepath: str) -> str:
        """
        Create backup of a file
        
        Args:
            filepath: Path to file to backup
            
        Returns:
            Path to backup file
        """
        source = Path(filepath)
        if not source.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{source.stem}_backup_{timestamp}{source.suffix}"
        backup_path = self.backups_dir / backup_name
        
        shutil.copy2(source, backup_path)
        print(f"💾 Backup created: {backup_path}")
        
        return str(backup_path)
    
    def load_book(self, filepath: str) -> Dict[str, Any]:
        """
        Load book from JSON file
        
        Args:
            filepath: Path to book file
            
        Returns:
            Book data dictionary
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def list_books(self) -> List[Dict[str, str]]:
        """
        List all generated books
        
        Returns:
            List of book info dictionaries
        """
        books = []
        
        for filepath in self.books_dir.glob("*.json"):
            stat = filepath.stat()
            books.append({
                "filename": filepath.name,
                "path": str(filepath),
                "size": f"{stat.st_size / 1024:.1f} KB",
                "created": datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
            })
        
        return sorted(books, key=lambda x: x["created"], reverse=True)
    
    def clean_old_files(self, days: int = 30) -> int:
        """
        Clean files older than specified days
        
        Args:
            days: Number of days to keep files
            
        Returns:
            Number of files deleted
        """
        cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)
        deleted = 0
        
        for dir_path in [self.books_dir, self.reports_dir, self.backups_dir]:
            for filepath in dir_path.glob("*"):
                if filepath.stat().st_mtime < cutoff_time:
                    filepath.unlink()
                    deleted += 1
        
        if deleted > 0:
            print(f"🗑️ Cleaned {deleted} old files")
        
        return deleted
    
    def _format_readable_report(self, report: Dict[str, Any]) -> str:
        """
        Format validation report for human reading
        
        Args:
            report: Validation report dictionary
            
        Returns:
            Formatted text report
        """
        lines = [
            "=" * 60,
            "LA CHASSE AU TRÉSOR - RAPPORT DE VALIDATION",
            "=" * 60,
            "",
            f"Score Global: {report.get('overall_score', 0)}/100",
            f"Statut: {'✅ VALIDE' if report.get('is_valid') else '❌ INVALIDE'}",
            "",
            "-" * 60,
            "STRUCTURE",
            "-" * 60
        ]
        
        structure = report.get("structure", {})
        lines.extend([
            f"✓ Page de titre: {'Oui' if structure.get('has_title') else 'Non'}",
            f"✓ Introduction: {'Oui' if structure.get('has_intro') else 'Non'}",
            f"✓ Paragraphes: {structure.get('paragraph_count', 0)}/95",
        ])
        
        if structure.get("missing_paragraphs"):
            lines.append(f"⚠ Paragraphes manquants: {', '.join(structure['missing_paragraphs'][:10])}")
        
        lines.extend([
            "",
            "-" * 60,
            "RÉFÉRENCES",
            "-" * 60
        ])
        
        references = report.get("references", {})
        lines.extend([
            f"✓ Références valides: {references.get('valid_references', 0)}",
            f"✗ Références invalides: {references.get('invalid_references', 0)}",
            f"⚠ Paragraphes inaccessibles: {len(references.get('unreachable_paragraphs', []))}",
        ])
        
        lines.extend([
            "",
            "-" * 60,
            "CONTENU",
            "-" * 60
        ])
        
        content = report.get("content", {})
        lines.extend([
            f"📝 Longueur moyenne: {content.get('avg_paragraph_length', 0):.0f} caractères",
            f"📝 Minimum: {content.get('min_paragraph_length', 0)} caractères",
            f"📝 Maximum: {content.get('max_paragraph_length', 0)} caractères",
        ])
        
        lines.extend([
            "",
            "-" * 60,
            "JOUABILITÉ",
            "-" * 60
        ])
        
        gameplay = report.get("gameplay", {})
        lines.extend([
            f"🎮 Chemins vers la fin: {len(gameplay.get('paths_to_end', []))}",
            f"🎮 Chemin le plus court: {gameplay.get('shortest_path', 'N/A')} paragraphes",
            f"🎮 Chemin le plus long: {gameplay.get('longest_path', 'N/A')} paragraphes",
            f"🎮 Impasses inattendues: {len(gameplay.get('dead_ends', []))}",
        ])
        
        lines.extend([
            "",
            "-" * 60,
            "AUTHENTICITÉ",
            "-" * 60
        ])
        
        authenticity = report.get("authenticity", {})
        lines.extend([
            f"🎬 Phrases Philippe: {'✓' if authenticity.get('has_philippe_phrases') else '✗'}",
            f"🚁 Mentions hélicoptère: {'✓' if authenticity.get('has_helicopter_mentions') else '✗'}",
            f"📺 Segments studio: {'✓' if authenticity.get('has_studio_segments') else '✗'}",
            f"🔍 Énigmes présentes: {'✓' if authenticity.get('has_enigmas') else '✗'}",
            f"⚡ Niveau d'enthousiasme: {authenticity.get('enthusiasm_level', 0):.1f} exclamations/paragraphe",
        ])
        
        # Add issues summary
        all_issues = []
        for category in ["structure", "references", "content", "gameplay", "authenticity"]:
            if category in report:
                all_issues.extend(report[category].get("issues", []))
        
        if all_issues:
            lines.extend([
                "",
                "-" * 60,
                "PROBLÈMES DÉTECTÉS",
                "-" * 60
            ])
            for issue in all_issues:
                lines.append(f"⚠ {issue}")
        
        lines.extend([
            "",
            "=" * 60,
            f"Rapport généré le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "=" * 60
        ])
        
        return "\n".join(lines)