from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

from studioclock.models import Clock


class ClockPermissionTests(TestCase):
    def setUp(self):
        self.clock = Clock.objects.create(name="Test Clock")
        self.user = User.objects.create_user(username="clock-user", password="password")
        self.mutation_views = [
            (reverse("clock:create"), "add_clock"),
            (reverse("clock:edit", args=[self.clock.pk]), "change_clock"),
            (reverse("clock:delete", args=[self.clock.pk]), "delete_clock"),
        ]

    def test_clock_list_is_public(self):
        response = self.client.get(reverse("clock:list"))

        self.assertEqual(response.status_code, 200)

    def test_mutation_views_require_login(self):
        for url, _ in self.mutation_views:
            with self.subTest(url=url):
                response = self.client.get(url)

                self.assertEqual(response.status_code, 302)

    def test_mutation_views_require_their_model_permission(self):
        self.client.force_login(self.user)

        for url, codename in self.mutation_views:
            with self.subTest(permission=codename):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 403)

                permission = Permission.objects.get(
                    content_type__app_label="studioclock",
                    codename=codename,
                )
                self.user.user_permissions.add(permission)
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.user.user_permissions.clear()
