from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import functional_session_factory
from ftw.builder.testing import set_builder_session_factory
from ftw.testing import ComponentRegistryLayer
from ftw.testing import FunctionalSplinterTesting
from plone.app.testing import applyProfile
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
from zope.configuration import xmlconfig


class MetaZCMLLayer(ComponentRegistryLayer):

    def setUp(self):
        super(MetaZCMLLayer, self).setUp()
        import rohberg.magazine
        self.load_zcml_file('meta.zcml', rohberg.magazine)


META_ZCML = MetaZCMLLayer()


class ThemeLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        xmlconfig.string(
            '<configure xmlns="http://namespaces.zope.org/zope">'
            '  <include package="z3c.autoinclude" file="meta.zcml" />'
            '  <includePlugins package="plone" />'
            '  <includePluginsOverrides package="plone" />'
            '</configure>',
            context=configurationContext)
            
        import rohberg.magazine
        xmlconfig.file('configure.zcml', rohberg.magazine,
                       context=configurationContext)
                       
        # z2.installProduct(app, 'rohberg.magazine')
        
        # import plone.app.contenttypes
        # xmlconfig.file('configure.zcml', plone.app.contenttypes,
        #                context=configurationContext)
        

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'rohberg.magazine:default')


THEME_FIXTURE = ThemeLayer()

THEME_INTEGRATION_TESTING = IntegrationTesting(
    bases=(THEME_FIXTURE, ),
    name='rohberg.magazine:integration')

THEME_FUNCTIONAL_TESTING = FunctionalSplinterTesting(
    bases=(THEME_FIXTURE,
           set_builder_session_factory(functional_session_factory)),
    name="rohberg.magazine:functional")
