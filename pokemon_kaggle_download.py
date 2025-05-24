import os
from kaggle.api.kaggle_api_extended import KaggleApi
import zipfile
import glob

# Initialize Kaggle API
api = KaggleApi()
api.authenticate()

# Define dataset and destination
dataset_owner_slug = "kvpratama/pokemon-images-dataset"
# Use environment variable for download path, default to /app/pokemon_dataset
download_path = os.getenv('POKEMON_DATASET_PATH', '/app/pokemon_dataset')
os.makedirs(download_path, exist_ok=True)

# Check if images already exist in pokemon subdirectory
pokemon_dir = os.path.join(download_path, "pokemon")
if os.path.exists(pokemon_dir):
    existing_images = glob.glob(os.path.join(pokemon_dir, "*.png"))
    if existing_images:
        print(f"Found {len(existing_images)} existing Pokémon images in {pokemon_dir}")
        print("Skipping download as images are already present.")
        exit(0)

# Download dataset
print(f"Downloading Pokémon dataset to {download_path}...")
api.dataset_download_files(dataset_owner_slug, path=download_path, unzip=False)

# Path to the zip file
zip_path = os.path.join(download_path, "pokemon-images-dataset.zip")

# Extract contents
print("Extracting Pokémon dataset...")
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(download_path)

# Clean up the zip file
os.remove(zip_path)

print(f"✅ Pokémon dataset downloaded and extracted successfully to {download_path}.")
