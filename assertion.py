import collections


def checkFor(description):

    return Description(description)


def verify(actual):

    assert isinstance(actual, Actual), 'Expected {0} ({1}). Actual {0} ({2})'.format(actual, Actual, type(actual))

    return VerifyObject(actual)


class Description(object):

    def __init__(self, description):

        self.__description = description

    def using(self, value):

        return Actual(self.__description, value)


class Actual(object):

    def __init__(self, description, value):

        self.__description = description
        self.__value       = value

    @property
    def description(self):

        return self.__description

    @property
    def value(self):

        return self.__value


class VerifyObject(object):

    def __init__(self, actual):

        self.__actual = actual

    def __reportCompareString(self, expected, actual, reverse = False, showType = False):

        return '{0}: Expected{1} {2}{3}. Actual {4}{5}.'.format(
            self.__actual.description,
            ' not' if reverse else '',
            expected,
            ' ({0})'.format(type(expected)) if showType else '',
            actual,
            ' ({0})'.format(type(actual)) if showType else ''
        )

    def __reportTypeString(self, expected, actual, reverse = False):

        return '{0}: {1}: Expected{2} {3}. Actual {4}.'.format(
            self.__actual.description,
            self.__actual.value,
            ' not' if reverse else '',
            type(expected),
            type(actual)
        )

    def __reportInstanceString(self, expected, actual, reverse = False):

        return '{0}: {1}: Expected{2} {3}. Actual {4}.'.format(
            self.__actual.description,
            self.__actual.value,
            ' not' if reverse else '',
            expected.__class__,
            actual.value.__class__
        )

    def callWith(self, *args, **kwargs):

        return VerifyCallable(self.__actual, *args, **kwargs)

    @property
    def collection(self):

        return VerifyCollection(self.__actual)
    def isTrue(self):

        assert self.__actual.value is True, self.__reportCompareString(True, self.__actual.value)
        return True

    def isFalse(self):

        assert self.__actual.value is False, self.__reportCompareString(False, self.__actual.value)
        return True

    def isNone(self):

        assert self.__actual.value is None, self.__reportCompareString(None, self.__actual.value)
        return True

    def isNotNone(self):

        assert self.__actual.value is not None, self.__reportCompareString(None, self.__actual.value, reverse = True)
        return True

    def isEqualTo(self, expected):

        assert self.__actual.value == expected, self.__reportCompareString(expected, self.__actual.value, showType = True)
        return True

    def isNotEqualTo(self, expected):

        assert self.__actual.value != expected, self.__reportCompareString(expected, self.__actual.value, reverse = True, showType = True)
        return True

    def isOfType(self, expected):

        assert type(self.__actual.value) == expected, self.__reportTypeString(expected, self.__actual.value)
        return True

    def isNotOfType(self, expected):

        assert type(self.__actual.value) != expected, self.__reportTypeString(expected, self.__actual.value, reverse = True)
        return True

    def isInstanceOf(self, expected):

        assert isinstance(self.__actual.value, expected), self.__reportInstanceString(expected, self.__actual.value)
        return True

    def isNotInstanceOf(self, expected):

        assert not isinstance(self.__actual.value, expected), self.__reportInstanceString(expected, self.__actual.value, reverse = True)
        return True


class VerifyCallable(object):

    def __init__(self, actual, *args, **kwargs):

        self.__actual = actual
        self.__args   = args
        self.__kwargs = kwargs

    def shouldThrow(self, expected):

        assert issubclass(expected, Exception), '{0} ({1}) is not an exception.'.format(expected, type(expected))

        try:
            self.__actual.value(*self.__args, **self.__kwargs)

        except expected:
            return True

        raise AssertionError('{0}: {1}({2}{3}{4}) did not throw {5}.'.format(
            self.__actual.description,
            self.__actual.value.__name__,
            ', '.join(self.__args),
            ', ' if self.__args and self.__kwargs else '',
            ', '.join(['{0}={1}'.format(name, value) for name, value in self.__kwargs.items()]),
            expected.__name__
        ))

    def shouldNotThrow(self):

        try:
            self.__actual.value(*self.__args, **self.__kwargs)

        except Exception as error:
            raise type(error)('{0}: {1}'.format(self.__actual.description, error.message))

        return True


class VerifyCollection(object):

    def __init__(self, actual):

        assert isinstance(actual.value, collections.Sequence), '{0} ({1}) is not a sequence.'.format(actual, type(actual))

        self.__actual = actual

    def contains(self, expected):

        assert self.__actual.value.contains(expected), '{0}: Expected {1} in {2}.'.format(self.__actual.description, expected, self.__actual.value)
        return True

    def notContains(self, expected):

        assert not self.__actual.value.contains(expected), '{0}: Expected {1} not in {2}.'.format(self.__actual.description, expected, self.__actual.value)
        return True

    def isEmpty(self):

        assert not self.__actual.value, '{0}: Expected empty. Actual {1}.'.format(self.__actual.description, self.__actual.value)
        return True

    def isNotEmpty(self):

        assert self.__actual.value, '{0}: Expected not empty. Actual {1}.'.format(self.__actual.description, self.__actual.value)
        return True

    def isEqualTo(self, expected):

        assert isinstance(expected, collections.Sequence), 'Expected value must be a sequence.'
        assert tuple(self.__actual.value) == tuple(expected), '{0}: Expected {1}. Actual {2}.'.format(self.__actual.description, expected, self.__actual.value)