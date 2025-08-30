# 🚁 La Chasse au Trésor - Adventure Book Generator

AI-powered adventure book generator featuring both simple and advanced CrewAI multi-agent systems, inspired by the iconic 1980s French TV show "La Chasse au Trésor" with Philippe de Dieuleveult.

## 📚 Description

This project automatically generates interactive "choose your own adventure" books inspired by the 1980s TV show "La Chasse au Trésor". The system uses AI to create authentic stories featuring:

- **Philippe de Dieuleveult Style**: Authentic enthusiasm and wonder
- **Cultural Enigmas**: Based on history and geography
- **1980s TV Format**: Episode structure with suspense
- **Immersive Descriptions**: Exotic locations and local encounters
- **Narrative Choices**: Multiple branches for replayability

## 🚀 Installation

1. **Clone the repository**
```bash
git clone https://github.com/nmarchand73/lachasseautresor.git
cd lachasseautresor
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure OpenAI API**
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

## 📖 Usage

### 🤖 CrewAI Mode (Recommended)

High-quality generation with 6 specialized agents:

```bash
# Interactive CrewAI mode
python -m src.main generate --crew --interactive

# Direct CrewAI generation
python -m src.main generate --crew --theme "Les Mystères d'Égypte" --sections 35

# Install CrewAI dependencies first
python install_crewai.py
```

### 🎯 Simple Mode (Fast)

Basic generation for quick testing:

```bash
# Interactive mode
python -m src.main generate --interactive

# Direct generation
python -m src.main generate --theme "Les Trésors de Petra" --sections 15
```

**Interactive features:**
- 📍 **Step 1**: Choose destination (Egypt, Greece, Peru, France, Cambodia, Jordan, Tibet, or custom)
- 🎭 **Step 2**: Select theme with region-specific suggestions
- 📖 **Step 3**: Pick length (Short/Standard/Complete/Custom 1-200 paragraphs)

### 🔧 System Commands

```bash
# Check system status and configuration
python -m src.main info

# Install and verify CrewAI setup
python install_crewai.py

# Show all available commands
python -m src.main --help
```


## 📁 Project Structure

```
lachasseauxtresor/
├── src/
│   ├── simple_generator.py       # Basic AI generator
│   ├── crewai_generator_v2.py    # Advanced CrewAI system
│   ├── main.py                   # CLI interface
│   ├── crewai_config/           # CrewAI configuration
│   │   ├── agents.yaml          # 6 specialized agents
│   │   └── tasks.yaml           # Multi-phase workflow
│   └── crewai_tools/           # Custom CrewAI tools
├── output/                     # Generated books
│   └── markdown/              # Markdown format only
├── brief/                     # Project documentation
│   ├── concept.md            # Original concept
│   └── PRD_*.md             # Specifications
├── install_crewai.py         # CrewAI setup script
├── CLAUDE.md                # Development guide
└── requirements.txt         # Dependencies
```

## 🎬 Generation Systems

### 🤖 CrewAI Multi-Agent System (Premium)

6 specialized agents modeling the original TV show team:
- **Jacques Antoine**: Enigma creator and producer
- **Philippe Gildas**: Studio presenter and cultural expert
- **Philippe de Dieuleveult**: Field adventurer and reporter
- **Pilote**: Helicopter navigator and aerial reconnaissance
- **Expert Local**: Cultural guides and local knowledge
- **Réalisateur TV**: Episode structure and pacing

**Benefits:**
- 3-5x faster generation
- Superior narrative quality
- Authentic TV show atmosphere
- Cultural accuracy and educational value
- Period-accurate constraints (1980s)

### 🔧 Simple Generator (Standard)

Basic OpenAI-powered generation for quick testing and development.

## 📊 Output Format

Books are generated in **Markdown format only**:

### Markdown Format
Organized structure with:
- **Table of contents** with navigation links
- **Numbered sections** with explicit titles
- **Human-readable formatting**
- **Compatible** with Markdown editors
- **Interactive links** between sections
- **YAML metadata** in header

### Generated file structure

```markdown
---
title: "La Chasse au Trésor: The Mysteries of Egypt"
sections_found: 5
---

# Story Content (Spine Order)

## Table of Contents

- [**Introduction**](#introduction) (`intro`)
- [**Section 1: Title**](#section-1-title) (`1`)
- [**Section 2: Title**](#section-2-title) (`2`)

---

## Introduction

[Introduction content...]

**Choices:**

- [Start the adventure](#section-1)

---

## Section 1: Title

[Section content...]

**Choices:**

- [Choice 1](#section-2)
- [Choice 2](#section-2)
```

## 🔧 Configuration

Edit the `.env` file to customize:

```env
# OpenAI API Key (optional - fallback without AI available)
OPENAI_API_KEY=your_key_here

# OpenAI Model
OPENAI_MODEL_NAME=gpt-4o-mini

# Generation parameters
TEMPERATURE=0.7
MAX_TOKENS=2000
```

## 🎯 Generation Workflow

### Interactive Mode
1. **Questionnaire**: Choose destination, theme, length, and generation mode
2. **Validation**: Preview configuration and confirm settings
3. **Generation**: AI-powered content creation with progress tracking
4. **Review**: Quality assessment with authenticity scoring
5. **Export**: Markdown format with navigation and metadata

### Direct Mode  
1. **Configuration**: Command-line parameters or defaults
2. **Generation**: Content creation with specified theme and length
3. **Export**: Timestamped files in output/ directory

## ⚙️ Current Status

**Current version**: Dual-system adventure book generator featuring:

### ✅ Completed Features
- **CrewAI Multi-Agent System**: 6 specialized agents with authentic TV show roles
- **Interactive wizard**: Guided theme and country selection
- **Flexible generation**: 1-200 paragraphs with intelligent mode selection
- **Premium CLI interface**: Rich output with progress tracking
- **Dual generators**: Simple (fast) and CrewAI (quality) options
- **Markdown export**: Navigation, metadata, and cross-references
- **Cultural accuracy**: Regional themes with historical authenticity
- **1980s authenticity**: Period constraints and technology limitations
- **Signal handling**: Graceful interruption with CTRL+C

### 🎯 System Capabilities
- **Generation modes**: Short (15), Standard (35), Complete (95), Custom (1-200)
- **Cultural destinations**: 7 pre-configured regions with themed suggestions
- **Quality systems**: Both rapid prototyping and premium generation
- **Installation support**: Automated CrewAI setup and verification

## 🧪 Quick Start

```bash
# 1. Install CrewAI for best quality (recommended)
python install_crewai.py

# 2. Generate your first adventure (interactive)
python -m src.main generate --crew --interactive

# 3. Or quick test with simple generator
python -m src.main generate --theme "Les Mystères d'Égypte" --sections 5

# 4. Check system status
python -m src.main info
```

## 📝 License

MIT License - See [LICENSE](LICENSE) for details.

## 🙏 Credits

Inspired by the TV show "La Chasse au Trésor" (1981-1984) created by Jacques Antoine and hosted by Philippe Gildas and Philippe de Dieuleveult.

## 🤝 Contributing

Contributions are welcome! Please feel free to:
1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.