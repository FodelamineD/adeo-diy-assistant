"""
Test script pour valider le fonctionnement du streaming SSE.
"""

import asyncio
import httpx
import json
import pytest
from uuid import uuid4

BASE_URL = "http://localhost:8000"
THREAD_ID = str(uuid4())


@pytest.mark.asyncio
async def test_classic_chat():
    """Test l'endpoint classique /chat"""
    print("\n" + "="*60)
    print("TEST 1: Chat Classique (/chat)")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{BASE_URL}/chat",
            json={
                "message": "Comment installer une terrasse en bois ?",
                "thread_id": THREAD_ID
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"Réponse:\n{data['response'][:200]}...")
        else:
            print(f"❌ Status: {response.status_code}")
            print(f"Error: {response.text}")


@pytest.mark.asyncio
async def test_streaming_chat():
    """Test l'endpoint de streaming /chat/stream"""
    print("\n" + "="*60)
    print("TEST 2: Chat en Streaming (/chat/stream)")
    print("="*60 + "\n")
    
    async with httpx.AsyncClient() as client:
        async with client.stream(
            "POST",
            f"{BASE_URL}/chat/stream",
            json={
                "message": "Cite les 3 outils essentiels pour une terrasse",
                "thread_id": THREAD_ID
            }
        ) as response:
            
            if response.status_code == 200:
                print(f"✅ Status: {response.status_code}")
                print(f"Content-Type: {response.headers.get('content-type')}")
                print(f"\nRéception en direct (SSE):\n")
                
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        try:
                            chunk_data = json.loads(line[6:])  # Enlever "data: "
                            chunk = chunk_data.get("chunk", "")
                            print(f"  {chunk}", end="", flush=True)
                        except json.JSONDecodeError:
                            pass
                
                print("\n\n✅ Streaming complété!")
            else:
                print(f"❌ Status: {response.status_code}")
                print(f"Error: {response.text}")


@pytest.mark.asyncio
async def test_health():
    """Test le health check"""
    print("\n" + "="*60)
    print("TEST 0: Health Check (/health)")
    print("="*60)
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/health")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Service opérationnel: {data['status']}")
            print(f"📦 Version: {data['version']}")
        else:
            print(f"❌ Service indisponible: {response.status_code}")


async def main():
    """Lance tous les tests"""
    print("\n" + "="*70)
    print("🚀 TESTS D'API - ADEO DIY ASSISTANT")
    print("="*70)
    
    try:
        # Test health d'abord
        await test_health()
        
        # Tests des endpoints
        await test_classic_chat()
        await test_streaming_chat()
        
        print("\n" + "="*70)
        print("✅ TOUS LES TESTS COMPLÉTÉS")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        print("\n💡 Conseil: Vérifiez que le serveur API est lancé sur http://localhost:8000")


if __name__ == "__main__":
    asyncio.run(main())
