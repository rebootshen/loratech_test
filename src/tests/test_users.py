import unittest
import os
import json
from ..app import create_app

import logging
logger = logging.getLogger('file')

class UsersTest(unittest.TestCase):
  """
  Users Test Case
  """
  def setUp(self):
    """
    Test Setup
    """
    self.app = create_app("testing")
    self.client = self.app.test_client
    self.user = {
      'name': 'olawale1',
      'email': 'olawale1@mail.com',
      'password': 'passw0rd!1'
    }

    #with self.app.app_context():
      # create all tables
      #db.create_all()

  def testRoute(self):
        # This test works just fine
        resp = self.client().get('/', content_type='html/text')
        logger.info(resp.data)
        logger.info(type(resp))
        self.assertEqual(resp.status, "200 OK", "Status should be 200, was %s" % resp.status)

  
  def test_user_creation(self):
    """ test user creation with valid credentials """
    res = self.client().post('/users/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user))
  
    json_data = json.loads(res.data)
    print(json_data)
    self.assertTrue(json_data.get('jwt_token'))
    self.assertEqual(res.status_code, 201)

  def test_user_creation_with_existing_email(self):
    """ test user creation with already existing email"""
    res = self.client().post('/users/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user))
    json_data = json.loads(res.data)
    print(json_data)
    self.assertEqual(res.status_code, 400)
    self.assertTrue(json_data.get('error'))
    
  def tearDown(self):
    """
    Tear Down
    """
    #with self.app.app_context():
      #db.session.remove()
      #db.drop_all()

if __name__ == "__main__":
  unittest.main() 