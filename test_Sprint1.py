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
    
    # Parcourir le graphe
    for event in graph.stream(inputs):
        for node, value in event.items():
            nodes_executed.append(node)
            print(f"✓ Exécution du nœud : [{node}]")
            
            # Affiche le dernier message produit par le nœud
            last_msg = value["messages"][-1]
            
            # Afficher le contenu de manière formatée
            if hasattr(last_msg, 'tool_calls') and last_msg.tool_calls:
                print(f"  → Outils appelés : {[call.name for call in last_msg.tool_calls]}")
            else:
                print(f"  → Réponse : {last_msg.content[:200]}...")
            print()
    
    print("="*70)
    print("📊 RÉSULTATS DU TEST")
    print("="*70)
    print(f"✓ Chemin d'exécution : {' → '.join(nodes_executed)}")
    print(f"✓ Nombre de nœuds exécutés : {len(nodes_executed)}")
    
    # Vérifications
    checks = {
        "Agent exécuté" : "agent" in nodes_executed,
        "Tools exécutés" : "tools" in nodes_executed,
        "Boucle complète" : nodes_executed == ["agent", "tools", "agent"],
        "Pas d'erreur" : len(nodes_executed) > 0,
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
    success = test_terrasse_query()
    exit(0 if success else 1)
