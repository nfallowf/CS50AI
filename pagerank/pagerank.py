import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    probability_distribution = {}

    # Randomly choose from the links from this page
    length = len(list(corpus[page]))
    for pages in list(corpus[page]) or []:
        probability = (damping_factor * (1/length))
        probability += (1 - damping_factor) * (1/(len(corpus)))
        probability_distribution[pages] =  probability

    # Randomly choose from all pages in corpus
    for pages in corpus:
        if pages not in probability_distribution:
            probability_distribution[pages] = (1 - damping_factor) * (1/len(corpus))

    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    corpus_keys = list(corpus.keys())               # List of keys(page names) in the corpus
    randomInt = random.randint(0, len(corpus)-1)    # Generate a random number to pick a random page to start in the corpus
    random_page = corpus_keys[randomInt]
    page_rank = dict.fromkeys(corpus_keys, 0)       # Create a new dictionary with the same keys as the corpus to count occurances
    page_rank[random_page] += 1

    # Select random pages, and count how many times each page is selected
    for i in range(n):
        probability_distribution = transition_model(corpus, random_page, damping_factor)
        random_page = random.choices(list(probability_distribution.keys()), list(probability_distribution.values()))[0]
        page_rank[random_page] += 1

    # Update the values to represent the proportion of the total sample
    for key, value in page_rank.items():
        page_rank[key] = value / n

    return page_rank

def calculate_pagerank(corpus, damping_factor, incoming_links, page_rank, N, page):
    old = page_rank[page]
    rank = (1-damping_factor)/N
    sum = 0
    for link in incoming_links:
        if len(corpus[link]) != 0:
            sum += page_rank[link]/len(corpus[link])
        else:
            sum += page_rank[link]/len(corpus)
    rank += damping_factor * sum
    new = rank
    page_rank[page] = new
    delta = abs(old-new)
    return (page_rank, delta)

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)
    corpus_keys = list(corpus.keys())
    page_rank = dict.fromkeys(corpus_keys, 1/N)     # Create new dictionary for the pagerank, initialize each to 1/N
    delta = float('inf')
    while delta > 0.000000001:
        for page, links in corpus.items():
            incoming_links = []
            for k, v in corpus.items():

                if len(v) == 0:
                    incoming_links.append(k)

                for link in v:
                    if link == page:
                        incoming_links.append(k)
            page_rank, change = calculate_pagerank(corpus, damping_factor, incoming_links, page_rank, N, page)
            if change < delta:
                delta = change
    return page_rank

if __name__ == "__main__":
    main()
