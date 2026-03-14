# ADEO DIY Assistant - Wood Deck Planner 🛠️

> **De l'expérimentation à l'industrialisation.**  
> Projet de démonstration conçu pour la Squad AI Factory d'ADEO, illustrant la transformation de concepts académiques en solutions robustes et industrialisées.

---

## 🎯 Vision Métier

Le **DIY Assistant** est un agent intelligent qui accompagne les clients dans la planification de projets complexes (ex: terrasse en bois). Il ne se contente pas de répondre à des questions ; il **raisonne** en croisant des sources techniques (RAG) et des données opérationnelles (Stocks/Prix) pour garantir la faisabilité du projet.

### Pourquoi ce projet ?

- **Alignement Retail :** Répond à un besoin critique de conseil expert à l'échelle
- **Architecture Agnostique :** Convertible pour n'importe quel rayon d'ADEO (Cuisine, Énergie, Sanitaire)
- **Production-Ready :** Structuré selon les standards de production (sécurité, persistance, tests)

---

## 🛠️ Stack Technique

- **Framework Agentic :** `LangGraph` (StateGraph) pour orchestration déterministe
- **Intelligence :** `OpenAI GPT-4` avec Tool-Calling avancé
- **RAG :** `LangChain` + `FAISS` pour recherche documentaire
- **Persistance :** JSON-based session storage
- **MLOps (Futur) :** `ZenML` pour pipelines
- **Serving (Futur) :** `FastAPI` pour API haute performance

---

## 🏗️ Architecture

```
adeo-diy-assistant/
├── data/                    # Sources de connaissances
│   └── guide_terrasse.txt   # Guide de construction terrasse
├── src/
│   ├── agents/
│   │   └── graph.py         # Logique LangGraph (agent → tools → agent)
│   ├── tools/
│   │   ├── stock.py         # Outil: prix et stock produits
│   │   └── search.py        # Outil: recherche dans guide (RAG)
│   ├── main.py              # Point d'entrée (mode interactif)
│   └── persistence.py       # Gestion historique JSON
├── test_Sprint1.py          # Test validation requête combinée
├── test_Sprint1_structure.py# Checklist automatisée
├── SPRINT_1_CHECKLIST.md    # Validation complète Sprint 1
└── requirements.txt         # Dépendances Python
```

---

## 🚀 Installation & Lancement

### 1. Préparation

```bash
# Créer environnement virtuel
python -m venv .venv

# Activer
source .venv/bin/activate           # macOS/Linux
# ou
.venv\Scripts\activate              # Windows

# Installer dépendances
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copier template
cp .env.example .env

# Ajouter VOTRE clé API OpenAI dans .env
# OPENAI_API_KEY=sk-proj-xxxxx...
```

### 3. Lancer l'Agent

```bash
# Mode interactif
python src/main.py

# Puis taper des questions comme:
# "Combien coûtent les lames et comment je les fixe ?"
```

### 4. Vérifier la Structure

```bash
python test_Sprint1_structure.py
```

---

## ✨ Fonctionnalités Sprint 1

| Critère | Statut | Détails |
|---------|--------|---------|
| **Tool-Calling** | ✅ | Agent choisit automatiquement `check_stock_and_price` ou `search_technical_guide` |
| **Gestion Erreurs** | ✅ | Retourne "Produit inconnu" au lieu d'halluciner |
| **Boucle LangGraph** | ✅ | Agent → Tools → Agent → END (routing complet) |
| **Persistance** | ✅ | Historique sauvegardé en `conversation_history.json` |
| **Type Hints** | ✅ | Code typé (TypedDict, Annotated, List, Dict) |
| **Sécurité** | ✅ | Clés API protégées (.env masqué, .env.example fourni) |

---

## 📋 Roadmap

### ✅ Sprint 1 - "The Brain" (COMPLET)

- Moteur de raisonnement LangGraph
- Tool-Calling stable (Stock + Technique)
- Persistance conversation
- Gestion des erreurs robuste

**Status:** ✅ Production-ready (MVP)

### 🔄 Sprint 2 - "The Factory"

- API FastAPI (`/chat`, `/history`)
- Pipelines ZenML pour données
- Monitoring & Metrics

### 🚀 Sprint 3 - "The Ship"

- Conteneurisation Docker
- IaC Terraform
- Déploiement production

---

## 📚 Documentation

- [SPRINT_1_CHECKLIST.md](SPRINT_1_CHECKLIST.md) - Validation complète des critères
- `.env.example` - Variables d'environnement requises
- `requirements.txt` - Dépendances Python

---

## 🧪 Tests

```bash
# Validation structure (recommandé d'abord)
python test_Sprint1_structure.py

# Test requête combinée (nécessite OPENAI_API_KEY valide)
python test_Sprint1.py

# Mode interactif (test manuel)
python src/main.py
# Taper : "Combien coûtent les lames et comment je les fixe ?"
```

---

## 🔐 Sécurité

- ✅ Clés API dans `.env` (non committées)
- ✅ `.gitignore` protège dossiers sensibles (`.venv/`, `__pycache__/`)
- ✅ `.env.example` fourni pour documentation
- ✅ Compliant OWASP (pas de secrets en dur)

---

## 📝 Exemple de Requête

**Question (combinée):**
```
"Combien coûtent les lames de terrasse en pin et comment je les fixe ?"
```

**Flux interne:**
1. L'agent reçoit la question
2. Identifie 2 intentions : "coûtent" (Stock) + "comment" (Technique)
3. Appelle `check_stock_and_price(["lame_terrasse_pin"])`
4. Appelle `search_technical_guide("fixation lames terrasse")`
5. Synthétise les résultats en réponse cohérente
6. Sauvegarde en `conversation_history.json`

**Aucune hallucination :** Si produit inconnu, retourne "non référencé"

---

## 👥 Auteur

**Djaksoo** - AI Factory ADEO

---

## 📄 License

MIT License
