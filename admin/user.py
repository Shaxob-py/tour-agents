from starlette_admin.contrib.sqla import ModelView


class UserModelView(ModelView):
    fields = [
        "id",
        "username",
        "phone_number",  # TODO phone number chiroyli chiqishi kk
        "telegram_id",
        "role",
        # StringField("username", label="Username", help_text="togri yoz", ),
        # StringField("phone_number", label="Phone"),
        # IntegerField("telegram_id", label="Telegram ID"),
        # EnumField("role", enum=User.Role, label="Role"),
    ]

    label = 'Userlar'
    identity = 'Userlar'
    exclude_fields_from_list = ["password"]
    searchable_fields = ["username", "phone_number"]
    # TODO faqat userlar chiqsin filter qoshish kk


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
    identity = 'Adminlar'
    exclude_fields_from_list = ["password"]
    searchable_fields = ["username", "phone_number"]
