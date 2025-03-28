from django.test import TestCase


class Login_view_test(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        pass

    def redirect_for_logged_user(self):
        # If user logged -> redirect to index
        pass

    def check_not_logged_user(self):
        # If user not logged - should return login page
        pass


class Login_API_test(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        pass

    def redirect_for_logged_user(self):
        # If user logged -> redirect to index
        pass

    def logging_in(self):
        # Pass valid credentials -> should set cookies and redirect to index
        pass

    def invalid_credentials(self):
        # Should throw 401
        pass


class Register_view_test(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        pass

    def redirect_for_logged_user(self):
        # If user logged -> redirect to index
        pass

    def check_not_logged_user(self):
        # If user not logged - should return register page
        pass


class Register_API_test(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        pass

    def redirect_for_logged_user(self):
        # If user logged -> redirect to index
        pass

    def sign_up(self):
        # If data is valid -> should return 201
        pass

    def invalid_data(self):
        # Should throw 401
        pass
