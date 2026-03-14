import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()
from src.agents.graph import graph
from src.persistence import load_conversation_history, save_conversation_history

def run_test_query(query: str, messages_history: list = None) -> tuple:
    """
    Lance une requête dans le graphe et affiche le flux d'exécution.
    
    Args:
        query: La question de l'utilisateur
        messages_history: L'historique des messages précédents
        
    Returns:
        Tuple (messages_updated, last_response)
    """
    print(f"\n--- Question : {query} ---")
    
    # Initialiser avec l'historique ou commencer frais
    if messages_history:
        messages = messages_history
    else:
        messages = []
    
    # Ajouter la nouvelle question
    messages.append(("user", query))
    
    # État initial avec historique
    inputs = {"messages": messages}
    
    last_response = None
    # Parcours du graphe
    for event in graph.stream(inputs):
        for node, value in event.items():
            print(f"\n[Nœud : {node}]")
            # Affiche le dernier message produit par le nœud
            last_msg = value["messages"][-1]
            last_response = last_msg.content
            print(f"Réponse : {last_response}")
            # Mettre à jour l'historique global
            messages = value["messages"]
    
    return messages, last_response


def interactive_mode():
    """Mode interactif pour discuter continuellement avec l'agent."""
    print("\n🤖 ADEO DIY Assistant - Mode Interactif")
    print("=" * 50)
    print("Tapez 'quitter' pour arrêter | 'reset' pour effacer l'historique")
    print("=" * 50)
    
    # Charger l'historique existant
    messages = load_conversation_history()
    if messages:
        print(f"\n✓ Historique chargé ({len(messages)} messages précédents)")
    
    while True:
        try:
            query = input("\n👤 Vous : ").strip()
            
            # Commandes spéciales
            if query.lower() == "quitter":
                print("✓ Historique sauvegardé. À bientôt!")
                break
            elif query.lower() == "reset":
                from src.persistence import clear_conversation_history
                clear_conversation_history()
                messages = []
                print("✓ Historique effacé. Nouvelle conversation.")
                continue
            elif not query:
                continue
            
            # Exécuter la requête
            messages, response = run_test_query(query, messages)
            
            # Sauvegarder l'historique après chaque requête
            save_conversation_history(messages)
            
        except KeyboardInterrupt:
            print("\n\n✓ Interruption de l'utilisateur. Historique sauvegardé.")
            save_conversation_history(messages)
            break
        except Exception as e:
            print(f"\n❌ Erreur : {e}")
            continue


if __name__ == "__main__":
    # Mode interactif
    interactive_mode()