from plone.testing import z2
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting


class Layer(PloneSandboxLayer):
    
    defaultBases = (PLONE_FIXTURE,)
    
    def setUpZope(self, app, configurationContext):
        import collective.firehose
        self.loadZCML(package=collective.firehose)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'collective.firehose:default')


FIXTURE = NetImpactLayer()
INTEGRATION_TESTING = IntegrationTesting(bases=(FIXTURE,), name='collective.firehose:Integration')
FUNCTIONAL_TESTING = FunctionalTesting(bases=(FIXTURE,), name='collective.firehose:Functional')
