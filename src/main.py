import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()
from src.agents.graph import graph

def run_test_query(query: str) -> None:
    """Lance une requête dans le graphe et affiche le flux d'exécution."""
    print(f"\n--- Question : {query} ---")
    
    # État initial
    inputs = {"messages": [("user", query)]}
    
    # Parcours du graphe
    for event in graph.stream(inputs):
        for node, value in event.items():
            print(f"\n[Nœud : {node}]")
            # Affiche le dernier message produit par le nœud
            last_msg = value["messages"][-1]
            print(f"Réponse : {last_msg.content}")

if __name__ == "__main__":
    # Test 1 : Requête combinée (Stock + Technique)
    run_test_query("Quel est le prix des plots réglables et quel est l'entraxe conseillé pour le pin ?")

   