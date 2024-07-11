from django.test import TestCase


class TestGame(TestCase):

    def test_status_code(self):
        response = self.client.get('/game-shop/')
        self.assertEqual(response.status_code, 200)