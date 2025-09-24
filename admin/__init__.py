from starlette_admin.contrib.sqla import Admin, ModelView

from admin.auth import UsernameAndPasswordProvider
from admin.user import UserAdmin
from database import User
from database.base_model import db


admin = Admin(
    engine=db.engine,
    title="Trip",
    templates_dir="templates",
    auth_provider=UsernameAndPasswordProvider()
)

admin.add_view(ModelView(User))
admin.add_view(UserAdmin(User))