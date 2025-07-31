import requests
from bs4 import BeautifulSoup

def get_soup(url):
    """
    Download the page content from `url` and return a BeautifulSoup object.
    HINT: Use requests and BeautifulSoup.
    """
    # TODO: Implement this function
    
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    
    return soup 

# Test: Try calling get_soup with the jobs site URL
job_url = "https://realpython.github.io/fake-jobs/"
soup = get_soup(job_url)
print(soup.prettify()[:50])