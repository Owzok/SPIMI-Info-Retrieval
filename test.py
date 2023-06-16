list_1 = [1, 2, 2, 4, 5]
list_2 = [2, 2, 3, 4, 6]
list_3 = [1, 2, 2, 3, 3]
list_4 = [1, 3, 4, 4, 10]

def sort_lists(list1, list2, capacity):
    index_1 = 0
    index_2 = 0

    new_list1 = []
    new_list2 = []

    while index_1 < len(list1) and index_2 < len(list2):
        print(index_1, index_2)
        if list1[index_1] > list2[index_2]:
            if len(new_list1) >= capacity:
                new_list2.append(list2[index_2])
            else:
                new_list1.append(list2[index_2])
            index_2 += 1

        elif list1[index_1] < list2[index_2]:
            if len(new_list1) >= capacity:
                new_list2.append(list1[index_1])
            else:
                new_list1.append(list1[index_1])
            index_1 += 1
        else:
            if len(new_list1) >= capacity:
                new_list2.append(list1[index_1])
            else:
                new_list1.append(list1[index_1])
            index_1 += 1
            if len(new_list1) >= capacity:
                new_list2.append(list1[index_2])
            else:
                new_list1.append(list1[index_2])
            index_2 += 1
            
    while index_1 < len(list1):
        if len(new_list1) >= capacity:
            new_list2.append(list1[index_1])
        else:
            new_list1.append(list1[index_1])
        index_1 += 1

    while index_2 < len(list2):
        if len(new_list1) >= capacity:
            new_list2.append(list2[index_2])
        else:
            new_list1.append(list2[index_2])
        index_2 += 1

    return new_list1, new_list2

print(sort_lists(list_1, list_3, 5))
