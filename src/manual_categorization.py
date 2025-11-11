import re
import json

def parse_bibtex(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    entries = content.split('\n@')
    parsed_entries = []

    for entry in entries:
        if not entry.strip():
            continue

        key_match = re.search(r'\w+\s*\{\s*([^,]+),', entry)
        citation_key = key_match.group(1).strip() if key_match else ""

        title_match = re.search(r'title\s*=\s*\{(.*?)\}', entry, re.IGNORECASE | re.DOTALL)
        title = title_match.group(1).replace('\n', ' ').strip() if title_match else ""
        title = title.replace('{', '').replace('}', '')

        abstract_match = re.search(r'abstract\s*=\s*\{(.*?)\}', entry, re.IGNORECASE | re.DOTALL)
        abstract = abstract_match.group(1).replace('\n', ' ').strip() if abstract_match else ""
        abstract = abstract.replace('{', '').replace('}', '')

        parsed_entries.append({
            'citation_key': citation_key,
            'title': title,
            'abstract': abstract
        })

    return parsed_entries

def categorize_papers(papers):
    categorization_map = {
        "Abd-El-Atty2024": {"application": "Aquaculture & automated monitoring", "methodology": "Traditional supervised"},
        "Aftab2024": {"application": "Aquaculture & automated monitoring", "methodology": "Deep learning - CNN & Variants"},
        "Alfano2022": {"application": "Plankton & phytoplankton analysis", "methodology": "Unsupervised and self-supervised"},
        "Anastasiadi2023": {"application": "Fisheries management & stock assessment", "methodology": "Traditional supervised"},
        "Andrialovanirina2023": {"application": "Fisheries management & stock assessment", "methodology": "Unsupervised and self-supervised"},
        "Ardhi2022": {"application": "Plankton & phytoplankton analysis", "methodology": "Deep learning - CNN & Variants"},
        "Aruna2023": {"application": "Aquaculture & automated monitoring", "methodology": "Deep learning - CNN & Variants"},
        "Ayon2024": {"application": "Plankton & phytoplankton analysis", "methodology": "Traditional supervised"},
        "Ayyagari2023": {"application": "Fisheries management & stock assessment", "methodology": "Deep learning - CNN & Variants"},
        "Ayyagari2025": {"application": "Fisheries management & stock assessment", "methodology": "Deep learning - CNN & Variants"},
        "BenSlima2026": {"application": "Fisheries management & stock assessment", "methodology": "Unsupervised and self-supervised"},
        "Ber2021": {"application": "Fisheries management & stock assessment", "methodology": "Deep learning - CNN & Variants"},
        "Bi2023": {"application": "Aquaculture & automated monitoring", "methodology": "Evolutionary computation"},
        "Bonofiglio2022": {"application": "Fisheries management & stock assessment", "methodology": "Deep learning - CNN & Variants"},
        "Brautaset2025": {"application": "Fisheries management & stock assessment", "methodology": "Deep learning - CNN & Variants"},
        "Bravata2020": {"application": "Fisheries management & stock assessment", "methodology": "Deep learning - CNN & Variants"},
        "Cassy2024": {"application": "Aquaculture & automated monitoring", "methodology": "Deep learning - CNN & Variants"},
        "Cayetano2024": {"application": "Fisheries management & stock assessment", "methodology": "Deep learning - CNN & Variants"},
        "Cheng2025": {"application": "Fisheries management & stock assessment", "methodology": "Traditional supervised"},
        "Chérubin2020": {"application": "Fisheries management & stock assessment", "methodology": "Traditional supervised"},
        "Ciranni2025": {"application": "Plankton & phytoplankton analysis", "methodology": "Unsupervised and self-supervised"},
        "Connolly2023": {"application": "Fisheries management & stock assessment", "methodology": "Deep learning - CNN & Variants"},
        "Coskuner-Weber2025": {"application": "Aquaculture & automated monitoring", "methodology": "Traditional supervised"},
        "Currie2021": {"application": "Aquaculture & automated monitoring", "methodology": "Evolutionary computation"},
        "Dalal2024": {"application": "Molecular level analysis & food science", "methodology": "Traditional supervised"},
        "De2023": {"application": "Molecular level analysis & food science", "methodology": "Traditional supervised"},
        "Dhamdhere2025": {"application": "Aquaculture & automated monitoring", "methodology": "Traditional supervised"},
        "Ditria2025": {"application": "Fisheries management & stock assessment", "methodology": "Traditional supervised"},
        "Do2023": {"application": "Fisheries management & stock assessment", "methodology": "Traditional supervised"},
        "Dubus2023": {"application": "Fisheries management & stock assessment", "methodology": "Traditional supervised"},
        "Effrosynidis2020": {"application": "Fisheries management & stock assessment", "methodology": "Traditional supervised"},
        "Eickholt2025": {"application": "Fisheries management & stock assessment", "methodology": "Deep learning - CNN & Variants"},
        "Fahim2025": {"application": "Aquaculture & automated monitoring", "methodology": "Traditional supervised"},
        "Fan2024": {"application": "Aquaculture & automated monitoring", "methodology": "Traditional supervised"},
        "Fan2025": {"application": "Aquaculture & automated monitoring", "methodology": "Evolutionary computation"},
        "Friedland2021": {"application": "Fisheries management & stock assessment", "methodology": "Traditional supervised"},
        "Gladju2022": {"application": "Aquaculture & automated monitoring", "methodology": "Traditional supervised"},
        "Goulart2021": {"application": "Plankton & phytoplankton analysis", "methodology": "Unsupervised and self-supervised"},
        "Griffin2022": {"application": "Fisheries management & stock assessment", "methodology": "Traditional supervised"},
        "Gültepe2022": {"application": "Fisheries management & stock assessment", "methodology": "Traditional supervised"},
        "Hajari2024": {"application": "Fisheries management & stock assessment", "methodology": "Traditional supervised"},
        "Hamzaoui2023": {"application": "Aquaculture & automated monitoring", "methodology": "Deep learning - CNN & Variants"},
        "Huang2023a": {"application": "Fisheries management & stock assessment", "methodology": "Traditional supervised"},
        "Huang2023b": {"application": "Fisheries management & stock assessment", "methodology": "Traditional supervised"},
        "Huang2025a": {"application": "Molecular level analysis & food science", "methodology": "Evolutionary computation"},
        "Huang2025b": {"application": "Molecular level analysis & food science", "methodology": "Evolutionary computation"},
        "Indhumathi2024": {"application": "Fisheries management & stock assessment", "methodology": "Traditional supervised"},
        "Jalal2025": {"application": "Fisheries management & stock assessment", "methodology": "Deep learning - CNN & Variants"},
        "Jang2023": {"application": "Molecular level analysis & food science", "methodology": "Traditional supervised"},
        "Jayanthi2025": {"application": "Aquaculture & automated monitoring", "methodology": "Deep learning - CNN & Variants"},
        "Ju2020": {"application": "Fisheries management & stock assessment", "methodology": "Deep learning - CNN & Variants"},
        "Kerr2020": {"application": "Plankton & phytoplankton analysis", "methodology": "Deep learning - CNN & Variants"},
        "Khiari2024": {"application": "Molecular level analysis & food science", "methodology": "Traditional supervised"},
        "Kim2025": {"application": "Fisheries management & stock assessment", "methodology": "Deep learning - CNN & Variants"},
        "Klaoudatos2024": {"application": "Fisheries management & stock assessment", "methodology": "Traditional supervised"},
        "Koo2024": {"application": "Fisheries management & stock assessment", "methodology": "Traditional supervised"},
        "Kumar2023a": {"application": "Fisheries management & stock assessment", "methodology": "Deep learning - CNN & Variants"},
        "Kumar2023b": {"application": "Fisheries management & stock assessment", "methodology": "Deep learning - CNN & Variants"},
        "Kumaran2025": {"application": "Aquaculture & automated monitoring", "methodology": "Deep learning - CNN & Variants"},
        "Kunimatsu2025": {"application": "Fisheries management & stock assessment", "methodology": "Traditional supervised"},
        "Kupsa2025": {"application": "Aquaculture & automated monitoring", "methodology": "Deep learning - CNN & Variants"},
        "Kwon2025": {"application": "Plankton & phytoplankton analysis", "methodology": "Deep learning - CNN & Variants"},
        "Lai2024": {"application": "Fisheries management & stock assessment", "methodology": "Deep learning - CNN & Variants"},
        "Lal2025": {"application": "Plankton & phytoplankton analysis", "methodology": "Deep learning - CNN & Variants"},
        "Leong2025": {"application": "Fisheries management & stock assessment", "methodology": "Deep learning - CNN & Variants"},
        "Liao2024": {"application": "Fisheries management & stock assessment", "methodology": "Traditional supervised"},
        "Lindo2024": {"application": "Aquaculture & automated monitoring", "methodology": "Traditional supervised"},
        "Liu2020": {"application": "Plankton & phytoplankton analysis", "methodology": "Traditional supervised"},
        "Liu2021": {"application": "Plankton & phytoplankton analysis", "methodology": "Traditional supervised"},
        "Lu2022": {"application": "Fisheries management & stock assessment", "methodology": "Traditional supervised"},
        "Lu2024": {"application": "Molecular level analysis & food science", "methodology": "Traditional supervised"},
        "Ma2021": {"application": "Plankton & phytoplankton analysis", "methodology": "Deep learning - CNN & Variants"},
        "Martins2023": {"application": "Molecular level analysis & food science", "methodology": "Traditional supervised"},
        "Masoudi2024": {"application": "Plankton & phytoplankton analysis", "methodology": "Unsupervised and self-supervised"},
        "Mayormente2024": {"application": "Aquaculture & automated monitoring", "methodology": "Traditional supervised"},
        "McCarthy2023": {"application": "Fisheries management & stock assessment", "methodology": "Traditional supervised"},
        "McDonald2024": {"application": "Fisheries management & stock assessment", "methodology": "Traditional supervised"},
        "McLeay2021": {"application": "Aquaculture & automated monitoring", "methodology": "Deep learning - CNN & Variants"},
        "Mcmillan2023a": {"application": "Aquaculture & automated monitoring", "methodology": "Deep learning - CNN & Variants"},
        "McMillan2023b": {"application": "Aquaculture & automated monitoring", "methodology": "Deep learning - CNN & Variants"},
        "McMillan2025c": {"application": "Aquaculture & automated monitoring", "methodology": "Deep learning - transformers"},
        "Mcmillan2024": {"application": "Aquaculture & automated monitoring", "methodology": "Deep learning - transformers"},
        "Meeanan2023": {"application": "Fisheries management & stock assessment", "methodology": "Traditional supervised"},
        "Meeanan2024": {"application": "Fisheries management & stock assessment", "methodology": "Traditional supervised"},
        "Mehrab2025": {"application": "Fisheries management & stock assessment", "methodology": "Deep learning - CNN & Variants"},
        "Mots'oehli2024": {"application": "Fisheries management & stock assessment", "methodology": "Deep learning - CNN & Variants"},
        "Muinde2023": {"application": "Aquaculture & automated monitoring", "methodology": "Traditional supervised"},
        "Munger2022": {"application": "Fisheries management & stock assessment", "methodology": "Deep learning - CNN & Variants"},
        "Nandyala2024": {"application": "Aquaculture & automated monitoring", "methodology": "Traditional supervised"},
        "Navarro2024": {"application": "Aquaculture & automated monitoring", "methodology": "Traditional supervised"},
        "Nojima2024": {"application": "Fisheries management & stock assessment", "methodology": "Evolutionary computation"},
        "OKeeffe2023": {"application": "Aquaculture & automated monitoring", "methodology": "Deep learning - CNN & Variants"},
        "Osman2024": {"application": "Molecular level analysis & food science", "methodology": "Traditional supervised"},
        "Pagire2022": {"application": "Fisheries management & stock assessment", "methodology": "Deep learning - CNN & Variants"},
        "Park2024": {"application": "Fisheries management & stock assessment", "methodology": "Deep learning - CNN & Variants"},
        "Petrellis2023": {"application": "Aquaculture & automated monitoring", "methodology": "Deep learning - CNN & Variants"},
        "Pillay2021": {"application": "Fisheries management & stock assessment", "methodology": "Unsupervised and self-supervised"},
        "Pramunendar2020": {"application": "Fisheries management & stock assessment", "methodology": "Traditional supervised"},
        "Priya2023": {"application": "Plankton & phytoplankton analysis", "methodology": "Traditional supervised"},
        "Pu2021": {"application": "Plankton & phytoplankton analysis", "methodology": "Deep learning - CNN & Variants"},
        "Qu2024": {"application": "Fisheries management & stock assessment", "methodology": "Deep learning - CNN & Variants"},
        "Rahman2024": {"application": "Fisheries management & stock assessment", "methodology": "Deep learning - CNN & Variants"},
        "Rajkumar2024": {"application": "Aquaculture & automated monitoring", "methodology": "Traditional supervised"},
        "Raju2025": {"application": "Aquaculture & automated monitoring", "methodology": "Deep learning - CNN & Variants"},
        "Raman2023": {"application": "Fisheries management & stock assessment", "methodology": "Traditional supervised"},
        "Ramírez-Coronel2024": {"application": "Aquaculture & automated monitoring", "methodology": "Traditional supervised"},
        "Rasdas2023": {"application": "Fisheries management & stock assessment", "methodology": "Traditional supervised"},
        "Rowan2023": {"application": "Aquaculture & automated monitoring", "methodology": "Traditional supervised"},
        "Ruigrok2022": {"application": "Molecular level analysis & food science", "methodology": "Traditional supervised"},
        "Saberi2021": {"application": "Aquaculture & automated monitoring", "methodology": "Unsupervised and self-supervised"},
        "Sah2025": {"application": "Aquaculture & automated monitoring", "methodology": "Deep learning - CNN & Variants"},
        "Salman2020": {"application": "Fisheries management & stock assessment", "methodology": "Deep learning - CNN & Variants"},
        "Seto2025": {"application": "Molecular level analysis & food science", "methodology": "Traditional supervised"},
        "Shen2020": {"application": "Molecular level analysis & food science", "methodology": "Traditional supervised"},
        "Shen2022": {"application": "Molecular level analysis & food science", "methodology": "Traditional supervised"},
        "Smoliński2020": {"application": "Fisheries management & stock assessment", "methodology": "Traditional supervised"},
        "Somek2023": {"application": "Plankton & phytoplankton analysis", "methodology": "Deep learning - CNN & Variants"},
        "Stanley2022": {"application": "Fisheries management & stock assessment", "methodology": "Deep learning - CNN & Variants"},
        "Swyers2024": {"application": "Fisheries management & stock assessment", "methodology": "Traditional supervised"},
        "Testolin2022": {"application": "Fisheries management & stock assessment", "methodology": "Deep learning - CNN & Variants"},
        "Tran2024": {"application": "Aquaculture & automated monitoring", "methodology": "Traditional supervised"},
        "Vargas2024": {"application": "Fisheries management & stock assessment", "methodology": "Traditional supervised"},
        "Varma2020": {"application": "Plankton & phytoplankton analysis", "methodology": "Deep learning - CNN & Variants"},
        "Vilas2022": {"application": "Fisheries management & stock assessment", "methodology": "Traditional supervised"},
        "Vu2025": {"application": "Fisheries management & stock assessment", "methodology": "Traditional supervised"},
        "Walker2021": {"application": "Plankton & phytoplankton analysis", "methodology": "Traditional supervised"},
        "Watanabe2025": {"application": "Fisheries management & stock assessment", "methodology": "Unsupervised and self-supervised"},
        "Weiss2022": {"application": "Fisheries management & stock assessment", "methodology": "Deep learning - CNN & Variants"},
        "Wood2022": {"application": "Molecular level analysis & food science", "methodology": "Traditional supervised"},
        "Wood2025": {"application": "Molecular level analysis & food science", "methodology": "Deep learning - transformers"},
        "Wood2025a": {"application": "Molecular level analysis & food science", "methodology": "Deep learning - transformers"},
        "Wood2025b": {"application": "Molecular level analysis & food science", "methodology": "Unsupervised and self-supervised"},
        "Yadav2023": {"application": "Aquaculture & automated monitoring", "methodology": "Deep learning - CNN & Variants"},
        "Yin2024": {"application": "Aquaculture & automated monitoring", "methodology": "Deep learning - CNN & Variants"},
        "Yuan2024": {"application": "Fisheries management & stock assessment", "methodology": "Deep learning - CNN & Variants"},
        "Zhan2024": {"application": "Fisheries management & stock assessment", "methodology": "Deep learning - CNN & Variants"},
        "Zhang2023": {"application": "Aquaculture & automated monitoring", "methodology": "Deep learning - CNN & Variants"},
        "Zhang2024": {"application": "Aquaculture & automated monitoring", "methodology": "Deep learning - CNN & Variants"},
        "Zhao2021": {"application": "Aquaculture & automated monitoring", "methodology": "Deep learning - CNN & Variants"},
        "Zheng2024": {"application": "Fisheries management & stock assessment", "methodology": "Deep learning - CNN & Variants"},
        "Zheng2025": {"application": "Fisheries management & stock assessment", "methodology": "Deep learning - CNN & Variants"},
        "Zhong2024": {"application": "Aquaculture & automated monitoring", "methodology": "Deep learning - CNN & Variants"},
        "Zhou2023": {"application": "Aquaculture & automated monitoring", "methodology": "Deep learning - CNN & Variants"},
        "Zhuang2024": {"application": "Fisheries management & stock assessment", "methodology": "Deep learning - CNN & Variants"},
        "Zou2024": {"application": "Aquaculture & automated monitoring", "methodology": "Deep learning - CNN & Variants"}
    }

    categorized_papers = []
    for paper in papers:
        citation_key = paper['citation_key']
        if citation_key in categorization_map:
            paper['application_category'] = categorization_map[citation_key]['application']
            paper['methodology_category'] = categorization_map[citation_key]['methodology']
        else:
            paper['application_category'] = 'Other'
            paper['methodology_category'] = 'Other'
        categorized_papers.append(paper)
        
    return categorized_papers

if __name__ == '__main__':
    bib_file = '/Users/woodj/Desktop/congenial-potato/refs.bib'
    papers = parse_bibtex(bib_file)
    categorized_papers = categorize_papers(papers)
    
    output_path = '/Users/woodj/Desktop/congenial-potato/src/categorized_papers.json'
    with open(output_path, 'w') as f:
        json.dump(categorized_papers, f, indent=4)
    
    print(f"Categorized papers saved to {output_path}")
