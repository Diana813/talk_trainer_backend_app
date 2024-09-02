class VowelChecker:
    three_letter_combinations = [
        'eau', 'iou', 'uoi'
    ]
    two_letter_combinations = [
        'ae', 'ai', 'ao', 'au', 'ea', 'ei', 'eo', 'eu',
        'ia', 'ie', 'io', 'iu', 'oa', 'oe', 'oi', 'oo', 'ou',
        'ua', 'ue', 'ui', 'uo'
    ]
    vowels = set('aeiouyąęó')

    def count_syllables(self, word):
        word = word.lower()
        syllable_count = 0
        i = 0
        length = len(word)

        while i < length:
            if word[i] in self.vowels:
                matched_combination = False
                for combination in self.three_letter_combinations:
                    if word[i:i + len(combination)] == combination:
                        syllable_count += 1
                        i += len(combination) - 1
                        matched_combination = True
                        break
                if not matched_combination:
                    for combination in self.two_letter_combinations:
                        if word[i:i + len(combination)] == combination:
                            syllable_count += 1
                            i += len(combination) - 1
                            matched_combination = True
                            break
                if not matched_combination:
                    syllable_count += 1
            i += 1

        return max(syllable_count, 1)

