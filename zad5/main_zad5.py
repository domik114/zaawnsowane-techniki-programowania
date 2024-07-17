import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
import matplotlib.pyplot as plt

class WebScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        self.categories = {}

    def scrape_page(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.title.text if soup.title else None
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None

    def process_category(self, category, urls):
        titles = []
        for url in urls:
            title = self.scrape_page(url)
            if title:
                titles.append(title)
        self.categories[category] = titles

    def scrape_websites(self):
        websites = {
            'Informacyjne': ['https://www.onet.pl/', 'https://www.wp.pl/', 'https://www.tvn24.pl/', 'https://www.bbc.com/news', 'https://www.cnn.com/', 'https://www.theguardian.com/', 'https://www.reuters.com/', 'https://www.aljazeera.com/'],
            'Sportowe': ['https://www.sport.pl/', 'https://www.goal.com/', 'https://www.espn.com/', 'https://www.skysports.com/'],
            'Plotkarskie': ['https://www.pudelek.pl/', 'https://www.plotek.pl/', 'https://www.tmz.com/', 'https://people.com/'],
            'Gry': ['https://www.ign.com/', 'https://www.polygon.com/', 'https://www.gamespot.com/'],
            'Planszowki': ['https://boardgamegeek.com/', 'https://www.dicetower.com/'],
            'Wedkarstwo': ['https://fishingbooker.com/', 'https://www.in-fisherman.com/'],
        }

        with ThreadPoolExecutor(max_workers=5) as executor:
            for category, urls in websites.items():
                executor.submit(self.process_category, category, urls)

    def count_words(self):
        word_counts = {}
        for category, titles in self.categories.items():
            word_counts[category] = Counter(" ".join(titles).split())
        return word_counts

    def plot_word_frequency(self, word_counts):
        for category, counter in word_counts.items():
            labels, values = zip(*counter.items())
            plt.figure(figsize=(8, 6))
            plt.bar(labels, values)
            plt.title(f"Word Frequency in {category} Websites")
            plt.xlabel("Words")
            plt.ylabel("Frequency")
            plt.xticks(rotation=60)
            plt.show()

if __name__ == "__main__":
    scraper = WebScraper()
    scraper.scrape_websites()
    word_counts = scraper.count_words()
    scraper.plot_word_frequency(word_counts)
