import unittest


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        import median_two_sorted_arrays as med
        self.sortedlist1 = med.WindowSortedList([1, 2, 3, 4, 5, 12], bounds = (2, 5))
        self.sortedlist2 = med.WindowSortedList([7, 9, 10, 11], bounds = (0, 2))
        
        self.sortedlist3 = med.WindowSortedList([1, 2, 3, 4, 5])
        self.sortedlist4 = med.WindowSortedList([8, 9, 10, 11])

    def test_window_disjoint(self):
        self.assertTrue(self.sortedlist1.is_disjoint_and_less_than(self.sortedlist2))
        self.assertTrue(self.sortedlist2.is_disjoint_and_greater_than(self.sortedlist1))
    
    def test_disjoint_list_median(self):
        import median_two_sorted_arrays as med
        self.assertEqual(med.Solution.median_from_disjoint_lists((self.sortedlist3, self.sortedlist4)), 5)
        self.assertEqual(med.Solution.median_from_disjoint_lists((self.sortedlist1, self.sortedlist2)), 6)

if __name__ == '__main__':
    unittest.main()
