from starlette_admin import IntegerField, EnumField, StringField
from starlette_admin.contrib.sqla import ModelView

from database import User


class UserModelView(ModelView):
    fields = [
        StringField("username", label="Username", help_text="togri yoz", ),
        StringField("phone_number", label="Phone"),
        IntegerField("telegram_id", label="Telegram ID"),
        EnumField("role", enum=User.Role, label="Role"),
    ]

    label = 'Userlar'
    identity = 'users'
    exclude_fields_from_list = ["password"]
    searchable_fields = ["username", "phone_number"]
    edit_template = 'custom/admin_edit.html'

    field_overrides = {
        "phone_number": {"id": "phone"}
    }

    extra_js = [
        "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js",
        "https://cdnjs.cloudflare.com/ajax/libs/jquery.mask/1.14.16/jquery.mask.min.js",
        "/static/js/phone-mask.js",  # biz yaratgan fayl
    ]

    def get_list_query(self, request):
        return super().get_list_query(request).where(User.role == User.Role.USER)

    def get_count_query(self, request):
        return super().get_count_query(request).where(User.role == User.Role.USER)

class AdminModelView(ModelView):
    fields = [
        "id",
        "username",
        "phone_number",
        "telegram_id",
        "role",
        # StringField("username", label="Username", help_text="togri yoz", ),
        # StringField("phone_number", label="Phone"),
        # IntegerField("telegram_id", label="Telegram ID"),
        # EnumField("role", enum=User.Role, label="Role"),
    ]
    label = 'Adminlar'
    identity = 'admins'
    exclude_fields_from_list = ["password"]
    searchable_fields = ["username", "phone_number"]



    def get_list_query(self, request):
        return super().get_list_query(request).where(User.role == User.Role.ADMIN)

    def get_count_query(self, request):
        return super().get_count_query(request).where(User.role == User.Role.ADMIN)