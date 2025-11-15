from infrastructure.db_connections import create_all_tables, sqlite_connection
from persistent.db.link import Link, LinkUsage
from sqlalchemy import insert, select
from datetime import datetime

class LinkRepository:
    def __init__(self):
        self._sessionmaker = sqlite_connection()
        create_all_tables()

    async def create_link(self,real_link, short_link) -> None:
        stmp = insert(Link).values( {"short_link": short_link , "real_link": real_link} ) 

        async with self._sessionmaker() as session:
            await session.execute(stmp)
            await session.commit()

    
    async def put_link_usage(self,used_Link_id:str, short_link:str, user_agent:str,created_at:datetime, ip:str) -> None:

        stmp = insert(LinkUsage).values( {"used_link_id":used_Link_id ,"short_link": short_link, "user_agent": user_agent, "created_at": created_at, "ip": ip} ) 

        async with self._sessionmaker() as session:
            await session.execute(stmp)
            await session.commit()

    async def get_link(self,short_link)-> Link | None:

        stmp = select(Link).where(Link.short_link == short_link).limit(1)

        async with self._sessionmaker() as session:
           resp = await session.execute(stmp)

        row = resp.fetchone()
        if row is None: return None

        return row[0]
    
    async def get_linkUsage_staticstic(self,short_link:str, page:int, page_size:int)->list[LinkUsage]:#LinkUsage:

        stmp = select(LinkUsage).where(LinkUsage.short_link == short_link).order_by(LinkUsage.created_at.desc() ).offset( (page-1) *page_size).limit(page_size)

        async with self._sessionmaker() as session:
           resp = await session.execute(stmp)
           
        return [row[0] for row in resp.fetchall()]