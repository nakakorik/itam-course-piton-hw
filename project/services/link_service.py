from utils.strings import rand_string
from utils.utc_now import utcnow
from repositories.link_repository import LinkRepository
import re

class LinkService:
    def __init__(self):
        self.links:dict[str: str] = {}
        self._link_repository = LinkRepository()

    async def create_link(self, link:str) -> str | None:

        if re.search(r'https?://',link) is None: link = "https://" + link

        if link.find('.') == -1 : return None

        short_link: str = rand_string(k=5)
        #self.links[short_link] = link
        
        await self._link_repository.create_link(real_link=link,short_link=short_link)

        return short_link
        
    async def get_real_link(self, short_link:str, user_agent:str,ip:str) -> str | None :
        link = await self._link_repository.get_link(short_link=short_link)
        if link is None: return None

        await self._link_repository.put_link_usage(used_Link_id = link.id, user_agent = user_agent, created_at = utcnow(), short_link = link.short_link,ip=ip) 

        return str(link.real_link)
    


    async def get_linkUsage_statistick(self, short_link:str, page:int, page_size:int) -> list[dict[str: any]] | None :
        link_rows = await self._link_repository.get_linkUsage_staticstic(short_link=short_link,page=page,page_size=page_size)
        if link_rows is None: return None

        link_stats: list[dict[str: any]] = []
        for row in link_rows:
            link_stats.append( {"Used Link Id": row.used_link_id, "User Agent": row.user_agent, "Created at": str(row.created_at), "IP": row.ip} )

        return link_stats


    