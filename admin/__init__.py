from starlette_admin.contrib.sqla import Admin, ModelView

from admin.auth import UsernameAndPasswordProvider
from database import User
from database.base_model import db

# faqat admin obyektini yaratamiz
admin = Admin(
    engine=db.engine,
    title="Trip",
    templates_dir="templates",
    auth_provider=UsernameAndPasswordProvider()
)

# model qo‘shamiz
admin.add_view(ModelView(User))
