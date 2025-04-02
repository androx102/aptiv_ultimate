from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
import pathlib
import unittest
from rest_framework_simplejwt.tokens import AccessToken
from .models import *


templates_dir = pathlib.Path(__file__).resolve().parent / "templates" / "backend_main"
partials_dir = pathlib.Path(__file__).resolve().parent / "templates" / "partials"

SKIP_OLD_TESTS = False


class AcessTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        cls.token = str(AccessToken.for_user(cls.user))

        cls.protected_views_endpoints = [
            {
                "url": reverse("processes"),
                "template": f"{templates_dir}/proc-browser.html",
            },
            {
                "url": reverse("snapshots"),
                "template": f"{templates_dir}/snapshots.html",
            },
            {"url": reverse("kill-log"), "template": f"{templates_dir}/kill-log.html"},
        ]

        cls.protected_api_endpoints = [
            reverse("take_snapshot"),
            reverse("kill_proc"),
            reverse("export_snap"),
        ]

        cls.sign_in_url = reverse("sign_in")
        cls.sign_in_template = f"{templates_dir}/sign-in.html"
        cls.sign_up_url = reverse("sign_up")
        cls.sign_up_template = f"{templates_dir}/sign-up.html"
        cls.index_url = reverse("index")
        cls.index_template = f"{templates_dir}/index.html"

        cls.sign_in_api_url = reverse("sign_in_api")
        cls.sign_up_api_url = reverse("sign_up_api")

    def setUp(self):
        self.client = Client()

    @unittest.skipIf(SKIP_OLD_TESTS, "Skipping old tests")
    def test_not_logged_user_acess(self):
        for endpoint in self.protected_views_endpoints:
            response = self.client.get(endpoint["url"])
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, self.sign_in_url)

        for endpoint in self.protected_api_endpoints:
            response = self.client.get(endpoint)
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, self.sign_in_url)

        response = self.client.get(self.sign_in_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.sign_in_template)

        response = self.client.get(self.sign_up_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.sign_up_template)

        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.index_template)

    # @unittest.skipIf(SKIP_OLD_TESTS, "Skipping old tests")
    def test_user_logged_get_view(self):
        self.client.cookies["access_token"] = self.token

        for endpoint in self.protected_views_endpoints:
            response = self.client.get(endpoint["url"])
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, endpoint["template"])

        response = self.client.get(self.sign_in_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.index_url)

        response = self.client.get(self.sign_up_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.index_url)

        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.index_template)

        response = self.client.post(self.sign_in_api_url)
        self.assertEqual(response.status_code, 302)  # issue here
        self.assertRedirects(response, self.index_url)

        response = self.client.post(self.sign_up_api_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.index_url)


########## Auth ##########


class LoginAPITest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        cls.sing_in_api_url = reverse("sign_in_api")

    def setUp(self):
        self.client = Client()
        self.valid_data = {"username": "testuser", "password": "testpass"}

    @unittest.skipIf(SKIP_OLD_TESTS, "Skipping old tests")
    def test_sign_in_sucess(self):
        """Valid credentials should log in the user, set cookies, and redirect to index."""
        response = self.client.post(self.sing_in_api_url, self.valid_data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.cookies)
        self.assertEqual(response.cookies["access_token"].value != "", True)

    @unittest.skipIf(SKIP_OLD_TESTS, "Skipping old tests")
    def test_sign_in_invalid_credentials_fail(self):
        """Invalid credentials should return a 401 Unauthorized status."""
        self.valid_data["password"] = "wrongpassword"
        response = self.client.post(self.sing_in_api_url, self.valid_data)

        self.assertEqual(response.status_code, 401)
        self.assertNotIn("access_token", response.cookies)


class RegisterAPITest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        cls.sign_up_api_url = reverse("sign_up_api")

    def setUp(self):
        self.client = Client()
        self.existing_user_data = {
            "username": "testuser",
            "password": "testpass",
            "email": "testuser@example.com",
        }
        self.valid_user_data = {
            "username": "newuser",
            "password": "newpassword123",
            "email": "newuser@example.com",
        }

    @unittest.skipIf(SKIP_OLD_TESTS, "Skipping old tests")
    def test_sign_up_sucess(self):
        """Test that a valid sign-up request returns a 201 status code."""

        response = self.client.post(self.sign_up_api_url, self.valid_user_data)
        user = get_user_model().objects.get(username="newuser")

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "newuser@example.com")

    @unittest.skipIf(SKIP_OLD_TESTS, "Skipping old tests")
    def test_sign_up_invalid_data_fail(self):
        """Test that invalid data returns a 400 Bad Request status code."""

        self.valid_user_data["email"] = "invalid-email"

        response = self.client.post(self.sign_up_api_url, self.valid_user_data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.json())

    @unittest.skipIf(SKIP_OLD_TESTS, "Skipping old tests")
    def test_username_or_email_already_taken_fail(self):
        response = self.client.post(self.sign_up_api_url, self.existing_user_data)
        self.assertEqual(response.status_code, 400)


########## Process browser ##########
class ProcessBrowserViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        cls.token = str(AccessToken.for_user(cls.user))
        cls.proc_browser_view = reverse("processes")
        cls.proc_table_template = f"{partials_dir}/proc_table.html"

    def setUp(self):
        self.client = Client()
        self.client.cookies["access_token"] = self.token

    @unittest.skipIf(SKIP_OLD_TESTS, "Skipping old tests")
    def test_get_partial_view(self):
        response = self.client.get(
            self.proc_browser_view, headers={"HX-Request": "true"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.proc_table_template)


class ProcessBrowserKillAPITest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        cls.token = str(AccessToken.for_user(cls.user))
        cls.kill_proc_api = reverse("kill_proc")

    def setUp(self):
        self.client = Client()
        self.client.cookies["access_token"] = self.token
        self.valid_data = {
            "pid": 2137,
            "proc_name": "test_proc_name",
        }

    @unittest.skipIf(SKIP_OLD_TESTS, "Skipping old tests")
    @override_settings(DUMMY_PROCESS_DATA=True)
    def test_kill_process_sucess(self):
        self.valid_data["pid"] = "2137"
        response = self.client.post(self.kill_proc_api, self.valid_data)
        self.assertEqual(response.status_code, 200)

    @unittest.skipIf(SKIP_OLD_TESTS, "Skipping old tests")
    @override_settings(DUMMY_PROCESS_DATA=True)
    def test_kill_process_invalid_pid_fail(self):
        self.valid_data["pid"] = "420"
        response = self.client.post(self.kill_proc_api, self.valid_data)
        self.assertEqual(response.status_code, 400)


class ProcessBrowserSnapAPITest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        cls.token = str(AccessToken.for_user(cls.user))
        cls.take_snapshot_api = reverse("take_snapshot")

    def setUp(self):
        self.client = Client()
        self.client.cookies["access_token"] = self.token

    @unittest.skipIf(SKIP_OLD_TESTS, "Skipping old tests")
    @override_settings(DUMMY_PROCESS_DATA=True)
    def test_take_snapshot_sucess(self):
        response = self.client.get(self.take_snapshot_api)
        self.assertEqual(response.status_code, 200)

    #########################################################
    @unittest.skipIf(SKIP_OLD_TESTS, "Skipping old tests")
    @override_settings(DUMMY_PROCESS_DATA=False)
    def test_take_snapshot_fail(self):
        response = self.client.get(self.take_snapshot_api)

    # self.assertEqual(response.status_code, 500)

    #########################################################


########## Snapshot browser ##########
class SnapshotBrowserViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        cls.token = str(AccessToken.for_user(cls.user))
        cls.snapshots_url = reverse("snapshots")
        cls.snap_details_template = f"{templates_dir}/snap_details.html"
        cls.snap_table_template = f"{partials_dir}/snap_table.html"

    def setUp(self):
        self.client = Client()
        self.client.cookies["access_token"] = self.token
        self.test_snap_object = SnapshotObject.objects.create(
            snapshot_author=self.user,
        )

        self.assertTrue(
            SnapshotObject.objects.filter(
                snapshot_id=self.test_snap_object.snapshot_id
            ).exists()
        )

    @unittest.skipIf(SKIP_OLD_TESTS, "Skipping old tests")
    def test_get_details_correct_id_sucess(self):
        """If user logged in, they should see snaphosts details page."""
        response = self.client.get(
            f"{self.snapshots_url}?snap_id={self.test_snap_object.snapshot_id}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.snap_details_template)

    @unittest.skipIf(SKIP_OLD_TESTS, "Skipping old tests")
    def test_get_details_wrong_id_fail(self):
        response = self.client.get(
            f"{self.snapshots_url}?snap_id={'1dd4f9b0-5a36-490d-a327-4f9d002bd18b'}"
        )
        self.assertEqual(response.status_code, 404)

    @unittest.skipIf(SKIP_OLD_TESTS, "Skipping old tests")
    def test_deleted_snapshot_sucess(self):
        """If snap_ID is valid -> remove from DB, return 200"""
        valid_data = {
            "snapshot_id": self.test_snap_object.snapshot_id,
        }

        response = self.client.delete(
            self.snapshots_url,
            valid_data,
            format="json",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            SnapshotObject.objects.filter(
                snapshot_id=self.test_snap_object.snapshot_id
            ).exists()
        )
        self.assertTemplateUsed(response, self.snap_table_template)

    @unittest.skipIf(SKIP_OLD_TESTS, "Skipping old tests")
    def test_deleted_snapshot_fail(self):
        """If snap_ID is not valid ->return 404"""
        valid_data = {
            "snapshot_id": "1dd4f9b0-5a36-490d-a327-4f9d002bd18b",
        }

        response = self.client.delete(
            self.snapshots_url,
            valid_data,
            format="json",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)


################ DRAFTS ################
class SnapshotExportAPITest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        cls.token = str(AccessToken.for_user(cls.user))
        cls.snapshots_export_url = reverse("export_snap")

    def setUp(self):
        self.client = Client()
        self.client.cookies["access_token"] = self.token
        self.test_snap_object = SnapshotObject.objects.create(
            snapshot_author=self.user,
        )

        self.assertTrue(
            SnapshotObject.objects.filter(
                snapshot_id=self.test_snap_object.snapshot_id
            ).exists()
        )

    @unittest.skipIf(SKIP_OLD_TESTS, "Skipping old tests")
    def test_export_snapshot_sucess(self):
        valid_data = {"snap_id": self.test_snap_object.snapshot_id}

        response = self.client.get(self.snapshots_export_url, valid_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Disposition"],
            f'attachment; filename="snapshot_{self.test_snap_object.snapshot_id}.xlsx"',
        )
        self.assertEqual(
            response["Content-Type"],
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    @unittest.skipIf(SKIP_OLD_TESTS, "Skipping old tests")
    def test_export_snapshot_fail(self):
        not_valid_data = {"snap_id": "1dd4f9b0-5a36-490d-a327-4f9d002bd18b"}

        response = self.client.get(self.snapshots_export_url, not_valid_data)


class KillLogBrowserViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        cls.token = str(AccessToken.for_user(cls.user))
        cls.kill_log_url = reverse("kill-log")

    def setUp(self):
        self.client = Client()
        self.client.cookies["access_token"] = self.token
        self.test_killlog_object = KillLog_object.objects.create(
            KillLog_Author=self.user,
            KillLog_Process_Name="test process",
            KillLog_Process_Id=2137,
        )

        self.assertTrue(
            KillLog_object.objects.filter(
                KillLog_ID=self.test_killlog_object.KillLog_ID
            ).exists()
        )

    @unittest.skipIf(SKIP_OLD_TESTS, "Skipping old tests")
    def test_remove_kill_log_entry_sucess(self):
        """If kill_id is valid -> remove from DB, return 200"""
        valid_data = {
            "kill_id": self.test_killlog_object.KillLog_ID,
        }

        response = self.client.delete(
            self.kill_log_url,
            valid_data,
            format="json",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            KillLog_object.objects.filter(
                KillLog_ID=self.test_killlog_object.KillLog_ID
            ).exists()
        )

    @unittest.skipIf(SKIP_OLD_TESTS, "Skipping old tests")
    def test_remove_kill_log_entry_fail(self):
        """If kill_id is not valid -> return 400"""
        not_valid_data = {
            "kill_id": "1dd4f9b0-5a36-490d-a327-4f9d002bd18b",
        }
        response = self.client.delete(
            self.kill_log_url,
            not_valid_data,
            format="json",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)
