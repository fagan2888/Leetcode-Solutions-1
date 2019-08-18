import logging

logging.basicConfig(filename='/tmp/out', level=logging.DEBUG)

from typing import List, Tuple

class WindowSortedList():
    def __init__(self, input_list, bounds = None):
        """
        Python passes references by value, so creating these window objects is O(1).
        """
        if bounds is None:
            self.lower_bound, self.upper_bound = (0, len(input_list))
        else:
            assert(bounds[0] < bounds[1])
            self.lower_bound, self.upper_bound = bounds
        self.sorted_list = input_list

    def __str__(self):
        return '<WindowSortedList:low={},high={};min={},max={}>'.format(self.lower_bound, self.upper_bound, self.lower_bound_value, self.upper_bound_value)

    def __eq__(self, other):
        return self.sorted_list == other.sorted_list and self.lower_bound == other.lower_bound and self.upper_bound == other.upper_bound
    
    @property
    def lower_bound_value(self):
        return self.sorted_list[self.lower_bound]
    
    @property
    def upper_bound_value(self):
        return self.sorted_list[self.upper_bound - 1]
    
    def safe_get(self, i):
        """Get index if possible, otherwise return None. i cannot be negative."""
        assert(i > 0)
        if i >= len(self.sorted_list):
            return None
        else:
            return self.sorted_list[i]
    
    def is_disjoint_and_less_than(self, other):
        """I'm using an odd definition of disjoint, disjoint here means the
        boundaries could have the same value but there is no overlap otherwise.
        """
        return self.upper_bound_value <= other.lower_bound_value
    
    def is_disjoint_and_greater_than(self, other):
        """I'm using an odd definition of disjoint, disjoint here means the
        boundaries could have the same value but there is no overlap otherwise.
        """
        return self.lower_bound_value >= other.upper_bound_value
    
    def partition(self, pivot = None):
        if pivot is None:
            pivot = (self.upper_bound - self.lower_bound) // 2 + self.lower_bound
        if self.lower_bound_value == self.upper_bound_value:
            # Doesn't make sense to partition if we only have one value.
            return self, None
        return (WindowSortedList(self.sorted_list, (self.lower_bound, pivot)),
            WindowSortedList(self.sorted_list, (pivot, self.upper_bound)))
        

class Solution:
    @staticmethod
    def median_from_single_sorted_array(sorted_array):
        is_odd = len(sorted_array) % 2 == 1
        target_index = (len(sorted_array) - 1) // 2
        
        if is_odd:
            return sorted_array[target_index]
        else:
            return (sorted_array[target_index] + sorted_array[target_index + 1]) / 2.
    
    @staticmethod
    def median_from_disjoint_lists(nums: Tuple[WindowSortedList, WindowSortedList]) -> float:
        """
        Lower list must be listed first in this function. Lists must be
        disjoint: They have share a boundary but cannot otherwise overlap. The
        first list must be the lower list.
        """
        assert(nums[0].is_disjoint_and_less_than(nums[1]))
        
        is_odd = (len(nums[0].sorted_list) + len(nums[1].sorted_list)) % 2 == 1
        target_index = (len(nums[0].sorted_list) + len(nums[1].sorted_list) - 1) // 2
        
        # Watch for fishiness, target index should be a candidate.
        assert(target_index >= nums[0].lower_bound + nums[1].lower_bound)
        assert(target_index <  nums[0].upper_bound + nums[1].upper_bound)
        
        if nums[0].upper_bound + nums[1].lower_bound > target_index:
            # Case when the target is within the lesser list
            first_target_val = nums[0].sorted_list[target_index - nums[1].lower_bound]
            if not is_odd:
                # This is inelegant but I think it keeps things sane. We're
                # doing the pivoting to find the 'target_index". In the case of
                # an even total length, the median is a function of the two
                # central values. This may be "off the end" of our pivoted
                # subarray. Checking for this does not hurt time complexity.
                candidates = [nums[1].lower_bound_value,
                        nums[0].safe_get(target_index - nums[1].lower_bound + 1)]
                second_target_val = min(c for c in candidates if c is not None)
        else:
            # Case when the target is wthin the greater list
            first_target_val = nums[1].sorted_list[target_index - nums[0].upper_bound]
            if not is_odd:
                candidates = [nums[1].safe_get(target_index - nums[0].upper_bound + 1),
                        nums[0].safe_get(nums[0].upper_bound)]
                second_target_val = min(c for c in candidates if c is not None)
        
        # We only get here if we had a second target val due to is_odd being false
        if is_odd:
            return first_target_val
        else:
            return (first_target_val + second_target_val) / 2.

    def median_from_window_sorted_lists(self, nums: Tuple[WindowSortedList, WindowSortedList]) -> float:
        """
        Recursive function to split the lists and find the median.
        This is O(log(m+n)) becuase it throws away half of one of the arrays on
        each iteration, or returns an answer in constant time.
        """
        logging.debug('Recursing')
        for num in nums:
            logging.debug(num)
        is_odd = (len(nums[0].sorted_list) + len(nums[1].sorted_list)) % 2 == 1
        target_index = (len(nums[0].sorted_list) + len(nums[1].sorted_list) - 1) // 2
        
        logging.debug("Target index: {}".format(target_index))
        
        if nums[0].is_disjoint_and_less_than(nums[1]):
            return self.median_from_disjoint_lists(nums)
        if nums[1].is_disjoint_and_less_than(nums[0]):
            return self.median_from_disjoint_lists((nums[1], nums[0]))
        
        # Our lists still overlap. Recurse until this is no longer true.
        partition00, partition01  = nums[0].partition()
        partition10, partition11  = nums[1].partition()

        if partition01 is None:
            if nums[0].lower_bound_value <= partition10.upper_bound_value:
                logging.debug("Case 1, nums[0] contains one value, value within first partition of nums[1]")
                pivot_point = partition00.upper_bound + partition10.upper_bound
                if pivot_point > target_index:
                    newlists = (nums[0], partition10)
                else:
                    # Could directly call median_from_disjoint_lists here,
                    # because the median is definitely inside partition11 but
                    # doing it this way to minimize function exit points.
                    newlists = (nums[0], partition11)
            else:
                logging.debug("Case 2, nums[0] contains one value, value beyond first partition of nums[1]")
                pivot_point = nums[0].lower_bound + partition10.upper_bound
                if pivot_point > target_index:
                    # Could directly call median_from_disjoint_lists here,
                    # because the median is definitely inside partition10 but
                    # doing it this way to minimize function exit points.
                    newlists = (nums[0], partition10)
                else:
                    newlists = (nums[0], partition11)
        elif partition11 is None:
            # This happens when nums[1] contains only one value.
            if nums[1].lower_bound_value <= partition00.upper_bound_value:
                logging.debug("Case 3, nums[1] contains one value, value within first partition of nums[0]")
                # Case when partition10's value is within partition00
                pivot_point = nums[1].upper_bound + partition00.upper_bound
                if pivot_point > target_index:
                    newlists = (partition00, nums[1])
                else:
                    # Could directly call median_from_disjoint_lists here,
                    # because the median is definitely inside partition01 but
                    # doing it this way to minimize function exit points.
                    newlists = (partition01, nums[1])
            else:
                logging.debug("Case 4, nums[1] contains one value, value beyond first partition of nums[0]")
                # Case when partition10's value is beyond partition00
                pivot_point = nums[1].lower_bound + partition00.upper_bound
                if pivot_point > target_index:
                    # Could directly call median_from_disjoint_lists here,
                    # because the median is definitely inside partition10 but
                    # doing it this way to minimize function exit points.
                    newlists = (partition00, nums[1])
                else:
                    newlists = (partition01, nums[1])
        elif nums[0].is_disjoint_and_less_than(partition11):
            logging.debug("Case 5, nums[0] disjoint from partition11")
            pivot_point = nums[0].upper_bound + partition11.lower_bound
            if pivot_point > target_index:
                newlists = (nums[0], partition10)
            else:
                newlists = (nums[0], partition11)
        
        elif nums[1].is_disjoint_and_less_than(partition01):
            logging.debug("Case 6, nums[1] disjoint from partition01")
            pivot_point = nums[1].upper_bound + partition01.lower_bound
            if pivot_point > target_index:
                newlists = (nums[1], partition00)
            else:
                newlists = (nums[1], partition01)
       
        elif partition00.is_disjoint_and_less_than(nums[1]):
            logging.debug("Case 7, partition00 disjoint from nums[1]")
            pivot_point = partition00.upper_bound + nums[1].lower_bound
            if pivot_point > target_index:
                newlists = (partition00, nums[1])
            else:
                newlists = (partition01, nums[1])
        
        elif partition10.is_disjoint_and_less_than(nums[0]):
            logging.debug("Case 8, partition10 disjoint from nums[0]")
            pivot_point = partition10.upper_bound + nums[0].lower_bound
            if pivot_point > target_index:
                newlists = (partition10, nums[0])
            else:
                newlists = (partition11, nums[0])
        
        elif partition00.is_disjoint_and_less_than(partition11) and partition10.is_disjoint_and_less_than(partition01):
            logging.debug("Case 9, partition00 disjoint from partition11 and partition10 disjoint from partition01")
            pivot_point = partition00.upper_bound + partition10.upper_bound
            if pivot_point > target_index:
                newlists = (partition00, partition10)
            else:
                newlists = (partition01, partition11)
        
        elif partition10.is_disjoint_and_less_than(partition01):
            logging.debug("Case 10, partition10 disjoint from partition01")
            pivot_point = partition00.upper_bound + partition10.upper_bound
            if pivot_point > target_index:
                newlists =  (partition00, nums[1])
            else:
                newlists = (nums[0], partition11)
        
        elif partition00.is_disjoint_and_less_than(partition11):
            logging.debug("Case 11, partition00 disjoint from partition11")
            pivot_point = partition00.upper_bound + partition10.upper_bound
            if pivot_point > target_index:
                newlists = (nums[0], partition10)
            else:
                newlists = (partition01, nums[1])
        else:
            # Missed a case!
            logging.error("Value did not conform to any of our defined cases.")
            raise ValueError
        
        if newlists == nums:
            # Duped recursion
            logging.error("Recursion reached fixed point (this should never happen).")
            raise RecursionError
        return self.median_from_window_sorted_lists(newlists)
    
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        if len(nums1) == 0 and len(nums2) == 0:
            # Not sure if I'm supposed to catch this or not...
            return None
        elif len(nums1) == 0:
            return self.median_from_single_sorted_array(nums2)
        elif len(nums2) == 0:
            return self.median_from_single_sorted_array(nums1)
        else:        
            return self.median_from_window_sorted_lists((WindowSortedList(nums1), WindowSortedList(nums2)))



import unittest

class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.sortedlist1 = WindowSortedList([1, 2, 3, 4, 5, 12], bounds = (2, 5))
        self.sortedlist2 = WindowSortedList([7, 9, 10, 11], bounds = (0, 2))
        
        self.sortedlist3 = WindowSortedList([1, 2, 3, 4, 5])
        self.sortedlist4 = WindowSortedList([8, 9, 10, 11])
        
        self.sortedarray1 = [0, 1, 2, 4, 5, 10, 12, 15]
        self.sortedarray2 = [4, 6, 7, 8, 9, 10, 25]

    def test_window_disjoint(self):
        self.assertTrue(self.sortedlist1.is_disjoint_and_less_than(self.sortedlist2))
        self.assertTrue(self.sortedlist2.is_disjoint_and_greater_than(self.sortedlist1))
    
    def test_disjoint_list_median(self):
        self.assertEqual(Solution.median_from_disjoint_lists((self.sortedlist3, self.sortedlist4)), 5)
        self.assertEqual(Solution.median_from_disjoint_lists((self.sortedlist1, self.sortedlist2)), 6)
    
    @staticmethod
    def generate_lists_with_median():
        import random
        from statistics import median
        length_one = random.randrange(1, 10)
        length_two = random.randrange(1, 10)

        first_list = [random.randrange(100) for x in range(length_one)]
        second_list = [random.randrange(100) for x in range(length_two)]
        first_list.sort()
        second_list.sort()

        the_median = median(first_list + second_list)
        return ((first_list, second_list), the_median)

    def test_median_from_sorted_arrays(self):
        # Some specifically pesky examples
        #self.assertEqual(Solution().findMedianSortedArrays(self.sortedarray1, self.sortedarray2), 7)
        self.assertEqual(Solution().findMedianSortedArrays([1, 2, 3, 4], []), 2.5)
        self.assertEqual(Solution().findMedianSortedArrays([26, 33, 49, 50, 65, 70, 74, 79, 84], [19, 29, 32, 53, 90]), 51.5)
        self.assertEqual(Solution().findMedianSortedArrays([1, 6, 19, 32, 36, 42, 46, 76], [23, 28, 57, 58, 83, 85, 90]), 42)
        

        for i in range(100):
            # Test 20 random pairs of sorted lists
            sortedlists, the_median = self.generate_lists_with_median()
            logging.debug("Testing lists:")
            logging.debug(sortedlists)
            logging.debug(the_median)
            result = Solution().findMedianSortedArrays(*sortedlists)
            logging.debug("Found answer: {}".format(result))
            self.assertEqual(result, the_median)

if __name__ == '__main__':
    unittest.main()
