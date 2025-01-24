"""
Tests for IntegrationTestCase class hook functions.
"""

# System Imports.
from unittest.mock import patch

# Third-Party Imports.
from django.contrib.auth.models import AnonymousUser
from pytest import warns

# Internal Imports.
from django_expanded_test_cases import IntegrationTestCase


# region Verify Hook Function Access


class IntegrationHookTestCase(IntegrationTestCase):

    @classmethod
    @patch('django_expanded_test_cases.mixins.core_mixin.ETC_AUTO_GENERATE_USERS_IN_SETUPTESTDATA', True)
    def setUpTestData(cls, *args, **kwargs):
        """Override setting for faster tests."""
        super().setUpTestData(*args, **kwargs)

    @patch('django_expanded_test_cases.mixins.core_mixin.ETC_AUTO_GENERATE_USERS_IN_SETUPTESTDATA', True)
    def setUp(self, *args, **kwargs):
        """Override setting for faster tests."""
        super().setUp(*args, **kwargs)


class TestIntegrationHooks__CanAccessPreBuiltinHook(IntegrationHookTestCase):
    """Tests to ensure _assertResponse__pre_builtin_tests() hook function can be accessed.

    Separate class to ensure other tests don't potentially affect state of class.
    """

    def test_hook_is_called(self):
        """Verifies hook function is called and changes state as expected."""

        # Verify initial state of class variable.
        self.assertEqual(True, self.hook_checks.pre_assert_is_okay)

        # Call a basic assertResponse.
        # We don't even care if it works, this is only to trigger the hook function.
        self.assertResponse('')

        # Verify variable changed after call. This variable is only changed in the hook function.
        self.assertEqual(False, self.hook_checks.pre_assert_is_okay)


class TestIntegrationHooks__CanAccessPostBuiltinHook(IntegrationHookTestCase):
    """Tests to ensure _assertResponse__post_builtin_tests() hook function can be accessed.

    Separate class to ensure other tests don't potentially affect state of class.
    """

    def test_hook_is_called(self):
        """Verifies hook function is called and changes state as expected."""

        # Verify initial state of class variable.
        self.assertEqual(True, self.hook_checks.post_assert_is_okay)

        # Call a basic assertResponse.
        # We don't even care if it works, this is only to trigger the hook function.
        self.assertResponse('')

        # Verify variable changed after call. This variable is only changed in the hook function.
        self.assertEqual(False, self.hook_checks.post_assert_is_okay)


class TestIntegrationHooks__CanAccessAuthSetupHook(IntegrationHookTestCase):
    """Tests to ensure _get_login_user__extra_user_auth_setup() hook function can be accessed.

    Separate class to ensure other tests don't potentially affect state of class.
    """

    def test_hook_is_called(self):
        """Verifies hook function is called and changes state as expected.

        Note: This hook is only called if assertion has a user to try to auth with.
        """

        # Verify initial state of class variable.
        self.assertEqual(True, self.hook_checks.auth_setup_is_okay)

        # Call a basic assertResponse.
        # We don't even care if it works, this is only to trigger the hook function.
        self.assertResponse(
            '',
            user=self.test_user,
        )

        # Verify variable changed after call. This variable is only changed in the hook function.
        self.assertEqual(False, self.hook_checks.auth_setup_is_okay)


# endregion Verify Hook Function Access


# region Hook Warning Functionality


class TestIntegrationHooks__HookRaisesWarning(IntegrationHookTestCase):
    """Tests to ensure appropriate warnings raise with hook logic.

    Separate class to ensure other tests don't potentially affect state of class.
    """

    expected_warn_msg = (
        "Supplemental args/kwargs have been provided to an assertResponse statement. "
        "Any supplemental args/kwargs are exclusively used to provide custom data to "
        "built-in hook functions, but no hook functions seem to be implemented for your project. "
        "Either remove the use of args/kwargs in the assertion, or implement one of the hook functions."
    )

    def test_warning_raises_with_args__with_anonymous_user(self):
        """Verify arg/kwarg warning raises when user is anonymous."""

        with warns(Warning) as warning_msgs:
            self.assertResponse(
                '',
                'extra_test_arg',
                user=AnonymousUser,
            )
        self.assertText(self.expected_warn_msg, warning_msgs[0].message.args[0])

    def test_warning_raises_with_args__with_real_user(self):
        """Verify arg/kwarg warning raises when user is present."""

        with warns(Warning) as warning_msgs:
            self.assertResponse(
                '',
                'extra_test_arg',
                user=self.test_user,
            )
        self.assertText(self.expected_warn_msg, warning_msgs[0].message.args[0])

    def test_warning_raises_with_kwargs__with_anonymous_user(self):
        """Verify arg/kwarg warning raises when user is anonymous."""

        with warns(Warning) as warning_msgs:
            self.assertResponse(
                '',
                user=AnonymousUser,
                extra_test_kwarg="extra_test_value",
            )
        self.assertText(self.expected_warn_msg, warning_msgs[0].message.args[0])

    def test_warning_raises_with_kwargs__with_real_user(self):
        """Verify arg/kwarg warning raises when user is present."""

        with warns(Warning) as warning_msgs:
            self.assertResponse(
                '',
                user=self.test_user,
                extra_test_kwarg="extra_test_value",
            )
        self.assertText(self.expected_warn_msg, warning_msgs[0].message.args[0])


class TestIntegrationHooks__PreBuiltinHookAffectsWarning(IntegrationHookTestCase):
    """Tests to ensure appropriate warnings are affected by implementation of
    _assertResponse__pre_builtin_tests() hook.

    Separate class to ensure other tests don't potentially affect state of class.
    """

    def _assertResponse__pre_builtin_tests(
        self,
        *args,
        **kwargs,
    ):
        """Implement PreBuiltin hook.
        It doesn't have to do anything, we just want it implemented to verify class logic.
        """
        pass

    def test_warning_does_not_raise_with_args__with_anonymous_user(self):
        """Verify arg/kwarg warning does not raise when user is anonymous."""

        self.assertResponse(
            '',
            'extra_test_arg',
            user=AnonymousUser,
        )

    def test_warning_does_not_raise_with_args__with_real_user(self):
        """Verify arg/kwarg warning does not raise when user is present."""

        self.assertResponse(
            '',
            'extra_test_arg',
            user=self.test_user,
        )

    def test_warning_does_not_raise_with_kwargs__with_anonymous_user(self):
        """Verify arg/kwarg warning does not raise when user is anonymous."""

        self.assertResponse(
            '',
            user=AnonymousUser,
            extra_test_kwarg="extra_test_value",
        )

    def test_warning_does_not_raise_with_kwargs__with_real_user(self):
        """Verify arg/kwarg warning does not raise when user is present."""

        self.assertResponse(
            '',
            user=self.test_user,
            extra_test_kwarg="extra_test_value",
        )


class TestIntegrationHooks__PostBuiltinHookAffectsWarning(IntegrationHookTestCase):
    """Tests to ensure appropriate warnings are affected by implementation of
    _assertResponse__post_builtin_tests() hook.

    Separate class to ensure other tests don't potentially affect state of class.
    """

    def _assertResponse__post_builtin_tests(
        self,
        *args,
        **kwargs,
    ):
        """Implement PostBuiltin hook.
        It doesn't have to do anything, we just want it implemented to verify class logic.
        """
        pass

    def test_warning_does_not_raise_with_args__with_anonymous_user(self):
        """Verify arg/kwarg warning does not raise when user is anonymous."""

        self.assertResponse(
            '',
            'extra_test_arg',
            user=AnonymousUser,
        )

    def test_warning_does_not_raise_with_args__with_real_user(self):
        """Verify arg/kwarg warning does not raise when user is present."""

        self.assertResponse(
            '',
            'extra_test_arg',
            user=self.test_user,
        )

    def test_warning_does_not_raise_with_kwargs__with_anonymous_user(self):
        """Verify arg/kwarg warning does not raise when user is anonymous."""

        self.assertResponse(
            '',
            user=AnonymousUser,
            extra_test_kwarg="extra_test_value",
        )

    def test_warning_does_not_raise_with_kwargs__with_real_user(self):
        """Verify arg/kwarg warning does not raise when user is present."""

        self.assertResponse(
            '',
            user=self.test_user,
            extra_test_kwarg="extra_test_value",
        )


class TestIntegrationHooks__CanAccessAuthSetupHookAffectsWarning(IntegrationHookTestCase):
    """Tests to ensure appropriate warnings are affected by implementation of
    _get_login_user__extra_user_auth_setup() hook.

    Separate class to ensure other tests don't potentially affect state of class.
    """

    def _get_login_user__extra_user_auth_setup(
        self,
        user,
        *args,
        **kwargs,
    ):
        """Implement UserAuthSetup hook.
        It doesn't have to do anything, we just want it implemented to verify class logic.
        """

        # This hook requires a return value of the actual user object.
        return user

    def test_warning_does_not_raise_with_args__with_anonymous_user(self):
        """Verify arg/kwarg warning does not raise when user is anonymous."""

        self.assertResponse(
            '',
            'extra_test_arg',
            user=AnonymousUser,
        )

    def test_warning_does_not_raise_with_args__with_real_user(self):
        """Verify arg/kwarg warning does not raise when user is present."""

        self.assertResponse(
            '',
            'extra_test_arg',
            user=self.test_user,
        )

    def test_warning_does_not_raise_with_kwargs__with_anonymous_user(self):
        """Verify arg/kwarg warning does not raise when user is anonymous."""

        self.assertResponse(
            '',
            user=AnonymousUser,
            extra_test_kwarg="extra_test_value",
        )

    def test_warning_does_not_raise_with_kwargs__with_real_user(self):
        """Verify arg/kwarg warning does not raise when user is present."""

        self.assertResponse(
            '',
            user=self.test_user,
            extra_test_kwarg="extra_test_value",
        )


# endregion Hook Warning Functionality
