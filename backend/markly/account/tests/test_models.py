from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from account.models import Contact


class ModelTest(APITestCase):
    """Testing Contact model and follow system"""
    fixtures = ['account/fixtures/dump.json']

    def test_follow_system(self):
        """Test that following works as expected"""
        a, b, c = get_user_model().objects.all()[:3]

        Contact.objects.create(follow_from=a, follow_to=b)
        Contact.objects.create(follow_from=a, follow_to=c)
        Contact.objects.create(follow_from=b, follow_to=c)

        self.assertIn(b, a.following.all())
        self.assertIn(c, a.following.all())
        self.assertIn(a, c.followers.all())
        self.assertIn(b, c.followers.all())
        self.assertNotIn(a, c.following.all())
        self.assertNotIn(b, c.following.all())
