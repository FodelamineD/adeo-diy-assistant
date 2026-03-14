import json
import os
from typing import List, Dict, Any
from datetime import datetime

CONVERSATION_FILE = "conversation_history.json"


def load_conversation_history() -> List[tuple]:
    """
    Charge l'historique de conversation depuis le fichier JSON.
    
    Returns:
        Liste de tuples (role, content) pour reconstituer les messages.
    """
    if not os.path.exists(CONVERSATION_FILE):
        return []
    
    try:
        with open(CONVERSATION_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Reconvertir en format tuple (role, content)
            return [(msg["role"], msg["content"]) for msg in data.get("messages", [])]
    except (json.JSONDecodeError, IOError):
        print(f"⚠️ Erreur lors du chargement de {CONVERSATION_FILE}. Démarrage avec historique vide.")
        return []


def save_conversation_history(messages: List[Dict[str, Any]]) -> None:
    """
    Sauvegarde l'historique de conversation dans un fichier JSON.
    
    Args:
        messages: Liste des messages du state (objets LangChain BaseMessage)
    """
    try:
        conversation_data = {
            "timestamp": datetime.now().isoformat(),
            "messages": []
        }
        
        # Extraire le contenu des messages LangChain
        for msg in messages:
            conversation_data["messages"].append({
                "role": msg.type if hasattr(msg, 'type') else "unknown",
                "content": msg.content if hasattr(msg, 'content') else str(msg),
            })
        
        with open(CONVERSATION_FILE, "w", encoding="utf-8") as f:
            json.dump(conversation_data, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"⚠️ Impossible de sauvegarder l'historique : {e}")


def clear_conversation_history() -> None:
    """Efface l'historique de conversation."""
    if os.path.exists(CONVERSATION_FILE):
        os.remove(CONVERSATION_FILE)
        print("✓ Historique de conversation supprimé.")
