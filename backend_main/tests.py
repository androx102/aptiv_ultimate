from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from .models import *
import pathlib

templates_dir = pathlib.Path(__file__).resolve().parent / "templates" / "backend_main"
partials_dir = pathlib.Path(__file__).resolve().parent / "templates" / "partials"



class LoginViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        cls.token = str(AccessToken.for_user(cls.user)) 
        cls.sign_in_url = reverse("sign_in") 
        cls.index_url = reverse("index")  
        cls.sign_in_template = f"{templates_dir}/sign-in.html"

    def setUp(self):
        self.client = Client()
        

    def test_redirect_for_logged_user(self):
        """If user is logged in, they should be redirected to the index page."""
        self.client.cookies["access_token"] = self.token
        
        response = self.client.get(self.sign_in_url)

        self.assertEqual(response.status_code, 302)  
        self.assertRedirects(response, self.index_url)


    def test_dispaly_for_not_logged_user(self):
        """If user is not logged in, they should see the login page."""
        response = self.client.get(self.sign_in_url)
        
        self.assertEqual(response.status_code, 200)  
        self.assertTemplateUsed(response, self.sign_in_template)


class LoginAPITest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        cls.token = str(AccessToken.for_user(cls.user))
        cls.sing_in_api_url = reverse("sign_in_api") 
        cls.index_url = reverse("index")  

    def setUp(self):
        self.client = Client()

    def test_redirect_for_logged_user(self):
        """If the user is already logged in, they should be redirected to the index page."""
        self.client.cookies["access_token"] = self.token

        response = self.client.post(self.sing_in_api_url, {"username": "testuser", "password": "testpass"})
            
        self.assertEqual(response.status_code, 302)  
        self.assertRedirects(response, self.index_url)

    def test_logging_in(self):
        """Valid credentials should log in the user, set cookies, and redirect to index."""
        response = self.client.post(self.sing_in_api_url, {"username": "testuser", "password": "testpass"})
        
        self.assertEqual(response.status_code, 200)  
        self.assertIn("access_token", response.cookies)  
        self.assertEqual(response.cookies["access_token"].value != "", True)  

    def test_invalid_credentials(self):
        """Invalid credentials should return a 401 Unauthorized status."""
        response = self.client.post(self.sing_in_api_url, {"username": "testuser", "password": "wrongpass"})
        
        self.assertEqual(response.status_code, 401)  
        self.assertNotIn("access_token", response.cookies)  



class RegisterViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="testuser", password="testpass")
        cls.token = str(AccessToken.for_user(cls.user)) 

        cls.sign_up_url = reverse("sign_up") 
        cls.index_url = reverse("index")  
        cls.sign_in_template = f"{templates_dir}/sign-up.html"

    def setUp(self):
        self.client = Client()

    def test_redirect_for_logged_user(self):
        """If user is logged in, they should be redirected to the index page."""
        self.client.cookies["access_token"] = self.token
        
        response = self.client.get(self.sign_up_url)

        self.assertEqual(response.status_code, 302)  
        self.assertRedirects(response, self.index_url)
    

    def test_dispaly_for_not_logged_user(self):
        """If user is not logged in, they should see the sing-up page."""
        response = self.client.get(self.sign_up_url)
        
        self.assertEqual(response.status_code, 200)  
        self.assertTemplateUsed(response, self.sign_in_template)


class RegisterAPITest(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        self.client = Client()
        self.sign_up_api_url = reverse('sign_up_api') 
        self.index_url = reverse('index')  

    def test_redirect_for_logged_user(self):
        """Test that logged-in users are redirected to the index page."""
        
        user = get_user_model().objects.create_user(username="testuser", password="testpass")
        token = str(AccessToken.for_user(user))
        self.client.cookies["access_token"] = token


        valid_data = {
            'username': 'newuser',
            'password': 'newpassword123',
            'email': 'newuser@example.com',
        }

        response = self.client.post(self.sign_up_api_url, valid_data)    
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.index_url)

    def test_sign_up(self):
        """Test that a valid sign-up request returns a 201 status code."""
        valid_data = {
            'username': 'newuser',
            'password': 'newpassword123',
            'email': 'newuser@example.com',
        }

        response = self.client.post(self.sign_up_api_url, valid_data)

        self.assertEqual(response.status_code, 201)
        user = get_user_model().objects.get(username="newuser")
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'newuser@example.com')

    def test_invalid_data(self):
        """Test that invalid data returns a 400 Bad Request status code."""
        invalid_data = {
            'username': 'newuser',
            'password': 'short',  
            'email': 'invalid-email',
        }

        response = self.client.post(self.sign_up_api_url, invalid_data)

        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response.json())



class ProcessBrowserViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        cls.token = str(AccessToken.for_user(cls.user)) 
        cls.proc_browser_view = reverse("processes") 
        cls.sing_in_url = reverse("sign_in")  
        cls.proc_browser_template = f"{templates_dir}/proc-browser.html"

    def setUp(self):
        self.client = Client()
        
    def test_acess_denied(self):
        response = self.client.get(self.proc_browser_view)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.sing_in_url)
        
    def test_has_acess(self):
        self.client.cookies["access_token"] = self.token
        response = self.client.get(self.proc_browser_view)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.proc_browser_template)
        
        
class ProcessBrowserKillAPITest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        cls.token = str(AccessToken.for_user(cls.user)) 
        cls.kill_proc_api = reverse("kill_proc") 
        cls.sing_in_url = reverse("sign_in")  

    def setUp(self):
        self.client = Client()

    def test_acess_denied(self):
        
        valid_data = {
            "KillLog_Author": self.user,
            "KillLog_Process_Name": "proc_name",
            "KillLog_Process_Id": 2137,
        }

        response = self.client.post(self.kill_proc_api,valid_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.sing_in_url)
        

        
class ProcessBrowserSnapAPITest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        cls.token = str(AccessToken.for_user(cls.user)) 
        cls.take_snapshot_api = reverse("take_snapshot") 
        cls.sing_in_url = reverse("sign_in")

    def setUp(self):
        self.client = Client()

    def test_acess_denied(self):
        
        valid_data = {
            "snapshot_author": self.user,
        }

        response = self.client.post(self.take_snapshot_api,valid_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.sing_in_url)
        
        
class SnapshotBrowserViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        cls.token = str(AccessToken.for_user(cls.user)) 
        cls.snapshots_url = reverse("snapshots") 
        cls.sing_in_url = reverse("sign_in")
        cls.snapshots_template = f"{templates_dir}/snapshots.html"

    def setUp(self):
        self.client = Client()

    def test_acess_denied(self):        
        response = self.client.get(self.snapshots_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.sing_in_url)
        
    def test_has_access(self):
        self.client.cookies["access_token"] = self.token
        response = self.client.get(self.snapshots_url)
        self.assertEqual(response.status_code, 200)  
        self.assertTemplateUsed(response, self.snapshots_template)
        
        
    #Need to fix this !!!
    def Atest_deleted_snapshot(self):
        self.test_snap_object = SnapshotObject.objects.create(
            snapshot_author=self.user,
        )

        self.assertTrue(SnapshotObject.objects.filter(snapshot_id=self.test_snap_object.snapshot_id).exists())
        
        self.client.cookies["access_token"] = self.token
        valid_data = {
            "snapshot_id": int(self.test_snap_object.snapshot_id),
        }
        response = self.client.delete(self.snapshots_url, valid_data)
        print(response.json())
        self.assertEqual(response.status_code, 200)  
        self.assertFalse(SnapshotObject.objects.filter(snapshot_id=self.test_snap_object.snapshot_id).exists())
        #self.assertTemplateUsed(response, self.snap_details_template)
        
class SnapshotDetailsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        cls.token = str(AccessToken.for_user(cls.user)) 
        cls.snapshots_url = reverse("snapshots") 
        cls.sing_in_url = reverse("sign_in")
        cls.snap_details_template = f"{templates_dir}/snap_details.html"
        

    def setUp(self):
        self.client = Client()
        self.test_snap_object = SnapshotObject.objects.create(
            snapshot_author=self.user,
        )

        self.assertTrue(SnapshotObject.objects.filter(snapshot_id=self.test_snap_object.snapshot_id).exists())


    def test_acess_denied(self):        
        response = self.client.get(f"{self.snapshots_url}?snap_id={self.test_snap_object.snapshot_id}")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.sing_in_url)
        
    def test_has_access(self):
        self.client.cookies["access_token"] = self.token
        response = self.client.get(f"{self.snapshots_url}?snap_id={self.test_snap_object.snapshot_id}")
        self.assertEqual(response.status_code, 200)  
        self.assertTemplateUsed(response, self.snap_details_template)
        
