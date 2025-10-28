#!/usr/bin/env python3

"""
This script searches the Semantic Scholar database for papers matching
a specific set of keyword groups.

It searches for papers that contain:
(EITHER 'machine learning' OR 'deep learning')
AND
(EITHER 'fish' OR 'marine biomass' OR 'fisheries' OR 'plankton' OR
 'acoustics' OR 'aquaculture')
 
The search is performed on the paper's title, abstract, and keywords.
"""

import requests
import json
import time
import urllib.parse # Import this to show the full URL

def build_query_group(keywords):
    """
    Creates an (A OR B OR C) string from a list of keywords.
    Handles multi-word phrases with quotes.
    """
    quoted_keywords = []
    for k in keywords:
        # If a keyword contains a space, wrap it in quotes for an exact phrase match
        if ' ' in k:
            quoted_keywords.append(f'"{k}"')
        else:
            quoted_keywords.append(k)
    
    return f"({' OR '.join(quoted_keywords)})"

def quote_keyword(keyword):
    """Helper function to quote a single keyword if it has a space."""
    if ' ' in keyword:
        return f'"{keyword}"'
    return keyword

def search_semantic_scholar(query_string, limit=20, query_label="Query", seen_paper_ids=None):
    """
    Performs a search on the Semantic Scholar API given a query string.
    
    Args:
        query_string (str): The search query.
        limit (int): Max results for this query.
        query_label (str): A label to print for this query.
        seen_paper_ids (set): A set of paper IDs to filter out duplicates.
                               If None, duplicates won't be tracked.
    """
    
    print(f"\n--- Running: {query_label} ---")
    print(f"Constructed Query: {query_string}\n")
    
    # 2. Set up the API call
    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"
    
    # Define the parameters
    # ** FIX: Manually encode the query string to use %20 for spaces, not + **
    # The API is strict and returns 400 if spaces are encoded as '+'
    try:
        encoded_query = urllib.parse.quote(query_string)
    except Exception as e:
        print(f"Error encoding query string: {e}")
        return

    # Pass other params normally
    other_params = {
        'limit': limit,
        'fields': 'title,abstract,year,authors.name,url,keywords,paperId' # Added paperId
    }
    
    # Build the full URL with the correctly encoded query
    # requests will handle encoding the *other* params
    full_url = f"{base_url}?query={encoded_query}"

    # Semantic Scholar API is public but recommends an API key for
    # higher rate limits. For simple scripts, it often works without one.
    # If you get rate-limited (HTTP 429), get a free key at:
    # https://www.semanticscholar.org/product/api
    # headers = {'x-api-key': 'YOUR_API_KEY_HERE'}

    # --- DEBUG: Show the exact URL being requested ---
    # We now build the debug URL slightly differently
    debug_url = f"{full_url}&{urllib.parse.urlencode(other_params)}"
    print(f"DEBUG: Requesting URL:\n{debug_url}\n")
    # --- End DEBUG ---
    
    print(f"Querying Semantic Scholar API... (showing top {limit} results)")

    # 3. Make the request
    try:
        # ** FIX: Add a short sleep to avoid 429 rate-limiting **
        print("Waiting 2 seconds to be polite to the API...")
        time.sleep(2)
        
        # response = requests.get(full_url, params=other_params, headers=headers) # Use this if you have an API key
        response = requests.get(full_url, params=other_params)
        
        # Print status code for debugging, even if it's 200
        print(f"DEBUG: Received HTTP Status Code: {response.status_code}")

        # Raise an exception for bad status codes (like 404, 500)
        response.raise_for_status()
        
        data = response.json()
        
        # --- DEBUG: Print the raw JSON response (or part of it) ---
        # This shows us exactly what the API returned
        # Use json.dumps for pretty printing
        print("DEBUG: API Response (snippet):")
        print(json.dumps(data, indent=2,
                         ensure_ascii=False)[:1000] + "...\n")
        # --- End DEBUG ---
        
        total_results = data.get('total', 0)
        if total_results == 0:
            print("No papers found matching your criteria for this query.")
            return

        print(f"Found {total_results} total matching papers for this query.")
        print("--------------------------------------------------\n")
        
        # 4. Parse and print results
        papers_found_in_this_query = 0
        for i, paper in enumerate(data.get('data', [])):
            paper_id = paper.get('paperId')
            
            # De-duplication check
            if seen_paper_ids is not None and paper_id in seen_paper_ids:
                print(f"--- Skipping duplicate paper (ID: {paper_id}) ---")
                continue
            
            if seen_paper_ids is not None and paper_id:
                seen_paper_ids.add(paper_id)
            
            papers_found_in_this_query += 1
            print(f"--- Result {i + 1} (Query: {query_label}) ---")
            
            title = paper.get('title', 'N/A')
            year = paper.get('year', 'N/A')
            url = paper.get('url', 'N/A')
            
            # Authors is a list of dicts, extract the 'name' field
            authors = [author['name'] for author in paper.get('authors', [])]
            author_str = ", ".join(authors) if authors else "N/A"
            
            # Keywords is a list of dicts, extract the 'keyword' field
            keywords_list = [kw['keyword'] for kw in paper.get('keywords', []) if kw]
            keyword_str = ", ".join(keywords_list) if keywords_list else "N/A"

            # Get a snippet of the abstract
            abstract = paper.get('abstract')
            abstract_snippet = (abstract[:300] + '...') if abstract else 'N/A'
            
            print(f"Title:    {title}")
            print(f"Year:     {year}")
            print(f"Authors:  {author_str}")
            print(f"Keywords: {keyword_str}")
            print(f"URL:      {url}")
            print(f"Abstract: {abstract_snippet}\n")
            
            # Be polite to the API and don't spam requests
            time.sleep(0.5) 
        
        if papers_found_in_this_query == 0 and total_results > 0:
            print("All results for this query were duplicates of previous queries.")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        # Check if response is available to check status_code
        if hasattr(response, 'status_code') and response.status_code == 429:
            print("ERROR: You are being rate-limited. Please get a free API key from")
            print("https://www.semanticscholar.org/product/api and add it to the 'headers' variable.")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
    except json.JSONDecodeError:
        print("Failed to decode the response from the server.")
        print(f"Response text: {response.text}")

def main():
    # Define your keyword sets
    ml_keywords = {'machine learning', 'deep learning', 'artificial intelligence'}
    marine_keywords = {
        'fish', 
        'marine biomass', 
        'fisheries', 
        'plankton', 
        'acoustics', 
        'aquaculture'
    }
    
    # --- Build Queries ---
    query_group1 = build_query_group(ml_keywords)
    
    # This set will store paperId strings to avoid printing duplicates
    seen_paper_ids = set()
    
    # --- Run Searches ---
    # New Strategy: Loop through marine keywords and run one query for each.
    # This avoids the complex (A OR B) AND (C OR D OR E) query that returned 0.
    
    print(f"Starting multi-query search. Will run {len(marine_keywords)} separate queries.")
    
    for marine_kw in marine_keywords:
        # Build a simpler query
        # e.g., (ML_Group) AND "fish"
        # e.g., (ML_Group) AND "marine biomass"
        quoted_marine_kw = quote_keyword(marine_kw)
        
        complex_query = f"{query_group1} AND {quoted_marine_kw}"
        
        # Run the search for this specific keyword
        search_semantic_scholar(
            complex_query, 
            limit=10,  # Request 10 for each keyword
            query_label=f"ML AND {quoted_marine_kw}",
            seen_paper_ids=seen_paper_ids
        )
    
    print(f"\n--- Search complete. Found {len(seen_paper_ids)} unique papers. ---")


if __name__ == "__main__":
    main()

