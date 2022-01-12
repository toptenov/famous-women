from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .utils import *


class WomenHome(DataMixin, ListView):  # Важно первым ставить именно класс DataMixin
    """
    Представление знаменитых женщин без разделения на категории
    """
    model = Women  # Модель, для которой в этом представлении будут отображаться данные
    template_name = 'women/index.html'  # Ссылка на шаблон, использующий данные из модели model текущего класса
    context_object_name = 'posts'  # Определяет имя переменной, для использования в данных из текущего класса в ->
    # -> html-шаблоне. По умолчанию называется object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        """Функция формирует статический (неизменяемые типы данных) и динамический (изменяемые типы данных) контекст для
        последующей передачи в html-шаблон"""
        context = super().get_context_data(**kwargs)  # Приобщить к результату работы функции тот контекст, который ->
        # -> уже сформирован в классе. В нашем случае, например, context_object_name. Данные будут переданны в список ->
        # -> context в виде именованных параметров
        c_def = self.get_user_context(title="Главная страница")  # Получение стандартного контекста из DataMixin
        return dict(list(context.items()) + list(c_def.items()))  # Соединение уникального контекста и контекста ->
        # -> полученного из класса DataMixin

    def get_queryset(self):
        return Women.objects.filter(is_published=True).select_related('cat')  # .select_related('cat') - таким ->
        # -> образом мы подгружаем названия категорий из таблицы Category одним SQL-запросом ("жадная" загрузка ->
        # -> связанных данных)


# def index(request):
#     posts = Women.objects.all()
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }
#
#     return render(request, 'women/index.html', context=context)


# # @login_required  # Декоратор, предоставляющий доступ к странице только авторизованным пользователям. Не забудь ->
# # -> импортировать login_required, если хочешь использовать
# def about(request):
#     return render(request, 'women/about.html', {'menu': menu, 'title': 'О сайте'})


class AboutPage(DataMixin, TemplateView):
    template_name = 'women/about.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        """Функция формирует статический (неизменяемые типы данных) и динамический (изменяемые типы данных) контекст для
        последующей передачи в html-шаблон"""
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="О сайте")
        return dict(list(context.items()) + list(c_def.items()))


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    """
    Представление страницы добавления новых постов
    """
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')  # URL-адрес для перенаправления ответа при успешной обработке формы. Если ->
    # -> не указать этот параметр, то при успешной обработке формы Django автоматически перенаправит пользователя ->
    # -> на страницу, указанную в классе Women.get_absolute_url(). В нашем случае, это страница вновь добавленного ->
    # -> поста.
    login_url = reverse_lazy('home')  # Страница, куда перенаправляет пользователя, в случае, если он не авторизован
    raise_exception = True  # В случае, если пользователь не авторизован - raise 403

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")
        return dict(list(context.items()) + list(c_def.items()))


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#
#     return render(request, 'women/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})


# def contact(request):
#     return HttpResponse("Обратная связь")


class ContactFormView(DataMixin, FormView):
    """
    Представление страницы отправки обратной связи
    """
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    # Функция, вызываемая в случае успешно заполненной формы пользователем
    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


# def login(request):
#     return HttpResponse("Авторизация")


def page_not_found(request, exception):
    return HttpResponseNotFound(f'<h1>Страница не найдена</h1><br>{exception}')


class ShowPost(DataMixin, DetailView):
    """
    Представление отдельной страницы поста
    """
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'  # Имя параметра, указанного в URL-адресе, содержащем заголовок. По умолчанию ->
    # -> slug_url_kwarg = 'slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])  # Заголовок в данном случае формируется на основе ->
        # -> контекста, полученного ранее
        return dict(list(context.items()) + list(c_def.items()))


# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#
#     return render(request, 'women/post.html', context=context)


class WomenCategory(DataMixin, ListView):
    """
    Представление знаменитых женщин по категориям
    """
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')  # ->
        # -> Атрибут cat__slug - это атрибут slug из связанной модели Category. То есть мы из модели Women обратились ->
        # -> к атрибуту модели Category. Мы можем это делать через двойное подчеркивание потому что они связаны

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))


# def show_category(request, cat_slug):
#     cats = Category.objects.all()
#     cat = get_object_or_404(Category, slug=cat_slug)
#     posts = Women.objects.all()
#
#     if len(posts) == 0:
#         raise Http404()
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'cats': cats,
#         'title': 'Отображение по рубрикам',
#         'cat_selected': cat.id,
#     }
#
#     return render(request, 'women/index.html', context=context)


class RegisterUser(DataMixin, CreateView):
    """
    Представление страницы регистрации пользователя
    """
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    # Метод, который вызывается при успешной отправленной форме регистрации
    def form_valid(self, form):
        user = form.save()  # Сохранение регистрационных данных пользователя в БД
        login(self.request, user)  # Функция Django, которая авторизовывает пользователя
        return redirect('home')  # Перенаправление пользователя домой после успешной авторизации


class LoginUser(DataMixin, LoginView):
    """
    Представление страницы авторизации пользователя
    """
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    # Куда перенаправлять пользователя после успешной авторизации:
    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    """
    Функция представления logout
    """
    logout(request)
    return redirect('login')
