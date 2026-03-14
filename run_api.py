"""
Lanceur de l'API ADEO DIY Assistant - Sprint 2
Usage : python run_api.py
"""
import os
import sys
from pathlib import Path

# Ajouter le repertoire courant au path Python
sys.path.insert(0, str(Path(__file__).parent))

# Verifier que .env existe avec une vraie clé API
env_file = Path(".env")
if not env_file.exists():
    print("\nERREUR : Fichier .env non trouvé")
    print("Creation d'un .env de test...\n")
    with open(".env", "w") as f:
        f.write("OPENAI_API_KEY=sk-test-xxxxx\n")
        f.write("TAVILY_API_KEY=tvly-test-xxxxx\n")
    print("ATTENTION : Veuillez editer .env avec vos vraies cles API avant de lancer l'API!")
    print()

# Charger les variables d'environnement
from dotenv import load_dotenv
load_dotenv()

# Verifier la cle API
api_key = os.getenv("OPENAI_API_KEY", "")
if api_key.startswith("sk-test") or api_key.startswith("your_"):
    print("\nATTENTION : Cle API invalide ou de test!")
    print("Veuillez configurer OPENAI_API_KEY dans .env avec votre vraie cle OpenAI")
    print("Obtenir une cle : https://platform.openai.com/account/api-keys\n")
    sys.exit(1)

# Lancer l'API
if __name__ == "__main__":
    from src.api.server import app
    import uvicorn
    
    print("\n" + "="*70)
    print("ADEO DIY Assistant API - Sprint 2")
    print("="*70)
    print("\nLancement du serveur...")
    print("Documentation Swagger : http://localhost:8000/docs")
    print("Health check : http://localhost:8000/health")
    print("\nAppuyez sur CTRL+C pour arreter le serveur\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
