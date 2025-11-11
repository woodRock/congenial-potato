import re
from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer

def bertopic_analysis(input_file):
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

    if len(abstracts) < 10: # BERTopic needs a minimum number of documents
        print("Not enough documents to perform BERTopic analysis.")
        return

    print("Running BERTopic analysis... This may take a few minutes.")
    # Initialize BERTopic model with a CountVectorizer that removes stop words
    vectorizer_model = CountVectorizer(stop_words="english")
    topic_model = BERTopic(vectorizer_model=vectorizer_model, verbose=True)

    # Fit the model on the abstracts
    topics, _ = topic_model.fit_transform(abstracts)

    # Get the topic information
    topic_info = topic_model.get_topic_info()

    # Print the topics
    for index, row in topic_info.iterrows():
        print(f"Topic {row['Topic']}: {row['Name']}")
        print(f"  Representation: {row['Representation']}")
        print("\n")

if __name__ == "__main__":
    bertopic_analysis("/Users/woodj/Desktop/congenial-potato/refs.bib")