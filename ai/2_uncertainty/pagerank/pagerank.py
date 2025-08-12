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
    print(f"corpus: {corpus}")
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
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    links = corpus[page]

    # if no links exist, probability to visit a page = 1/num of pages
    if not links:
        random_page_probability = 1 / len(corpus)
        return {c_page: random_page_probability for c_page in corpus}
    else:
        # if links do exist, use damping_factor for probabilites
        random_page_probability = (1 - damping_factor) / len(corpus)
        random_link_probability = damping_factor / len(links)
        # set each page to have the random page probability, then add the link probabilities
        transition_model = {c_page: random_page_probability for c_page in corpus}
        for link in links:
            transition_model[link] += random_link_probability

        return transition_model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    visited_count = {page: 0 for page in corpus}
    current_page = random.choice(list(corpus.keys()))

    for _ in range(n):
        # count the visit to ensure probabilites sum to 1
        visited_count[current_page] += 1
        # get probabilites for this current page
        transitions = transition_model(corpus, current_page, damping_factor)
        # get pages / probs for choices method
        pages = list(transitions.keys())
        probabilities = list(transitions.values())
        # get new curent page
        current_page = random.choices(pages, weights=probabilities)[0]

    pagerank = {}
    for page in corpus:
        # after generating sample set with transition model, calc pr
        pagerank[page] = visited_count[page] / n

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    threshold = 0.001

    pagerank = {page: 1 / len(corpus) for page in corpus}

    converged = False

    while not converged:
        new_pagerank = {}

        for page in corpus:
            # probability to randomly visit current page
            random_page_probability = (1 - damping_factor) / len(corpus)

            # probability to visit current page via link with
            # summation of all pages that link to current page
            random_link_probability = 0
            for linking_page in corpus:
                # if current page is in another page's list of links, add to summed probability
                if page in corpus[linking_page]:
                    random_link_probability += pagerank[linking_page] / len(
                        corpus[linking_page]
                    )
                # else, if the linking page has no links, treat as linking to all pages
                elif len(corpus[linking_page]) == 0:
                    random_link_probability += pagerank[linking_page] / len(corpus)
            # calc new pagerank for the page
            new_pagerank[page] = (
                random_page_probability + damping_factor * random_link_probability
            )
        # check if we have converged
        converged = all(
            abs(new_pagerank[page] - pagerank[page]) < threshold for page in corpus
        )

        pagerank = new_pagerank

    return pagerank


if __name__ == "__main__":
    main()
