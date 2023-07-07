from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Songs
from .serializers import SongsSerializer

class BaseViewTest(APITestCase):
    client = APIClient()
    
    @staticmethod
    def create_song(title="", artist=""):
        if title != "" and artist != "":
            Songs.objects.create(title=title, artist=artist)

    def setUp(self):
        self.create_song("feels", "davido")
        self.create_song("afire love", "ed sheeran")
        self.create_song("f.n", "lil tjay")
        self.create_song("give me love", "ed sheeran")

class GetAllSongsTest(BaseViewTest):
    def test_get_all_songs(self):
        response = self.client.get(
            reverse("songs-all", kwargs={"version": "v1"})
        )
        
        expected = Songs.objects.all()
        serialized = SongsSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)