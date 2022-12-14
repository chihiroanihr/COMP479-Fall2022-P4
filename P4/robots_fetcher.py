from reppy.robots import Robots
from P4.crawler import write_log


class RobotsFetcher(object):
    def __init__(self, url, urlparsed):
        self.url = url
        self.urlparsed = urlparsed
    
    def fetch_robots(self):
        # Create path for robots.txt
        if self.urlparsed.path == '/':
            robots_url = self.url + '/robots.txt'
        else:
            robots_url = self.url.replace(self.urlparsed.path, '/robots.txt')

        # Log
        write_log('ROBOTS',
                    'Reading robots.txt file at: {0}'.format(robots_url),
                    package='reppy')

        # Fetch the robots.txt file for given URL, and create Robots instance
        robots = Robots.fetch(robots_url)
        
        return robots