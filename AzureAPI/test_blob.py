import pytest
import os
from azure.storage.blob import BlobServiceClient

def test_blob_connection_and_container():
    """
    Test que la connexion au Blob Storage fonctionne et que le conteneur 'models' existe,
    ainsi que les fichiers nécessaires au démarrage de l'API.
    """
    connection_string = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
    
    # Si on tourne ce test en local sans variable d'environnement, on passe le test (skip)
    if not connection_string:
        pytest.skip("La variable AZURE_STORAGE_CONNECTION_STRING est manquante. Test ignoré.")
        
    # 1. Initialisation du client
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client("models")
    except Exception as e:
        pytest.fail(f"Impossible de se connecter au Blob Storage. Vérifiez la chaîne de connexion. Erreur : {e}")
    
    # 2. Vérifier que le conteneur existe
    assert container_client.exists(), "Le conteneur 'models' n'existe pas sur le Blob Storage."
    
    # 3. Vérifier la présence de tous les fichiers critiques
    blobs = [blob.name for blob in container_client.list_blobs()]
    
    expected_files = [
        "user_histories_dict.pkl",
        "als_user_factors.npy",
        "als_item_factors.npy",
        "als_user_mapping.pkl",
        "als_item_mapping.pkl"
    ]
    
    for file in expected_files:
        assert file in blobs, f"Le fichier critique '{file}' est manquant dans le Blob Storage !"
