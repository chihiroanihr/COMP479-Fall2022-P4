import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup

# Sort query strings (remove duplicate keys)
# def process_links(links):
#     for link in links:
#         link.url = url_query_cleaner(link.url)
#         yield link

# Define a spider class that inherits from scrapy.Spider
class ConcordiaSpider(CrawlSpider):
    # Give a name to a spider class
    name = "concordia_spider" 

    # Define the allowed domains that the spider is allowed to crawl
    allowed_domains = ['concordia.ca']

    # Define other necessary configurations
    custom_settings = {
        'CLOSESPIDER_PAGECOUNT': 10, # limit number of pages that the spider can crawl
        'ROBOTSTXT_OBEY': True, # Obey robot exclusion
        'HTTPCACHE_ENABLED': True # Cache requests, save time
    }

    # Define the first URL that the spider should crawl
    start_urls = ["https://www.concordia.ca/ginacody.html"] 

    # [TEST] Define the URLs for the spider as the local test files that you have created
    # start_urls = ['x', 'y', ...]
    '''
    # This is a shortcut to start_requiest() method
    def start_requests(self):
        urls = ["https://www.concordia.ca/ginacody.html"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    '''

    # Define a Rule object that specifies the pattern and action for extracting link from pages
    rules = (
        # For filtering out URLs
        Rule(
            LinkExtractor(
                # deny=[
                #     re.escape('https://www.imdb.com/offsite'),
                #     re.escape('https://www.imdb.com/whitelist-offsite'),
                # ],
            ), 
            # process_links=process_links,
            callback='parse',
            follow=True # Spider automatically follows the link that matches the rule's pattern, and crawls the pages they point to.
        ),
    )

    # Define the sets that will store the visited and to-visit URLs
    visited_URLs = set()
    to_visit_URLs = set(start_urls)

    # Define a method that will be called to parse the URLs after a response has been recieved from the target website
    def parse(self, response):
        self.logger.info('Parsing page: %s', response.url)

        # Add the current URL to the visted links set
        self.visited_URLs.add(response.url)

        # Remove the current URL from the to-visit links set
        self.to_visit_URLs.remove(response.url)

        # Add any new URLs that were found on the current page to the to-visit links set
        for URL in response.xpath("//a/@href"):
            self.to_visit_URLs.add(URL)

        # Check if there are any links left to visit
        if self.to_visit_URLs:
            # Yield a request for the next link in the to-visit links set
            yield scrapy.Request(self.to_visit_URLs.pop(), self.parse)

        # Use Beautiful Soup to parse the HTML response
        soup = BeautifulSoup(response.text, 'lxml') # use lxml to get decent HTML parsing speed

        # Extract the text from the page
        text = soup.fndAll(text=True)
        # body_element = soup.find("body")
        # body = body_element.extract()
        
        # Yield the logs and extracted data as an item that will be stored in a structured format
        yield {
            "log": self.logger.get_log(),
            "url": response.url,
            "title": soup.h1.string,
            "body": text
        }
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')

    # # Define a method that will be called to process the items that are extracted by the spider
    # def process_item(self, item, spider):
    #     # Save the logs and links that are contained in the item
    #     with open("logs.txt", "a") as f:
    #         f.write(item["log"])
    #     with open("links.txt", "a") as f:
    #         f.write(item["link"])

    #     # return the processed item
    #     return item