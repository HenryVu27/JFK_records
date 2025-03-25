import json
import re
from datetime import datetime
from dateutil.parser import parse
import os

def extract_dates_from_text(text):
    """
    Extract all dates from the given text in various formats.
    Returns a list of standardized date strings and their original context.
    """
    # Various date patterns to look for
    prefix = r'(?:(?:on|On|Date:|DATE)\s+)?'
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
 
    matches = []
    for match in re.finditer(combined_pattern, text, re.IGNORECASE):
        date_str = match.group(0).strip()
        date_str = re.sub(r'^(?:on|On|Date:|DATE)\s+', '', date_str, flags=re.IGNORECASE)
        try:
            date_str = parse(date_str).strftime("%Y-%m-%d")
        except Exception:
            continue
        date_str = parse(date_str).strftime("%Y-%m-%d")
        # Get some context around the date
        start = max(0, match.start() - 100)
        end = min(len(text), match.end() + 100)
        # extend start and end to get full word instead of just char
        while start > 0 and not text[start - 1].isspace():
            start -= 1
        while end < len(text) and not text[end].isspace():
            end += 1
        context = text[start:end].strip()
        context = re.sub(r'\s+', ' ', context)  # replace multiple spaces and newlines with a single space
        # Store results
        matches.append({
            'date_str': date_str,
            'context': context
        })
    return matches

def process_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
    dates = extract_dates_from_text(content)
    return dates

def process_directory(directory_path):
    all_dates = {}
    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory_path, filename)
            dates = process_text_file(file_path)
            if dates:
                all_dates[filename] = dates
    return all_dates

if __name__ == "__main__":
    data_dir = os.path.join(os.path.dirname(__file__), "texts")
    all_dates = process_directory(data_dir)
    
    all_dates_json = os.path.join(os.path.dirname(__file__), "all_dates.json")
    with open(all_dates_json, "w") as file:
        json.dump(all_dates, file, indent = 4)

