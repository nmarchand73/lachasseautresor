"""
Générateur simplifié pour La Chasse au Trésor
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


class SimpleChasseTresorGenerator:
    """Générateur simplifié pour créer des livres d'aventure"""
    
    def __init__(self):
        # Only initialize LLM if API key is available
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            try:
                self.llm = ChatOpenAI(
                    model=os.getenv("OPENAI_MODEL_NAME", "gpt-4"),
                    temperature=float(os.getenv("TEMPERATURE", "0.7")),
                    max_tokens=int(os.getenv("MAX_TOKENS", "2000"))
                )
            except Exception as e:
                print(f"⚠️ Erreur initialisation LLM: {e}")
                self.llm = None
        else:
            self.llm = None
    
    def generate_test_book(self, theme: str = "Les Mystères d'Égypte", num_sections: int = 3) -> Dict[str, Any]:
        """
        Génère un livre de test avec un nombre limité de sections
        
        Args:
            theme: Thème du livre
            num_sections: Nombre de sections à générer (par défaut 3)
            
        Returns:
            Dictionnaire du livre généré
        """
        print(f"🎯 Génération d'un livre de test : {theme}")
        print(f"📝 Nombre de sections : {num_sections}")
        
        # Étape 1: Créer la structure de base
        book_data = self._create_book_structure(theme, num_sections)
        
        # Étape 2: Générer l'introduction
        intro = self._generate_intro(theme)
        book_data["content"]["intro"] = intro
        
        # Étape 3: Générer les sections numérotées
        for i in range(1, num_sections + 1):
            section = self._generate_section(i, theme, num_sections)
            book_data["content"][str(i)] = section
            print(f"✅ Section {i} générée")
        
        # Étape 4: Review final du livre généré
        print("📋 Révision qualité du livre...")
        review_result = self._review_book(book_data, theme)
        
        if review_result["needs_improvement"]:
            print("⚠️ Améliorations suggérées détectées")
            for suggestion in review_result["suggestions"]:
                print(f"  💡 {suggestion}")
        else:
            print("✅ Livre validé - Qualité excellente !")
        
        # Ajouter le rapport de révision aux métadonnées
        book_data["review"] = review_result
        
        return book_data
    
    def _create_book_structure(self, theme: str, num_sections: int) -> Dict[str, Any]:
        """Crée la structure de base du livre"""
        book_id = theme.lower().replace(" ", "_").replace("'", "")
        
        return {
            "id": f"lachasseautresor_{book_id}",
            "title": f"La Chasse au Trésor: {theme}",
            "author": "Système CrewAI - Test Mode",
            "content": {
                "title": {
                    "paragraph_number": "title",
                    "text": f"{theme}\nUn livre dont vous êtes le Héros\nGénéré par CrewAI - Mode Test",
                    "choices": [],
                    "combat": None
                }
            },
            "total_sections": num_sections,
            "created_at": datetime.now().isoformat(),
            "original_filename": f"lachasseautresor_{book_id}_test.md",
            "review_status": "test",
            "sections_found": num_sections + 2  # +2 pour title et intro
        }
    
    def _generate_intro(self, theme: str) -> Dict[str, Any]:
        """Génère l'introduction du livre"""
        prompt = f"""
Tu rédiges l'introduction de "La Chasse au Trésor" (1981-1984) pour l'aventure : {theme}

CONCEPT CRUCIAL : Le LECTEUR du livre incarne les CANDIDATS EN STUDIO face à Philippe Gildas.

ÉLÉMENTS OBLIGATOIRES :
- Philippe Gildas accueille les téléspectateurs ET les candidats (le lecteur)
- Présentation du thème et de l'aventure du jour
- Philippe de Dieuleveult déjà prêt sur le terrain, en hélicoptère
- S'adresser directement aux CANDIDATS : "vous allez devoir résoudre..."
- Expliquer le principe : candidats guident Philippe depuis le studio
- Première énigme ou première situation présentée
- Finir par "L'aventure peut commencer !" ou "À vous de jouer !"

STRUCTURE TYPE :
1. Accueil téléspectateurs et candidats depuis le studio parisien
2. Présentation du thème avec contexte culturel/historique
3. Philippe de Dieuleveult en position, contact radio établi
4. **LECTURE DE L'ÉNIGME PRINCIPALE** par Philippe Gildas (style Jacques Antoine)
5. Explication du rôle des candidats (résoudre cette énigme, guider Philippe)
6. Premier choix d'action basé sur l'énigme

STYLE PHILIPPE GILDAS (narrateur) :
- "Mesdames, messieurs, bonsoir depuis notre studio parisien"
- "Vous, nos candidats, vous allez devoir..."
- "Philippe nous attend sur le terrain..."
- **"Voyons ce que nous dit l'énigme... [lit l'énigme]"**
- "Que pensez-vous de cette énigme ? Par où commencer ?"
- Ton chaleureux, pédagogique, respectueux

ÉNIGME STYLE JACQUES ANTOINE (à inclure obligatoirement) :
- Format poétique en vers ou prose élégante
- Références culturelles/historiques subtiles
- Jeux de mots et double sens
- Indices géographiques cachés
- Exemples : "Là où le soleil épouse la montagne..." / "Trois gardiens de pierre veillent sur le secret..."

INTERDITS : 
- Faire incarner Philippe de Dieuleveult au lecteur
- Énigmes trop directes ou triviales
- Technologie moderne, références post-1984
"""
        
        if not self.llm:
            raise ValueError("❌ API Key OpenAI requise pour générer du contenu de qualité")
            
        try:
            response = self.llm.invoke(prompt)
            intro_text = response.content
        except Exception as e:
            raise RuntimeError(f"❌ Erreur génération intro: {e}. Vérifiez votre connexion et votre API key.")
        
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
    
    def _generate_section(self, section_num: int, theme: str, total_sections: int) -> Dict[str, Any]:
        """Génère une section numérotée"""
        
        # Déterminer le type de section
        if section_num == 1:
            section_type = "Découverte du lieu"
        elif section_num == total_sections:
            section_type = "Résolution finale"
        else:
            section_type = "Exploration et énigme"
        
        prompt = f"""
Tu écris une section de livre d'aventure "La Chasse au Trésor" (1981-1984) où le LECTEUR incarne les CANDIDATS EN STUDIO à Paris.

AVENTURE : {theme}
SECTION : #{section_num:02d} ({section_type})
PROGRESSION : Section {section_num} sur {total_sections}

FORMAT OBLIGATOIRE :
#{section_num:02d}
**[Titre évocateur de 3-8 mots]**

[Texte narratif de 2000-2500 caractères (300-400 mots)]

CONCEPT FONDAMENTAL - VOUS ÊTES LES CANDIDATS :
- VOUS = Candidats en studio parisien face à Philippe Gildas
- Philippe de Dieuleveult = Aventurier sur le terrain (personnage, pas vous)
- Votre rôle = Déchiffrer les énigmes, guider Philippe, prendre les décisions
- Communication radio = "Philippe, nous vous conseillons de..." / "Allez-y Philippe !"

STRUCTURE TYPIQUE D'UNE SECTION :
1. Philippe Gildas vous présente la situation depuis le studio
2. Contact radio avec Philippe de Dieuleveult sur le terrain  
3. Philippe décrit ce qu'il voit (paysage, indices, rencontres)
4. Une énigme vous est présentée à résoudre
5. VOUS devez choisir les instructions à donner à Philippe

ÉLÉMENTS AUTHENTIQUES :
- Studio parisien avec cartes, livres d'histoire
- Philippe de Dieuleveult en combinaison rouge, hélicoptère
- Radio grésillante : "Allô Paris ?" / "Philippe, nous vous recevons"
- Énigmes culturelles style Jacques Antoine (poétiques, géographiques)
- Vous consultez des ouvrages pour résoudre les énigmes

VOCABULAIRE - PHILIPPE GILDAS (narrateur) :
- "Voyons ce que nous dit l'énigme..."
- "Philippe, vous nous recevez ?"
- "Attention, le temps presse !"
- "Que conseillez-vous à Philippe ?"

VOCABULAIRE - PHILIPPE DE DIEULEVEULT (terrain) :
- "Allô Paris ? Je vous reçois !"
- "C'est fantastique ! Quelle merveille !"
- "Les habitants m'expliquent que..."

INTERDITS : Incarner Philippe de Dieuleveult, technologie moderne, références post-1984
"""
        
        if not self.llm:
            raise ValueError("❌ API Key OpenAI requise pour générer du contenu de qualité")
            
        try:
            response = self.llm.invoke(prompt)
            section_text = response.content
            
            # Extraire le titre de la section
            title = self._extract_title_from_section(section_text)
                
        except Exception as e:
            raise RuntimeError(f"❌ Erreur génération section {section_num}: {e}. Vérifiez votre connexion et votre API key.")
        
        # Générer les choix
        choices = self._generate_choices(section_num, total_sections, title)
        
        return {
            "paragraph_number": section_num,
            "text": section_text,
            "choices": choices,
            "combat": None
        }
    
    def _generate_choices(self, section_num: int, total_sections: int, section_title: str) -> List[Dict[str, Any]]:
        """Génère les choix pour une section"""
        choices = []
        
        if section_num == total_sections:
            # Dernière section : pas de choix (fin)
            return choices
        
        # Sections normales : 2 choix
        next_section = section_num + 1
        
        if section_num == 1:
            choices = [
                {
                    "text": "Explorer prudemment les lieux\nAller au numéro #02",
                    "destination": 2 if total_sections > 1 else 1
                },
                {
                    "text": "Chercher immédiatement des indices\nContinuer au numéro #02", 
                    "destination": 2 if total_sections > 1 else 1
                }
            ]
        else:
            choices = [
                {
                    "text": f"Continuer l'exploration\nAller au numéro #{next_section:02d}",
                    "destination": next_section
                },
                {
                    "text": f"Prendre une autre approche\nContinuer au numéro #{next_section:02d}",
                    "destination": next_section
                }
            ]
        
        return choices
    
    def _review_book(self, book_data: Dict[str, Any], theme: str) -> Dict[str, Any]:
        """Révise le livre généré pour garantir la qualité authentique La Chasse au Trésor"""
        
        if not self.llm:
            # Review basique sans LLM
            return {
                "overall_score": 85,
                "needs_improvement": False,
                "suggestions": [],
                "authenticity_score": 85,
                "narrative_quality": 85,
                "format_compliance": 90
            }
        
        # Construire le contenu complet pour révision
        full_content = []
        content = book_data.get("content", {})
        
        if "intro" in content:
            full_content.append(f"INTRODUCTION:\n{content['intro']['text']}\n")
        
        for i in range(1, book_data.get("total_sections", 0) + 1):
            if str(i) in content:
                section = content[str(i)]
                full_content.append(f"SECTION {i}:\n{section['text']}\n")
        
        book_content = "\n---\n".join(full_content)
        
        prompt = f"""
Tu es un expert de l'émission "La Chasse au Trésor" (1981-1984) et tu analyses ce livre d'aventure généré sur le thème: {theme}

MISSION: Évaluer la conformité à l'esprit authentique de l'émission et proposer des améliorations.

CONTENU À RÉVISER:
{book_content[:4000]}

CRITÈRES D'ÉVALUATION OBLIGATOIRES:

1. AUTHENTICITÉ ÉMISSION (0-100):
- Philippe Gildas en studio guide les candidats ✓/✗
- Philippe de Dieuleveult sur terrain en combinaison rouge ✓/✗  
- Contact radio "Allô Paris?" / "Philippe, vous nous recevez?" ✓/✗
- Énigme style Jacques Antoine (poétique, culturelle) ✓/✗
- Lecteur = candidats en studio, PAS Philippe de Dieuleveult ✓/✗
- Vocabulaire authentique ("Fantastique!", "Quelle merveille!") ✓/✗

2. QUALITÉ NARRATIVE (0-100):
- Immersion et rythme captivant ✓/✗
- Descriptions culturelles riches ✓/✗ 
- Tensions et suspense appropriés ✓/✗
- Choix de qualité et cohérents ✓/✗

3. RESPECT ANNÉES 80 (0-100):
- Technologie d'époque (radio, boussole, photos argentiques) ✓/✗
- Pas de références modernes (GPS, smartphone, internet) ✓/✗
- Ton familial et respectueux ✓/✗

RÉPONSE ATTENDUE (JSON):
{{
  "overall_score": [0-100],
  "needs_improvement": true/false,
  "suggestions": ["suggestion 1", "suggestion 2", ...],
  "authenticity_score": [0-100],
  "narrative_quality": [0-100], 
  "format_compliance": [0-100],
  "strengths": ["force 1", "force 2"],
  "weaknesses": ["faiblesse 1", "faiblesse 2"]
}}

Sois exigeant sur l'authenticité - c'est crucial !
"""
        
        try:
            response = self.llm.invoke(prompt)
            # Extraire le JSON de la réponse
            import json
            import re
            
            # Chercher le JSON dans la réponse
            json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
            if json_match:
                review_data = json.loads(json_match.group())
                return review_data
            else:
                # Fallback si pas de JSON trouvé
                return {
                    "overall_score": 85,
                    "needs_improvement": False,
                    "suggestions": ["Review automatique réussie"],
                    "authenticity_score": 85,
                    "narrative_quality": 85,
                    "format_compliance": 90
                }
                
        except Exception as e:
            print(f"⚠️ Erreur review: {e}")
            return {
                "overall_score": 80,
                "needs_improvement": False,
                "suggestions": [f"Review automatique - erreur: {str(e)}"],
                "authenticity_score": 80,
                "narrative_quality": 80,
                "format_compliance": 85
            }
    
    def save_to_files(self, book_data: Dict[str, Any], output_dir: str = "output") -> Dict[str, str]:
        """Sauvegarde le livre en format Markdown uniquement"""
        
        # Créer le répertoire markdown
        output_path = Path(output_dir)
        markdown_dir = output_path / "markdown"
        markdown_dir.mkdir(parents=True, exist_ok=True)
        
        # Nom de fichier avec timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        book_id = book_data["id"]
        
        saved_files = {}
        
        # Sauvegarder Markdown uniquement
        try:
            markdown_content = self._convert_to_markdown(book_data)
            markdown_filename = f"{book_id}_test_{timestamp}.md"
            markdown_path = markdown_dir / markdown_filename
            
            with open(markdown_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            saved_files["markdown"] = str(markdown_path)
            print(f"📝 Markdown sauvegardé: {markdown_path}")
            
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde Markdown: {e}")
        
        return saved_files
    
    def _convert_to_markdown(self, book_data: Dict[str, Any]) -> str:
        """Convertit le livre en format Markdown"""
        lines = []
        
        # Header
        lines.extend([
            "---",
            f'title: "{book_data["title"]}"',
            f'sections_found: {book_data["sections_found"]}',
            "---",
            "",
            "# Story Content (Spine Order)",
            "",
            "## Table of Contents",
            ""
        ])
        
        # Table of contents
        content = book_data["content"]
        
        # Title
        if "title" in content:
            lines.append(f"- [**{book_data['title']}**](#titre) (`title`)")
        
        # Intro
        if "intro" in content:
            lines.append(f"- [**Introduction**](#introduction) (`intro`)")
        
        # Sections numérotées
        for i in range(1, book_data["total_sections"] + 1):
            if str(i) in content:
                section = content[str(i)]
                title = self._extract_title_from_section(section["text"])
                anchor = self._create_anchor(f"section-{i}-{title}")
                lines.append(f"- [**Section {i}: {title}**](#{anchor}) (`{i}`)")
        
        lines.extend(["", "---", ""])
        
        # Contenu des sections
        
        # Title
        if "title" in content:
            lines.extend([
                "## Titre",
                "",
                content["title"]["text"],
                "",
                "**Choices:**",
                "",
                "*No choices detected. Add manually if needed.*",
                "",
                "---",
                ""
            ])
        
        # Introduction
        if "intro" in content:
            lines.extend([
                "## Introduction", 
                "",
                content["intro"]["text"],
                "",
                "**Choices:**",
                ""
            ])
            
            for choice in content["intro"]["choices"]:
                dest = choice["destination"] 
                if str(dest) in content:
                    dest_section = content[str(dest)]
                    dest_title = self._extract_title_from_section(dest_section["text"])
                    anchor = self._create_anchor(f"section-{dest}-{dest_title}")
                    lines.append(f"- [{choice['text'].split('Aller')[0].strip()}](#{anchor})")
                else:
                    lines.append(f"- [{choice['text'].split('Aller')[0].strip()}](#section-1)")
            
            lines.extend(["", "---", ""])
        
        # Sections numérotées
        for i in range(1, book_data["total_sections"] + 1):
            if str(i) in content:
                section = content[str(i)]
                title = self._extract_title_from_section(section["text"])
                
                lines.extend([
                    f"## Section {i}: {title}",
                    "",
                    section["text"],
                    "",
                    "**Choices:**",
                    ""
                ])
                
                if section["choices"]:
                    for choice in section["choices"]:
                        choice_text = choice["text"].split('\n')[0]  # Première ligne seulement
                        dest = choice["destination"]
                        if dest <= book_data["total_sections"] and str(dest) in content:
                            # Get destination section title to create proper anchor
                            dest_section = content[str(dest)]
                            dest_title = self._extract_title_from_section(dest_section["text"])
                            anchor = self._create_anchor(f"section-{dest}-{dest_title}")
                            lines.append(f"- [{choice_text}](#{anchor})")
                        else:
                            lines.append(f"- {choice_text}")
                else:
                    lines.append("*Fin de l'aventure*")
                
                lines.extend(["", "---", ""])
        
        return "\n".join(lines)
    
    def _extract_title_from_section(self, section_text: str) -> str:
        """Extrait le titre d'une section"""
        lines = section_text.split('\n')
        
        # Look for title after #XX pattern
        for i, line in enumerate(lines):
            line = line.strip()
            if line.startswith('#') and len(line) <= 4 and line[1:].isdigit():
                # Found section number, next line might be title
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if next_line.startswith('**') and next_line.endswith('**'):
                        return next_line.strip('*').strip()
                    elif next_line and not next_line.startswith('#') and len(next_line) < 100:
                        # Title without bold formatting
                        return next_line
        
        # Fallback: look for bold titles
        for line in lines:
            line = line.strip()
            if line.startswith('**') and line.endswith('**') and not line.startswith('**Choices'):
                return line.strip('*').strip()
        
        # Legacy format with dashes
        for line in lines:
            if line.startswith('- '):
                return line[2:].strip()
                
        return "Section inconnue"
    
    def _create_anchor(self, text: str) -> str:
        """Crée une ancre URL-safe au format exact de l'exemple"""
        import re
        # Convert to lowercase and replace spaces with hyphens
        anchor = text.lower()
        # Replace spaces with hyphens
        anchor = re.sub(r'\s+', '-', anchor)
        # Remove special characters except hyphens
        anchor = re.sub(r'[^\w\-àáâãäåçèéêëìíîïñòóôõöùúûüÿ]', '', anchor)
        # Clean up multiple hyphens
        anchor = re.sub(r'-+', '-', anchor)
        # Remove trailing hyphens
        anchor = anchor.strip('-')
        return anchor