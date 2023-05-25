from spimi import *

documents = read_txt_files("./documents/")

spimi = SPIMI()

# Menu
# [0] : Just generate inverted index and end
# [1] : Search (includes generation)
# [2] : Quit

print("[0] : Just generate inverted index \n[1] : Search\n[2] : Quit")
x = -1
while x != 0 and x != 1:
    x = int(input())
    if x == 0:
        print("gaa")
        spimi.index_documents(documents)
    elif x == 1:
        query = str(input("Enter the query: "))
        results, m_time = spimi.search_query(query, documents)

        print(f"\nSearch Results of '{query}':")
        for i in range(len(documents)):
            if i == results[0][0]:
                print(f"\n>> Found in: {m_time} seconds")

        for doc_id, score in results:
            print(f"Document ID: {doc_id}, Score: {score}")
    elif x == 2:
        break