from shelve import Shelf
from unittest import TestCase

from app import app
from models import db, Pet, update_db
from forms import AddPetForm

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet_shop_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Don't req CSRF for testing
app.config['WTF_CSRF_ENABLED'] = False

db.drop_all()
db.create_all()


class PetViewTestCase(TestCase):
    """Tests pet shop view functions."""
    
    def setUp(self):
        """Make demo data."""

        Pet.query.delete()
        pet = Pet(name="Test_Pet", species="dog")
        update_db(pet)

        self.pet_id = pet.id

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()
    
    #  Test get routes
    def test_get_home_page(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test_Pet', html)

    def test_get_add_pet(self):
        with app.test_client() as client:
            resp = client.get("/add")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<input class="form-control" id="name" name="name" required type="text" value="">', html)

    def test_get_edit_pet(self):
        with app.test_client() as client:
            resp = client.get(f"/{self.pet_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test_Pet", html)
    
    # Test post routes

    def test_post_add_pet(self):
        with app.test_client(self) as client:
            p ={'name': 'ginger', 'species':'cat'}
            resp = client.post("/add", data = p, follow_redirects = True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('fgdfdg', html)
    # def test_user_edit(self):
    #     with app.test_client() as client:
    #         resp = client.post(
    #             f"/users/{self.user_id}/edit",
    #             data={'name': 'Test2', 'email': "test2@test.com"},
    #             follow_redirects=True)
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn(f"User {self.user_id} updated!", html)

    #         user = User.query.get(self.user_id)
    #         self.assertEquals(user.name, "Test2")
    #         self.assertEquals(user.email, "test2@test.com")
    # def test_post_edit_pet(self):
    #     with app.test_client() as client:
    #         resp = client.get(f"/{self.pet_id}")
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn("Test_Pet", html)



    
    # def test_add_pet_fail(self): 
    #     with app.test_client() as

# class UserViewsTestCase(TestCase):
#     """Tests for views for Users."""


#     def test_user_edit_form(self):
#         with app.test_client() as client:
#             resp = client.get(f"/users/{self.user_id}/edit")
#             html = resp.get_data(as_text=True)

#             self.assertEqual(resp.status_code, 200)
#             self.assertIn("<form", html)

#     def test_user_edit(self):
#         with app.test_client() as client:
#             resp = client.post(
#                 f"/users/{self.user_id}/edit",
#                 data={'name': 'Test2', 'email': "test2@test.com"},
#                 follow_redirects=True)
#             html = resp.get_data(as_text=True)

#             self.assertEqual(resp.status_code, 200)
#             self.assertIn(f"User {self.user_id} updated!", html)

#             user = User.query.get(self.user_id)
#             self.assertEquals(user.name, "Test2")
#             self.assertEquals(user.email, "test2@test.com")

#     def test_user_edit_form_fail(self):
#         with app.test_client() as client:
#             # add w/ invalid email
#             resp = client.post(
#                 f"/users/{self.user_id}/edit",
#                 data={'name': 'Test3', 'email': 'not-an-email'})
#             html = resp.get_data(as_text=True)

#             self.assertEqual(resp.status_code, 200)
#             self.assertIn("<form", html)
#             self.assertNotIn("updated!", html)
