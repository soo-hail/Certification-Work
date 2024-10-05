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
            pages[filename] = set(links) - {filename} # IGNORE LINK TO SAME PAGE.

    # Only include links to other pages in the corpus (CONSIDERING ONLY PAGES THAT ARE IN "CORPUS")
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
    linked_pages = corpus.get(page, set())  # SET OF ALL PAGES LINKED TO CURRENT-PAGE.
    all_pages = set(corpus.keys())  # SET OF ALL PAGES.

    distribution = {}
    if len(linked_pages) == 0:
        # ASSIGN EQUAL PROBABILITY TO ALL THE PAGES.
        n = len(all_pages)
        for p in all_pages:
            distribution[p] = 1 / n
    else:
        # ASSIGN PROBABILITY TO ALL THE PAGES (1 - DAMPING_FACTOR)
        n = len(all_pages)
        for p in all_pages:
            distribution[p] = (1 - damping_factor) / n

        # ASSIGN PROBABILITY TO LINKED PAGES.
        n = len(linked_pages)
        for p in linked_pages:
            distribution[p] += damping_factor / n

    return distribution

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # INITIALIZE RANKS OF ALL PAGES TO 0.
    ranks = {page: 0 for page in corpus.keys()}

    # GENERATE THE FIRST SAMPLE.
    current_state = random.choice(list(corpus.keys()))
    ranks[current_state] += 1

    # GENERATE "N-1" SAMPLES.
    for _ in range(1, n):
        tp = transition_model(corpus, current_state, damping_factor)
        current_state = random.choices(list(tp.keys()), list(tp.values()), k=1)[0]
        ranks[current_state] += 1

    # NORMALIZING THE RANKS SO, THEY SUM TO 1
    for page in ranks:
        ranks[page] /= n

    return ranks

def iterate_pagerank(corpus, damping_factor, threshold=0.001):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    n = len(corpus)  # TOTAL NO. OF PAGES.

    # ASSUMING THAT EACH PAGE'S RANK IS 1/N (EQUALLY LIKELY).
    ranks = {page: 1 / n for page in corpus.keys()}

    # ITERATIVELY UPDATE RANKS UNTIL THEY "CONVERGE" (RANKS BECOME STABLE, FURTHER ITERATIONS WILL HAVE NO IMPACT ON RANKS)
    converged = False

    while not converged:
        new_ranks = ranks.copy()  # TO COMPARE NEW AND OLD RANKS FOR "CONVERGENCE".
        for page in corpus.keys():  # ITERATING ALL THE PAGES
            new_ranks[page] = get_rank(page, corpus, damping_factor, ranks)

        # CHECK IF CONVERGED (FURTHER ITERATIONS WILL NOT IMPACT THE RANK OF A PAGE).
        converged = all(abs(new_ranks[page] - ranks[page]) < threshold for page in corpus.keys())

        ranks = new_ranks  # UPDATE RANKS

    # NORMALIZING SUM OF ALL RANKS TO 1.
    total_sum = sum(ranks.values())
    for page in ranks.keys():
        ranks[page] = ranks[page] / total_sum

    return ranks

def get_rank(page, corpus, damping_factor, current_ranks):
    n = len(corpus)  # TOTAL NO. OF PAGES.
    rank = (1 - damping_factor) / n

    # FOR ALL PAGES THAT ARE LINKED TO THE CURRENT PAGE.
    for p in corpus:
        if page in corpus[p] or len(corpus[p]) == 0:
            num_links = len(corpus[p]) if len(corpus[p]) > 0 else n
            rank += damping_factor * current_ranks[p] / num_links

    return rank

if __name__ == "__main__":
    main()
