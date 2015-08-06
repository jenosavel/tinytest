import logging


class TestClass(object):

    class Fixtures:

        SETUP   = 'setup'
        CLEANUP = 'cleanup'
        TEST    = 'test'

        SKIP    = 'doNotRun'

        ALL = [SETUP, CLEANUP, TEST]

    @property
    def log(self):

        return logging.getLogger(self.__class__.__name__)


####################################################################
#
#   Fixture Decorators
#
####################################################################

def cleanup(method):
    """
    Mark a method as the cleanup fixture
    """

    assert callable(method), 'Method is not callable. {0}'.format(method)
    
    method.fixture = TestClass.Fixtures.CLEANUP
    return method


def describe(stringParam):
    """
    Add a description for reporting readability.
    """

    def callableTest(method):

        assert callable(method), 'Method is not callable. {0}'.format(method)

        method.description = stringParam
        return method

    return callableTest


def setup(method):
    """
    Mark a method as the setup fixture
    """

    assert callable(method), 'Method is not callable. {0}'.format(method)

    method.fixture = TestClass.Fixtures.SETUP
    return method


def skip(method):
    """
    Temporarily skip a method during execution.
    """

    assert callable(method), 'Method is not callable. {0}'.format(method)

    method.doNotRun = True
    return method


def should(stringParam):
    """
    Mark a method as a test fixture. Provide a readable reporting statement.
    """

    def callableTest(method):

        assert callable(method), 'Method is not callable. {0}'.format(method)

        method.fixture     = TestClass.Fixtures.TEST
        method.description = stringParam

        return method

    return callableTest