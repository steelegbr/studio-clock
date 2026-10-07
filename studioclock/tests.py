from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

from studioclock.models import Clock, Font, FontWeight


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


class ClockRenderTests(TestCase):
    def test_render_uses_clock_colours_and_name_without_logo(self):
        clock = Clock.objects.create(
            name="Studio Clock",
            background_colour="#123456",
            foreground_colour="#ABCDEF",
        )

        response = self.client.get(reverse("clock:render", args=[clock.pk]))

        self.assertRegex(
            response.content.decode(),
            r'style="background-color: #123456;\s*color: #ABCDEF"',
        )
        self.assertContains(
            response,
            '<span class="clock-branding-name">Studio Clock</span>',
            html=True,
        )
        self.assertNotContains(response, "clock-branding-logo")

    def test_render_loads_and_applies_selected_font_and_weight(self):
        font = Font.objects.create(name="Share Tech Mono", family="Share Tech Mono")
        weight = FontWeight.objects.create(font=font, weight=700, name="Bold")
        clock = Clock.objects.create(name="Studio Clock", font=weight)

        response = self.client.get(reverse("clock:render", args=[clock.pk]))

        self.assertContains(
            response,
            "https://fonts.googleapis.com/css2?family=Share%20Tech%20Mono:wght@700&display=swap",
        )
        self.assertRegex(
            response.content.decode(),
            r"font-family: 'Share Tech Mono';\s*font-weight: 700",
        )

    def test_render_displays_clock_logo_when_present(self):
        clock = Clock.objects.create(name="Studio Clock")
        Clock.objects.filter(pk=clock.pk).update(logo="logos/studio-clock.png")

        response = self.client.get(reverse("clock:render", args=[clock.pk]))

        self.assertContains(response, 'class="clock-branding-logo"')
        self.assertNotContains(response, "clock-branding-name")


class ClockUploadFormTests(TestCase):
    def test_create_and_edit_forms_use_multipart_encoding(self):
        user = User.objects.create_superuser(
            username="clock-admin",
            password="password",
        )
        self.client.force_login(user)
        clock = Clock.objects.create(name="Studio Clock")

        for url in (
            reverse("clock:create"),
            reverse("clock:edit", args=[clock.pk]),
        ):
            with self.subTest(url=url):
                self.assertContains(
                    self.client.get(url),
                    'enctype="multipart/form-data"',
                )
