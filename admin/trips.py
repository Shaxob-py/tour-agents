from starlette_admin.contrib.sqla import ModelView


class TripModelView(ModelView):
    fields = [
        "id",
        "away_from",
        "destination",
        "days",
        "description",
        "start_date",
        "end_date",
        "is_ai_suggestion",
        "view_count",
        "user_id",
        "likes_count",
        "dislikes_count",
    ]
    label = 'Trip'
    identity = 'Trip'
