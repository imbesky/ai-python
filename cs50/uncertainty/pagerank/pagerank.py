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
    result = dict()
    for c in corpus:
        result[c] = 0
    linked = len(corpus[page])

    if linked != 0:
        for p in result:
            result[p] += (1 - damping_factor) / len(corpus)
            if p in corpus[page]:
                result[p] += damping_factor / linked
    elif linked == 0:
        for p in result:
            result[p] = 1 / len(corpus)

    return result


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to
    """
    visited = []
    pages = []
    for c in corpus:
        pages.append(c)

    def next_page(current_page):
        probabilities = []
        transition = transition_model(corpus, current_page, damping_factor)
        for p in corpus:
            probabilities.append(transition[p])
        return random.choices(pages, probabilities)[0]

    visited.append(random.choices(pages)[0])
    for i in range(n - 1):
        visited.append(next_page(visited[len(visited) - 1]))

    result = dict()
    for c in corpus:
        result[c] = visited.count(c) / len(visited)
    return result


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_ranks = dict()
    for c in corpus:
        page_ranks[c] = 1 / len(corpus)

    def calculate_pagerank(page):
        pr = (1 - damping_factor) / len(corpus)
        for other_page in corpus:
            if len(corpus[other_page]) != 0 and page in corpus[other_page]:
                pr += page_ranks[other_page] / len(corpus[other_page])
            else:
                pr += page_ranks[other_page] / len(corpus)
        return pr

    while True:
        pr_sum = 0
        new_pr = dict()
        for p in page_ranks:
            new = calculate_pagerank(p)
            new_pr[p] = new
            pr_sum += new
        done = 0
        for p in new_pr:
            new = new_pr[p] / pr_sum
            if abs(new - page_ranks[p]) < 0.001:
                done += 1
            page_ranks[p] = new
        if done == len(corpus) and pr_sum >= 1:
            break

    return page_ranks


if __name__ == "__main__":
    main()
