from starlette_admin.contrib.sqla import ModelView
from starlette_admin.fields import StringField, EnumField

from database.users import User


class UserAdmin(ModelView):
    fields = [
        "id",
        StringField("username", label="Username"),
        StringField("phone_number", label="Phone"),
        StringField("telegram_id", label="Telegram ID"),
        EnumField("role", enum=User.Role, label="Role"),
    ]

    exclude_fields_from_list = ["password"]
    searchable_fields = ["username", "phone_number"]
    sortable_fields = ["id", "username", "role"]