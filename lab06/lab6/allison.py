def allison_global_alignment(s1: str, s2: str,
                             match_score: int = 2,
                             mismatch_score: int = -1,
                             gap_penalty: int = -1) -> tuple[int, str, str]:
    m, n = len(s1), len(s2)
    dp = [[i * gap_penalty if j == 0 else j * gap_penalty if i == 0 else 0 for j in range(n + 1)] for i in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            match = dp[i-1][j-1] + (match_score if s1[i-1] == s2[j-1] else mismatch_score)
            delete = dp[i-1][j] + gap_penalty
            insert = dp[i][j-1] + gap_penalty
            dp[i][j] = max(match, delete, insert)

    a1, a2, i, j = [], [], m, n
    while i > 0 or j > 0:
        score = dp[i][j]
        if i > 0 and j > 0 and score == dp[i-1][j-1] + (match_score if s1[i-1] == s2[j-1] else mismatch_score):
            a1.append(s1[i-1]); a2.append(s2[j-1]); i -= 1; j -= 1
        elif i > 0 and score == dp[i-1][j] + gap_penalty:
            a1.append(s1[i-1]); a2.append('-'); i -= 1
        else:
            a1.append('-'); a2.append(s2[j-1]); j -= 1

    return dp[m][n], ''.join(reversed(a1)), ''.join(reversed(a2))

def allison_local_alignment(s1: str, s2: str,
                            match_score: int = 2,
                            mismatch_score: int = -1,
                            gap_penalty: int = -1) -> tuple[int, str, str, int, int]:
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    max_score, max_pos = 0, (0, 0)

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            match = dp[i - 1][j - 1] + (match_score if s1[i - 1] == s2[j - 1] else mismatch_score)
            delete = dp[i - 1][j] + gap_penalty
            insert = dp[i][j - 1] + gap_penalty
            dp[i][j] = max(0, match, delete, insert)
            if dp[i][j] > max_score:
                max_score = dp[i][j]
                max_pos = (i, j)

    i, j = max_pos
    aligned_s1, aligned_s2 = [], []
    while i > 0 and j > 0 and dp[i][j] != 0:
        score = dp[i][j]
        diag = dp[i - 1][j - 1]
        up = dp[i - 1][j]
        left = dp[i][j - 1]
        if score == diag + (match_score if s1[i - 1] == s2[j - 1] else mismatch_score):
            aligned_s1.append(s1[i - 1])
            aligned_s2.append(s2[j - 1])
            i -= 1
            j -= 1
        elif score == up + gap_penalty:
            aligned_s1.append(s1[i - 1])
            aligned_s2.append('-')
            i -= 1
        else:
            aligned_s1.append('-')
            aligned_s2.append(s2[j - 1])
            j -= 1

    aligned_s1.reverse()
    aligned_s2.reverse()
    return max_score, ''.join(aligned_s1), ''.join(aligned_s2), i, j
