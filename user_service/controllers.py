from litestar import Controller, get, post, put, delete
from litestar.di import Provide
from litestar.dto import DTOData
from litestar.exceptions import NotFoundException
from litestar.status_codes import HTTP_201_CREATED
from sqlalchemy.ext.asyncio import AsyncSession

from user_service.db.engine import get_db
from user_service.db.models import User
from user_service.schemas import UserResponseDataclassDTO, UserResponseDTO, UserCreateDataclassDTO, UserCreateDTO, \
    UserUpdateDataclassDTO, UserUpdateDTO
from user_service.utils import hash_password


class UserController(Controller):
    path = '/user'
    dependencies = {"db": Provide(get_db)}

    @get('/', return_dto=UserResponseDataclassDTO)
    async def get_all_users(self, db: AsyncSession) -> list[UserResponseDTO]:
        users = await User.get_all_users(db)
        return [self._user_to_dto(user) for user in users]

    @get('/{user_id:int}', return_dto=UserResponseDataclassDTO)
    async def get_user(self, db: AsyncSession, user_id: int) -> UserResponseDTO:
        user = await User.get_user(db, user_id)
        if not user:
            raise NotFoundException("User not found")
        return self._user_to_dto(user)

    @post('/', status_code=HTTP_201_CREATED, dto=UserCreateDataclassDTO, return_dto=UserResponseDataclassDTO)
    async def create_user(self, db: AsyncSession, data: DTOData[UserCreateDTO]) -> UserResponseDTO:
        user_data = data.as_builtins()
        user_data["password"] = hash_password(user_data.get("password"))
        user = await User.create_user(db, user_data)
        return self._user_to_dto(user)

    @put('/{user_id:int}', dto=UserUpdateDataclassDTO, return_dto=UserResponseDataclassDTO)
    async def update_user(self, db: AsyncSession, user_id: int, data: DTOData[UserUpdateDTO]) -> UserResponseDTO:
        update_data = {k: v for k, v in data.as_builtins().items() if v is not None}
        if "password" in update_data.keys():
            update_data["password"] = hash_password(update_data.get("password"))
        user = await User.update_user(db, user_id, update_data)
        if not user:
            raise NotFoundException("User not found")
        return self._user_to_dto(user)

    @delete('/{user_id:int}')
    async def delete_user(self, db: AsyncSession, user_id: int) -> None:
        user = await User.get_user(db, user_id)
        if not user:
            raise NotFoundException("User not found")
        return await User.delete_user(db, user_id)

    @staticmethod
    def _user_to_dto(user: User) -> UserResponseDTO:
        return UserResponseDTO(
            id=user.id,
            name=user.name,
            surname=user.surname,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
