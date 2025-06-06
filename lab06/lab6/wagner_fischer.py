def wagner_fischer(s1: str, s2: str,
                  insert_cost: int = 1,
                  delete_cost: int = 1,
                  substitute_cost: int = 1) -> int:
    m, n = len(s1), len(s2)

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1): dp[i][0] = i * delete_cost
    for j in range(n + 1): dp[0][j] = j * insert_cost

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else substitute_cost

            dp[i][j] = min(
                dp[i - 1][j] + delete_cost, # usniecie
                dp[i][j - 1] + insert_cost, # insert
                dp[i - 1][j - 1] + cost # zmiana
            )

    return dp[m][n]

def wagner_fischer_with_alignment(s1: str, s2: str) -> tuple[int, str, str]:
    m, n = len(s1), len(s2)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1): dp[i][0] = i
    for j in range(n+1): dp[0][j] = j
    for i in range(1, m+1):
        for j in range(1, n+1):
            cost = 0 if s1[i-1] == s2[j-1] else 1
            dp[i][j] = min(dp[i-1][j-1] + cost, dp[i-1][j] + 1, dp[i][j-1] + 1)
    a1, a2, i, j = [], [], m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and dp[i][j] == dp[i-1][j-1] + (0 if s1[i-1] == s2[j-1] else 1):
            a1.append(s1[i-1])
            a2.append(s2[j-1])
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i-1][j] + 1:
            a1.append(s1[i-1])
            a2.append('-')
            i -= 1
        else:
            a1.append('-')
            a2.append(s2[j-1])
            j -= 1
    return dp[m][n], ''.join(reversed(a1)), ''.join(reversed(a2))

def wagner_fischer_space_optimized(s1: str, s2: str) -> int:
    if len(s1) < len(s2):
        s1, s2 = s2, s1  # s2 krotsszy

    previous = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1, 1):
        current = [i]
        for j, c2 in enumerate(s2, 1):
            cost = 0 if c1 == c2 else 1
            current.append(min(
                previous[j] + 1,         # usuniecie
                current[j - 1] + 1,      # wstawienie
                previous[j - 1] + cost   # zamiana
            ))
        previous = current
    return previous[-1]