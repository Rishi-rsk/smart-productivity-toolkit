import os
from collections import Counter
import string


def read_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print("[✗] File not found.")
    except Exception as e:
        print(f"[✗] Error: {e}")
    return None


def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text


def analyze_text(text):
    lines = text.splitlines()
    words = text.split()
    characters = len(text)

    clean_words = clean_text(text).split()
    freq = Counter(clean_words)

    return {
        "lines": len(lines),
        "words": len(words),
        "characters": characters,
        "frequency": freq
    }


def display_results(stats):
    print("\n" + "=" * 50)
    print("        📊 TEXT ANALYSIS REPORT")
    print("=" * 50)

    print(f"Total Lines      : {stats['lines']}")
    print(f"Total Words      : {stats['words']}")
    print(f"Total Characters : {stats['characters']}")

    print("\nTop 10 Words:")
    for word, count in stats["frequency"].most_common(10):
        print(f"{word}: {count}")

    print("=" * 50 + "\n")


def create_sample_file(filepath):
    sample = """Python is amazing.
Python is easy to learn.
Data science uses Python.
Developers love Python."""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(sample)


def main():
    print("=" * 50)
    print("   📊 Word Count & Text Analyzer")
    print("=" * 50)

    filepath = input("Enter file path (or press Enter for sample.txt): ").strip()

    if not filepath:
        filepath = "sample.txt"
        if not os.path.exists(filepath):
            create_sample_file(filepath)

    text = read_file(filepath)

    if text:
        stats = analyze_text(text)
        display_results(stats)


if __name__ == "__main__":
    main()