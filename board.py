import unittest


class Item:
    def __init__(self, *args, **kwargs):
        self._attempts = 0.0        # number of times this item has been selected
        self._accuracy = 0.0        # the number of times this item was correctly chosen
        self._response_time = None  # the average response time for this item

    def get_attempt_prob(self):
        """ Given attempt metrics what should the probability of selecting this item"""
        if self._attempts == 0.0:
            return 1.0

        return 1.0 / self._attempts

    def get_response_time_prob(self):
        # normalise
        # assume max(response_time) = 5 seconds

        if self._response_time is None:
            return 1

        return min(1, self._response_time / 5.0)

    def get_accuracy_probability(self):
        assert 0.0 <= self._accuracy <= 1.0

        return 1.0 - self._accuracy

    def get_probability(self):
        return self.get_attempt_prob() + \
               self.get_response_time_prob() + \
               self.get_accuracy_prob() / 3



class ProbabilitlyTestCase(unittest.TestCase):
    def setUp(self):
        self.item = Item()

    def test_no_attempts_high_probability(self):
        assert self.item._attempts == 0

        self.assertEquals(self.item.get_attempt_prob(), 1.0)

    def test_lots_of_attempts_low_probability(self):

        self.item._attempts = 10

        self.assertLess(self.item.get_attempt_prob(), 0.5)

    def test_lots_of_attempts_not_zero(self):

        self.item._attempts = 5

        self.assertGreater(self.item.get_attempt_prob(), 0.0)

    def test_response_time_prob_undefined_is_1(self):
        assert self.item._response_time is None

        self.assertEquals(self.item.get_response_time_prob(), 1.0)

    def test_response_time_prob_0_is_0(self):

        self.item._response_time = 0.0

        self.assertEquals(self.item.get_response_time_prob(), 0)

    def test_response_time_prob_max_is_1(self):

        self.item._response_time = 5.0

        self.assertEquals(self.item.get_response_time_prob(), 1)

    def test_resposen_time_greater_than_max_is_1(self):

        self.item._response_time = 6.0

        self.assertEquals(self.item.get_response_time_prob(), 1)

    def test_accuracy_1_is_0(self):
        """100% accuracy means probability should be 0"""

        self.item._accuracy = 1.0

        self.assertEquals(self.item.get_accuracy_probability(), 0.0)

    def test_accuracy_0_is_1(self):
        """0% accuracy means probability should be 1"""

        self.item._accuracy = 0.0

        self.assertEquals(self.item.get_accuracy_probability(), 1.0)


if __name__ == "__main__":
    unittest.main()