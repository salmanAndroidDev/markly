from urllib import request
from django.core.files.base import ContentFile


def download_image(url):
    """Downloads ipg, jpeg fils from given URL"""
    response = request.urlopen(url)
    return ContentFile(response.read())