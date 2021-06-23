from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from images.serializers import ImageCreateSerializer


class SerializerTest(APITestCase):
    """Test that serializer works as expected"""
    fixtures = ['account/fixtures/dump.json', 'images/fixtures/dump.json']

    def setUp(self):
        self.data = {
            "url": 'https://cdn.mos.cms.futurecdn.net/tW2sFPx3Uu6caULTtrsD8Y-320-80.jpg',
            "title": 'amazing picture from the world',
            "description": 'there is amazing thign in the world and you have to'
                           'understand them super amazingly for your own view'
        }

    def test_serializer_validate_url(self):
        """Test that validating url works as expected"""

        serializer = ImageCreateSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_not_valid_url(self):
        """Test that validating url not work with png extension"""
        self.data['url'] = 'www.somebadthing.png'
        serializer = ImageCreateSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
