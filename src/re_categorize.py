import json
import os

def get_categories(papers):
    application_categories = set()
    methodology_categories = set()
    for paper in papers:
        application_categories.add(paper['application_category'])
        methodology_categories.add(paper['methodology_category'])
    return sorted(list(application_categories)), sorted(list(methodology_categories))

def re_categorize_papers():
    file_path = os.path.join(os.path.dirname(__file__), 'categorized_papers.json')
    with open(file_path, 'r') as f:
        papers = json.load(f)

    application_categories, methodology_categories = get_categories(papers)

    for paper in papers:
        if paper['application_category'] == 'Other':
            print(f"Title: {paper['title']}")
            print(f"Abstract: {paper['abstract']}")
            print("Current application category: Other")
            for i, category in enumerate(application_categories):
                print(f"{i+1}. {category}")
            
            while True:
                try:
                    choice = int(input(f"Select a new application category (1-{len(application_categories)}): "))
                    if 1 <= choice <= len(application_categories):
                        paper['application_category'] = application_categories[choice-1]
                        break
                    else:
                        print("Invalid choice. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

        if paper['methodology_category'] == 'Other':
            print(f"Title: {paper['title']}")
            print(f"Abstract: {paper['abstract']}")
            print("Current methodology category: Other")
            for i, category in enumerate(methodology_categories):
                print(f"{i+1}. {category}")

            while True:
                try:
                    choice = int(input(f"Select a new methodology category (1-{len(methodology_categories)}): "))
                    if 1 <= choice <= len(methodology_categories):
                        paper['methodology_category'] = methodology_categories[choice-1]
                        break
                    else:
                        print("Invalid choice. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

    with open(file_path, 'w') as f:
        json.dump(papers, f, indent=4)

if __name__ == '__main__':
    re_categorize_papers()
