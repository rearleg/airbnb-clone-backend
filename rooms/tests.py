from rest_framework.test import APITestCase
from . import models
from users.models import User


class TestAmenities(APITestCase):

    NAME = "Amenity Test"
    DESC = "Des"
    URL = "/api/v1/rooms/amenities/"

    def setUp(self):
        models.Amenity.objects.create(name=self.NAME, description=self.DESC)

    def test_all_amenities(self):

        response = self.client.get(self.URL)
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "Status code isn't 200.",
        )
        self.assertIsInstance(
            data,
            list,
        )
        self.assertEqual(
            len(data),
            1,
        )
        self.assertEqual(
            data[0]["name"],
            self.NAME,
        )
        self.assertEqual(
            data[0]["description"],
            self.DESC,
        )

    def test_create_amenity(self):

        new_ameneity_name = "new Amenity"
        new_amenitiy_description = "New Amenity Code."

        response = self.client.post(
            self.URL,
            data={
                "name": new_ameneity_name,
                "description": new_amenitiy_description,
            },
        )
        data = response.json()
        self.assertEqual(
            response.status_code,
            200,
            "Not 200 status code.",
        )
        self.assertEqual(
            data["name"],
            new_ameneity_name,
        )
        self.assertEqual(
            data["description"],
            new_amenitiy_description,
        )

        # long name test
        response = self.client.post(
            self.URL,
            data={
                "name": "a" * 151,
                "description": new_amenitiy_description,
            },
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.post(self.URL)
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertIn("name", data)


class TestAmenity(APITestCase):

    NAME = "Test Amenity"
    DESC = "Test Dsc"
    URL = "/api/v1/rooms/amenities/1/"

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_amenity_not_found(self):

        response = self.client.get("/api/v1/rooms/amenities/2/")

        self.assertEqual(response.status_code, 404)

    def test_get_amenity(self):

        response = self.client.get(self.URL)

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(
            data["name"],
            self.NAME,
        )
        self.assertEqual(
            data["description"],
            self.DESC,
        )

    def test_put_amenity(self):

        new_name = "곰 세마리"
        new_description = "가 한 집에 있어."

        # name put test
        response = self.client.put(self.URL, data={"name": new_name})
        data = response.json()
        self.assertEqual(
            response.status_code,
            200,
            "Not 200 status code.",
        )
        self.assertEqual(
            data["name"],
            new_name,
        )

        # descritipn put test
        response = self.client.put(self.URL, data={"description": new_description})
        data = response.json()
        self.assertEqual(
            response.status_code,
            200,
            "Not 200 status code.",
        )
        self.assertEqual(
            data["description"],
            new_description,
        )

        # long name test
        response = self.client.put(self.URL, data={"name": "a" * 151})
        self.assertEqual(response.status_code, 400)

    def test_delete_amenity(self):

        response = self.client.delete(self.URL)
        self.assertEqual(response.status_code, 204)


class TestRooms(APITestCase):

    def setUp(self):
        user = User.objects.create(username="test")
        user.set_password("123")
        user.save()
        self.user = user

    def test_create_room(self):

        response = self.client.post("/api/v1/rooms/")

        self.assertEqual(response.status_code, 403)

        self.client.force_login(
            self.user,
        )
        response = self.client.post("/api/v1/rooms/")
        print(response.json())
