# 🚁 La Chasse au Trésor - Adventure Book Generator

AI-powered system based on CrewAI to automatically generate interactive "choose your own adventure" books inspired by the iconic 1980s French TV show "La Chasse au Trésor" with Philippe de Dieuleveult.

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

### 🎯 Interactive Mode (Recommended)

Create personalized adventures with guided setup:

```bash
# Interactive creation wizard - starts questionnaire
python -m src.main create

# Or force interactive mode on generate command
python -m src.main generate -i
```

**Interactive features:**
- 📍 **Step 1**: Choose destination (Egypt, Greece, Peru, France, Cambodia, Jordan, Tibet, or custom)
- 🎭 **Step 2**: Select theme with region-specific suggestions
- 📖 **Step 3**: Pick length (Test/Short/Standard/Complete/Custom 1-200 paragraphs)
- ⚡ **Step 4**: Choose generation mode (fast/detailed)

### 🚀 Quick Generation

```bash
# Quick test (recommended first try)
python -m src.main test

# Generate with specific parameters
python -m src.main generate --theme "Les Mystères d'Égypte" --sections 30

# Complete Golden Bullets format (95 paragraphs)
python -m src.main generate --sections 95
```

### 📋 Management Commands

```bash
# List all generated books
python -m src.main list-books

# Validate a book structure
python -m src.main validate output/books/book.json

# Preview a Markdown book
python -m src.main preview output/markdown/book.md

# Clean old files (30+ days)
python -m src.main clean

# System information
python -m src.main info

# Show all available commands
python -m src.main --help
```

### 🧪 Testing

```bash
# Complete system test with example generation
python test_clean.py
```

## 📁 Project Structure

```
lachasseauxtresor/
├── src/
│   ├── simple_generator.py    # Main generator
│   ├── main.py               # CLI interface
│   └── utils/                # Utilities
│       ├── file_handler.py   # File management
│       └── json_formatter.py # JSON utilities
├── output/                   # Generated books
│   ├── books/               # JSON files
│   └── markdown/            # Markdown files
├── brief/                   # Project documentation
│   ├── concept.md           # Original concept
│   ├── PRD_*.md            # Specifications
│   └── book_golden_bullets.json # Format example
├── test_*.py               # Test scripts
├── CLAUDE.md              # Claude instructions
├── QUICKSTART.md          # Quick guide
└── requirements.txt       # Dependencies
```

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

**Current version**: Full-featured interactive generation system with:
- ✅ **Interactive wizard**: Guided theme and country selection
- ✅ **Flexible paragraph count**: 1-200 paragraphs with smart modes
- ✅ **Complete CLI interface**: 8 commands with rich output
- ✅ **Content generator**: OpenAI-powered with authentic TV show style
- ✅ **Markdown export**: Navigation, metadata, and cross-references  
- ✅ **Content validation**: Quality review and structure checking
- ✅ **Automated tests**: Full system validation
- ✅ **Regional themes**: Pre-configured suggestions by destination
- 🚧 CrewAI integration (in development)

> **Note**: JSON generation (Golden Bullets format) has been temporarily disabled to focus on Markdown format quality.

## 🧪 Tests

```bash
# Complete system test
python test_clean.py

# Import tests (optional)
python test_imports.py
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