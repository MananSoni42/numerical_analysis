def sum_exists(arr,sum):
    dp = arr.copy()
    for i in range(1,len(arr)):
        dp[i] = dp[i]>sum?
        for j in range(i):
            if dp[j] + arr[i] <= sum:
                dp[i] = max(dp[i], arr[i])
        if dp[i] == sum:
            return True
    print(dp)
    return False

print(sum_exists([4,1,10,12,5,2], 9))
print(sum_exists([4,1,10,12,5,2], 1))
print(sum_exists([4,1,10,12,5,2], 100))
