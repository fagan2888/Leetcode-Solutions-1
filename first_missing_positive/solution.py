from typing import List, Tuple


class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        num_positives = 0
        the_min = len(nums)
        the_max = 0
        the_sum = 0
        for i in range(len(nums)):
            if nums[i] > 0:
                num_positives += 1
                the_sum += nums[i]
                if nums[i] < the_min:
                    the_min = nums[i]
                if nums[i] > the_max:
                    the_max = nums[i]
        print('the_min', the_min)
        if the_min != 1:
            return 1
        expected_sum_given_length = num_positives * (num_positives + 1) / 2
        expected_sum_given_max = the_max * (the_max + 1) / 2
        if the_sum == expected_sum_given_length and the_sum == expected_sum_given_max:
            return the_max + 1
        for i in range(len(nums)):
            # Bucket sort.
            if nums[i] < 1 or nums[i] > len(nums):
                nums[i] = None
            else:
                swapped = nums[nums[i] - 1]
                nums[nums[i] - 1] = nums[i]
                if swapped is None or swapped < 1 or swapped > len(nums):
                    nums[i] = None
                else:
                    nums[i] = swapped
                counter = 0
                while 1:
                    if nums[i] is None or nums[i] == i + 1:
                        break
                    swapped = nums[nums[i] - 1]
                    if swapped == nums[i]:
                        break
                    else:
                        nums[nums[i] - 1] = nums[i]
                        if swapped is None or swapped < 1 or swapped > len(nums):
                            nums[i] = None
                        else:
                            nums[i] = swapped
                    counter += 1
                    #if counter > 3:
                    #    import pdb; pdb.set_trace()
        for i in range(len(nums)):
            if nums[i] is None or nums[i] != i + 1:
                return i+1
        return len(nums)


if __name__ == '__main__':
    pass
