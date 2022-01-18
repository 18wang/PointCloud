def majorityElement(A, N):
    # Your code here

    dict_count = dict()

    max = 1
    result = A[1]
    for i in A:
        if dict_count.get(i):
            dict_count[i] = dict_count[i] + 1
            if dict_count[i] > max:
                max = dict_count[i]
                result = i
        else:
            dict_count[i] = 1

    return result, max

print(majorityElement([1, 2], 2))
