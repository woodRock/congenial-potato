import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

def topic_modeling(input_file, num_topics=5, num_words=3):
    with open(input_file, 'r') as f:
        content = f.read()

    entries = content.split('\n@')
    abstracts = []

    for entry in entries:
        if not entry.strip():
            continue

        if 'abstract' in entry:
            abstract_match = re.search(r'abstract\s*=\s*{(.*?)}', entry, re.IGNORECASE | re.DOTALL)
            if abstract_match:
                abstracts.append(abstract_match.group(1))

    if not abstracts:
        print("No abstracts found.")
        return

    # Create a CountVectorizer to convert the text data to a matrix of token counts
    vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
    try:
        dtm = vectorizer.fit_transform(abstracts)
    except ValueError:
        print("Could not vectorize abstracts. Maybe they are all stop words?")
        return


    # Create an LDA model
    lda = LatentDirichletAllocation(n_components=num_topics, random_state=0)

    # Fit the LDA model to the document-term matrix
    lda.fit(dtm)

    # Print the top words for each topic
    for i, topic in enumerate(lda.components_):
        print(f'Topic {i + 1}:')
        print(" ".join([vectorizer.get_feature_names_out()[j] for j in topic.argsort()[-num_words:]]))

if __name__ == "__main__":
    topic_modeling("/Users/woodj/Desktop/congenial-potato/refs.bib")