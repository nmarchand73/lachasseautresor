# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

"La Chasse au Trésor" - An interactive adventure book generator inspired by the 1980s French TV show hosted by Philippe de Dieuleveult. The project aims to create "choose your own adventure" books using a CrewAI-based agentic system that captures the authentic spirit of the original show.

## Project Structure

```
LACHASSEAUXTRESOR/
├── brief/
│   ├── concept.md                            # Core concept and game mechanics
│   ├── PRD_CrewAI_Adventure_Book_Generator.md # Detailed product requirements
│   └── book_golden_bullets.json              # Example book in Golden Bullets format
```

## Book Format Specification

Books follow the **Golden Bullets format** with these key specifications:
- **95 numbered paragraphs** plus special sections (title, intro)
- **Paragraph length**: 2000-2500 characters (300-400 words)
- **2-3 choices per paragraph** for navigation
- **JSON structure** with specific schema (see brief/book_golden_bullets.json)

### JSON Structure
```json
{
  "id": "adventure_name",
  "title": "Title",
  "content": {
    "title": { /* title page */ },
    "intro": { /* introduction */ },
    "1-95": { /* numbered paragraphs */ }
  }
}
```

## CrewAI Agent Architecture

The system uses specialized agents modeling the original TV show team:

1. **Agent Jacques Antoine** - Producer/Enigma Creator
2. **Agent Philippe Gildas** - Studio Presenter
3. **Agent Philippe de Dieuleveult** - Field Adventurer
4. **Agent Pilot** - Helicopter Navigator
5. **Agent Local Expert** - Cultural Guides
6. **Agent TV Director** - Pacing and Structure

## Key Narrative Elements

### Essential TV Show Elements to Maintain
- Studio/field duo dynamic with radio communication
- Red jumpsuit iconic adventurer outfit
- Helicopter as primary transport
- Cultural and historical enigmas
- Enthusiastic discovery tone ("Fantastique!", "Quelle merveille!")
- Educational aspect without being preachy

### 1980s Constraints
- No GPS/smartphones (compass and map navigation)
- Radio communication with interference
- Film camera with limited shots
- No internet (book knowledge from studio)

## Writing Guidelines

### Tone and Style
- **Target audience**: Family-friendly, ages 7-77
- **Narrative voice**: Second person, direct and immersive
- **Enthusiasm level**: High but sincere (Philippe de Dieuleveult style)
- **Cultural respect**: Authentic representation of local populations
- **Educational**: Learn through adventure, not lectures

### Paragraph Structure
1. Scene setting and atmosphere
2. Action or discovery
3. Decision point with clear choices
4. Navigation instructions ("Aller au numéro #XX")

## Development Tasks

When implementing the CrewAI system:
1. Start with agent definitions matching PRD specifications
2. Implement the three-phase workflow: Pre-production → Generation → Post-production
3. Validate JSON output against Golden Bullets schema
4. Ensure paragraph cross-references are valid
5. Maintain the TV show episode structure (3 treasures, 15 minutes each)

## Output Formats

The system supports two output formats:

### Markdown Format (Default)
- Human-readable format with table of contents
- Section-based structure with clear navigation
- Compatible with documentation systems
- Use: `python -m src.main generate` or `--format markdown`

### JSON Format  
- Golden Bullets compatible JSON structure
- Machine-readable for game engines
- Full paragraph data with choices
- Use: `--format json` or `--format both`

## Commands

Key CLI commands for development:
- `generate`: Create new adventure book
- `validate`: Check book structure and references
- `preview`: View Markdown preview of book
- `list-books`: Show all generated books
- `clean`: Remove old files

## Testing Approach

Since no code exists yet, when code is developed:
- Test JSON output validation against schema
- Verify paragraph numbering continuity
- Check choice destination validity
- Ensure narrative coherence across branches
- Validate cultural and historical accuracy

## Important Notes

- The project is currently in conceptual phase with specifications only
- No implementation code exists yet
- Focus on maintaining authenticity to the 1980s TV show
- Prioritize cultural sensitivity and educational value
- Keep the adventure spirit alive with genuine enthusiasm