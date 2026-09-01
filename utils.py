import secrets
import string
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import UrlShortener

ALPHABET = string.ascii_letters + string.digits

async def generate_unique_short_code(
    db: AsyncSession, length: int = 6, max_retries: int = 10 
) -> str:
    for _ in range(max_retries):
        code = "".join(secrets.choice(ALPHABET) for _ in range(length))
        
        query = select(UrlShortener).where(UrlShortener.short_code == code)
        result = await db.execute(query)
        existing_item = result.scalar_one_or_none()
        
        if not existing_item:
            return code
    
    raise RuntimeError(
        "Не вдалося згенерувати унікальний код. Спробуйте збільшити довжину коду."
    )