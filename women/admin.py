from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class WomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'get_html_photo', 'cat', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {'slug': ("title",)}  # Автоматическое создание slug-url при создании поста
    fields = ('title', 'slug', 'cat', 'content', 'photo', 'get_html_photo', 'is_published', 'time_create', 'time_update')  # ->
    # -> Определение порядка вывода полей при редактировании поста
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')  # Отображение нередактируемых полей на ->
    # -> странице редактирования поста
    save_on_top = True  # Панель сохранения изменений в посте отображать вверху страницы

    # Формирование миниматюры фотографии поста, для отображения в админ-панели
    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")  # mark_safe говорит о том, что не следует ->
            # -> экранировать данных html-код. То есть его надо отобразить на странице

    # Как в админ-панели называть атрибут с Фотографией поста
    get_html_photo.short_description = "Миниатюра"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ("name",)} # Автоматическое создание slug-url при создании категории


admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Админ-панель сайта о знаменитых женщинах'
admin.site.site_header = 'Админ-панель сайта о знаменитых женщинах'
