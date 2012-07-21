#
# Copyright (C) 2007-2012 by Johan De Taeye, frePPLe bvba
#
# This library is free software; you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero
# General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# file : $URL$
# revision : $LastChangedRevision$  $LastChangedBy$
# date : $LastChangedDate$

from datetime import datetime
import tempfile

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from freppledb.input.models import Location, Calendar

class DataLoadTest(TestCase):

  def setUp(self):
    # Login
    self.client.login(username='frepple', password='frepple')

  def test_input_customer(self):
    response = self.client.get('/admin/input/customer/?format=json')
    self.assertContains(response, '"records":2,')

  def test_input_flow(self):
    response = self.client.get('/admin/input/flow/?format=json')
    self.assertContains(response, '"records":19,')

  def test_input_buffer(self):
    response = self.client.get('/admin/input/buffer/?format=json')
    self.assertContains(response, '"records":8,')

  def test_input_calendar(self):
    response = self.client.get('/admin/input/calendar/?format=json')
    self.assertContains(response, '"records":4,')

  def test_input_calendar(self):
    response = self.client.get('/admin/input/calendarbucket/?format=json')
    self.assertContains(response, '"records":5,')

  def test_input_demand(self):
    response = self.client.get('/admin/input/demand/?format=json')
    self.assertContains(response, '"records":14,')

  def test_input_item(self):
    response = self.client.get('/admin/input/item/?format=json')
    self.assertContains(response, '"records":5,')

  def test_input_load(self):
    response = self.client.get('/admin/input/load/?format=json')
    self.assertContains(response, '"records":3,')

  def test_input_location(self):
    response = self.client.get('/admin/input/location/?format=json')
    self.assertContains(response, '"records":2,')

  def test_input_operation(self):
    response = self.client.get('/admin/input/operation/?format=json')
    self.assertContains(response, '"records":14,')

  def test_input_operationplan(self):
    response = self.client.get('/admin/input/operationplan/?format=json')
    self.assertContains(response, '"records":4,')

  def test_input_parameter(self):
    response = self.client.get('/admin/common/parameter/?format=json')
    self.assertContains(response, '"records":2,')

  def test_input_resource(self):
    response = self.client.get('/admin/input/resource/?format=json')
    self.assertContains(response, '"records":3,')

  def test_input_suboperation(self):
    response = self.client.get('/admin/input/suboperation/?format=json')
    self.assertContains(response, '"records":4,')

  def test_csv_upload(self):
    self.assertEqual(
      [(i.name, i.category or u'') for i in Location.objects.all()],
      [(u'factory 1',u''), (u'factory 2',u'')]
      )
    try:
      data = tempfile.TemporaryFile(mode='w+b')
      print >>data, 'name, category'
      print >>data, 'factory 3, cat1'
      print >>data, 'factory 4,'
      data.seek(0)
      response = self.client.post('/admin/input/location/', {'csv_file': data})
      self.assertRedirects(response, '/admin/input/location/')
    finally:
      data.close()
    self.assertEqual(
      [(i.name, i.category or u'') for i in Location.objects.order_by('name')],
      [(u'factory 1',u''), (u'factory 2',u''), (u'factory 3',u'cat1'), (u'factory 4',u'')]
      )
