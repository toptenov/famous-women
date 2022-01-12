from django.db.models import Count
from django.core.cache import cache

from .models import *

menu = [
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить статью", 'url_name': 'add_page'},
    {'title': "Обратная связь", 'url_name': 'contact'},
]


class DataMixin:
    """
    Класс, формирующий общий контекст, общую информацию для классов из view.py. Цель данного кода исключить
    дублирование кода.
    """
    paginate_by = 3  # Количество постов на одной странице

    # Функция формирования контекста по умолчанию:
    def get_user_context(self, **kwargs):
        context = kwargs  # Получение уникальных атрибутов со значениями (например title) в виде словаря
        cats = cache.get('cats')
        if not cats:
            cats = Category.objects.all().annotate(Count('women'))  # Сохраняем в c.women__count количество постов в ->
            # -> каждой категории
            cache.set('cats', cats, 60)  # Занести данные в кэш на 60 секунд. Название кэша = cats

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:  # Если is_authenticated = False (пользователь не авторизвован)
            user_menu.pop(1)  # Удалить из user_menu {'title': "Добавить статью", 'url_name': 'add_page'}
        context['menu'] = user_menu

        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context