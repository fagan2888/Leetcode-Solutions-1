from typing import List, Tuple

class Solution:
    @staticmethod
    def is_couple(left, right):
        if left < right:
            return left % 2 == 0 and right - left == 1
        else:
            return right % 2 == 0 and left - right == 1
    
    def minSwapsCouples(self, row: List[int]) -> int:
        pairs_needing_swaps = []
        for i in range(len(row) // 2):
            print('Checking row {}'.format(i))
            if not self.is_couple(row[i*2], row[i*2 + 1]):
                print('Does need a swap.')
                pairs_needing_swaps.append(i)
        pairwise_available = 0
        # Worst case is we need to daisy chain, best case is each swap is pairwise.
        for i in pairs_needing_swaps:
            print('i', i)
            for j in pairs_needing_swaps:
                print('j', j)
                if i == j:
                    continue
                print('self.is_couple(row[i*2], row[j*2])', self.is_couple(row[i*2], row[j*2]))
                print('self.is_couple(row[i*2 + 1], row[j*2 + 1])', self.is_couple(row[i*2 + 1], row[j*2 + 1]))
                print('self.is_couple(row[i*2 + 1], row[j*2])', self.is_couple(row[i*2 + 1], row[j*2]))
                print('self.is_couple(row[i*2], row[j*2 + 1])', self.is_couple(row[i*2], row[j*2 + 1]))
                if self.is_couple(row[i*2], row[j*2]) and self.is_couple(row[i*2 + 1], row[j*2 + 1]):
                    pairwise_available += 1
                elif self.is_couple(row[i*2 + 1], row[j*2]) and self.is_couple(row[i*2], row[j*2 + 1]):
                    pairwise_available += 1
        if len(pairs_needing_swaps) != pairwise_available:
           return (pairwise_available // 2) + len(pairs_needing_swaps) - pairwise_available - 1
        else:
            return pairwise_available // 2


#print(Solution().minSwapsCouples([2,0,5,4,3,1]))
assert(Solution().minSwapsCouples([5,4,2,6,3,1,0,7]) == 2)
assert(Solution().minSwapsCouples([10,7,4,2,3,0,9,11,1,5,6,8]) == 4)

