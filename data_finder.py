
import re
from datetime import datetime
import os

def extract_dates_from_text(text):
    """
    Extract all dates from the given text in various formats.
    Returns a list of standardized date strings and their original context.
    """
    # Various date patterns to look for
    date_patterns = [
        # MM/DD/YY or MM/DD/YYYY
        r'\b(0?[1-9]|1[0-2])[/](0?[1-9]|[12][0-9]|3[01])[/](19|20)?[0-9]{2}\b',
        
        # Month name DD, YYYY
        r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})(?:st|nd|rd|th)?,\s+(\d{4})\b',
        
        # DD Month name YYYY
        r'\b(\d{1,2})(?:st|nd|rd|th)?\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})\b',
        
        # YYYY-MM-DD
        r'\b(19|20)[0-9]{2}[-](0?[1-9]|1[0-2])[-](0?[1-9]|[12][0-9]|3[01])\b',
        
        # Special format for documents like "Date: MM/DD/YY"
        r'Date\s*:\s*(0?[1-9]|1[0-2])[/](0?[1-9]|[12][0-9]|3[01])[/](19|20)?[0-9]{2}',
        
        # For dates written as "DATE: DD MMM YYYY" or similar
        r'(?:DATE|Date)\s*:\s*(\d{1,2})\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{4})',
        
        # For dates in text like "on 16 September 1982"
        r'\bon\s+(\d{1,2})\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})\b'
    ]
    
    # Combined pattern
    combined_pattern = '|'.join(date_patterns)
    
    # Find all date matches with surrounding context
    matches = []
    for pattern in date_patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            # Get the matched date string
            date_str = match.group(0)
            
            # Get some context around the date (up to 50 chars before and after)
            start = max(0, match.start() - 50)
            end = min(len(text), match.end() + 50)
            context = text[start:end].strip()
            
            # Replace multiple spaces and newlines with a single space
            context = re.sub(r'\s+', ' ', context)
            
            matches.append({
                'date_str': date_str,
                'context': context,
                'position': match.start()
            })
    
    # Sort matches by position in the document
    matches.sort(key=lambda x: x['position'])
    
    return matches

def process_text_file(file_path):
    """Process a single text file and extract dates."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
        
    dates = extract_dates_from_text(content)
    
    print(f"\nDates found in {os.path.basename(file_path)}:")
    for i, date_info in enumerate(dates, 1):
        print(f"{i}. {date_info['date_str']}")
        print(f"   Context: \"{date_info['context']}\"")
        print()
    
    return dates

def process_directory(directory_path):
    """Process all .txt files in a directory."""
    all_dates = {}
    
    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory_path, filename)
            all_dates[filename] = process_text_file(file_path)
    
    return all_dates

# Example usage
if __name__ == "__main__":
    # For a single file
    # dates = process_text_file('path/to/your/file.txt')
    
    # For a directory of files
    # all_dates = process_directory('path/to/your/directory')
    
    # For testing with your sample text
    data_dir = os.path.join(os.path.dirname(__file__), "texts")
    file_path = os.path.join(data_dir, "194-10013-10011.txt")
    with open(file_path, 'r', encoding = 'utf-8') as file:
        sample_text = file.read()
    
    dates = extract_dates_from_text(sample_text)
    print("Dates found in sample text:")
    for i, date_info in enumerate(dates, 1):
        print(f"{i}. {date_info['date_str']}")
        print(f"   Context: \"{date_info['context']}\"")
        print()