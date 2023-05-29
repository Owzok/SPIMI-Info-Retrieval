file_paths = ['./blocks/block-0.txt', './blocks/block-1.txt', './blocks/block-2.txt', './blocks/block-3.txt']

merged_block = merge_all_blocks(file_paths)

write_to_disk_with_tfidf(merged_block, "spimi_inverted_index_good.txt", 6)