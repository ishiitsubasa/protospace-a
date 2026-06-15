from django.test import TestCase
from tests.factories.users import UserFactory
from time import sleep
from django.core.exceptions import ValidationError

class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.build()

    def test_user_creation(self):
        self.user.full_clean()

    def test_user_nickname_cannot_be_blank(self):
        self.user.nickname = ''
        with self.assertRaises(ValidationError) as cm:
            self.user.full_clean()
        self.assertIn('nickname', cm.exception.message_dict)
        self.assertEqual(cm.exception.message_dict['nickname'], ['このフィールドは空ではいけません。'])

    def test_user_profile_cannot_be_blank(self):
        self.user.profile = ''
        with self.assertRaises(ValidationError) as cm:
            self.user.full_clean()
        self.assertIn('profile', cm.exception.message_dict)
        self.assertEqual(cm.exception.message_dict['profile'], ['このフィールドは空ではいけません。'])

    def test_user_belonging_cannot_be_blank(self):
        self.user.belonging = ''
        with self.assertRaises(ValidationError) as cm:
            self.user.full_clean()
        self.assertIn('belonging', cm.exception.message_dict)
        self.assertEqual(cm.exception.message_dict['belonging'], ['このフィールドは空ではいけません。'])

    def test_email_cannot_be_blank(self):
        self.user.email = ''
        with self.assertRaises(ValidationError) as cm:
            self.user.full_clean()
        self.assertIn('email', cm.exception.message_dict)
        self.assertEqual(cm.exception.message_dict['email'], ['このフィールドは空ではいけません。'])

    def test_unique_email_constraint(self):
        self.user.save()
        sleep(1)
        another_user = UserFactory.build(email=self.user.email)
        with self.assertRaises(ValidationError) as cm:
            another_user.full_clean()
        self.assertIn('email', cm.exception.message_dict)
        self.assertEqual(cm.exception.message_dict['email'], ["この Email を持った Custom user が既に存在します。"])

    def test_nickname_max_length(self):
        self.user.nickname = 'a' * 22
        with self.assertRaises(ValidationError) as cm:
            self.user.full_clean()
        self.assertIn('nickname', cm.exception.message_dict)
        self.assertEqual(cm.exception.message_dict['nickname'], ['このフィールドは最大10文字までです。'])

    def test_password_cannot_be_blank(self):
        self.user.password = ''
        with self.assertRaises(ValidationError) as cm:
            self.user.full_clean()
        self.assertIn('password', cm.exception.message_dict)
        self.assertEqual(cm.exception.message_dict['password'], ['このフィールドは空ではいけません。'])

    def test_password_minimum_length(self):
        self.user.password = 'a'*3
        with self.assertRaises(ValidationError) as cm:
            self.user.full_clean()
        self.assertIn('password', cm.exception.message_dict)
        self.assertEqual(cm.exception.message_dict['password'], ['パスワードは8文字以上で入力してください。'])