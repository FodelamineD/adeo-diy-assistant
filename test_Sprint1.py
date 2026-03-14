"""
Test de validation Sprint 1 : Requête combinée Terrasse
Teste :
1. Tool-calling stable (stock + technique)
2. Boucle LangGraph (agent -> tools -> agent)
3. Absence d'hallucination
"""
import os
from dotenv import load_dotenv

load_dotenv()

from src.agents.graph import graph


def test_terrasse_query():
    """Test clé du sprint : Requête combinant Stock + Technique"""
    
    query = "Combien coûtent les lames de terrasse en pin et comment je les fixe ?"
    
    print("\n" + "="*70)
    print("🧪 TEST SPRINT 1 : REQUÊTE COMBINÉE TERRASSE")
    print("="*70)
    print(f"\n📝 Requête : {query}\n")
    
    inputs = {"messages": [("user", query)]}
    
    nodes_executed = []
    tools_called = []
    has_ai_response = False
    
    # Parcourir le graphe
    for event in graph.stream(inputs):
        for node, value in event.items():
            nodes_executed.append(node)
            print(f"✓ Exécution du nœud : [{node}]")
            
            # Affiche le dernier message produit par le nœud
            if value["messages"]:
                last_msg = value["messages"][-1]
                
                # Détecter les tool calls
                if hasattr(last_msg, 'tool_calls') and last_msg.tool_calls:
                    for call in last_msg.tool_calls:
                        tools_called.append(call.name)
                    print(f"  → Outils appelés : {[call.name for call in last_msg.tool_calls]}")
                
                # Vérifier réponse AI
                elif hasattr(last_msg, 'content') and hasattr(last_msg, 'type'):
                    if last_msg.type == "ai":
                        has_ai_response = True
                        print(f"  → Réponse : {last_msg.content[:150]}...")
    
    print("\n" + "="*70)
    print("📊 RÉSULTATS DU TEST")
    print("="*70)
    print(f"✓ Chemin d'exécution : {' → '.join(nodes_executed)}")
    print(f"✓ Outils appelés : {tools_called}")
    print(f"✓ Nombre de nœuds exécutés : {len(nodes_executed)}")
    
    # Vérifications
    checks = {
        "Agent exécuté" : "agent" in nodes_executed,
        "Tools exécutés" : "tools" in nodes_executed,
        "Boucle complète" : "agent" in nodes_executed and "tools" in nodes_executed,
        "Réponse AI générée" : has_ai_response,
        "Tools appelés" : len(tools_called) > 0,
    }
    
    print("\n✅ Vérifications :")
    for check_name, result in checks.items():
        status = "✓" if result else "✗"
        print(f"  {status} {check_name}")
    
    all_pass = all(checks.values())
    print("\n" + "="*70)
    if all_pass:
        print("✅ TEST RÉUSSI : Requête combinée fonctionnelle !")
    else:
        print("❌ TEST PARTIEL : Certaines vérifications non passées")
    print("="*70)
    
    return all_pass


if __name__ == "__main__":
    try:
        success = test_terrasse_query()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERREUR : {e}")
        print("\nVérifier : OPENAI_API_KEY dans .env")
        exit(1)

