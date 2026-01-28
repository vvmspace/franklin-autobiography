import os
import re

CHAPTERS_DIR = "/Users/vvm/solving/convert/chapters"
OUTPUT_FILE = "/Users/vvm/solving/convert/chapter_map.md"

def extract_info(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Persons: look for **Name Surname** (as we formatted them)
    # Also we can look for just capitalized sequences if we missed some, but sticking to bold is safer for "Mentioned People".
    # User said "Where what faces are mentioned".
    # Regex: \*\*([A-ZА-ЯЁ][a-zа-яё]+\s+[A-ZА-ЯЁ][a-zа-яё]+)\*\*
    people = sorted(list(set(re.findall(r'\*\*([A-ZА-ЯЁ][a-zа-яё]+\s+[A-ZА-ЯЁ][a-zа-яё]+)\*\*', content))))

    # Years: **1xxx**
    years = sorted(list(set(re.findall(r'\*\*(1[0-9]{3}|20[0-2][0-9])\*\*', content))))

    # Locations: Heuristic.
    # Look for known keywords or patterns.
    # Keyword list (English/Russian mixed as text is mixed):
    # London, Boston, Philadelphia, America, England, Street, House, Road, River...
    # Also "New England", "Pennsylvania", "Burlington", "New York".
    # Let's search for Capitalized words that are NOT in the 'people' list.
    
    potential_caps = re.findall(r'\b([A-ZА-ЯЁ][a-zа-яё]+(?:-[A-ZА-ЯЁ][a-zа-яё]+)?)\b', content)
    
    # Filter out common words at start of sentences? Hard to detect start of sentence without nltk.
    # We will use a whitelist of common geographical terms and specific known cities.
    
    target_locations = [
        "London", "Лондон",
        "Boston", "Бостон",
        "Philadelphia", "Филадельфия",
        "New York", "Нью-Йорк",
        "Pennsylvania", "Пенсильвания",
        "England", "Англия",
        "America", "Америка",
        "Europe", "Европа",
        "Paris", "Париж",
        "France", "Франция",
        "Scotland", "Шотландия",
        "Ireland", "Ирландия",
        "Holland", "Голландия",
        "Germany", "Германия",
        "Italy", "Италия",
        "Spain", "Испания",
        "China", "Китай",
        "Turkey", "Турция",
        "Burlington", "Берлингтон",
        "Amboy", "Амбой",
        "Newcastle", "Ньюкасл",
        "Carolina", "Каролина",
        "Georgia", "Джорджия",
        "Virginia", "Вирджиния",
        "Maryland", "Мэриленд",
        "Rhode Island", "Род-Айленд",
        "Connecticut", "Коннектикут",
        "Massachusetts", "Массачузетс",
        "New England", "Новая Англия",
        "Street", "стрит", # streets
    ]
    
    found_locations = set()
    for loc in target_locations:
        if loc in content:
             found_locations.add(loc)
             
    # Also check context for "Street"
    # re.findall(r'([A-Z][a-z]+ Street)', content)
    # re.findall(r'([А-Я][а-а]+-стрит)', content)
    
    streets_ru = re.findall(r'([А-ЯЁ][а-яё]+-стрит)', content)
    found_locations.update(streets_ru)
    
    locations = sorted(list(found_locations))

    return people, years, locations

def main():
    files = sorted([f for f in os.listdir(CHAPTERS_DIR) if f.endswith('.md') and not f.startswith('format_')])
    
    with open(OUTPUT_FILE, 'w') as out:
        out.write("# Chapter Map\n\n")
        
        for filename in files:
            if filename == 'combined_book.md': continue 
            
            filepath = os.path.join(CHAPTERS_DIR, filename)
            people, years, locations = extract_info(filepath)
            
            out.write(f"## {filename}\n\n")
            
            out.write("**Mentioned People**:\n")
            if people:
                out.write(", ".join(people) + "\n")
            else:
                out.write("None detected\n")
            out.write("\n")
            
            out.write("**Years**:\n")
            if years:
                out.write(", ".join(years) + "\n")
            else:
                out.write("None detected\n")
            out.write("\n")
            
            out.write("**Locations**:\n")
            if locations:
                out.write(", ".join(locations) + "\n")
            else:
                out.write("None detected\n")
            out.write("\n")
            
            out.write("**Key Actions**:\n")
            out.write("TODO\n\n")
            
            out.write("**Conclusions**:\n")
            out.write("TODO\n\n")
            
            out.write("---\n\n")

if __name__ == "__main__":
    main()
