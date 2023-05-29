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
        start_time = time.time()
        results = spimi.search_query(query, documents, 100)

        print(f"\nSearch Results of '{query}':")
        print("in", time.time()-start_time, "s")

        for doc_id, score in results:
            print(f"Document ID: {doc_id}, Score: {score}")
    elif x == 2:
        break