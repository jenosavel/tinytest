import inspect
import logging
import os
import sys
import traceback

from reporting import *
from test      import *


####################################################################
#
#   Execution Framework
#
####################################################################

class TinyTester(object):

    def __init__(self, level = 'INFO'):

        self.__fileHandler = None
        self.__formatter   = logging.Formatter('%(levelname)s: %(message)s')
        self.log           = logging.getLogger(self.__class__.__name__)

        for handler in self.log.handlers:
            self.log.removeHandler(handler)

        consoleHandler = logging.StreamHandler(sys.stdout)
        consoleHandler.setFormatter(self.__formatter)

        self.log.addHandler(consoleHandler)

        self.log.setLevel(level)
        self.log.propagate = False

    def addFileHandler(self, cls):

        assert not self.__fileHandler, 'File handler already exists.'

        testFile  = inspect.getfile(cls)
        testDir   = os.path.dirname(testFile)
        resultDir = os.path.join(testDir, 'results')
        path      = os.path.join(resultDir, '{0}.log'.format(cls.__name__))

        if not os.path.exists(resultDir):
            os.makedirs(resultDir)

        self.__fileHandler = logging.FileHandler(path, 'w')
        self.__fileHandler.setFormatter(self.__formatter)

        self.log.addHandler(self.__fileHandler)

    def removeFileHandler(self):

        assert self.__fileHandler, 'No file handler exists.'

        self.log.removeHandler(self.__fileHandler)
        self.__fileHandler = None

        self.log.debug('Result file closed.')

    def run(self, classes):

        assert isinstance(classes, list), 'Classes must be provided as a list'

        for cls in classes:

            if not issubclass(cls, TestClass):
                self.log.error('{0} does not inherit from TestClass'.format(cls))
                continue

            if hasattr(cls, TestClass.Fixtures.SKIP) and getattr(cls, TestClass.Fixtures.SKIP):
                continue

            self.addFileHandler(cls)

            self.log.info('[ {0} ]'.format(cls.description))

            instance = cls()

            setup   = None
            cleanup = None
            tests   = []

            for name in dir(cls):

                method = getattr(cls, name)

                if not hasattr(method, 'fixture'):
                    continue

                fixture = getattr(method, 'fixture')

                if fixture == TestClass.Fixtures.SETUP:
                    setup = method

                elif fixture == TestClass.Fixtures.CLEANUP:
                    cleanup = method

                elif fixture == TestClass.Fixtures.TEST:
                    tests.append(method)

            assert tests, 'No tests found.'

            report = Report()
            report.initialize([test.description for test in tests])

            for test in tests:

                if hasattr(test, TestClass.Fixtures.SKIP) and getattr(test, TestClass.Fixtures.SKIP):
                    continue

                self.log.info('[ {0} should {1} ]'.format(cls.description, test.description))
                status = Status.INCOMPLETE

                try:

                    if setup:
                        self.log.debug('[ Setup ]')
                        setup(instance)

                    try:
                        self.log.debug('[ Test ]')
                        test(instance)

                        status = Status.PASS

                    except AssertionError as assertion:

                        self.log.error(traceback.format_exc())
                        report.addFailure(assertion.message)

                        status = Status.FAIL
                        print 'test error: {0}'.format(assertion.message)

                    finally:

                        if cleanup:
                            self.log.debug('[ Cleanup ]')
                            cleanup(instance)

                except Exception as exception:

                    self.log.error(traceback.format_exc())
                    report.addFailure(str(exception))

                    status = Status.BLOCKED

                finally:

                    report.update(test.description, status)


            self.log.info('=============================================')
            self.log.info(cls.description)
            self.log.info('---------------------------------------------')

            results = report.results

            if not results:
                self.log.warning('No results')

            for result in results:
                self.log.info(result)

            self.log.info('=============================================')

            self.removeFileHandler()