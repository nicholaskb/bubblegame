import os
from kaggle.api.kaggle_api_extended import KaggleApi
import zipfile

# Initialize Kaggle API
api = KaggleApi()
api.authenticate()

# Define dataset and destination
dataset_owner_slug = "kvpratama/pokemon-images-dataset"
download_path = "./pokemon_dataset"
os.makedirs(download_path, exist_ok=True)

# Download dataset
print("Downloading Pokémon dataset...")
api.dataset_download_files(dataset_owner_slug, path=download_path, unzip=False)

# Path to the zip file
zip_path = os.path.join(download_path, "pokemon-images-dataset.zip")

# Extract contents
print("Extracting Pokémon dataset...")
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(download_path)

print("✅ Pokémon dataset downloaded and extracted successfully.")
