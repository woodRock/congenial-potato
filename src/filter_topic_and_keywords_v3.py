
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

def filter_by_topic_and_keywords(input_file, output_file, topics_to_include, keywords, num_topics=10):
    with open(input_file, 'r') as f:
        content = f.read()

    entries = content.split('\n@')
    abstracts = []
    entry_mapping = []

    for i, entry in enumerate(entries):
        if not entry.strip():
            continue

        if 'abstract' in entry:
            abstract_match = re.search(r'abstract\s*=\s*{(.*?)}', entry, re.IGNORECASE | re.DOTALL)
            if abstract_match:
                abstracts.append(abstract_match.group(1))
                entry_mapping.append(entry)

    if not abstracts:
        print("No abstracts found.")
        return

    vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
    try:
        dtm = vectorizer.fit_transform(abstracts)
    except ValueError:
        print("Could not vectorize abstracts. Maybe they are all stop words?")
        return

    lda = LatentDirichletAllocation(n_components=num_topics, random_state=0)
    topic_assignments = lda.fit_transform(dtm)

    filtered_entries = []
    for i, entry in enumerate(entry_mapping):
        if topic_assignments[i].argmax() in topics_to_include:
            abstract_match = re.search(r'abstract\s*=\s*{(.*?)}', entry, re.IGNORECASE | re.DOTALL)
            if abstract_match:
                abstract = abstract_match.group(1)
                if any(keyword.lower() in abstract.lower() for keyword in keywords):
                    if not entry.startswith('@'):
                        entry = '@' + entry
                    filtered_entries.append(entry)

    with open(output_file, 'w') as f:
        f.write('\n'.join(filtered_entries))

if __name__ == "__main__":
    # Topics to include (0-indexed)
    # Topic 1, 2, 4, 6, 8
    topics = [0, 1, 3, 5, 7]
    keywords = ["biomass", "abundance", "distribution", "stock assessment", "population"]
    filter_by_topic_and_keywords("/Users/woodj/Desktop/congenial-potato/filtered_by_type.bib", "/Users/woodj/Desktop/congenial-potato/final_filtered_refs.bib", topics, keywords)
