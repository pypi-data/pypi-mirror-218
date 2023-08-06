import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse, urljoin


class EmailScraper:
    def __init__(self, domain):
        self.domain = domain
        self.visited_urls = set()
        self.emails = set()

    def scrape_emails(self):
        self._crawl_page(self.domain)

    def _crawl_page(self, url):
        if url in self.visited_urls:
            return

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all email patterns in the page's text
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(email_pattern, response.text)

        # Add the found emails to the set
        for match in matches:
            self.emails.add(match)

        # Find emails in <a> tags
        for a_tag in soup.find_all('a'):
            href = a_tag.get('href')
            if href and href.startswith('mailto:'):
                email = href.split(':')[1]
                self.emails.add(email)

        self.visited_urls.add(url)

        # Find all internal links and recursively crawl
        parsed_url = urlparse(url)
        base_url = parsed_url.scheme + '://' + parsed_url.netloc

        for link in soup.find_all('a', href=True):
            link_url = urljoin(base_url, link['href'])
            if urlparse(link_url).netloc == parsed_url.netloc:
                self._crawl_page(link_url)

    def get_emails(self):
        return list(self.emails)