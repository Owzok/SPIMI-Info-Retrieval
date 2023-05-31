stops = ['stop1.txt', 'stop2.txt', 'stop3.txt', 'stop4.txt']

stop_words = set()

# Read words from each file and add them to the set
for file_name in stops:
    with open(file_name, 'r') as file:
        words = file.read().split()
        stop_words.update(words)

# Write the unique stop words to the output file
with open('../stop_words_spanish.txt', 'w') as output_file:
    for word in stop_words:
        output_file.write(word + '\n')