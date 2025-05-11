# Initialise le pipeline Hugging Face de traduction (fr → en)
# Utilise le GPU si disponible (torch.device) et affiche les logs

from transformers import pipeline
import torch
import time
from progress_tracker import PhaseProgress

# Initialisation visuelle de la phase de chargement
tracker = PhaseProgress()
tracker.start()

tracker.add_phase("📦 Chargement du modèle", total=1)
start_time = time.time()

# Sélection du device (GPU si dispo)
device = 0 if torch.cuda.is_available() else -1

# Chargement du modèle Hugging Face
translator_pipeline = pipeline("translation", model="Helsinki-NLP/opus-mt-fr-en", device=device)

tracker.advance("📦 Chargement du modèle")
tracker.log(f"✅ Modèle chargé en {time.time() - start_time:.2f}s (device : {'GPU' if device == 0 else 'CPU'})")
tracker.stop()

# Fonction unique exposée : traduction d'une ligne
def translate_text(text):
    result = translator_pipeline(text, max_length=512)
    return result[0]["translation_text"] + "\n"
