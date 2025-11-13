from infrastructure.db_connections import create_all_tables, sqlite_connection
from persistent.db.link import Link, Link_Usage
from sqlalchemy import insert, select

class LinkRepository:
    def __init__(self):
        self._sessionmaker = sqlite_connection()
        create_all_tables()

    async def create_link(self,real_link, short_link) -> None:
        stmp = insert(Link).values( {"short_link": short_link , "real_link": real_link} ) 

        async with self._sessionmaker() as session:
            await session.execute(stmp)
            await session.commit()

    
    async def put_link_usage(self,usedLink_id, short_link, user_agent,created_at ) -> None:

        stmp = insert(Link_Usage).values( {"usedlink_id":usedLink_id ,"short_link": short_link, "user_agent": user_agent, "created_at": created_at} ) 

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
    
    async def get_linkUsage_staticstic(self,short_link,page:int,page_size:int)->list[Link_Usage]:#Link_Usage:

        stmp = select(Link_Usage).where(Link_Usage.short_link == short_link).order_by(Link_Usage.created_at.desc() ).offset(page).limit(page_size)

        async with self._sessionmaker() as session:
           resp = await session.execute(stmp)
           
        return [row[0] for row in resp.fetchall()]