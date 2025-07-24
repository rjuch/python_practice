from collections import Counter

def steadyGene(gene):
    # Write your code here
    n = len(gene)
    
    steady_count = n//4

    totals = {letter:0 for letter in 'ACTG'}
    diffs = {letter:0 for letter in 'ACTG'}
    excess_letters = []
    deficit_letters = []
    total_excess = 0
    
    # get letter count
    for i in range(0, n):
        totals[gene[i]] += 1
  
    for letter in 'ACTG':
        diffs[letter] = totals[letter] - steady_count
        if diffs[letter] > 0:
            excess_letters.append(letter)
            total_excess += diffs[letter]
        else:
            deficit_letters.append(letter)

    if all(diffs[letter] == 0 for letter in 'ACTG'):
        return 0

    total_excess = int(total_excess)
    
    print(totals)
    print(diffs)
    print(excess_letters)
    print(deficit_letters)
    print(total_excess) # at least this many replacements
    
    # start with smallest window, for efficiency
    
    for window in range(total_excess, int(total_excess + 2000)):
        print(f'window: {window}')
        for start in range(0, n - window + 1):
            end = start + window
            if end >= n:
                continue
            gene_substring = gene[start:end]
            
            substring_excess_letter_counts = Counter(gene_substring)

            #substring_excess_letter_counts = {letter:0 for letter in excess_letters}
            
            # for substring_letter in gene_substring: 
            #     if substring_letter in excess_letters:
            #         substring_excess_letter_counts[substring_letter] += 1
            
            if all(substring_excess_letter_counts[excess_letter] == diffs[excess_letter] for excess_letter in excess_letters):
                return len(gene_substring)
            else:
                continue
            # found = True
            # for excess_letter in excess_letters:
            #     if substring_excess_letter_counts[excess_letter] != diffs[excess_letter]:
            #         found = False
            #         continue
            
            # if found:
            #     print(f'found: {gene_substring}')
            #     return len(gene_substring)
                
    return 0

def steadyGene_fast(s):
    from collections import Counter

    n = len(s)
    ideal = n // 4
    count = Counter(s)

    # If already steady
    if all(count[base] <= ideal for base in "ACGT"):
        return 0

    min_len = n
    left = 0
    window_count = Counter()

    for right in range(n):
        window_count[s[right]] += 1

        # Shrink the window from the left as long as the string
        # outside the window can be made steady
        while all(count[base] - window_count[base] <= ideal for base in "ACGT"):
            min_len = min(min_len, right - left + 1)
            window_count[s[left]] -= 1
            left += 1

    return min_len

x = steadyGene_fast('ACAAAAATAAACAAAAACAAAAAAAAAATAAATACAATAAAAAAAAAAAATGAAATACAACAACAAATAAAATAAAAACGACTAAAAAATAAAAAAAAAAAAAAAAAGAGTACTAAAAAAAAAAAAAAAAAATAAAAAAAAAAAAAACACAATCAAAATAAACAAAAAAAAAAAAACCAAAATAATCAACAAAAAAAAAAAAAACAAAAACAACAACAAACAAAAAAAAACACAAACAAAAAAAAAAAAAAAACAAAACAAACAAAAAAAAAAAAACAAAAAAACAAAAAAAAAAAAAAAAACAAAAAAAAAAATAAAAAAAAAAAAAAAAAAAAAACAAACAAAAAAAAAAAATACAAAAAGCTATAAAAAAAAAAAAATTAAAAAACAAAAAAAAATAAAAAAAAAAAAAAAAAAAAAAAATAAAAAAAAAAAAAAAAAAAAAATAAAAAAAAAAAAAAAAAAGAAAAACAAAAAAAAAAAAAAAAACAACCAAAAAACAAAAAAAAACTAAAAAAAAAAAAAAAAAAAAAAAAAAATAACAAAAAACACAAAAAAAAAAAAGAAAGAAAAAAAACACAAAAAAAAACAAACAAAAAAAAAAAAAAAAAAAGAAAACAAAAAAACAAAAAAAACAAAAAAAAAACAAAAATTGGACAAAAAAAAACAAAAAAAAAAAACAAAAAAAGTAAAACAAATAAAAAAACAAAAAAAACAAAAAAAAAAAAAAAAAACAAAAAAGAAACAAAAAACAAAAAAAAATAACAAAACCAAAAAACAAATAAAAAACAAAAAAAATAACACAAAAAAAAAAAGAAACAAAAAAAAAAAAAAAAAAAAAAATTATAAAAAAAAAAAAAAAACAAAAAAAAAAAAAACAAAAAAAAAAGGAAAAAAAAAAAAAAAAAAAAAAAAAAATAACTAAACAAAAAAAAACAAACAAAAAATCAAAAAAAAAAAAGAAAAAAGAATAAGCAACAAAAACACAAAAAAAAAAAAAAAAAAAAAAAACATAAACAATAATAAAAAAAAAACAAAAAAAACAAAAGAACAACAAAAAACAAAACTAAACAAATAAAAAAAAAAAAACAAAAACTACAAAAAAAAAAAGAAAAAAAAAGAAAAAAAAACAAATAAAAGAAAAAAAAAAAAAAAAAAAACACAAAAAAAAAAATAAAAAAAAAAAAAAAAACAAAATAAACAAAAACAAAGAAAAAAACAAACAAAAAAAAAAAACAAAAAACTAAAAACAAAAAAAAAACAAAACACAAAAAAAAAAAAAAATAAAAAAAAAACAAAAAAACAAAAAGGAAAAAAAAAAAAGAACAAAAAAAAAAACAACAGAAAAAAGAAAAGAAAAAAAAAAAAAGACCACAAAATAAAAAAAAACAACAAACAAAAAAAAACAAAACAAAAAAACGAACAAAAAAAACAAAAACAAAAAAAAAAAAAAAAAAAAAAAGGCAAAAACAAAAAAAACAAAACAAAACAAAAAAACAAAAAAAAATTAAGATAAAGAACAAAAAAAGAAGAGAAAAAATTAACAAAAAAAAAAAAATAAAAAATACAAAAAGAAATAAAAAATACAACACACAACAAAAACGAAAAAAAAAAAAAAAACACAAAATAGAAAAAAAAAAAAAACAAAAAAAAAAAAAAGAAAAAAACAAAAAAAAAAAAATAAAAAAAAACGACACAGAAACAAAAAATAACAAAAAAAAAAAAAATAAAAAAAAAACAAAAAAAAAACAAAAAATAAAAAAAAAAACAAACAAAAAAAAAAAAAAAATAAAAAAAAAAAAAGCAAAACATAAACAAGAAAAAAAAAAAAAGTACAAATAACAAAACAAAAAAGACACTAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAAAAAAAAGAAAAAAAACCACAAAACAAAAAAATAAAGCAAAAAAAAAAAAAAAAAAAAAAAAAAAATAAATGAAAAAAAAAAGAAAACCAAAAAAATAAAAGA')
print(x)