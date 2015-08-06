class Status:

    BLOCKED    = 'blocked'
    FAIL       = 'fail'
    INCOMPLETE = 'incomplete'
    PASS       = 'pass'


class Report(object):

    REASON = 'reason'
    STATUS = 'status'

    def __init__(self):

        self.__results = {}
        self.__failure = None

    def initialize(self, tests):

        for test in tests:
            self.update(test, Status.INCOMPLETE)

    def update(self, test, status):

        self.__results[test] = { Report.STATUS: status }

        if status == Status.FAIL or status == Status.BLOCKED:
            self.__results[test][Report.REASON] = self.__failure
            self.__failure = None

    def addFailure(self, message):

        if not self.__failure:
            self.__failure = message

    @property
    def results(self):

        results = []

        if self.__results:

            statusPadding = max(len(result[Report.STATUS]) for result in self.__results.values()) + 2
            descPadding   = max(len(test) for test in self.__results.keys())

            for test, result in sorted(self.__results.iteritems(), key = lambda tuple: tuple[1][Report.STATUS]):

                status = result[Report.STATUS]
                failure = ' // {0}'.format(result[Report.REASON]) if status is Status.FAIL or status is Status.BLOCKED else ''

                results.append('{0} {1} {2}'.format(
                    '[{0}]'.format(status.upper()).ljust(statusPadding),
                    test.ljust(descPadding),
                    failure
                ))

        return results