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


def cleanup(method):

    assert callable(method), 'Method is not callable. {0}'.format(method)
    
    method.fixture = TestClass.Fixtures.CLEANUP
    return method


def description(stringParam):

    def callableTest(method):

        assert callable(method), 'Method is not callable. {0}'.format(method)

        method.description = stringParam
        return method

    return callableTest


def setup(method):

    assert callable(method), 'Method is not callable. {0}'.format(method)

    method.fixture = TestClass.Fixtures.SETUP
    return method


def skip(method):

    assert callable(method), 'Method is not callable. {0}'.format(method)

    method.doNotRun = True
    return method


def should(stringParam):

    def callableTest(method):

        assert callable(method), 'Method is not callable. {0}'.format(method)

        method.fixture     = TestClass.Fixtures.TEST
        method.description = stringParam

        return method

    return callableTest