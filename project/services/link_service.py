from utils.strings import rand_string
import re

class LinkService:
    def __init__(self):
        self.links:dict[str: str] = {}

    def create_link(self, link:str) -> str | None:

        if re.search(r'https?://',link) is None: link = "https://" + link

        if link.find('.') == -1 : return None

        short_link: str = rand_string(k=5)
        self.links[short_link] = link
        return short_link
        
    def get_link(self, long_link:str) -> str | None :
        return self.links.get(long_link)

    