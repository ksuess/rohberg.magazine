import transaction

from Products.CMFCore.utils import getToolByName
from ftw.builder import Builder
from ftw.builder import create
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from rohberg.magazine.testing import THEME_INTEGRATION_TESTING
from unittest2 import TestCase


class TestFyloutView(TestCase):

    layer = THEME_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        transaction.commit()

    def test_view_appended_to_url_if_obj_in_property(self):
        properties = getToolByName(self.portal, 'portal_properties')
        properties.site_properties.typesUseViewActionInListings=('Folder')

        folder = create(Builder('folder'))
        view = self.portal.unrestrictedTraverse('xyz')
        view()
        self.assertEqual('http://nohost/plone/folder/view',
                         view.url(folder))