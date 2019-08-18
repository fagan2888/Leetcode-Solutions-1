from typing import Tuple
import logging


class Solution:
    def is_match_compiled(self, s: str, patterns: [Tuple[int, bool]]) -> bool:
        
        spointer = 0
        ppointer = 0
        while spointer < len(s) or ppointer < len(patterns):
            logging.debug("Spointer set to {}, ppointer set to {}.".format(spointer, ppointer))
            if spointer == len(s):
                logging.debug("Finished string, unfinished regexp")
                # We must have some unfinished ppointers, all remaining patterns need to be star patterns.
                return all(patterns[i][1] for i in range(ppointer, len(patterns)))
            elif ppointer == len(patterns):
                logging.debug("Finished regexp, unfinished string")
                # We must have unfinished portions of the string, return False.
                return False
            elif not patterns[ppointer][1]:
                logging.debug("Non star pattern.")
                # Simple enough, check if they are equal, if not return false.
                if patterns[ppointer][0] == '.':
                    ppointer += 1
                    spointer += 1
                    continue
                else:
                    if patterns[ppointer][0] != s[spointer]:
                        return False
                    else:
                        ppointer += 1
                        spointer += 1
                        continue
            else:
                logging.debug("Found star pattern.")
                # We have a multi pointer, this is where it gets tricky.
                # Consecutive multi pointers demand that we run through the string until we run into the next non-repeating element.
                star_patterns = []
                final_pattern = None
                for i in range(ppointer, len(patterns)):
                    if patterns[i][1]:
                        star_patterns.append(patterns[i][0])
                        ppointer += 1
                    if not patterns[i][1]:
                        logging.debug('Final pattern will be {}'.format(patterns[i]))
                        final_pattern = patterns[i][0]
                        ppointer += 1
                        break
                starpointer = 0
                maxstarmatch = spointer
                finalmatches = []
                all_valid = any(x == '.' for x in star_patterns)
                for i in range(spointer, len(s)):
                    logging.debug('Looking at string pointer {} with value {}'.format(i, s[i]))
                    valid = False
                    if final_pattern is not None and (final_pattern == '.' or s[i] == final_pattern):
                        finalmatches.append(i)
                    if all_valid:
                        maxstarmatch += 1
                        valid = True
                    else:
                        while starpointer < len(star_patterns):
                            logging.debug('Examining star pattern {}'.format(star_patterns[starpointer]))
                            logging.debug('s[i] ("{}") == star_patterns[starpointer] ("{}") => {}'.format(s[i], star_patterns[starpointer], s[i] == star_patterns[starpointer]))
                            if s[i] == star_patterns[starpointer]:
                                maxstarmatch += 1
                                valid = True
                                break
                            else:
                                starpointer += 1
                    if not valid:
                        break
                if final_pattern is not None:
                    if len(finalmatches) == 0:
                        logging.debug("Did not find a final match after stars")
                        return False
                    else:
                        return any(self.is_match_compiled(s[match + 1:], patterns[ppointer:]) for match in finalmatches)
                else:
                    spointer = maxstarmatch
        logging.debug("Concluded loop")
        return spointer == len(s) and ppointer == len(patterns)
    
    def isMatch(self, s: str, p: str) -> bool:
        logging.info("Solving string {}, pattern {}".format(s, p))
        if s==p:
            # Special case where both are empty or identical.
            return True
        # Patterns are (value, multimatch)
        patterns = []
        i = 0
        while i < len(p):
            if i < len(p) - 1 and p[i + 1] == '*':
                assert(p[i] != '*') # 'Two asterisks in a row is invalid.'
                patterns.append((p[i], True))
                i += 2
            else:
                assert(p[i] != '*') # 'Invalid asterisk.'
                patterns.append((p[i], False))
                i += 1  
        
        return self.is_match_compiled(s, patterns)

if __name__ == '__main__':
    print('Running asserts.')
    assert(not Solution().isMatch('abcd', 'd*'))
    assert(Solution().isMatch('aa', 'a*'))
    assert(Solution().isMatch('ab', '.*'))
    assert(Solution().isMatch('aab', 'c*a*b'))
    assert(not Solution().isMatch('mississippi', 'mis*is*p*.'))
    assert(Solution().isMatch('mississippi', 'mis*is*ip*.'))
    assert(Solution().isMatch('a', 'ab*'))
    assert(Solution().isMatch('ab', '.*..'))
    print('...done.')



