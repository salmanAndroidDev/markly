import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from account.models import Profile


def build_url_with_query_params(url, args):
    """Append args to url www.asdf.com?id=4&user=salman"""
    assert type(args) == dict
    assert type(url) == str
    URL = url
    if URL[-1] == '/':
        URL = URL[:-1]
    URL = URL + '?'
    for key in args.keys():
        URL = f"{URL}{key}={args[key]}&"
    return URL[:-1]


def create_user(username='dummy', password='dummypass1234'):
    """Handy function to create a user"""
    return get_user_model().objects.create_user(
        username=username, password=password
    )


class TestView(TestCase):
    """
        Test API view
    """
    fixtures = ['account/fixtures/dump.json']

    def setUp(self):
        self.client = APIClient()
        self.user1 = create_user('user1', 'pass1234')
        self.user2 = create_user('user2', 'pass1234')

    @classmethod
    def setUpTestData(cls):
        """Create profile for all imported users"""
        users = get_user_model().objects.all()
        for user in users:
            if not Profile.objects.filter(user=user).exists():
                Profile.objects.create(user=user)

    def test_registration(self):
        """Test that user can be registered"""

        payload = {'user': {
            'username': 'somebody',
            'password': 'pass1234'
        }}
        URL = reverse('account:register')

        response = self.client.post(URL,
                                    json.dumps(payload),
                                    content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(username=payload['user']['username'])
        self.assertTrue(user.check_password(payload['user']['password']))
        profile_exists = Profile.objects.filter(user=user).exists()
        self.assertTrue(profile_exists)

    def test_modify_profile(self):
        """Test that user can modify it's data"""

        profile = Profile.objects.create(user=self.user1)
        Profile.objects.create(user=self.user2)

        payload = {"user": {
            "username": "SalmanAndB",
            "password": "BadPASS1234",
            'first_name': 'Salman',
            'last_name': 'Barani',
            'email': 'salmanAndB@outlook.com'
        }}
        URL = reverse('account:update')

        self.client.force_authenticate(self.user1)
        response = self.client.patch(URL, json.dumps(payload),
                                     content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        profile.refresh_from_db()
        for key in payload['user'].keys():
            if key == 'password':
                is_password_false = profile.user.check_password(payload['user'][key])
                is_password_true = profile.user.check_password('pass1234')
                self.assertFalse(is_password_false)
                self.assertTrue(is_password_true)
            else:
                self.assertEqual(getattr(profile.user, key), payload['user'][key])

    def test_follow_redirect(self):
        """Test that not authenticated users can't access follow view"""
        URL = reverse('account:follow')
        response = self.client.post(URL)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_follow_view(self):
        """Test that follow view works as expected"""
        p1, p2, p3, p4, p5 = Profile.objects.all()[:5]

        URL = build_url_with_query_params(reverse('account:follow'),
                                          {'profile_id': p2.id,
                                           'action': 'follow'})
        self.client.force_login(self.user1)
        response = self.client.post(URL)
        print(response)
