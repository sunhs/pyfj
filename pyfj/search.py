import os
from typing import *


def match_dispatcher(patterns: List[str], candidates: List[str], count=1) -> List[Tuple[int, str]]:
    cwd = os.getcwd()
    rst = []

    for idx, candidate in enumerate(candidates):
        if candidates == cwd:
            continue

        if len(patterns) == 1:
            if whole_match(patterns[0], candidate):
                rst.append((idx, candidate))
        else:
            parts = candidate.split("/")
            if part_match(patterns, parts):
                rst.append((idx, candidate))

        if len(rst) == count:
            break

    return rst


def whole_match(pattern: str, candidate: str) -> bool:
    return reverse_lcs(pattern, candidate)


def part_match(patterns: List[str], candidate_parts: List[str]) -> bool:
    rev_pats = reversed(patterns)
    rev_cand_parts = reversed(candidate_parts)

    pat = next(rev_pats)
    for cand_part in rev_cand_parts:
        if not reverse_lcs(pat, cand_part):
            continue

        try:
            pat = next(rev_pats)
        except StopIteration:
            return True

    return False


def reverse_lcs(pattern: str, target: str) -> bool:
    len_pattern, len_target = len(pattern), len(target)
    dp = [[0] * (len_target + 1) for _ in range(len_pattern + 1)]

    for i in range(len_pattern - 1, -1, -1):
        for j in range(len_target - 1, -1, -1):
            dp[i][j] = dp[i + 1][j + 1] + 1 if pattern[i] == target[j] else max(dp[i + 1][j], dp[i][j + 1])

    return dp[0][0] == len_pattern
