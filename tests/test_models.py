import warnings
warnings.filterwarnings("ignore")
import os
basedir = os.path.abspath(os.path.dirname(__file__))

from datetime import date
from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.Model.models import User, Student, Professor, ResearchPost, ResearchField, ProgrammingLanguage
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    ROOT_PATH = '..//'+basedir
    
class TestModels(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = Student(username='testuser', email='user@wsu.edu')
        u.set_password('testpass')
        self.assertFalse(u.check_password('wrongpass'))
        self.assertTrue(u.check_password('testpass'))
    
    def test_student_user_1(self):
        suser = Student(username='teststudentuser1',email='user1@wsu.edu')
        suser.set_password('testpass')
        self.assertFalse(suser.is_professor())
        l1 = ProgrammingLanguage(name='C++')
        l2 = ProgrammingLanguage(name='Java')
        suser.languages.append(l1)
        suser.languages.append(l2)
        self.assertEqual(suser.languages.all(), [l1,l2])
    

    def test_prof_user_1(self):
        puser = Professor(username='testprofuser1', email='user2@wsu.edu')
        puser.set_password('testpass')
        self.assertTrue(puser.is_professor())

    def test_rpost_1(self):

        rpost = ResearchPost(user_id='1', title="testpost1", start_date=date.fromtimestamp(20211203), end_date=date(2022,1,1))
        t = date.fromtimestamp(20211203)
        t.isoformat()
        self.assertEqual(rpost.get_start(), t.strftime('%m/%d/%Y'))
        self.assertNotEqual(rpost.get_start(), '5/24/2019')
        f = date(2022,1,1)
        
        self.assertEqual(rpost.get_end(),f.strftime('%m/%d/%Y'))
        self.assertNotEqual(rpost.get_end(), '5/24/2019')

    def test_rpost_2(self):
        rfields = ResearchField(name="Bio")
        rpost = ResearchPost(user_id='1', title="testpost1", start_date=date.fromtimestamp(20211203), end_date=date.fromtimestamp(20220101))
        rpost.research_fields.append(rfields)
        rf = [rfields]
        self.assertEqual(rpost.get_fields().all(), rf)


    




if __name__ == '__main__':
    unittest.main(verbosity=2)