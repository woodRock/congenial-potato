

import re

def filter_bibtex_type(input_file, output_file, types):
    with open(input_file, 'r') as f:
        content = f.read()

    entries = content.split('\n@')
    filtered_entries = []

    for entry in entries:
        if not entry.strip():
            continue

        # Ensure entry starts with @
        if not entry.startswith('@'):
            entry = '@' + entry

        # Check if 'type' field is present
        if 'type' in entry:
            # Extract type
            type_match = re.search(r'type\s*=\s*{(.*?)}', entry, re.IGNORECASE | re.DOTALL)
            if type_match:
                entry_type = type_match.group(1).strip()
                # Check if type is in the list of allowed types
                if entry_type in types:
                    filtered_entries.append(entry)

    with open(output_file, 'w') as f:
        f.write('\n'.join(filtered_entries))

if __name__ == "__main__":
    allowed_types = ["Article", "Conference paper", "Review"]
    filter_bibtex_type("/Users/woodj/Desktop/congenial-potato/refs.bib", "/Users/woodj/Desktop/congenial-potato/filtered_by_type.bib", allowed_types)

