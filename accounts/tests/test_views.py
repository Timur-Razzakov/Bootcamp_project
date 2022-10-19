from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.models import Empl_requisites, Subscription, Result, MyUser

User = get_user_model()


# class ViewsTestCase(TestCase):
#     def test_index_loads_properly(self):
#         """The index page loads properly"""
#         url = reverse('login')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)


class TaskPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создадим запись в БД
        Task.objects.create(
            title='Заголовок',
            text='Текст',
            slug='test-slug',
        )

    def setUp(self):
        # Создаем авторизованный клиент
        self.user = User.objects.create_user(username='StasBasov')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    # Проверяем используемые шаблоны
    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Собираем в словарь пары "имя_html_шаблона: reverse(name)"
        templates_pages_names = {
            'deals/home.html': reverse('deals:home'),
            'deals/added.html': reverse('deals:task_added'),
            'deals/task_list.html': reverse('deals:task_list'),
            'deals/task_detail.html': (
                reverse('deals:task_detail', kwargs={'slug': 'test-slug'})
            ),
        }
        # Проверяем, что при обращении к name вызывается соответствующий HTML-шаблон
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
