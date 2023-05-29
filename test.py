from collections import OrderedDict

def merge_sort_blocks(blocks):
    """
    Perform merge sort on a list of blocks
    """
    if len(blocks) <= 1:
        return blocks
    mid = len(blocks) // 2
    left = merge_sort_blocks(blocks[:mid])
    right = merge_sort_blocks(blocks[mid:])
    return merge_blocks(left, right)


def merge_blocks(block1, block2):
    """
    Merge two blocks by merging the lists for duplicate words
    """
    merged_block = OrderedDict()
    for block in [block1, block2]:
        for word, postings in block[0].items():
            if word in merged_block:
                # Check if the first value is the same
                if merged_block[word][0][0] == postings[0][0]:
                    merged_block[word][0] = (merged_block[word][0][0], merged_block[word][0][1] + postings[0][1])
                else:
                    merged_block[word] += postings
            else:
                merged_block[word] = postings
    sorted_block = OrderedDict(sorted(merged_block.items(), key=lambda x: x[0]))
    return [sorted_block]


# Example blocks
block1 = {'desayun': [(3, 1)], 'cuent': [(3, 1)], 'amig': [(3, 1), (4, 1), (5, 3)], 'experient': [(3, 1)], 'viv': [(3, 1), (5, 1)]}
block2 = {'desayun': [(3, 1)], 'graci': [(5, 2)], 'aragorn': [(5, 2)], 'nob': [(5, 1)], 'logr': [(5, 2)]}

blocks = [block1, block2]

parsed_blocks = merge_sort_blocks(blocks)

# Print the sorted and merged blocks
print(parsed_blocks)