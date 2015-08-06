from tinytest.test import *


@description('My one thing')
class MyTest(TestClass):

    @setup
    def someKindOfSetup(self):

        self.log.debug('In setup')

    @cleanup
    def cleanupOrSomething(self):

        self.log.debug('In cleanup')

    @should('do a thing')
    def aMethod(self):

        self.log.debug('Running a successful test here...')

    @should('do that other thing')
    def nameDoesntMatter(self):

        assert False, 'I always fail, just because!'


@description('Another thing')
class BadTest(TestClass):

    @setup
    def aMethod(self):

        assert False, 'Setup blocker!!'

    @cleanup
    def someotherthing(self):

        self.log.debug('In cleanup')

    @should('do a thing')
    def someThings(self):

        self.log.debug('Testing some things')

    @skip
    @should('maybe sometimes do a thing')
    def thingsImLazyAbout(self):

        self.log.debug('Skipping some tests here, like a jerk')


if __name__ == '__main__':

    from tinytest import TinyTester

    TinyTester(level='DEBUG').run([MyTest, BadTest])