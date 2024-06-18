import time
import random
import pandas as pd
from scholarly import scholarly, ProxyGenerator
import logging

# set up logging to capture log messages
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

## set up random proxies to avoid many requests error
# load random proxies from a text file
def load_proxies(file_path):
    with open('src/proxies.txt', 'r') as file:
        proxies = [line.strip() for line in file if line.strip()]
    return proxies

proxies = load_proxies('src/proxies.txt')

# get random proxies
def get_random_proxy():
    return random.choice(proxies)

# configure proxy generator
def configure_proxy():
    pg = ProxyGenerator()
    proxy = get_random_proxy()
    pg.SingleProxy(http=proxy, https=proxy)
    scholarly.use_proxy(pg)

# search author name based on investigator name
def search_author(name):
    try:
        search_query = scholarly.search_author(name)
        author = next(search_query)
        author = scholarly.fill(author)
        return author
    except StopIteration:
        logging.error(f"author not found: {name}")
        return None
    except Exception as e:
        logging.error(f"An error occured:{e}")
        return None

# get the publication details of the author
# set maximum queries to limit code running time
def get_publications(authors, max_queries):
    published = [] # set empty list for the publications
    query_count= 0

    for name in authors:
        if query_count >= max_queries:
            break
        while True:
            try:
                configure_proxy()
                author = search_author(name)
                if author:
                    for pub in author['publications']:
                        pub['investigator'] = name
                        published.append(pub)
                query_count += 1 # update the query count
                break 
            except Exception as e:
                logging.error(f"Error author{name}:{e}")
                time.sleep(random.uniform(30,60))
        if query_count >= max_queries:
            break 
        time.sleep(random.uniform(5,10)) # set to avoid triggering rate limits
    return published

def save_to_csv(published, filename):
    published_df = pd.DataFrame(published) # convert to dataframe
    published_df.to_csv(filename, index=False) # save as csv

def main():
    # read file from processed data, obtain investigator column
    df = pd.read_csv('./data/processed/authors/author.csv')
    authors = df['investigator'].tolist()
    
    max_queries = 3 # can set own max query

    published = get_publications(authors, max_queries)

    save_to_csv(published, 'data/raw/scholarly/authors_published_03.csv') # save data for cleaning

if __name__ == "__main__":
    main()