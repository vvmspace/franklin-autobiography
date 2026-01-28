import os
import re

CHAPTERS_DIR = "/Users/vvm/solving/convert/chapters"

def format_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    original_content = content

    # 1. Bold Years (4 digits, 1000-2999)
    # Avoid double bolding if already bolded
    # Look for years not preceded by ** and not followed by **
    # But regex lookbehind needs fixed width.
    # Simpler: Matches \b\d{4}\b. Check if surrounded.
    
    # We will use a callback to check context
    def replace_year(match):
        year = match.group(1)
        start, end = match.span()
        # Check if already surrounded by **
        if start >= 2 and content[start-2:start] == "**" and end <= len(content)-2 and content[end:end+2] == "**":
            return year # Already bold
        return f"**{year}**"

    # Regex for years: 1000-2999
    content = re.sub(r'\b(1[0-9]{3}|20[0-2][0-9])\b', replace_year, content)

    # 2. Italicize «...»
    # Regex for «text». Check if already *...*
    def replace_title(match):
        full_match = match.group(0) # «...»
        start, end = match.span()
        # Check if already italicized or bolded
        if (start >= 1 and content[start-1] == "*") or (start >= 2 and content[start-2:start] == "**"):
             return full_match
        return f"*{full_match}*"

    content = re.sub(r'(«[^»\n]+»)', replace_title, content)

    # 3. Bold First Occurrence of Names
    # Pattern: Capitalized Word + Space + Capitalized Word
    # Exclude common false positives if necessary (like "Глава I", "Новый Год" though "Новый Год" fits)
    # We'll stick to the broad definition but maybe exclude beginning of sentences if we could detect that, 
    # but "first occurrence" logic helps.
    
    seen_names = set()
    
    # We need to iterate through matches and replace ONLY if not seen.
    # Since re.sub processes usually sequentially, we can use a callback with side effects.
    
    def replace_name(match):
        name = match.group(0)
        # Check if it looks like a name (both parts capitalized)
        # Verify it's not already bolded
        start, end = match.span()
        if start >= 2 and content[start-2:start] == "**":
            seen_names.add(name) # Mark as seen so we don't bold subsequents if they were manually bolded
            return name
            
        if name in seen_names:
            return name
        
        # Heuristic: Filter out likely non-names if needed. 
        # For now, simplistic approach as requested.
        # Check against a blocklist? 
        # "Глава I", "Глава II" etc are usually headers. 
        if "Глава" in name:
            return name

        seen_names.add(name)
        return f"**{name}**"

    # Using a slightly more specific regex for Cyrillic/Latin names
    # [A-ZА-ЯЁ][a-zа-яё]+ \s+ [A-ZА-ЯЁ][a-zа-яё]+
    pattern_name = r'\b([A-ZА-ЯЁ][a-zа-яё]+)\s+([A-ZА-ЯЁ][a-zа-яё]+)\b'
    content = re.sub(pattern_name, replace_name, content)
    
    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Updated {os.path.basename(filepath)}")
    else:
        print(f"No changes for {os.path.basename(filepath)}")

def main():
    files = sorted([os.path.join(CHAPTERS_DIR, f) for f in os.listdir(CHAPTERS_DIR) if f.endswith('.md')])
    # Add combined_book.md
    combined_book = "/Users/vvm/solving/convert/combined_book.md"
    if os.path.exists(combined_book):
        files.append(combined_book)
        
    for filepath in files:
        format_file(filepath)

if __name__ == "__main__":
    main()
