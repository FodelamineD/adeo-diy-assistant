# CORRECTIONS EFFECTUÉES - API Sprint 2

## Erreurs Corrigées

### 1. **Erreur pip install -r requirements.txt**
**Problème :** ZenML causait des problèmes de dépendances incompatibles  
**Solution :** Commenté ZenML (reporter à Sprint 3)  
**Fichier modifié :** `requirements.txt`

**Avant :**
```
...
zenml  # Cause des erreurs de compilation
```

**Après :**
```
...
# zenml  # (Sprint 3)
```

### 2. **Erreur d'importation dans server.py**
**Problème :** `from src.agents.graph import app as langgraph_agent`  
Solution :** Le graphe LangGraph s'appelle `graph`, pas `app`  
**Fichier modifié :** `src/api/server.py`

**Avant :**
```python
from src.agents.graph import app as langgraph_agent  # ❌ 'app' n'existe pas
```

**Après :**
```python
from src.agents.graph import graph  # ✅ Correct
```

### 3. **Erreur de syntaxe dans server.py**
**Problème :** Indentation incorrecte des classes Pydantic  
**Solution :** Réorganisé le code avec bon formatage  
**Fichier modifié :** `src/api/server.py`

**Avant :**
```python
class ChatResponse(BaseModel):
    response: str = ...
    # ❌ Commentaire mal indenté à l'intérieur de la classe
```

**Après :**
```python
class ChatResponse(BaseModel):
    response: str = ...

# ✅ Code bien organisé
```

### 4. **Erreur de méthode API (ainvoke vs invoke)**
**Problème :** `await langgraph_agent.ainvoke()` n'existe pas sur graphe compilé  
**Solution :** Utiliser `graph.invoke()` au lieu  
**Fichier modifié :** `src/api/server.py`

**Avant :**
```python
result = await langgraph_agent.ainvoke(inputs, config=config)  # ❌ ainvoke n'existe pas
```

**Après :**
```python
result = graph.invoke(inputs, config=config)  # ✅ Correct
```

### 5. **Module src non reconnu**
**Problème :** Pas de `src/__init__.py` et `src/api/__init__.py`  
**Solution :** Créé les fichiers __init__.py manquants  
**Fichiers créés :**
- `src/__init__.py`
- `src/api/__init__.py`

### 6. **Problème d'encodage UTF-8**
**Problème :** Accents français causaient UnicodeDecodeError en Windows  
**Solution :** Enlevé tous les accents spéciaux du code  
**Fichier modifié :** `src/api/server.py`

---

## Fichiers Créés/Modifiés

| Fichier | Action | Description |
|---------|--------|-------------|
| `requirements.txt` | ✏️ Modifié | Commenté ZenML |
| `src/api/server.py` | ✏️ Refondu | Corrections syntaxe + imports |
| `src/__init__.py` | 🆕 Créé | Module Python |
| `src/api/__init__.py` | 🆕 Créé | Module Python |
| `run_api.py` | 🆕 Créé | Lanceur API simple |

---

## Comment Tester la Correction

### 1. Vérifier les dépendances
```bash
pip install -r requirements.txt
# ✅ Doit fonctionner sans erreur
```

### 2. Vérifier la syntaxe API
```bash
python -c "from src.api.server import app; print('OK')"
# ❌ Erreur attendue : "The api_key client option must be set..."
# C'est normal - cela signifie la syntaxe est correcte
```

### 3. Lancer l'API (avec vraie clé OpenAI)
```bash
# 1. Ajouter OPENAI_API_KEY dans .env
# 2. Lancer
python run_api.py

# Puis tester dans un autre terminal :
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Combien coûte une lame de terrasse?"}'
```

---

## Fichiers de Configuration

### .env (À compléter)
```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx  # Votre vraie clé OpenAI
TAVILY_API_KEY=tvly-xxxxxxxxxxxxx     # Optionnel
```

### requirements.txt (Optimisé)
```
langgraph
langchain-openai
... (packages critiques)
fastapi
uvicorn
# zenml  # À décommenter pour Sprint 3
```

---

## Checklist de Validation

- [x] requirements.txt corrigé
- [x] server.py refondu (syntaxe OK)
- [x] Imports corrigés (graph vs app)
- [x] Méthode invoke() utilisée (pas ainvoke)
- [x] Modules __init__.py créés
- [x] Accents supprimés (UTF-8 OK)
- [x] Lanceur run_api.py créé
- [x] Documentation des corrections créée

---

## Prochaines Étapes

1. ✅ Corriger les erreurs → **FAIT**
2. ⏳ Configurer .env avec OPENAI_API_KEY valide
3. ⏳ Lancer : `python run_api.py`
4. ⏳ Tester l'endpoint /chat
5. ⏳ Avancer vers Sprint 2 complet

---

**Status :** ✅ Erreurs corrigées, API prête à tester
