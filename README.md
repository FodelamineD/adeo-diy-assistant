# 🛠️ ADEO DIY Assistant 

> **Note** Ce projet n'est pas une solution commerciale finale, mais un **laboratoire d'apprentissage**. L'objectif central était de maîtriser le cycle de vie complet du MLOps en intégrant des briques technologiques complexes dans une architecture industrialisée.

---

## 🎯 Vision du Projet
L'objectif est de démontrer ma capacité à assembler des composants de pointe pour répondre à un besoin métier concret (planification de terrasse DIY). Le focus est mis sur la **structure**, la **modularité** et la **densité de signal technique** plutôt que sur la simple génération de texte.

---

## 🏗️ L'Architecture "Factory" (Les Briques)
Chaque pièce du puzzle a été choisie pour simuler l'environnement de l'**AI Factory d'ADEO** :

* **Raisonnement (Le Chef) :** `LangGraph` pour créer un agent capable de prendre des décisions logiques et déterministes.
* **Données (La Recette) :** `RAG` (Retrieval Augmented Generation) avec FAISS pour ancrer les réponses dans des guides techniques réels et éviter les hallucinations.
* **Serving (Le Guichet) :** `FastAPI` avec support SSE (Streaming) pour transformer l'IA en un service web asynchrone.
* **Standardisation (Le Container) :** `Docker` (Multi-stage build) pour garantir un environnement de production reproductible.
* **Infrastructure (Le Plan) :** `Terraform` pour définir les ressources Cloud (AWS/GCP) via le code (IaC).
* **Orchestration (La Chaîne) :** `ZenML` pour automatiser les pipelines de données et garantir la traçabilité.

---

## 🚦 Diagnostic Technique : Le Challenge du "Timeout"

Dans la version actuelle, une latence supérieure à 30 secondes a été identifiée lors de certaines requêtes complexes (voir illustration ci-dessous). 

> **Diagnostic :**
> Ce délai n'est pas une erreur de code, mais un défi classique de production ML lié à la profondeur du graphe de décision. L'agent doit effectuer plusieurs cycles de "Réflexion -> Recherche RAG -> Validation", ce qui impacte le temps de réponse total.

### **Pistes de résolution (Optimisation)**

* **Streaming SSE :** Déjà initié pour améliorer l'expérience utilisateur en affichant les tokens en temps réel.
* **Asynchronisme :** Implémentation de workers (Celery/Redis) pour les calculs de stock les plus lourds.
* **Optimisation du RAG :** Passage à une recherche vectorielle hybride pour réduire le temps d'extraction.

---

## 🚀 Ce que ce projet prouve
* **Capacité d'intégration :** Faire communiquer une UI Streamlit, une API FastAPI et un agent LangGraph de manière fluide.
* **Posture MLOps :** Prioriser la robustesse (CI/CD via GitHub Actions, Docker) sur la simple performance brute du modèle.
* **Sécurité & Hygiène :** Gestion stricte des secrets (clés API) via des fichiers `.env` et `.gitignore` pour protéger les assets de l'entreprise.

---

**Lamine Diakhaby** *Focus sur l'industrialisation et la fiabilité des systèmes.* *Recherche d'alternance ML Engineer - Septembre 2026*
