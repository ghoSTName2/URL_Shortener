from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from database import get_db
from models import UrlShortener
from schemas import URLCreate, URLResponse, URLStatsResponse
from utils import generate_unique_short_code

router = APIRouter(tags=['URLs'])

@router.post(
    '/shorten', response_model=URLResponse, status_code=status.HTTP_201_CREATED
)
async def create_short_url(
    payload: URLCreate, db: AsyncSession = Depends(get_db)
):
    short_code = await generate_unique_short_code(db, length=6)
    new_url = UrlShortener(
        short_code=short_code,
        original_url=str(
            payload.url
        )
    )
    
    db.add(new_url)
    await db.commit()
    await db.refresh(new_url)
    
    return new_url
    
@router.get('/{short_code}')
async def redirect_to_original(
    short_code:str, db: AsyncSession = Depends(get_db)
):
    query = select(UrlShortener).where(UrlShortener.short_code == short_code)
    result = await db.execute(query)
    db_url = result.scalar_one_or_none()
    
    if not db_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Коротке посилання не знайдено'
        )
    
    db_url.clicks += 1
    db_url.last_clicked_at = datetime.now(timezone.utc)
    
    await db.commit()
    
    return RedirectResponse(
        url=db_url.original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT
    )
    
@router.get('/{short_code}/stats', response_model=URLStatsResponse)
async def get_url_stats(short_code: str, db: AsyncSession = Depends(get_db)):
    query = select(UrlShortener).where(UrlShortener.short_code == short_code)
    result = await db.execute(query)
    db_url = result.scalar_one_or_none()
    
    if not db_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Коротке посилання не знайдено',
        )
    return db_url