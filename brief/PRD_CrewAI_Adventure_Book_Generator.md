# PRD - Générateur de Livres d'Aventure "La Chasse au Trésor"
## Système Agentic basé sur CrewAI - Version Authentique Années 80

**Version:** 2.0  
**Date:** 2025-01-27  
**Auteur:** Équipe de développement  

---

## 1. Vue d'ensemble du produit

### 1.1 Vision
Créer un système automatisé basé sur CrewAI capable de générer des livres d'aventure interactifs "dont vous êtes le héros" qui capturent **l'esprit authentique de l'émission "La Chasse au Trésor" des années 80**, avec Philippe de Dieuleveult comme modèle d'aventurier, des énigmes basées sur la découverte culturelle et l'ambiance unique de cette époque télévisuelle légendaire.

### 1.2 L'esprit "La Chasse au Trésor" à capturer

#### **Éléments essentiels de l'émission originale**
- **Le duo studio/terrain** : Les candidats en studio à Paris déchiffrent les énigmes et guident l'aventurier sur le terrain
- **La combinaison rouge iconique** : L'aventurier en combinaison rouge, reconnaissable entre tous
- **L'hélicoptère omniprésent** : Moyen de transport principal entre les lieux d'énigmes
- **Les énigmes culturelles** : Basées sur l'histoire, la géographie, les légendes locales
- **Le contact radio permanent** : "Allô Paris ? J'écoute l'énigme..."
- **L'enthousiasme communicatif** : "Fantastique !", "Quelle merveille !", "C'est extraordinaire !"
- **La découverte éducative** : Chaque trésor révèle une page d'histoire locale

### 1.3 Objectifs stratégiques revus
- **Authenticité années 80** : Reproduire fidèlement l'ambiance et le format de l'émission originale
- **Mécaniques de jeu fidèles** : Intégrer le système studio/terrain, les communications radio, l'hélicoptère
- **Ton Philippe de Dieuleveult** : Capturer son enthousiasme, son humilité et sa passion pour la découverte
- **Énigmes à la Jacques Antoine** : Créer des énigmes intelligentes mêlant culture et observation
- **Format télévisuel** : Structurer comme des épisodes de 45 minutes avec 3 trésors à découvrir

---

## 2. Architecture du système CrewAI - Équipe de Production TV

### 2.1 Agents spécialisés (L'équipe de production de l'émission)

#### **Agent Jacques Antoine (Producteur-Concepteur)**
```
role: "Producteur et créateur d'énigmes à la manière de Jacques Antoine"
goal: "Concevoir des énigmes intelligentes et des aventures captivantes"
backstory: "Producteur de génie des jeux télévisés, créateur de concepts innovants"
```

**Responsabilités :**
- Concevoir la structure globale de chaque "émission-livre" (3 trésors, 45 minutes de jeu)
- Créer des énigmes poétiques et culturelles dans le style Jacques Antoine
- Superviser la cohérence du concept télévisuel
- Valider que chaque énigme a une dimension éducative
- S'assurer du respect du format original (1981-1984)

**Style d'énigmes Jacques Antoine :**
- Énigmes en vers ou prose poétique
- Références culturelles subtiles
- Jeux de mots et double sens
- Indices visuels et géographiques

#### **Agent Philippe Gildas (Présentateur Studio)**
```
role: "Présentateur en studio guidant les candidats"
goal: "Maintenir le lien studio-terrain et guider la progression"
backstory: "Journaliste chevronné, voix rassurante et neutre du studio parisien"
```

**Responsabilités :**
- Introduire chaque destination avec contexte historique/géographique
- Lire les énigmes aux "candidats" (le lecteur)
- Maintenir le contact avec le terrain ("Philippe, vous nous recevez ?")
- Donner des indices supplémentaires si nécessaire
- Féliciter ou encourager selon les choix

**Phrases types :**
- "Voyons ce que nous dit l'énigme..."
- "Philippe est en approche de la zone..."
- "Attention, le temps presse !"
- "Magnifique ! Vous avez trouvé !"

#### **Agent Philippe de Dieuleveult (Aventurier Terrain)**
```
role: "L'aventurier intrépide en combinaison rouge"
goal: "Incarner l'esprit d'aventure et de découverte avec humilité"
backstory: "Reporter globe-trotter passionné, toujours prêt à relever les défis"
```

**Responsabilités :**
- Décrire les lieux avec enthousiasme et émerveillement
- Interagir respectueusement avec les populations locales
- Affronter les défis physiques avec courage mais prudence
- Transmettre sa passion pour la découverte culturelle
- Maintenir le contact radio avec Paris

**Phrases caractéristiques :**
- "C'est absolument fantastique !"
- "Quelle merveille de la nature !"
- "Les habitants m'ont expliqué que..."
- "J'aperçois quelque chose d'extraordinaire !"
- "Allô Paris ? Je suis sur place..."

#### **Agent Pilote d'Hélicoptère**
```
role: "Pilote expert guidant l'aventurier vers les destinations"
goal: "Assurer les transitions aériennes et offrir une vue d'ensemble"
backstory: "Pilote chevronné connaissant parfaitement les régions survolées"
```

**Responsabilités :**
- Décrire les survols et vues aériennes spectaculaires
- Suggérer des zones d'atterrissage stratégiques
- Fournir des informations géographiques vues du ciel
- Créer des moments de tension (météo, carburant limité)
- Offrir une perspective unique sur les sites

**Éléments caractéristiques :**
- Descriptions de paysages vus du ciel
- Repérage de détails invisibles du sol
- Contraintes techniques (zones d'atterrissage, autonomie)
- Conditions météo affectant la progression

#### **Agent Expert Local (Intervenants sur place)**
```
role: "Habitants locaux, guides, historiens rencontrés sur place"
goal: "Enrichir culturellement et humainement l'aventure"
backstory: "Personnages authentiques partageant leur savoir local"
```

**Responsabilités :**
- Fournir des informations culturelles authentiques
- Partager légendes et traditions locales
- Donner des indices subtils ou créer des fausses pistes
- Incarner l'hospitalité et la richesse humaine des lieux
- Ajouter une dimension humaine à l'aventure

#### **Agent Réalisateur TV**
```
role: "Réalisateur orchestrant le rythme télévisuel"
goal: "Maintenir le format et le rythme d'une émission TV des années 80"
backstory: "Réalisateur expérimenté en programmes d'aventure"
```

**Responsabilités :**
- Structurer en "séquences TV" de 15 minutes (3 par émission)
- Créer des moments de suspense avant les coupures publicitaires
- Alterner séquences action/réflexion/découverte culturelle
- Maintenir le rythme "45 minutes" de l'émission originale
- Gérer les transitions studio/terrain/hélicoptère

### 2.2 Flux de travail revu - Production d'une "émission-livre"

```
PHASE 1: PRÉ-PRODUCTION (comme pour l'émission TV)
├── Jacques Antoine conçoit les 3 énigmes principales
├── Repérage des 3 destinations par l'équipe
├── Recherche culturelle et historique approfondie
└── Validation de la faisabilité des parcours

PHASE 2: TOURNAGE/GÉNÉRATION
├── Séquence d'ouverture en studio avec Philippe Gildas
├── Pour chaque trésor (3 séquences de 15 min):
│   ├── Lecture de l'énigme en studio
│   ├── Décollage en hélicoptère
│   ├── Exploration sur le terrain
│   ├── Rencontres avec habitants locaux
│   ├── Résolution de l'énigme
│   └── Découverte du trésor et explication culturelle
└── Séquence de clôture avec bilan des découvertes

PHASE 3: POST-PRODUCTION
├── Montage des séquences
├── Ajout des éléments culturels enrichis
├── Validation de la cohérence narrative
└── Export au format livre interactif
```

---

## 3. Mécaniques de jeu spécifiques "La Chasse au Trésor"

### 3.1 Structure narrative adaptée au format Golden Bullets

#### **Format et structure du livre**
Chaque livre sera structuré selon le modèle de Golden Bullets avec environ 95 paragraphes numérotés :

**INTRODUCTION (Paragraphes "intro" et 1-3)**
- Mise en place du contexte et de la mission
- Présentation du personnage principal et de son équipement
- Rencontre avec les personnages secondaires

**PREMIÈRE PARTIE DE L'AVENTURE (Paragraphes 4-30)**
- Premiers choix et embranchements
- Découverte progressive de l'intrigue principale
- Premières rencontres et obstacles

**PARTIE CENTRALE (Paragraphes 31-60)**
- Intensification des défis
- Révélations importantes sur la mission
- Confrontations avec les antagonistes

**PARTIE FINALE (Paragraphes 61-90)**
- Résolution des énigmes principales
- Confrontations décisives
- Découverte du trésor/objectif final

**CONCLUSION (Paragraphes 91-95)**
- Dénouement de l'aventure
- Conséquences des choix du lecteur
- Ouverture possible vers d'autres aventures

#### **Sections spéciales**
- Paragraphe "title" : Page de titre du livre
- Paragraphe "intro" : Introduction/prologue de l'histoire
- Paragraphes numérotés : Corps principal de l'aventure (1-95)
- Paragraphes de combat (optionnels) : Pour les séquences d'action

### 3.2 Format des paragraphes basé sur Golden Bullets

#### **Structure d'un paragraphe type**
Chaque paragraphe suivra cette structure standardisée :

```json
{
  "paragraph_number": number,
  "text": "#XX\n- Titre du paragraphe\nTexte principal du paragraphe sur 2000-2500 caractères (environ 300-400 mots)...",
  "choices": [
    {
      "text": "Description du choix → Aller au numéro #YY",
      "destination": YY
    },
    {
      "text": "Description du second choix → Continuer au numéro #ZZ",
      "destination": ZZ
    }
  ],
  "combat": null
}
```

#### **Exemple de paragraphe type**
```
#42
- Au pied du temple
Le temple se dresse devant vous, imposant et mystérieux. Ses pierres anciennes racontent une histoire millénaire que peu de gens peuvent déchiffrer. Vous observez les gravures sur les murs, cherchant un indice, une piste qui pourrait vous mener au trésor. Le soleil commence à décliner, projetant des ombres allongées sur le sol poussiéreux.

Un homme âgé s'approche lentement. Son visage ridé témoigne d'une vie riche en expériences.

— Vous cherchez quelque chose de précis ? demande-t-il dans un français approximatif.

— Je suis à la recherche d'un ancien artefact, lui répondez-vous.

Il hoche la tête, comme s'il comprenait parfaitement votre quête.

— La face nord cache bien des secrets, murmure-t-il. Mais seuls les plus perspicaces savent où regarder.

Que décidez-vous ?

Explorer la face nord du temple.
Aller au numéro #56

Questionner davantage le vieil homme.
Continuer au numéro #63
```

#### **Longueur et style des paragraphes**
- **Longueur moyenne** : 2000-2500 caractères (300-400 mots)
- **Style narratif** : Direct, immersif, à la seconde personne
- **Dialogues** : Formatés avec des tirets (—)
- **Structure** : Introduction, développement, choix
- **Nombre de choix** : Généralement 2, parfois 3 maximum

### 3.3 Typologie des énigmes "Jacques Antoine"

#### **Énigmes géographiques**
```
"Là où le fleuve embrasse la montagne,
Au pays où le condor accompagne
Le soleil dans sa course éternelle,
Se cache la cité sentinelle."
```

#### **Énigmes historiques**
```
"Trois pyramides gardent le secret,
Du pharaon qui jamais ne dormait.
Cherchez la plus petite des trois,
C'est là que repose le roi."
```

#### **Énigmes d'observation**
```
"Comptez les colonnes du temple sacré,
Divisez par le nombre de divinités.
Le résultat vous montrera
Quelle porte il faudra."
```

---

## 4. Tonalité et style narratif authentique

### 4.1 Le ton "Philippe de Dieuleveult"

#### **Caractéristiques essentielles**
- **Enthousiasme sincère** : Jamais blasé, toujours émerveillé
- **Humilité** : Respect profond pour les cultures visitées
- **Pédagogie naturelle** : Explications claires sans condescendance
- **Courage mesuré** : Brave mais pas casse-cou irresponsable
- **Humanité** : Vraie connection avec les populations locales

#### **Vocabulaire caractéristique**
- "Fantastique !", "Extraordinaire !", "Quelle merveille !"
- "Les habitants m'ont gentiment expliqué..."
- "C'est absolument incroyable ce que nous découvrons !"
- "Regardez cette splendeur !"
- "Je suis bouleversé par tant de beauté"

### 4.2 Le style "émission familiale du dimanche"

#### **Principes narratifs**
- **Accessible à tous** : 7 à 77 ans
- **Éducatif sans être scolaire** : Apprendre en s'amusant
- **Respectueux** : Jamais de moquerie ou stéréotypes
- **Positif** : Célébration de la découverte et de la culture
- **Familial** : Approprié pour toute la famille réunie

---

## 5. Spécifications techniques adaptées

### 5.1 Structure de données JSON basée sur Golden Bullets

```json
{
  "id": "adventure_name",
  "title": "Titre de l'Aventure",
  "author": "Système CrewAI",
  "content": {
    "title": {
      "paragraph_number": "title",
      "text": "Titre de l'Aventure\nUn livre dont vous êtes le Héros\nGénéré par CrewAI",
      "choices": [],
      "combat": null
    },
    "intro": {
      "paragraph_number": "intro",
      "text": "Texte d'introduction présentant le contexte...",
      "choices": [
        {
          "text": "Commencer l'aventure",
          "destination": 1
        }
      ],
      "combat": null
    },
    "1": {
      "paragraph_number": 1,
      "text": "#01\n- Titre du premier paragraphe\nTexte principal du premier paragraphe...",
      "choices": [
        {
          "text": "Premier choix → Aller au numéro #XX",
          "destination": XX
        },
        {
          "text": "Second choix → Continuer au numéro #YY",
          "destination": YY
        }
      ],
      "combat": null
    },
    // ... autres paragraphes numérotés de 2 à 95
  },
  "total_sections": 95,
  "created_at": "timestamp",
  "original_filename": "adventure_name.json",
  "review_status": "completed",
  "sections_found": 97  // Incluant title et intro
}
```

### 5.2 Contraintes spécifiques années 80

#### **Contraintes technologiques d'époque**
- Pas de GPS ni smartphone (orientation à la boussole et carte)
- Communication radio parfois difficile (grésillements, coupures)
- Appareil photo argentique (nombre de photos limité)
- Pas d'internet (connaissances livresques du studio)

#### **Contraintes culturelles années 80**
- Respect absolu des sites sacrés et traditions
- Interactions authentiques sans Google Translate
- Découvertes "vierges" sans TripAdvisor
- Émerveillement genuine pré-Instagram

---

## 6. Métriques de succès adaptées

### 6.1 Métriques d'authenticité

| Métrique | Cible | Mesure |
|----------|-------|---------|
| **Fidélité au format TV** | 95% | Structure en 3 séquences de 15 min |
| **Ton Philippe de Dieuleveult** | 90% | Analyse linguistique des exclamations |
| **Authenticité des énigmes** | 100% | Style Jacques Antoine vérifié |
| **Présence hélicoptère** | 30% | Des paragraphes avec références aériennes |
| **Interactions radio** | 20% | Des paragraphes avec contact studio |

### 6.2 Métriques d'expérience

| Aspect | Critère d'évaluation |
|--------|---------------------|
| **Nostalgie années 80** | Reconnaissance par fans de l'émission originale |
| **Aspect éducatif** | Apprentissages culturels par aventure |
| **Tension dramatique** | Moments de suspense "avant la pub" |
| **Émerveillement** | Descriptions enthousiastes des découvertes |
| **Respect culturel** | Représentation authentique des populations |

---

## 7. Exemples de génération basés sur Golden Bullets

### 7.1 Exemple de paragraphe d'introduction

```json
{
  "paragraph_number": "intro",
  "text": "Texas, 1869\n\nLe vent soulève la poussière sur la rue principale d'Amarillo. Votre réputation de tireur d'élite vous a valu le surnom de 'Golden Bullets' au sein de La Horde, un réseau de hors-la-loi qui lutte contre le gouverneur Wallace. Après avoir exécuté un traître dans un village frontalier, vous revenez enfin vers des terres connues.\n\nEn poussant les battants du Silver Dollar Saloon, une bouffée d'air chaud mêlée à l'odeur d'alcool et de tabac vous emplit les narines. Greg, le barman, essuie des verres derrière son comptoir. Son sourire en coin n'annonce jamais rien de bon.\n\n— Danny ! Ça tombe bien que tu sois là. J'ai une mission pour toi. Du genre... spécial.",
  "choices": [
    {
      "text": "Poursuivre l'aventure...",
      "destination": 1
    }
  ],
  "combat": null
}
```

### 7.2 Exemple de paragraphe standard

```json
{
  "paragraph_number": 42,
  "text": "#42\n- Face à un dilemme\n\nLe canyon s'étend devant vous, baigné par la lumière rouge du soleil couchant. Vous observez les parois rocheuses à la recherche d'un passage. Jack, votre guide, pointe du doigt une corniche étroite.\n\n— Par là, on pourrait atteindre l'autre versant, suggère-t-il en ajustant son chapeau usé.\n\nErin, l'éclaireuse, secoue la tête avec désapprobation.\n\n— Trop risqué. J'ai repéré un sentier plus bas qui contourne le précipice. Plus long, mais plus sûr.\n\nPaul, lui, ne cache pas son impatience.\n\n— On perd du temps ! Les soldats du gouverneur nous rattrapent. Il faut prendre un risque ou abandonner la mission.\n\nLe soleil disparaît rapidement. Bientôt, l'obscurité rendra tout déplacement périlleux. La décision vous revient.\n\nEmprunter la corniche dangereuse.\nAller au numéro #56\n\nSuivre le sentier plus long mais sécurisé.\nContinuer au numéro #63",
  "choices": [
    {
      "text": "Aller au numéro #56",
      "destination": 56
    },
    {
      "text": "Continuer au numéro #63",
      "destination": 63
    }
  ],
  "combat": null
}
```

---

## 8. Planning de développement adapté au format Golden Bullets

### Phase 1 - Prototype initial (4 semaines)
**Focus :** Structure et format Golden Bullets

**Priorités :**
- Mise en place des agents principaux (Storyteller, Plot Designer)
- Génération d'un livre court (30 paragraphes)
- Structure JSON conforme au format Golden Bullets
- Validation de la cohérence des embranchements

### Phase 2 - Livre complet (6 semaines)
**Focus :** Génération d'un livre complet

**Priorités :**
- Génération de 95 paragraphes structurés
- Tous les agents actifs et collaborant
- Système de validation des références croisées
- Richesse narrative et équilibrage des choix

### Phase 3 - Optimisation et qualité (4 semaines)
**Focus :** Perfectionnement du système

**Priorités :**
- Validation par tests utilisateurs
- Ajustements du style et de la longueur des paragraphes
- Optimisation des performances de génération
- Enrichissement des mécaniques narratives

---

## 9. Conclusion

Ce PRD définit un système de génération qui adapte le concept de "La Chasse au Trésor" au **format Golden Bullets**, créant ainsi des livres d'aventure interactifs riches et engageants. Les points clés de cette approche sont :

### Structure et format standardisés
- 95 paragraphes numérotés suivant le modèle Golden Bullets
- Paragraphes de 2000-2500 caractères (300-400 mots)
- Format JSON structuré et validé
- 2-3 choix par paragraphe pour une navigation fluide

### Richesse narrative
- Histoires immersives avec des personnages mémorables
- Embranchements multiples offrant une réelle rejouabilité
- Équilibre entre action, exploration et énigmes
- Ton adapté au genre et au public cible

### Innovation technique
- Système agentic CrewAI pour une génération collaborative
- Validation automatique de la cohérence narrative
- Équilibrage des parcours et des difficultés
- Exportation dans des formats adaptés aux différents supports

Ce système permettra de générer efficacement des livres d'aventure interactifs de qualité professionnelle, offrant aux lecteurs des expériences narratives riches et personnalisées dans la tradition des meilleurs "livres dont vous êtes le héros".

**"Votre aventure commence maintenant. À vous de faire les bons choix !"**