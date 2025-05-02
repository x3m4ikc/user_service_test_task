from litestar import Litestar
from user_service.controllers import UserController

app = Litestar(
    route_handlers=[UserController],
    debug=True
)
