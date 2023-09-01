import os
import re
from typing import *


def match_dispatcher(
    patterns: List[str], candidates: List[str], count: int = 1, sep: str = "/"
) -> List[Tuple[int, str]]:
    cwd = os.getcwd()
    rst: List[Tuple[int, str]] = []

    for idx, candidate in enumerate(candidates):
        if cwd in (candidate, os.path.realpath(candidate)) or not os.path.isdir(candidate):
            continue

        # if len(patterns) == 1 and not patterns[0].endswith("$"):
        #     if whole_match(patterns[0].lower(), candidate.lower()):
        #         rst.append((idx, candidate))
        # else:
        parts = re.split(sep, candidate)
        if part_match([p.lower() for p in patterns], [p.lower() for p in parts]):
            rst.append((idx, candidate))

        if len(rst) == count:
            return rst

    if len(patterns) == 1:
        for idx, candidate in enumerate(candidates):
            if candidate == cwd or not os.path.isdir(candidate):
                continue

            if whole_match(patterns[0].lower(), candidate.lower()):
                rst.append((idx, candidate))

            if len(rst) == count:
                return rst

    return rst


def whole_match(pattern: str, candidate: str) -> bool:
    return reverse_lcs(pattern, candidate)


def part_match(patterns: List[str], candidate_parts: List[str]) -> bool:
    rev_pats = reversed(patterns)
    rev_cand_parts = reversed(candidate_parts)

    pat = next(rev_pats)
    force_match_end = True
    if pat.endswith("$"):
        pat = pat[:-1]
        force_match_end = True

    for i, cand_part in enumerate(rev_cand_parts):
        if not reverse_lcs(pat, cand_part):
            if force_match_end and i == 0:
                return False
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
