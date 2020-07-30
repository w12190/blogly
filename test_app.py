from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True   

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class BloglyAppTestCase(TestCase):
    '''Tests for blogly flask routes'''

    def setUp(self):
        """Add a sample user."""

        User.query.delete()

        user = User(first_name='Wayne', last_name='Chen')
        db.session.add(user)
        db.session.commit()
        self.client = app.test_client()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()
    
    def test_root_route(self):
        '''Tests that the root route redirects to /user'''
        with self.client as client:
            response = client.get('/', follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)

    def test_new_user_form_displays(self):
        '''Tests that the new user form displays on the route /users/new'''
        with self.client as client:
            response = client.get('/users/new')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<form action="/users/new" method="POST">', html)

    
    def test_new_user_submission(self):
        '''Tests that the new user form submission redirects to the users page. The new user should be on the list of users'''
        with self.client as client:
            response = client.post('/users/new', data={'first_name': 'Michelle', 'last_name': 'Obama', 'image_url': 'a;lsdkjfl;aksdfj'}, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<li>Michelle Obama</li>', html)

    
    


'''

class PetViewsTestCase(TestCase):
    """Tests for views for Pets."""

    def setUp(self):
        """Add sample pet."""

        Pet.query.delete()

        pet = Pet(name="TestPet", species="dog", hunger=10)
        db.session.add(pet)
        db.session.commit()

        self.pet_id = pet.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_pets(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestPet', html)

'''