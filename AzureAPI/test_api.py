import pytest
import requests
import os

# On peut définir l'URL en variable d'environnement pour tester en local (http://localhost:7071/api/recommend)
# Si elle n'est pas définie, on teste directement l'API en production sur Azure.
API_URL = os.environ.get("API_TEST_URL", "https://globonews-api-p10-evg7eza5gqfnendh.francecentral-01.azurewebsites.net/api/recommend")

def test_api_status_code():
    """Vérifie que l'API répond bien avec un statut 200 OK pour un utilisateur valide."""
    response = requests.get(f"{API_URL}?user_id=42")
    assert response.status_code == 200, f"L'API a retourné une erreur {response.status_code}"

def test_api_response_format():
    """Vérifie que le format JSON retourné contient bien les bons champs et 5 recommandations."""
    response = requests.get(f"{API_URL}?user_id=42")
    data = response.json()
    
    assert "user_id" in data
    assert "status" in data
    assert "history_length" in data
    assert "recommendations" in data
    assert len(data["recommendations"]) == 5
    
    # Vérifie que la première recommandation contient bien un article_id et un score
    first_rec = data["recommendations"][0]
    assert "article_id" in first_rec
    assert "score" in first_rec

def test_api_cold_start():
    """Vérifie le comportement de l'API face à un utilisateur inconnu (Cold Start)."""
    response = requests.get(f"{API_URL}?user_id=99999999") # ID qui n'existe pas
    data = response.json()
    
    assert response.status_code == 200
    assert data["status"] in ["new_user", "cold_start"]
    assert len(data["recommendations"]) == 5 # Le Fallback de popularité doit renvoyer 5 articles

def test_api_missing_user_id():
    """Vérifie que l'API gère correctement l'absence de paramètre user_id."""
    response = requests.get(API_URL) # Requête sans "?user_id=..."
    assert response.status_code == 400
    assert "error" in response.json()
