from typing import Dict, Union, List
from langchain_core.tools import tool

# Base de données simulée (Référentiel ADEO)
CATALOG = {
    "lame_terrasse_pin": {"prix_unit": 12.50, "unite": "m2", "stock": 450},
    "lame_terrasse_composite": {"prix_unit": 45.00, "unite": "m2", "stock": 120},
    "lambourde_alu": {"prix_unit": 18.20, "unite": "unite", "stock": 85},
    "vis_inox_a2": {"prix_unit": 25.00, "unite": "boite_200", "stock": 50},
    "plot_reglable": {"prix_unit": 2.10, "unite": "unite", "stock": 300},
}

@tool
def check_stock_and_price(items: List[str]) -> Dict[str, Union[Dict, str]]:
    """
    Consulte le prix et la disponibilité pour une liste de produits de terrasse.
    
    Args:
        items: Liste des noms de produits (ex: ['lame_terrasse_pin', 'vis_inox_a2'])
        
    Returns:
        Un dictionnaire contenant les détails de prix et de stock ou un message d'erreur.
    """
    results = {}
    for item in items:
        if item in CATALOG:
            results[item] = CATALOG[item]
        else:
            results[item] = "Produit non référencé dans le catalogue DIY."
    return results