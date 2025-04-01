from transformers import MarianMTModel, MarianTokenizer
import os
import time
from tqdm import tqdm

def translate_text(text, src="fr", tgt="en"):
    """
    Effectue la traduction d'un texte avec MarianMT.
    """
    try:
        model_name = f"Helsinki-NLP/opus-mt-{src}-{tgt}"
        model = MarianMTModel.from_pretrained(model_name)
        tokenizer = MarianTokenizer.from_pretrained(model_name)

        tokens = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        translated = model.generate(**tokens)
        return tokenizer.decode(translated[0], skip_special_tokens=True)
    except Exception as e:
        print(f"Erreur lors de la traduction : {e}")
        return text  # Retourne le texte original en cas d'échec

def process_line(line, src="fr", tgt="en"):
    """
    Traduit uniquement les parties traduisibles d'une ligne contenant du Markdown.
    """
    if line.startswith('#') or line.startswith('```') or ('[' in line and '](' in line):
        # Retourner la ligne telle quelle si elle contient uniquement du Markdown
        return line
    else:
        # Traduire uniquement le texte brut
        return translate_text(line.strip(), src, tgt)

def translate_markdown_file(input_file, src="fr", tgt="en"):
    """
    Traduit un fichier Markdown ligne par ligne sans altérer le format Markdown.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        output_path = f"{os.path.splitext(input_file)[0]}_en_aiGenerated.md"
        with open(output_path, 'w', encoding='utf-8') as file:
            total_lines = len(lines)
            translated_count = 0

            for line in tqdm(lines, desc="Traduction", ncols=80, ascii=True):
                translated_line = process_line(line, src, tgt)
                file.write(translated_line + '\n')
                if translated_line != line:  # Vérifie si la ligne a été traduite
                    translated_count += 1

            print(f"Traduction sauvegardée dans : {output_path}")
            print(f"Résumé : {translated_count}/{total_lines} lignes traduites.")
    except FileNotFoundError:
        print(f"Erreur : Le fichier {input_file} n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur imprévue s'est produite : {e}")

if __name__ == "__main__":
    start_time = time.time()
    input_file = "cv_fr.md"  # Fichier Markdown à traduire
    source_lang = "fr"
    target_lang = "en"
    translate_markdown_file(input_file, src=source_lang, tgt=target_lang)
    print(f"Temps d'exécution : {time.time() - start_time:.2f} secondes")
