import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env AVANT tout import
load_dotenv()

from typing import Optional
from uuid import uuid4
from pydantic import BaseModel, Field
from fastapi import FastAPI, Request
import time

# Import de l'agent compile au Sprint 1
from src.agents.graph import graph

# --- MODELES DE DONNEES ---

class ChatRequest(BaseModel):
    """Requete du client."""
    message: str = Field(..., description="Question du client")
    thread_id: str = Field(default_factory=lambda: str(uuid4()), description="ID de conversation")


class ChatResponse(BaseModel):
    """Reponse de l'assistant."""
    response: str = Field(..., description="Reponse de l'expert LangGraph")


# --- INITIALISATION DE L'APPLICATION ---

app = FastAPI(
    title="ADEO DIY Assistant API",
    description="Service API pour l'agent expert DIY",
    version="1.0.0",
    docs_url="/docs"
)


# --- MIDDLEWARE DE MONITORING ---

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Mesure le temps de traitement."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    print(f"Requete traitee en : {process_time:.4f} secondes")
    return response


# --- ROUTES API ---

@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat_endpoint(request: ChatRequest):
    """Endpoint principal : reçoit une question et retourne la reponse."""
    try:
        # Preparer l'entree pour le graphe
        inputs = {"messages": [("user", request.message)]}
        config = {"configurable": {"thread_id": request.thread_id}}

        # Appeler le graphe LangGraph compile
        result = graph.invoke(inputs, config=config)

        # Recuperer la derniere reponse
        final_answer = result["messages"][-1].content

        return ChatResponse(response=final_answer)

    except Exception as e:
        error_msg = f"Erreur : {str(e)}"
        print(f"ERREUR : {error_msg}")
        return ChatResponse(response="L'expert DIY rencontre un probleme. Veuillez reessayer.")


@app.get("/health", tags=["Sante"])
async def health_check():
    """Verifie que le service est operationnel."""
    return {"status": "OK", "version": "1.0.0"}


@app.get("/", tags=["Root"])
async def root():
    """Route d'accueil."""
    return {
        "message": "Bienvenue sur ADEO DIY Assistant API",
        "docs": "http://localhost:8000/docs",
        "health": "http://localhost:8000/health"
    }


# --- DEMARRAGE ---

if __name__ == "__main__":
    import uvicorn
    print("\nLancement de l'API ADEO DIY Assistant...")
    print("Documentation Swagger : http://localhost:8000/docs")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )