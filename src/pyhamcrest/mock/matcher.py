# pragma no cover

from hamcrest.core.base_matcher import BaseMatcher


class MockMatcher(BaseMatcher):
    """
    allows hamcrest assertions involving mock methods
    e.g.
    assert_that(mock, not_called())
    this will be eventually factored out to a new package
    """

    def __init__(self, fn, args=()):
        self.fn = fn
        self.args = args

    def matches(self, mock, mismatch_description=None):
        return self._try_match(mock, True, mismatch_description)

    def _try_match(self, mock, capture_assertion_error, mismatch_description):
        method = getattr(mock, self.fn, None)
        matched = False
        try:
            if method:
                method(*self.args)
                matched = True
            else:
                self._append_description(mismatch_description, 'mock does not have method %s' % self.fn)
        except AssertionError as e:
            if not capture_assertion_error:
                raise e
            else:
                self._append_description(mismatch_description, 'False: ' + str(e))
        return matched

    def _append_description(self, out, desc):
        if out:
            out.append_text(desc)

    def describe_to(self, description):
        message = "%s(%s) to be true" % (self.fn, ", ".join([str(a) for a in self.args]))
        description.append_text(message)
        return False


def called_with(*args):
    return MockMatcher('assert_called_with', args)


def called_once():
    return MockMatcher('assert_called_once')


def called_once_with(*args):
    return MockMatcher('assert_called_once_with', args)


def not_called():
    return MockMatcher('assert_not_called')
