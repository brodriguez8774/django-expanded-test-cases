"""
Core testing logic, universal to all test cases.
"""

# System Imports.
from django.contrib.auth import get_user_model



class CoreTestCaseMixin:
    """Core testing logic, used in all other expanded TestCase classes.

    For compatibility, does not inherit from
        django.test.TestCase
        channels.testing.ChannelsLiveServerTestCase

    Inheriting from either (seems to) make it incompatible with the other.
    Therefore we treat this as a separate mixin that inherits from nothing, and is included in all.
    """

    def set_up(self):
        """
        Acts as the equivalent of the UnitTesting "setUp()" function.

        However, since this is not inheriting from a given TestCase, calling the literal function
        here would override instead.
        """
        # Generate "special case" test user instances.
        # Guarantees that there will always be at least some default User models when tests are run.
        self.test_superuser = get_user_model().objects.create_user(
            username='test_superuser',
            password='password',
            is_superuser=True,
        )
        self.test_admin = get_user_model().objects.create_user(
            username='test_admin',
            password='password',
            is_staff=True,
        )
        self.test_user = get_user_model().objects.create_user(username='test_user', password='password')

    def get_user(self, user, password='password'):
        """Returns user matching provided value.

        :param user: User model, or corresponding username, to use.
        :param password: Password str to assign to user.
        """

        # Check if instance is User model.
        if isinstance(user, get_user_model()):
            # Already User model. This is fine.
            pass

        # Handle all "special cases" for testing logic.
        elif user == 'test_superuser':
            user = self.test_superuser
        elif user == 'test_admin':
            user = self.test_admin
        elif user == 'test_user':
            user = self.test_user

        else:
            # Is not User model. Get or create.
            try:
                user = get_user_model().objects.get(username=str(user))
            except get_user_model().DoesNotExist:
                user = get_user_model().objects.create(username=str(user))

        # Handle passwords.
        password = str(password).strip()
        if len(password) == 0:
            # Empty password. Reset back to default.
            password = 'password'
        user.set_password(password)
        user.unhashed_password = password
        user.save()

        return user
