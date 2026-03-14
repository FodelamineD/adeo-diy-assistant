# ADEO DIY Assistant - Wood Deck Planner 🛠️

> **De l'expérimentation à l'industrialisation.**
> [cite_start]Projet de démonstration conçu pour la Squad AI Factory d'ADEO, illustrant la transformation de concepts académiques en solutions robustes et industrialisées. [cite: 6]

---

## 🎯 Vision Métier
Le **DIY Assistant** est un agent intelligent qui accompagne les clients dans la planification de projets complexes (ex: terrasse en bois). Il ne se contente pas de répondre à des questions ; il **raisonne** en croisant des sources techniques (RAG) et des données opérationnelles (Stocks/Prix) pour garantir la faisabilité du projet.

### Pourquoi ce projet ?
* **Alignement Retail :** Répond à un besoin critique de conseil expert à l'échelle.
* **Architecture Agnostique :** La matrice technique est convertible pour n'importe quel rayon d'ADEO (Cuisine, Énergie, Sanitaire).

---

## 🛠️ ML Toolbox (Stack Technique)
Priorisation de la **densité de signal** et réduction du bruit informationnel pour une efficacité maximale. [cite: 2025-12-18]

* **Agentic Framework :** `LangGraph` (StateGraph) pour une orchestration déterministe.
* **MLOps :** `ZenML` pour la gestion des pipelines et le versioning des artefacts.
* **Serving :** `FastAPI` (API asynchrone haute performance).
* **Infrastructure :** `Docker` (Conteneurisation) et `Terraform` (Infrastructure as Code).
* **Intelligence :** `OpenAI` via des stratégies de **Tool-Calling** avancées.

---

## 🏗️ Architecture du Projet
Organisation modulaire alignée sur les standards de production :

```text
adeo-diy-assistant/
├── data/               # Sources de connaissances (Guides de pose)
├── src/                # Cœur industriel
│   ├── agents/         # Logique du graphe de décision (LangGraph)
│   ├── tools/          # Outils métiers (Stock, Calculateurs, RAG)
│   └── main.py         # Point d'entrée pour les tests
├── infra/              # Provisionnement (Terraform, Docker)
└── pipelines/          # Pipelines d'orchestration (ZenML)
```
##  🚀 Installation & Lancement (Sprint 1)
1) Setup :
 ```text
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
 ```
2) Configuration :
 ```text
Ajouter votre OPENAI_API_KEY dans un fichier .env.
 ```
3) Exécution :
 ```text
python src/main.py
 ```

📈 Roadmap & Méthodologie

Développement piloté par la méthodologie Agile/BMAD avec validation par étapes.

[x] Sprint 1 (The Brain) : Moteur de raisonnement et Tool-Calling.

[ ] Sprint 2 (The Factory) : Pipeline ZenML et API de production FastAPI.

[ ] Sprint 3 (The Ship) : Conteneurisation et déploiement via Terraform.
