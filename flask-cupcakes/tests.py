from unittest import TestCase

from app import app
from models import db, Cupcake

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

db.drop_all()
db.create_all()


CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image": "http://test.com/cupcake2.jpg"
}


class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""

        Cupcake.query.delete()

        cupcake = Cupcake(**CUPCAKE_DATA)
        db.session.add(cupcake)
        db.session.commit()

        self.cupcake = cupcake

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

###########E####### Successful Routes ##########################

    def test_list_cupcakes(self):
        with app.test_client() as client:
            resp = client.get("/api/cupcakes")

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
                "cupcakes": [
                    {
                        "id": self.cupcake.id,
                        "flavor": "TestFlavor",
                        "size": "TestSize",
                        "rating": 5,
                        "image": "http://test.com/cupcake.jpg"
                    }
                ]
            })

    def test_get_cupcake(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake.id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image": "http://test.com/cupcake.jpg"
                }
            })

    def test_create_cupcake(self):
        with app.test_client() as client:
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 201)

            json = resp.json

            # don't know what ID we'll get, make sure it's an int & normalize
            self.assertIsInstance(json['cupcake']['id'], int)
            del json['cupcake']['id']

            self.assertEqual(json, {
                "cupcake": {
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 10,
                    "image": "http://test.com/cupcake2.jpg"
                }
            })

            self.assertEqual(Cupcake.query.count(), 2)
    
    def test_update_cupcake(self):
        with app.test_client() as client:
            
            url = f"/api/cupcakes/{self.cupcake.id}"
            self.cupcake.flavor = 'NewFlavor'
            cupcake_data = self.cupcake.serialize()
            resp = client.patch(url, json = cupcake_data)

            self.assertEqual(resp.status_code, 200)
            json = resp.json
            self.assertEqual(json, {
                "cupcake": {
                    "id": self.cupcake.id,
                    "flavor": "NewFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image": "http://test.com/cupcake.jpg"
                }
            })
    def test_delete_cupcake(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.delete(url)

            self.assertEqual(resp.status_code, 200)

            data = resp.json

            self.assertEqual(data, {'message': 'Deleted'})
            self.assertEqual(Cupcake.query.count(), 0)

    ##################### Bad Routes ###########################
    def test_bad_get(self):
        with app.test_client() as client:
            url= f'/api/cupcakes/a'
            resp = client.get(url)
            self.assertEqual(resp.status_code, 404)

    def test_bad_update(self):
        with app.test_client() as client:
            url= f'/api/cupcakes/a'
            resp = client.patch(url, json = CUPCAKE_DATA)
            self.assertEqual(resp.status_code, 404)
    def test_bad_delete(self):
        with app.test_client() as client:
            url= f'/api/cupcakes/a'
            resp = client.delete(url)
            self.assertEqual(resp.status_code, 404)