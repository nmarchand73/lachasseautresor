"""
Outils CrewAI spécialisés pour La Chasse au Trésor
Outils customisés selon les meilleures pratiques CrewAI 2024
"""
from crewai.tools import BaseTool
from typing import Type, Dict, Any, List
from pydantic import BaseModel, Field
import json
import re


class EnigmaValidatorInput(BaseModel):
    """Input pour l'outil de validation d'énigmes"""
    enigma_text: str = Field(description="Texte de l'énigme à valider")
    theme: str = Field(description="Thème de l'aventure")


class EnigmaValidatorTool(BaseTool):
    """Outil de validation des énigmes style Jacques Antoine"""
    name: str = "enigma_validator"
    description: str = "Valide qu'une énigme respecte le style poétique de Jacques Antoine avec références culturelles subtiles"
    args_schema: Type[BaseModel] = EnigmaValidatorInput

    def _run(self, enigma_text: str, theme: str) -> str:
        """Valide une énigme selon les critères Jacques Antoine"""
        
        criteria = {
            "poetic_style": False,
            "cultural_references": False,
            "word_play": False,
            "geographic_clues": False,
            "appropriate_length": False
        }
        
        score = 0
        
        # Vérifier le style poétique (rimes, rythme)
        if any(word in enigma_text.lower() for word in ["où", "là", "garde", "secret", "trésor", "mystère"]):
            criteria["poetic_style"] = True
            score += 20
        
        # Vérifier les références culturelles
        cultural_words = ["temple", "château", "église", "pyramide", "pharaon", "roi", "empereur", "légende"]
        if any(word in enigma_text.lower() for word in cultural_words):
            criteria["cultural_references"] = True
            score += 20
        
        # Vérifier les jeux de mots/double sens
        if "..." in enigma_text or ";" in enigma_text or len(enigma_text.split("\n")) > 1:
            criteria["word_play"] = True
            score += 20
        
        # Vérifier les indices géographiques
        geo_words = ["nord", "sud", "est", "ouest", "soleil", "ombre", "montagne", "rivière", "mer"]
        if any(word in enigma_text.lower() for word in geo_words):
            criteria["geographic_clues"] = True
            score += 20
        
        # Vérifier la longueur appropriée (ni trop courte, ni trop longue)
        if 50 <= len(enigma_text) <= 300:
            criteria["appropriate_length"] = True
            score += 20
        
        result = {
            "score": score,
            "criteria": criteria,
            "is_valid": score >= 60,
            "suggestions": []
        }
        
        if not criteria["poetic_style"]:
            result["suggestions"].append("Ajouter des éléments poétiques (rimes, rythme)")
        if not criteria["cultural_references"]:
            result["suggestions"].append("Intégrer des références culturelles/historiques")
        if not criteria["word_play"]:
            result["suggestions"].append("Développer les jeux de mots et double sens")
        
        return json.dumps(result, ensure_ascii=False, indent=2)


class SectionFormatterInput(BaseModel):
    """Input pour l'outil de formatage des sections"""
    section_number: int = Field(description="Numéro de la section")
    title: str = Field(description="Titre de la section")
    content: str = Field(description="Contenu narratif de la section")


class SectionFormatterTool(BaseTool):
    """Outil de formatage des sections selon le format Golden Bullets"""
    name: str = "section_formatter"
    description: str = "Formate une section selon le standard Golden Bullets (#XX **[Titre]** + contenu)"
    args_schema: Type[BaseModel] = SectionFormatterInput

    def _run(self, section_number: int, title: str, content: str) -> str:
        """Formate une section selon le format standard"""
        
        # Nettoyer le titre (supprimer les ** s'ils existent déjà)
        clean_title = title.strip().strip('*').strip()
        
        # Vérifier la longueur du contenu
        content_length = len(content)
        
        # Construire la section formatée
        formatted_section = f"#{section_number:02d}\n**{clean_title}**\n\n{content}"
        
        # Valider le format
        validation = {
            "format_valid": True,
            "title_length": len(clean_title),
            "content_length": content_length,
            "warnings": []
        }
        
        if len(clean_title) < 5:
            validation["warnings"].append("Titre trop court (< 5 caractères)")
        elif len(clean_title) > 50:
            validation["warnings"].append("Titre trop long (> 50 caractères)")
        
        if content_length < 1500:
            validation["warnings"].append(f"Contenu trop court ({content_length}/2000-2500 caractères)")
        elif content_length > 3000:
            validation["warnings"].append(f"Contenu trop long ({content_length}/2000-2500 caractères)")
        
        result = {
            "formatted_section": formatted_section,
            "validation": validation
        }
        
        return json.dumps(result, ensure_ascii=False, indent=2)


class RadioContactGeneratorInput(BaseModel):
    """Input pour l'outil de génération de contacts radio"""
    contact_type: str = Field(description="Type de contact: 'initial', 'progress', 'final'")
    situation: str = Field(description="Description de la situation actuelle")
    theme: str = Field(description="Thème de l'aventure")


class RadioContactGeneratorTool(BaseTool):
    """Outil de génération des communications radio authentiques"""
    name: str = "radio_contact_generator"
    description: str = "Génère des communications radio authentiques entre studio et terrain"
    args_schema: Type[BaseModel] = RadioContactGeneratorInput

    def _run(self, contact_type: str, situation: str, theme: str) -> str:
        """Génère une communication radio selon le type et la situation"""
        
        radio_templates = {
            "initial": [
                "Allô Philippe ? Vous nous recevez depuis {location} ?",
                "Philippe de Dieuleveult, nous vous entendons parfaitement depuis Paris !",
                "Contact établi ! Nous suivons votre progression sur nos cartes du studio."
            ],
            "progress": [
                "Où en êtes-vous Philippe ? Nous suivons avec passion votre avancement !",
                "Philippe, que voyez-vous maintenant ? Décrivez-nous la situation !",
                "Nous sommes suspendus à vos lèvres ! Que découvrez-vous ?"
            ],
            "final": [
                "Nous touchons au but ! Que voyez-vous Philippe ?",
                "L'émotion est à son comble ici au studio ! Confirmez-nous votre découverte !",
                "Fantastique ! Décrivez-nous ce moment extraordinaire !"
            ]
        }
        
        responses = {
            "terrain_initial": [
                "Allô Paris ? Je vous reçois 5 sur 5 ! C'est fantastique ici !",
                "Je suis bien arrivé ! Le paysage est absolument merveilleux !",
                "Contact parfait ! Je commence l'exploration, quelle aventure !"
            ],
            "terrain_progress": [
                "C'est extraordinaire ! Je viens de découvrir quelque chose d'incroyable !",
                "Quelle merveille ! Les habitants locaux sont d'une gentillesse remarquable !",
                "Je progresse selon vos conseils ! L'énigme commence à prendre sens !"
            ],
            "terrain_final": [
                "Incroyable ! Je crois que nous avons résolu l'énigme !",
                "C'est un moment magique ! La découverte dépasse tous nos espoirs !",
                "Mission accomplie ! Quelle aventure extraordinaire nous venons de vivre !"
            ]
        }
        
        # Sélectionner le bon template
        if contact_type in radio_templates:
            studio_lines = radio_templates[contact_type]
            terrain_lines = responses.get(f"terrain_{contact_type}", ["Reçu Paris !"])
        else:
            studio_lines = ["Allô Philippe ? Vous nous recevez ?"]
            terrain_lines = ["Reçu Paris, je vous entends parfaitement !"]
        
        # Générer le dialogue radio
        import random
        studio_line = random.choice(studio_lines)
        terrain_line = random.choice(terrain_lines)
        
        # Personnaliser selon la situation
        location = "sur place"
        if "egypte" in theme.lower():
            location = "d'Égypte"
        elif "grece" in theme.lower():
            location = "de Grèce"
        elif "perou" in theme.lower():
            location = "du Pérou"
        
        studio_line = studio_line.format(location=location)
        
        result = {
            "studio_contact": studio_line,
            "terrain_response": terrain_line,
            "radio_dialogue": f'— {studio_line}\n— {terrain_line}',
            "context": f"Contact radio {contact_type} pour {theme}"
        }
        
        return json.dumps(result, ensure_ascii=False, indent=2)


class CulturalContextValidatorInput(BaseModel):
    """Input pour l'outil de validation du contexte culturel"""
    content: str = Field(description="Contenu à valider")
    theme: str = Field(description="Thème cultural de l'aventure")


class CulturalContextValidatorTool(BaseTool):
    """Outil de validation de l'authenticité culturelle"""
    name: str = "cultural_context_validator"
    description: str = "Valide l'authenticité et le respect culturel du contenu"
    args_schema: Type[BaseModel] = CulturalContextValidatorInput

    def _run(self, content: str, theme: str) -> str:
        """Valide le contexte culturel et l'authenticité"""
        
        # Critères de validation culturelle
        validation_criteria = {
            "respectful_language": True,  # Pas de termes péjoratifs
            "historical_accuracy": False,  # Références historiques plausibles
            "cultural_sensitivity": True,  # Respect des traditions
            "educational_value": False,   # Valeur éducative présente
            "authentic_details": False    # Détails authentiques
        }
        
        issues = []
        score = 0
        
        # Vérifier la langue respectueuse
        problematic_terms = ["primitif", "sauvage", "arriéré", "bizarre"]
        if any(term in content.lower() for term in problematic_terms):
            validation_criteria["respectful_language"] = False
            issues.append("Utilisation de termes potentiellement irrespectueux")
        else:
            score += 20
        
        # Vérifier les références historiques
        historical_markers = ["siècle", "époque", "ancien", "tradition", "histoire"]
        if any(marker in content.lower() for marker in historical_markers):
            validation_criteria["historical_accuracy"] = True
            score += 20
        
        # Vérifier la sensibilité culturelle  
        respectful_terms = ["respectueusement", "tradition", "culture", "heritage", "local"]
        if any(term in content.lower() for term in respectful_terms):
            score += 20
        else:
            issues.append("Manque d'expressions de respect culturel")
        
        # Vérifier la valeur éducative
        educational_terms = ["apprendre", "découvrir", "comprendre", "signifie", "représente"]
        if any(term in content.lower() for term in educational_terms):
            validation_criteria["educational_value"] = True
            score += 20
        
        # Vérifier les détails authentiques selon le thème
        theme_keywords = {
            "egypte": ["pharaon", "pyramide", "nil", "hiéroglyphe", "temple"],
            "grece": ["temple", "colonne", "mythologie", "oracle", "agora"],
            "perou": ["inca", "machu picchu", "andes", "quechua", "llama"]
        }
        
        theme_lower = theme.lower()
        for theme_key, keywords in theme_keywords.items():
            if theme_key in theme_lower:
                if any(keyword in content.lower() for keyword in keywords):
                    validation_criteria["authentic_details"] = True
                    score += 20
                break
        
        result = {
            "cultural_score": score,
            "validation_criteria": validation_criteria,
            "is_culturally_appropriate": score >= 60,
            "issues": issues,
            "theme_context": theme
        }
        
        return json.dumps(result, ensure_ascii=False, indent=2)