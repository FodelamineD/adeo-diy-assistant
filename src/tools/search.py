from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.tools import tool

def _initialize_vector_store():
    """Initialise la base de données vectorielle à partir du fichier texte."""
    path = "data/guide_terrasse.txt"
    
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # Découpage en fragments pour garder le contexte
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.create_documents([text])

    # Création du store (en mémoire pour ce sprint)
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore.as_retriever()

# Initialisation du moteur de recherche
retriever = _initialize_vector_store()

@tool
def search_technical_guide(query: str) -> str:
    """
    Recherche des conseils techniques dans le guide de construction (normes, entraxes, méthodes).
    Utile quand l'utilisateur pose une question sur 'comment' construire.
    """
    docs = retriever.invoke(query)
    
    # Gestion du cas où aucun document n'est trouvé
    if not docs:
        return "Aucune information technique trouvée pour cette requête dans le guide. Veuillez reformuler votre question."
    
    # On concatène les résultats pour le cerveau (Brain)
    return "\n\n".join([doc.page_content for doc in docs])