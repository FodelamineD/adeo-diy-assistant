# 🌊 STREAMING API - Résumé des Changements

## 📍 Vue d'ensemble

Le serveur API passe de **réponses complètes** à **réponses en streaming en temps réel**.

### L'Analogie 

**Avant (classique)** 🍽️
```
Client → API → Attendre la fin → Réponse complète
         ├─ Cuire
         ├─ Assaisonner  
         ├─ Dresser      
         └─ Servir ensemble
```

**Après (streaming)** 🌊
```
Client → API → Réception immédiate de chaque token
         ├─ Token 1: "Pour"
         ├─ Token 2: "installer"
         ├─ Token 3: "une"
         └─ Etc.
```

---

## 🔧 Changements Apportés

### 1. **Structure du Fichier `src/api/server.py`**

#### Avant ❌
```python
# MAUVAIS ORDRE
async def response_generator(request: ChatRequest):  # ❌ ChatRequest pas défini
    async for event in langgraph_agent.astream():    # ❌ langgraph_agent n'existe pas

load_dotenv()  # ❌ Trop tard

class ChatRequest(...):  # ❌ Défini après utilisation

# Routes dans if __name__:  # ❌ Mauvaise indentation
```

#### Après ✅
```python
# BON ORDRE
load_dotenv()  # ✅ D'abord

class ChatRequest(...):  # ✅ Avant utilisation

async def response_generator(request: ChatRequest):  # ✅ Correct
    async for event in graph.astream():             # ✅ graph existe

# Routes au niveau racine  # ✅ Bonne indentation
```

---

## 🛣️ Les 3 Endpoints

### 1️⃣ **GET /** - Route d'accueil
```bash
curl http://localhost:8000/
```
```json
{
  "message": "Bienvenue sur ADEO DIY Assistant API",
  "routes": {
    "GET /": "Cette page",
    "GET /health": "Vérifier le statut",
    "POST /chat": "Chat classique",
    "POST /chat/stream": "Chat en streaming"
  }
}
```

---

### 2️⃣ **POST /chat** - Chat Classique
**Analogie**: Le client reçoit tout d'un coup, comme un plateau-repas complet.

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Comment installer une terrasse ?",
    "thread_id": "my-session-123"
  }'
```

**Réponse** (200 OK):
```json
{
  "response": "Pour installer une terrasse en bois, il faut [...réponse complète...]"
}
```

---

### 3️⃣ **POST /chat/stream** - Chat en Streaming
**Analogie**: Le client reçoit chaque token dès qu'il sort, comme une friteuse qui envoie les frites une à une.

```bash
curl -X POST http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Comment installer une terrasse ?",
    "thread_id": "my-session-123"
  }'
```

**Réponse** (200 OK + `text/event-stream`):
```
data: {"chunk": "Pour"}
data: {"chunk": " installer"}
data: {"chunk": " une"}
data: {"chunk": " terrasse"}
...
```

---

## 🚀 Comment Tester

### Prérequis
```bash
# Terminal 1: Lancer le serveur
python -m uvicorn src.api.server:app --reload
```

### Test 1: Health Check
```bash
curl http://localhost:8000/health
# ✅ {"status": "OK", "version": "1.0.0"}
```

### Test 2: Chat Classique
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Cite 2 outils pour bricoler",
    "thread_id": "test-1"
  }'
```

### Test 3: Chat Streaming
```bash
curl -X POST http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Cite 2 outils pour bricoler",
    "thread_id": "test-1"
  }'
```

### Test 4: Test Automatisé (Python)
```bash
# Terminal 2: Installer httpx
pip install httpx

# Lancer les tests
python test_streaming.py
```

---

## 🔍 Code Clé

### Le Générateur (Passe-plat)
```python
async def response_generator(request: ChatRequest):
    inputs = {"messages": [("user", request.message)]}
    config = {"configurable": {"thread_id": request.thread_id}}

    # Écouter l'expert en temps réel
    async for event in graph.astream(inputs, config=config, stream_mode="messages"):
        message = event[0]
        chunk = message.content
        
        if chunk:
            # Envoyer le morceau au client en SSE
            yield f"data: {json.dumps({'chunk': chunk})}\n\n"
```

### L'Endpoint Streaming
```python
@app.post("/chat/stream", tags=["Chat Streaming"])
async def chat_stream_endpoint(request: ChatRequest):
    return StreamingResponse(
        response_generator(request),
        media_type="text/event-stream"  # Format standard pour le Direct
    )
```

---

## 📊 Comparaison

| Aspect | `/chat` | `/chat/stream` |
|--------|---------|----------------|
| Temps jusqu'à réponse | Attente complète | Immédiat |
| UX | État de charge ? | Progression visible |
| Mémoire | Tout en RAM | Token par token |
| Latence perçue | Longue | Courte |
| Complexité client | Simple | Parsing SSE |

---

## 🎯 Prochaines Étapes

1. ✅ **Streaming basique** (DONE)
2. ⏳ **Ajouter pagination** pour histoire longue
3. ⏳ **Client web** avec réception SSE
4. ⏳ **Load testing** (50+ req/s)
5. ⏳ **Monitoring** avec Weights & Biases

---

## 💡 Notes Techniques

- **SSE (Server-Sent Events)** = Format texte standardisé pour streaming HTTP
- **Format**: `data: <json>\n\n` (deux newlines importantes!)
- **Async/Await**: FastAPI supporte les async generators
- **graph.astream()**: LangGraph natif, pas besoin de `langgraph_agent`

