import os


# ──────────────────────────────────────────
#  1. READ FILE
# ──────────────────────────────────────────

def read_file(filepath: str) -> str | None:
    """Read and return the contents of a text file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"[✓] File '{filepath}' read successfully ({len(content)} characters).")
        return content

    except FileNotFoundError:
        print(f"[✗] Error: File '{filepath}' was not found.")
    except IsADirectoryError:
        print(f"[✗] Error: '{filepath}' is a directory, not a file.")
    except PermissionError:
        print(f"[✗] Error: Permission denied when reading '{filepath}'.")
    except UnicodeDecodeError:
        print(f"[✗] Error: Could not decode '{filepath}'. Make sure it is a UTF-8 text file.")
    except OSError as e:
        print(f"[✗] OS Error while reading file: {e}")

    return None


# ──────────────────────────────────────────
#  2. FIND TEXT
# ──────────────────────────────────────────

def find_text(content: str, search_term: str) -> list[int]:
    """
    Find all line numbers where search_term appears.
    Returns a list of 1-based line numbers.
    """
    if not content:
        print("[!] Content is empty. Nothing to search.")
        return []

    lines = content.splitlines()
    matches = [i + 1 for i, line in enumerate(lines) if search_term in line]

    if matches:
        print(f"[✓] '{search_term}' found on line(s): {matches}")
    else:
        print(f"[!] '{search_term}' was not found in the file.")

    return matches


# ──────────────────────────────────────────
#  3. REPLACE TEXT
# ──────────────────────────────────────────

def replace_text(content: str, find: str, replace_with: str) -> str:
    """Replace all occurrences of `find` with `replace_with` in content."""
    if not content:
        print("[!] Content is empty. Nothing to replace.")
        return content

    count = content.count(find)
    if count == 0:
        print(f"[!] No occurrences of '{find}' found. Content unchanged.")
        return content

    updated_content = content.replace(find, replace_with)
    print(f"[✓] Replaced {count} occurrence(s) of '{find}' → '{replace_with}'.")
    return updated_content


# ──────────────────────────────────────────
#  4. WRITE / SAVE FILE
# ──────────────────────────────────────────

def write_file(filepath: str, content: str) -> bool:
    """Write content to a file, overwriting it if it exists."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[✓] File '{filepath}' saved successfully.")
        return True

    except PermissionError:
        print(f"[✗] Error: Permission denied when writing to '{filepath}'.")
    except IsADirectoryError:
        print(f"[✗] Error: '{filepath}' is a directory, not a file.")
    except OSError as e:
        print(f"[✗] OS Error while writing file: {e}")

    return False


# ──────────────────────────────────────────
#  5. DISPLAY FILE CONTENTS
# ──────────────────────────────────────────

def display_file(content: str, title: str = "File Contents") -> None:
    """Pretty-print file contents with line numbers."""
    if content is None:
        print("[!] No content to display.")
        return

    separator = "─" * 50
    print(f"\n{separator}")
    print(f"  {title}")
    print(separator)

    for i, line in enumerate(content.splitlines(), start=1):
        print(f"  {i:>3} │ {line}")

    print(separator + "\n")


# ──────────────────────────────────────────
#  6. CREATE A SAMPLE FILE (for demo)
# ──────────────────────────────────────────

def create_sample_file(filepath: str) -> None:
    """Create a sample text file for demonstration purposes."""
    sample_content = """\
Welcome to SaiKet Systems File Handler!

Python is a powerful programming language.
Python is used in web development, data science, and automation.
Many developers love Python for its simplicity and readability.

This file was created as a sample for Task 3.
We will find and replace words in this file using Python.
Python makes file handling easy and intuitive.
"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(sample_content)
        print(f"[✓] Sample file '{filepath}' created.\n")
    except OSError as e:
        print(f"[✗] Could not create sample file: {e}")


# ──────────────────────────────────────────
#  7. MAIN INTERACTIVE PROGRAM
# ──────────────────────────────────────────

def main():
    print("=" * 50)
    print("  SaiKet Systems — Basic File Handler")
    print("=" * 50 + "\n")

    # Step 1: Get or create a file
    filepath = input("Enter the file path (or press Enter to use 'sample.txt'): ").strip()
    if not filepath:
        filepath = "sample.txt"

    # Create sample file if it doesn't exist
    if not os.path.exists(filepath):
        print(f"[!] '{filepath}' not found. Creating a sample file...")
        create_sample_file(filepath)

    # Step 2: Read the file
    content = read_file(filepath)
    if content is None:
        print("\n[!] Could not read the file. Exiting.")
        return

    display_file(content, title="Original File")

    # Step 3: Interactive find & replace loop
    while True:
        print("\nOptions:")
        print("  1. Find text")
        print("  2. Find and replace text")
        print("  3. Display current file")
        print("  4. Save and exit")
        print("  5. Exit without saving")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == '1':
            search_term = input("Enter text to find: ")
            find_text(content, search_term)

        elif choice == '2':
            find_word    = input("Enter text to find   : ")
            replace_word = input("Enter replacement    : ")
            content = replace_text(content, find_word, replace_word)

        elif choice == '3':
            display_file(content, title="Current File")

        elif choice == '4':
            success = write_file(filepath, content)
            if success:
                print("\n[✓] All changes saved. Goodbye!")
            break

        elif choice == '5':
            print("\n[!] Exiting without saving. All changes discarded.")
            break

        else:
            print("[!] Invalid choice. Please enter a number between 1 and 5.")


# ──────────────────────────────────────────
#  ENTRY POINT
# ──────────────────────────────────────────

if __name__ == "__main__":
    main()
