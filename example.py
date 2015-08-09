####################################################################
#
#   Example command line usage:
#   >python -m tinytest --directory C:\path\to\tests --loglevel DEBUG
#
#   --directory
#       Path to the directory where test files are
#       Not required, defaults to current working directory
#
#   --loglevel
#       The logging level of output
#       Not required, defaults to INFO
#
####################################################################


from tinytest.test import *


@describe('My one thing')
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

    @should('show off assertions')
    def assertionsRCool(self):

        thingToTest = 1

        actual = checkFor('Unexpected int value').using(thingToTest)
        verify(actual).isEqualTo(2)


@describe('Another thing')
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