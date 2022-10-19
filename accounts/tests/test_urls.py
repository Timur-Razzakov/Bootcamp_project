from django.test import TestCase
from django.urls import reverse


class ViewsTestCase(TestCase):
    def test_login_view(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_register_view(self):
        url = reverse('user_registration')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_requisites_view(self):
        url = reverse('user_requisites')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_update_view(self):
        url = reverse('update')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_requisite_list_view(self):
        url = reverse('requisite_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

"""Не знаю как передать id"""
    # def test_requisite_update_view(self):
    #     url = reverse(f'requisites_update/',)
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)
