import json
import re
import os
from collections import Counter

def extract_cryptonyms_from_text(text):

    # Define patterns for cryptonyms (no inline flags)
    cryptonym_patterns = [
        # Pattern 1: Two-letter prefix followed by uppercase word (e.g., GPIDEAL, IJDECANTER)
        r'\b[A-Z]{2}[A-Z]+\b',
        
        # Pattern 2: Two-letter prefix, uppercase word, hyphen, and number (e.g., LITAMIL-9)
        r'\b[A-Z]{2}[A-Z]+-\d+\b',
        
        # Pattern 3: Explicit mention with "cryptonym" nearby (e.g., "cryptonym GPIDEAL")
        r'cryptonym\s+([A-Z]{2}[A-Z]+(?:-\d+)?)\b',
        
        # Pattern 4: Redacted cryptonyms (e.g., [REDACTED] in context where a cryptonym is expected)
        r'\[REDACTED\]'
    ]
    
    # Combined pattern
    combined_pattern = '|'.join(cryptonym_patterns)
    
    # Known cryptonyms
    known_cryptonyms = ["GPIDEAL", "GPFLOOR", "IJDECANTER", "LITAMIL-9", "AMLASH", "AMMUG" ]
    exact_pattern = r'\b(' + '|'.join(known_cryptonyms) + r')\b'    
    final_pattern = f'({exact_pattern})|({combined_pattern})'
    
    matches = []
    for match in re.finditer(final_pattern, text, re.IGNORECASE):
        # Extract the cryptonym (handle groups from the combined pattern)
        cryptonym = None
        if match.group(1):  # From exact_pattern
            cryptonym = match.group(1)
        elif match.group(2):  # From combined_pattern
            cryptonym = match.group(2)
            if len(cryptonym) < 5 or cryptonym.upper() in ["DATE", "CODE", "FORM", "FROM", "YEAR", "MONTH", "DAY"]:  # pitfalls
                continue
            # Ensure it looks like a cryptonym (e.g., starts with two letters)
            if not re.match(r'^[A-Z]{2}', cryptonym, re.IGNORECASE):
                continue
        if not cryptonym:
            continue
        # Get context around the cryptonym
        start = max(0, match.start() - 100)
        end = min(len(text), match.end() + 100)
        while start > 0 and not text[start - 1].isspace():
            start -= 1
        while end < len(text) and not text[end].isspace():
            end += 1
        context = text[start:end].strip()
        context = re.sub(r'\s+', ' ', context)  # Replace multiple spaces and newlines with a single space
        
        # Store results
        matches.append({
            'cryptonym': cryptonym,
            'context': context
        })
    
    return matches

def count_cryptonyms(all_cryptonyms):

    cryptonym_list = []
    for filename, matches in all_cryptonyms.items():
        for match in matches:
            cryptonym_list.append(match['cryptonym'])
    
    cryptonym_counts = Counter(cryptonym_list)
    return dict(cryptonym_counts)

def process_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
    cryptonyms = extract_cryptonyms_from_text(content)
    return cryptonyms

def process_directory(directory_path):
    all_cryptonyms = {}
    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory_path, filename)
            cryptonyms = process_text_file(file_path)
            if cryptonyms:
                all_cryptonyms[filename] = cryptonyms
    return all_cryptonyms

if __name__ == "__main__":
    data_dir = os.path.join(os.path.dirname(__file__), "texts")
    all_cryptonyms = process_directory(data_dir)
    
    # Count occurrences of each cryptonym
    cryptonym_counts = count_cryptonyms(all_cryptonyms)
    print(cryptonym_counts)
    
    all_cryptonyms_json = os.path.join(os.path.dirname(__file__), "all_cryptonyms.json")
    with open(all_cryptonyms_json, "w") as file:
        json.dump(all_cryptonyms, file, indent=4)