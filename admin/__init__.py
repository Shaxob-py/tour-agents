from starlette_admin.contrib.sqla import Admin
from admin.auth import UsernameAndPasswordProvider
from admin.trips import TripModelView
from admin.user import UserModelView, AdminModelView, SupportMessageAdmin
from database import User, Trip, SupportMessage
from database.base_model import db



admin = Admin(
    engine=db.engine,
    title="Trip",
    # templates_dir="templates",
    auth_provider=UsernameAndPasswordProvider()
)

admin.add_view(AdminModelView(User))
admin.add_view(TripModelView(Trip))
admin.add_view(UserModelView(User))
admin.add_view(SupportMessageAdmin(SupportMessage))

