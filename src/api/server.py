# ============================================================================
# ADEO DIY ASSISTANT - FastAPI Server avec Streaming en Temps Réel
# ============================================================================

# --- IMPORTS BASIQUES ---
import os
import json
import time
from typing import Optional
from uuid import uuid4

# --- LOAD ENVIRONMENT VARIABLES (MUST BE FIRST) ---
from dotenv import load_dotenv
load_dotenv()

# --- IMPORTS FASTAPI & PYDANTIC ---
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

# --- IMPORT DU GRAPH LANGGRAPH ---
from src.agents.graph import graph

# ============================================================================
# MODELES DE DONNEES (Pydantic)
# ============================================================================

class ChatRequest(BaseModel):
    """Requete du client."""
    message: str = Field(..., description="Question du client")
    thread_id: str = Field(default_factory=lambda: str(uuid4()), description="ID de conversation")


class ChatResponse(BaseModel):
    """Reponse de l'assistant."""
    response: str = Field(..., description="Reponse de l'expert LangGraph")


# ============================================================================
# GENERATEUR POUR STREAMING (Le passe-plat mot à mot)
# ============================================================================

async def response_generator(request: ChatRequest):
    """
    Cette fonction fait le lien en direct avec l'expert.
    Elle attrape chaque mot (token) et l'envoie immédiatement au client.
    
    L'analogie : Au lieu de préparer un plateau-repas complet en cuisine
    pour l'apporter à la fin, on ouvre un passe-plat où chaque fritte
    est donnée au client dès qu'elle sort de la friteuse.
    """
    inputs = {"messages": [("user", request.message)]}
    config = {"configurable": {"thread_id": request.thread_id}}

    # On utilise 'astream' pour écouter l'expert en temps réel
    # stream_mode="messages" nous donne chaque message de l'expert au fur et à mesure
    async for event in graph.astream(inputs, config=config, stream_mode="messages"):
        # L'événement est un tuple (idx, message)
        # On récupère le contenu du message (le texte généré)
        message = event[0]
        chunk = message.content
        
        if chunk:
            # On envoie le morceau de texte au client en format SSE (Server-Sent Events)
            # Format: "data: <json>\n\n" est le standard pour le streaming HTTP
            yield f"data: {json.dumps({'chunk': chunk})}\n\n"


app = FastAPI(
    title="ADEO DIY Assistant API",
    description="Service API pour l'agent expert DIY avec streaming en temps réel",
    version="1.0.0",
    docs_url="/docs"
)


# ============================================================================
# MIDDLEWARE DE MONITORING
# ============================================================================

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Mesure le temps de traitement de chaque requête."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    print(f"[{request.method} {request.url.path}] ⏱️ Traité en {process_time:.4f}s")
    return response


# ============================================================================
# ROUTES API
# ============================================================================

@app.get("/", tags=["Root"])
async def root():
    """Route d'accueil - affiche les endpoints disponibles."""
    return {
        "message": "Bienvenue sur ADEO DIY Assistant API",
        "docs": "http://localhost:8000/docs",
        "health": "http://localhost:8000/health",
        "routes": {
            "GET /": "Cette page",
            "GET /health": "Vérifier le statut du service",
            "POST /chat": "Chat classique (réponse complète au final)",
            "POST /chat/stream": "Chat en streaming (réponse mot par mot)"
        }
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Vérifie que le service est opérationnel."""
    return {"status": "OK", "version": "1.0.0"}


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint classique : reçoit une question et retourne la réponse complète.
    
    Analogie : Le client commande un repas en cuisine, et reçoit le 
    plateau-repas complet une fois qu'il est prêt.
    """
    try:
        # Préparer l'entrée pour le graphe
        inputs = {"messages": [("user", request.message)]}
        config = {"configurable": {"thread_id": request.thread_id}}

        # Appeler le graphe LangGraph compilé (invocation synchrone)
        # graph.invoke() attend une réponse complète
        result = graph.invoke(inputs, config=config)

        # Récupérer la dernière réponse du dialogue
        final_answer = result["messages"][-1].content

        return ChatResponse(response=final_answer)

    except Exception as e:
        error_msg = f"Erreur lors du traitement : {str(e)}"
        print(f"❌ ERREUR : {error_msg}")
        return ChatResponse(
            response="L'expert DIY rencontre un problème. Veuillez réessayer."
        )


@app.post("/chat/stream", tags=["Chat Streaming"])
async def chat_stream_endpoint(request: ChatRequest):
    """
    Endpoint de streaming : reçoit une question et retourne les tokens un par un.
    
    Analogie : Le client reste branché au passe-plat et reçoit chaque fritte
    dès qu'elle sort de la friteuse, au fur et à mesure.
    
    Format de réponse : Server-Sent Events (SSE)
    - Content-Type: text/event-stream
    - Format: "data: {\"chunk\": \"texte\"}\n\n"
    
    Avantages :
    - Réponse immédiate: l'utilisateur voit les premiers mots avant la fin
    - Meilleure UX: sensation de fluidité plutôt que d'attente
    - Économie de mémoire: pas de stockage du message complet avant envoi
    """
    return StreamingResponse(
        response_generator(request),
        media_type="text/event-stream"
    )


# ============================================================================
# POINT D'ENTREE
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("🚀 Lancement de l'API ADEO DIY Assistant")
    print("="*60)
    print("📚 Documentation Swagger : http://localhost:8000/docs")
    print("🔍 Santé du service : http://localhost:8000/health")
    print("="*60 + "\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )