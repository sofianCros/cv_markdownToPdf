# Traduction d'un fichier Markdown ligne par ligne avec conservation du format
# Entrée : cv_fr.md / Sortie : cv_en.md (PDF généré ensuite en cv_en_aiGenerated.pdf)

from translator import translate_text
from progress_tracker import PhaseProgress
from difflib import SequenceMatcher
import time

# Détermine si une ligne Markdown contient du contenu à traduire
def is_translatable_line(line):
    stripped = line.strip()
    return bool(stripped and not stripped.startswith("```") and not stripped.startswith("#"))

# Détecte les traductions trop proches du texte original (pas traduites ?)
def is_translation_suspect(original, translated):
    similarity = SequenceMatcher(None, original.strip(), translated.strip()).ratio()
    return similarity > 0.9

# Fonction principale : traduction du fichier ligne par ligne
def translate_markdown_file(source_path, target_path):
    tracker = PhaseProgress()
    tracker.start()

    # Lecture du fichier source
    tracker.add_phase("📄 Lecture", total=1)
    with open(source_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    tracker.advance("📄 Lecture")
    tracker.log(f"{len(lines)} lignes chargées depuis {source_path}")

    # Traduction des lignes
    tracker.add_phase("🔁 Traduction", total=len(lines))
    translated_lines = []
    start_time = time.time()

    for i, line in enumerate(lines):
        if is_translatable_line(line):
            translated = translate_text(line)
            if is_translation_suspect(line, translated):
                tracker.log(f"⚠️ Ligne {i+1} suspecte : {line.strip()}", style="bold yellow")
            translated_lines.append(translated)
        else:
            translated_lines.append(line)
        tracker.advance("🔁 Traduction")

    tracker.log(f"✅ Traduction terminée en {time.time() - start_time:.2f}s")

    # Écriture du fichier traduit
    tracker.add_phase("💾 Sauvegarde", total=1)
    with open(target_path, "w", encoding="utf-8") as file:
        file.writelines(translated_lines)
    tracker.advance("💾 Sauvegarde")
    tracker.log(f"✅ Fichier traduit sauvegardé : {target_path}")
    tracker.stop()

if __name__ == "__main__":
    translate_markdown_file("cv_fr.md", "exports/cv_en_aiGenerated.md")
