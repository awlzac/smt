from django.test import TestCase
from django.core.urlresolvers import reverse
import json

class SmtTests (TestCase):
    '''
    Unit tests for Sherpany Map Test.
    '''
      
    def setUp(self):
        TestCase.setUp(self)      
 
    def tearDown(self):
        TestCase.tearDown(self)

    def test_address(self):
        '''
        test adress views.
        '''
      
        # originally we have no list
        response = self.client.get(reverse('addrmap:address_get'))
        self.assertEqual(response.status_code, 200)
        jsonresp = json.loads(response.content.decode())
        self.assertEqual(len(jsonresp), 0)
      
        # add to list and verify addition has been made
        response = self.client.post(reverse('addrmap:address_add'), 
                                    {'desc': 'mae sai',
                                     'lat': 20.4,
                                     'lng': 99.9})
        self.assertEqual(response.status_code, 200)
        jsonresp = json.loads(response.content.decode())
        self.assertEqual(len(jsonresp), 1)
        self.assertEqual(jsonresp[0]['lat'], 20.4)
      
        # clear list and verify that list is empty
        response = self.client.post(reverse('addrmap:address_trunc'))
        self.assertEqual(response.status_code, 200)
        jsonresp = json.loads(response.content.decode())
        self.assertEqual(len(jsonresp), 0)
      
