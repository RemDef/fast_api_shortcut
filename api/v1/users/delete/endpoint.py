from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from users.services import delete_user

router = APIRouter()


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_endpoint(
    user_id: str,
    session: AsyncSession = Depends(get_session),
) -> None:
    await delete_user(session=session, user_id=user_id)
