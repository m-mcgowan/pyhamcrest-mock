import unittest
from unittest.mock import Mock

from hamcrest import assert_that, calling, is_, raises

from pyhamcrest.mock.matcher import MockMatcher, called_once_with


class MockMatcherTest(unittest.TestCase):

    def setUp(self):
        self.fn = 'doit'
        self.args = (1, 2)
        self.sut = MockMatcher(self.fn, self.args)

    def test_constructor(self):
        assert_that(self.sut.fn, is_(self.fn))
        assert_that(self.sut.args, is_(self.args))

    def test_matches_calles_try_match(self):
        return_value = [1, 2, 3]
        self.sut._try_match = Mock(return_value=return_value)
        mock1, mock2 = Mock(), Mock()
        result = self.sut.matches(mock1, mock2)
        assert_that(self.sut._try_match, called_once_with(mock1, True, mock2))
        assert_that(result, is_(return_value))

    def test_try_match_method_exists_returns_false_no_capture_assert(self):
        mock = Mock()
        mock.doit = Mock(side_effect=AssertionError)
        assert_that(calling(self.sut._try_match).with_args(mock, False, None), raises(AssertionError))

    def test_try_match_method_not_exists_no_capture_assert(self):
        mock = Mock()
        del mock.doit
        assert_that(self.sut._try_match(mock, False, None), is_(False))

    def test_try_match_method_not_exists_capture_assert(self):
        mock = Mock()
        del mock.doit
        assert_that(self.sut._try_match(mock, False, None), is_(False))

    def test_try_match_method_not_exists_no_capture_assert_with_description(self):
        mock = Mock()
        description = Mock()
        del mock.doit
        assert_that(self.sut._try_match(mock, False, description), is_(False))
        assert_that(description.append_text, called_once_with("mock does not have method doit"))
