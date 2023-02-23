menu = [{'title': 'Мой профиль', 'url_name': '#'},
        {'title': 'Поездки', 'url_name': 'trips'},
        {'title': 'Создать поездку', 'url_name': 'add_trip'}
]




class DataMixin:
    def get_user_contex(self, **kwargs):
        context = kwargs
        return context