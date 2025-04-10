import panflute as pf
from transformers import MarianMTModel, MarianTokenizer
from tqdm import tqdm
import time

# Load the translation model and tokenizer
MODEL_NAME = "Helsinki-NLP/opus-mt-fr-en"
model = MarianMTModel.from_pretrained(MODEL_NAME)
tokenizer = MarianTokenizer.from_pretrained(MODEL_NAME)

# Global variable for the progress bar
pbar = None

def translate_text(text):
    """
    Translates a text fragment from French to English using MarianMT.
    """
    try:
        tokens = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        translated = model.generate(**tokens)
        return tokenizer.decode(translated[0], skip_special_tokens=True)
    except Exception as e:
        pf.debug(f"Translation error for '{text}': {e}")
        return text

def action(elem, doc):
    """
    Action applied to each text fragment (pf.Str) in the AST.
    Translates the content and updates the progress bar.
    """
    global pbar
    if isinstance(elem, pf.Str) and elem.text.strip():
        elem.text = translate_text(elem.text)
        if pbar is not None:
            pbar.update(1)

def count_translatable_strings(doc):
    """
    Counts all pf.Str objects containing non-empty text in the AST.
    """
    count = 0

    def count_strings(elem, doc):
        nonlocal count
        if isinstance(elem, pf.Str) and elem.text.strip():
            count += 1
        return elem

    doc.walk(count_strings)
    return count

def main():
    input_file = "cv_fr.md"       # Input Markdown file
    output_file = "cv_fr_en.md"   # Output translated file

    print("Reading the Markdown file...")
    with open(input_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    print("Converting Markdown to AST...")
    try:
        doc = pf.convert_text(md_content, input_format="commonmark")
        if isinstance(doc, list):
            doc = pf.Doc(*doc)
    except Exception as e:
        print("Error converting Markdown to AST:", e)
        return
    print("AST conversion completed.")

    # Count the translatable text fragments in the AST
    total = count_translatable_strings(doc)
    print(f"{total} text fragments to translate.")

    # Initialize the progress bar
    global pbar
    pbar = tqdm(total=total, desc="Translating", ncols=80, ascii=True)

    print("Starting translation...")
    pf.run_filter(action, doc=doc)
    pbar.close()
    print("Translation completed.")

    print("Reconstructing the translated Markdown...")
    translated_md = pf.convert_text(doc, output_format="markdown")

    print(f"Saving the translated file to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(translated_md)
    print(f"Translation saved to: {output_file}")

if __name__ == '__main__':
    start_time = time.time()
    main()
    print(f"Execution time: {time.time() - start_time:.2f} seconds")
