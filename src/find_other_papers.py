

import re

def categorize_application_focus(abstract, title):
    text = (abstract + ' ' + title).lower()
    if any(keyword in text for keyword in ["aquaculture", "fish farming"]):
        return 'Aquaculture & Farming'
    if "plankton" in text:
        return 'Plankton & Larval Analysis'
    if any(keyword in text for keyword in ["fisheries assessment", "stock assessment"]):
        return 'Fisheries Management & Stock Assessment'
    if "remote sensing" in text:
        return 'Remote Sensing'
    if any(keyword in text for keyword in ["acoustic", "sonar"]):
        return 'Underwater Acoustics'
    if any(keyword in text for keyword in ["authenticity", "fraud"]):
        return 'Food Science & Authenticity'
    if "algal biomass" in text:
        return 'Algal Biomass'
    if "fisheries management" in text:
        return 'Fisheries Management & Stock Assessment'
    if any(keyword in text for keyword in ["species identification", "trait identification", "classification"]):
        return 'Species & Trait Identification'
    if any(keyword in text for keyword in ["ecology", "environmental monitoring", "water quality", "habitat"]):
        return 'Ecology & Environmental Monitoring'
    if any(keyword in text for keyword in ["genetics", "genomics", "dna"]):
        return 'Genetics & Genomics'
    return 'Other'

# --- Read and parse the bib file ---
with open('/Users/woodj/Desktop/congenial-potato/refs.bib', 'r') as f:
    content = f.read()

entries = content.split('\n@')

for entry in entries:
    if not entry.strip():
        continue

    title_match = re.search(r'title\s*=\s*{(.*?)}', entry, re.IGNORECASE | re.DOTALL)
    title = title_match.group(1) if title_match else ""

    abstract_match = re.search(r'abstract\s*=\s*{(.*?)}', entry, re.IGNORECASE | re.DOTALL)
    abstract = abstract_match.group(1) if abstract_match else ""

    category = categorize_application_focus(abstract, title)

    if category == 'Other':
        print(title)

