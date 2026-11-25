"""Complete dataset of 22 COL1000 Practice Problems v2 (IIT Delhi)."""

PROBLEMS = [
    {
        "id": 1,
        "slug": "collatz-steps",
        "title": "Collatz Steps",
        "difficulty": "Easy",
        "difficulty_tier": "Easy",
        "statement": (
            "Start with a positive integer `n`. Repeat the following rule until `n` becomes `1`: "
            "if `n` is even, replace it with `n/2`; if `n` is odd, replace it with `3n + 1`. "
            "Count how many times the rule was applied."
        ),
        "worked_example": (
            "For `n = 6` the numbers are `6 -> 3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1`. "
            "The rule was applied 8 times, so the answer is `8`."
        ),
        "input_format": "A single line containing the integer `n`.",
        "output_format": "Print the number of times the rule was applied. If `n = 1`, print `0`.",
        "constraints": "1 <= n <= 10^6. For every such n, the process reaches 1.",
        "starter_code": (
            "n = int(input())\n\n"
            "# Write your program here.\n"
            "# Store your final answer in the variable answer.\n\n"
            "print(answer)"
        ),
        "judge_mode": "exact",
        "sample_tests": [
            {"input": "6", "output": "8"},
            {"input": "1", "output": "0"},
            {"input": "27", "output": "111"},
        ],
        "hidden_tests": [
            {"input": "2", "output": "1"},
            {"input": "3", "output": "7"},
            {"input": "100", "output": "25"},
            {"input": "999999", "output": "258"},
        ],
        "hints": [
            "Initialize a counter `answer = 0` and loop `while n != 1:`.",
            "Inside the loop, check `n % 2 == 0` to use integer division `n = n // 2`; otherwise set `n = 3 * n + 1`. Increment `answer` on each iteration.",
        ],
        "solution_steps": [
            "Initialize `answer = 0` to count the number of rule applications.",
            "While `n > 1`, check if `n` is even (`n % 2 == 0`).",
            "If even, update `n //= 2`; otherwise, update `n = 3 * n + 1`.",
            "Increment `answer` by 1 after each update. When `n` reaches `1`, the loop terminates and `answer` holds the step count.",
            "Time Complexity: O(steps(n)). Space Complexity: O(1).",
        ],
        "solution_code": (
            "n = int(input())\n\n"
            "answer = 0\n"
            "while n != 1:\n"
            "    if n % 2 == 0:\n"
            "        n //= 2\n"
            "    else:\n"
            "        n = 3 * n + 1\n"
            "    answer += 1\n\n"
            "print(answer)"
        ),
    },
    {
        "id": 2,
        "slug": "sum-of-valid-numbers",
        "title": "Sum of the Valid Numbers",
        "difficulty": "Easy",
        "difficulty_tier": "Easy",
        "statement": (
            "A line contains several tokens separated by single spaces. A token is a *valid integer* "
            "if Python's `int(token)` accepts it, such as `12`, `-3` or `+5`. Any other token is *invalid*, "
            "such as `abc`, `3.5` or `4-2`. Add up all the valid integers and count the invalid tokens. "
            "Use `try` and `except` to handle the invalid tokens."
        ),
        "worked_example": (
            "For `10 abc 5 3.5 -2 x1`, the valid integers are `10`, `5` and `-2`, with sum `13`. "
            "The tokens `abc`, `3.5` and `x1` are invalid, so there are `3` invalid tokens. The answer is `13 3`."
        ),
        "input_format": "A single line containing the tokens, separated by single spaces.",
        "output_format": "Print two integers on one line, separated by a space: the sum of the valid integers, and the number of invalid tokens.",
        "constraints": "There are between 1 and 100 tokens. Each token has at most 10 characters, and uses only lowercase letters, digits, `+`, `-` and `.`.",
        "starter_code": (
            "tokens = input().split()\n\n"
            "# Write your program here.\n"
            "# Store the sum in the variable total.\n"
            "# Store the number of invalid tokens in the variable bad.\n\n"
            "print(total, bad)"
        ),
        "judge_mode": "exact",
        "sample_tests": [
            {"input": "10 abc 5 3.5 -2 x1", "output": "13 3"},
            {"input": "- -- 4-2 +5", "output": "5 3"},
            {"input": "hello world", "output": "0 2"},
        ],
        "hidden_tests": [
            {"input": "0 -0 +0 007", "output": "7 0"},
            {"input": "1.0 2. 3e4 -100 +100", "output": "0 3"},
            {"input": "-999 999 a b c", "output": "0 3"},
            {"input": "42", "output": "42 0"},
        ],
        "hints": [
            "Initialize `total = 0` and `bad = 0`, then iterate over each `tok` in `tokens`.",
            "Inside a `try:` block, do `total += int(tok)`. In `except ValueError:`, increment `bad += 1`.",
        ],
        "solution_steps": [
            "Initialize `total = 0` and `bad = 0`.",
            "Loop through every string `tok` in `tokens`.",
            "Attempt `val = int(tok)` inside a `try` block and add `val` to `total`.",
            "If `int(tok)` raises `ValueError`, catch it in `except ValueError:` and increment `bad` by 1.",
            "Time Complexity: O(N) where N is the number of tokens. Space Complexity: O(N) for storing `tokens`.",
        ],
        "solution_code": (
            "tokens = input().split()\n\n"
            "total = 0\n"
            "bad = 0\n"
            "for tok in tokens:\n"
            "    try:\n"
            "        total += int(tok)\n"
            "    except ValueError:\n"
            "        bad += 1\n\n"
            "print(total, bad)"
        ),
    },
    {
        "id": 3,
        "slug": "recursive-palindrome",
        "title": "Recursive Palindrome",
        "difficulty": "Easy",
        "difficulty_tier": "Easy",
        "statement": (
            "A string is a *palindrome* if it reads the same from left to right and from right to left. "
            "Complete the recursive function `is_pal(s)` so that it returns `True` if `s` is a palindrome "
            "and `False` otherwise. The function must call itself on a shorter string; it must not use a loop."
        ),
        "worked_example": (
            "For `level`, the first and last letters are both `l`. The letters in the middle, `eve`, "
            "form a palindrome too, so the answer is `True`. For `abca`, the first letter is `a` and the last "
            "letter is also `a`, but the middle part `bc` is not a palindrome, so the answer is `False`."
        ),
        "input_format": "A single line containing the string `s`.",
        "output_format": "Print `True` if `s` is a palindrome. Otherwise, print `False`.",
        "constraints": "1 <= |s| <= 500. The string contains only lowercase English letters.",
        "starter_code": (
            "def is_pal(s):\n"
            "    # Write your recursive code here.\n"
            "    # To run the program while it is incomplete, add a return statement.\n"
            "    pass\n\n"
            "s = input()\n"
            "answer = is_pal(s)\n\n"
            "print(answer)"
        ),
        "judge_mode": "exact",
        "sample_tests": [
            {"input": "racecar", "output": "True"},
            {"input": "ab", "output": "False"},
            {"input": "a", "output": "True"},
        ],
        "hidden_tests": [
            {"input": "abba", "output": "True"},
            {"input": "abca", "output": "False"},
            {"input": "level", "output": "True"},
            {"input": "abcdefedcba", "output": "True"},
        ],
        "hints": [
            "What is the base case? Any string of length 0 or 1 (`len(s) <= 1`) is automatically a palindrome.",
            "If `s[0] != s[-1]`, return `False`. Otherwise, recursively return `is_pal(s[1:-1])`.",
        ],
        "solution_steps": [
            "Base case: if `len(s) <= 1`, return `True` because an empty or single-character string reads the same forwards and backwards.",
            "Check the outer characters: if `s[0] != s[-1]`, the string cannot be a palindrome, so return `False`.",
            "Recursive step: return `is_pal(s[1:-1])`, which checks the substring with the first and last characters removed.",
            "Time Complexity: O(n^2) due to string slicing (or O(n) with index pointers). Space Complexity: O(n) recursion stack.",
        ],
        "solution_code": (
            "def is_pal(s):\n"
            "    if len(s) <= 1:\n"
            "        return True\n"
            "    if s[0] != s[-1]:\n"
            "        return False\n"
            "    return is_pal(s[1:-1])\n\n"
            "s = input()\n"
            "answer = is_pal(s)\n\n"
            "print(answer)"
        ),
    },
    {
        "id": 4,
        "slug": "versions-of-a-list",
        "title": "Versions of a List",
        "difficulty": "Medium",
        "difficulty_tier": "Medium",
        "statement": (
            "A list of `n` integers is changed `m` times. Each change has the form `i v`: set the item at "
            "position `i` (counting from 0) to the value `v`. After every change, the list is a new *version*. "
            "Version 0 is the original list. Record every version, so that all `m + 1` versions can be printed at the end."
        ),
        "worked_example": (
            "Start with the list `1 2 3` and the changes `0 9` and `2 7`. Version 0 is `1 2 3`. "
            "After the first change, version 1 is `9 2 3`. After the second change, version 2 is `9 2 7`. "
            "So the three lines `1 2 3`, `9 2 3` and `9 2 7` are printed."
        ),
        "input_format": "The first line contains `n`. The second line contains `n` integers. The third line contains `m`. Each of the next `m` lines contains two integers `i` and `v`.",
        "output_format": "Print `m + 1` lines. Line `j` (counting from 0) contains the items of version `j`, separated by spaces.",
        "constraints": "1 <= n <= 20. 0 <= m <= 20. 0 <= i < n. All values are between -100 and 100.",
        "starter_code": (
            "n = int(input())\n"
            "nums = list(map(int, input().split()))\n"
            "m = int(input())\n"
            "changes = []\n"
            "for _ in range(m):\n"
            "    i, v = map(int, input().split())\n"
            "    changes.append((i, v))\n\n"
            "# Write your program here.\n"
            "# Store the m + 1 versions, in order, in the list answer.\n"
            "# Each version is a list of integers.\n\n"
            "for version in answer:\n"
            "    print(*version)  # prints list entries without brackets"
        ),
        "judge_mode": "exact",
        "sample_tests": [
            {"input": "3\n1 2 3\n2\n0 9\n2 7", "output": "1 2 3\n9 2 3\n9 2 7"},
            {"input": "2\n5 5\n3\n1 6\n0 6\n1 5", "output": "5 5\n5 6\n6 6\n6 5"},
        ],
        "hidden_tests": [
            {"input": "4\n10 20 30 40\n0", "output": "10 20 30 40"},
            {"input": "1\n-5\n2\n0 100\n0 -100", "output": "-5\n100\n-100"},
            {"input": "3\n0 0 0\n3\n0 1\n1 2\n2 3", "output": "0 0 0\n1 0 0\n1 2 0\n1 2 3"},
        ],
        "hints": [
            "Be careful of list aliasing in Python! Appending `nums` directly (`answer.append(nums)`) only stores a reference to the same list.",
            "Use `nums.copy()` or `nums[:]` when appending each snapshot to `answer`.",
        ],
        "solution_steps": [
            "Start `answer = [nums.copy()]` to record Version 0 without aliasing.",
            "For each `(i, v)` in `changes`, update `nums[i] = v`.",
            "Append `nums.copy()` to `answer` after each update so later mutations do not overwrite earlier versions.",
            "Time Complexity: O((m + 1) * n). Space Complexity: O((m + 1) * n).",
        ],
        "solution_code": (
            "n = int(input())\n"
            "nums = list(map(int, input().split()))\n"
            "m = int(input())\n"
            "changes = []\n"
            "for _ in range(m):\n"
            "    i, v = map(int, input().split())\n"
            "    changes.append((i, v))\n\n"
            "answer = [nums.copy()]\n"
            "for i, v in changes:\n"
            "    nums[i] = v\n"
            "    answer.append(nums.copy())\n\n"
            "for version in answer:\n"
            "    print(*version)"
        ),
    },
    {
        "id": 5,
        "slug": "count-in-sorted-list",
        "title": "Count in a Sorted List",
        "difficulty": "Medium",
        "difficulty_tier": "Medium",
        "statement": (
            "A list of `n` integers is sorted in non-decreasing order, and some values may repeat. "
            "For each of `q` queries `x`, find how many times `x` appears in the list. "
            "The list and the number of queries can both be large, so scanning the whole list for every query is too slow. "
            "Use binary search to find where the value `x` starts and where it ends."
        ),
        "worked_example": (
            "In the list `1 2 2 2 5 9`, the value `2` appears 3 times, the value `9` appears once, "
            "and the value `3` does not appear. So the queries `2 3 9` give the answers `3`, `0` and `1`."
        ),
        "input_format": "The first line contains `n`. The second line contains the `n` sorted integers. The third line contains `q`. The fourth line contains the `q` query values.",
        "output_format": "Print `q` lines. Line `j` contains the number of times the `j`-th query value appears in the list.",
        "constraints": "1 <= n, q <= 10^5. All values are between -10^9 and 10^9.",
        "starter_code": (
            "n = int(input())\n"
            "a = list(map(int, input().split()))\n"
            "q = int(input())\n"
            "queries = list(map(int, input().split()))\n\n"
            "# Write your program here.\n"
            "# Store the q counts, in order, in the list answer.\n\n"
            "for c in answer:\n"
            "    print(c)"
        ),
        "judge_mode": "exact",
        "sample_tests": [
            {"input": "6\n1 2 2 2 5 9\n6\n2 3 1 9 0 10", "output": "3\n0\n1\n1\n0\n0"},
            {"input": "8\n-4 -4 0 3 3 3 8 8\n5\n3 -4 8 5 -5", "output": "3\n2\n2\n0\n0"},
        ],
        "hidden_tests": [
            {"input": "1\n42\n3\n41 42 43", "output": "0\n1\n0"},
            {"input": "5\n7 7 7 7 7\n2\n7 8", "output": "5\n0"},
            {"input": "6\n-1000000000 -5 0 0 0 1000000000\n4\n-1000000000 0 1000000000 1", "output": "1\n3\n1\n0"},
        ],
        "hints": [
            "Write a binary search helper `lower_bound(a, x)` that finds the first index `i` where `a[i] >= x` (or `len(a)` if all elements are `< x`).",
            "Then `upper_bound(a, x)` is the first index `i` where `a[i] > x`. The count of `x` is simply `upper_bound(a, x) - lower_bound(a, x)`.",
        ],
        "solution_steps": [
            "Define `lower_bound(a, x)` using binary search `[lo, hi] = [0, len(a)]`: while `lo < hi`, if `a[mid] < x` set `lo = mid + 1`, else `hi = mid`.",
            "Define `upper_bound(a, x)` similarly: while `lo < hi`, if `a[mid] <= x` set `lo = mid + 1`, else `hi = mid`.",
            "For each query `x`, the number of occurrences in sorted list `a` is `upper_bound(a, x) - lower_bound(a, x)`.",
            "Time Complexity: O(q log n). Space Complexity: O(n + q).",
        ],
        "solution_code": (
            "n = int(input())\n"
            "a = list(map(int, input().split()))\n"
            "q = int(input())\n"
            "queries = list(map(int, input().split()))\n\n"
            "def lower_bound(arr, x):\n"
            "    lo, hi = 0, len(arr)\n"
            "    while lo < hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        if arr[mid] < x:\n"
            "            lo = mid + 1\n"
            "        else:\n"
            "            hi = mid\n"
            "    return lo\n\n"
            "def upper_bound(arr, x):\n"
            "    lo, hi = 0, len(arr)\n"
            "    while lo < hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        if arr[mid] <= x:\n"
            "            lo = mid + 1\n"
            "        else:\n"
            "            hi = mid\n"
            "    return lo\n\n"
            "answer = [upper_bound(a, x) - lower_bound(a, x) for x in queries]\n\n"
            "for c in answer:\n"
            "    print(c)"
        ),
    },
    {
        "id": 6,
        "slug": "stairs-with-broken-steps",
        "title": "Stairs with Broken Steps",
        "difficulty": "Medium",
        "difficulty_tier": "Medium",
        "statement": (
            "A staircase has `n` steps, numbered 1 to `n`. You start on the ground (step 0) and want to reach step `n`. "
            "In one move you climb 1 step or 2 steps. Some steps are broken, and you must never land on a broken step. "
            "Count the number of different ways to reach step `n`. Two ways are different if the sequences of steps you land on are different. "
            "A simple recursive solution repeats the same work many times, so it is too slow for large `n`; remember the answers you have already found."
        ),
        "worked_example": (
            "Let `n = 5`, and step `3` is broken. You can reach step 2 in 2 ways, and step 4 in 2 ways (through step 2 only). "
            "Step 5 can be reached only from step 4, because step 3 is broken. So the answer is `2`: the ways are `0 -> 1 -> 2 -> 4 -> 5` and `0 -> 2 -> 4 -> 5`."
        ),
        "input_format": "The first line contains two integers `n` and `k`. The second line contains `k` distinct integers, the numbers of the broken steps. If `k = 0`, the second line is empty.",
        "output_format": "Print the number of ways to reach step `n`. If step `n` is broken, the answer is `0`.",
        "constraints": "1 <= n <= 50. 0 <= k <= n. Every broken step is between 1 and n.",
        "starter_code": (
            "n, k = map(int, input().split())\n"
            "broken = list(map(int, input().split())) if k > 0 else []\n\n"
            "# Write your program here.\n"
            "# Store your final answer in the variable answer.\n\n"
            "print(answer)"
        ),
        "judge_mode": "exact",
        "sample_tests": [
            {"input": "5 1\n3", "output": "2"},
            {"input": "10 3\n2 5 8", "output": "1"},
            {"input": "4 2\n1 2", "output": "0"},
        ],
        "hidden_tests": [
            {"input": "5 0\n", "output": "8"},
            {"input": "1 1\n1", "output": "0"},
            {"input": "1 0\n", "output": "1"},
            {"input": "30 2\n10 20", "output": "102850"},
        ],
        "hints": [
            "Use dynamic programming (or memoized recursion): let `dp[i]` be the number of ways to reach step `i`, starting with `dp[0] = 1`.",
            "Put `broken` into a `set`. For each step `i` from `1` to `n`: if `i` is in `broken_set`, `dp[i] = 0`; otherwise `dp[i] = dp[i - 1] + (dp[i - 2] if i >= 2 else 0)`.",
        ],
        "solution_steps": [
            "Store `broken` in a `set` for O(1) lookup.",
            "Create a DP array `dp` of size `n + 1` initialized to `0`, with `dp[0] = 1` (1 way to stand on the ground).",
            "For `i` from `1` to `n`: if `i` is broken, `dp[i] = 0`. Otherwise, `dp[i] = dp[i - 1]` plus `dp[i - 2]` (if `i >= 2`).",
            "The final answer is `dp[n]`. Time Complexity: O(n). Space Complexity: O(n).",
        ],
        "solution_code": (
            "n, k = map(int, input().split())\n"
            "broken = list(map(int, input().split())) if k > 0 else []\n\n"
            "broken_set = set(broken)\n"
            "dp = [0] * (n + 1)\n"
            "dp[0] = 1\n"
            "for i in range(1, n + 1):\n"
            "    if i in broken_set:\n"
            "        dp[i] = 0\n"
            "    else:\n"
            "        dp[i] = dp[i - 1] + (dp[i - 2] if i >= 2 else 0)\n\n"
            "answer = dp[n]\n"
            "print(answer)"
        ),
    },
    {
        "id": 7,
        "slug": "best-block-sum",
        "title": "Best Block Sum",
        "difficulty": "Medium",
        "difficulty_tier": "Medium",
        "statement": (
            "A *block* is one or more consecutive items of a list. Find the largest possible sum of a block. "
            "The list can contain negative numbers, and the block must have at least one item. "
            "A solution that tries every block is too slow for large lists. Instead, scan the list once, "
            "and keep track of the best sum of a block that ends at the current position."
        ),
        "worked_example": (
            "In the list `2 -5 4 -1 3 -6 2`, the block `4 -1 3` has sum `6`. No other block has a larger sum, so the answer is `6`."
        ),
        "input_format": "The first line contains `n`. The second line contains `n` integers.",
        "output_format": "Print the largest sum of a block.",
        "constraints": "1 <= n <= 10^5. Every value is between -1000 and 1000.",
        "starter_code": (
            "n = int(input())\n"
            "a = list(map(int, input().split()))\n\n"
            "# Write your program here.\n"
            "# Store your final answer in the variable answer.\n\n"
            "print(answer)"
        ),
        "judge_mode": "exact",
        "sample_tests": [
            {"input": "7\n2 -5 4 -1 3 -6 2", "output": "6"},
            {"input": "3\n-3 -1 -2", "output": "-1"},
            {"input": "6\n1 2 3 -10 4 5", "output": "9"},
        ],
        "hidden_tests": [
            {"input": "1\n-1000", "output": "-1000"},
            {"input": "5\n5 -2 3 -1 2", "output": "7"},
            {"input": "4\n-1 -2 -3 -4", "output": "-1"},
            {"input": "5\n10 -3 4 -20 12", "output": "12"},
        ],
        "hints": [
            "This is Kadane's algorithm: maintain `cur_max` (best sum ending at current index) and `answer` (best sum seen anywhere so far).",
            "Initialize both `cur_max` and `answer` to `a[0]`. For each `x` in `a[1:]`, update `cur_max = max(x, cur_max + x)` and `answer = max(answer, cur_max)`.",
        ],
        "solution_steps": [
            "Initialize `cur = a[0]` and `answer = a[0]` so even all-negative lists are handled properly.",
            "Iterate `x` over `a[1:]`: either extend the previous block (`cur + x`) or start a new block at `x`, whichever is larger: `cur = max(x, cur + x)`.",
            "Update `answer = max(answer, cur)`.",
            "Time Complexity: O(n). Space Complexity: O(1) extra space.",
        ],
        "solution_code": (
            "n = int(input())\n"
            "a = list(map(int, input().split()))\n\n"
            "cur = a[0]\n"
            "answer = a[0]\n"
            "for x in a[1:]:\n"
            "    cur = max(x, cur + x)\n"
            "    answer = max(answer, cur)\n\n"
            "print(answer)"
        ),
    },
    {
        "id": 8,
        "slug": "subsets-with-given-sum",
        "title": "Subsets with a Given Sum",
        "difficulty": "Hard",
        "difficulty_tier": "Hard",
        "statement": (
            "Given `n` distinct positive integers and a target `T`, find every subset of the numbers whose sum is exactly `T`. "
            "Write each subset with its numbers in increasing order. List the subsets in dictionary order: compare two subsets item by item from the left, "
            "and if one subset is the beginning of another, the shorter one comes first. "
            "Use backtracking: add a number, make the recursive call, then remove the number."
        ),
        "worked_example": (
            "For the numbers `2 3 5 7` and `T = 10`, the subsets with sum 10 are `2 3 5` and `3 7`. "
            "In dictionary order, `2 3 5` comes before `3 7`. If no subset has the sum `T`, print `-1`."
        ),
        "input_format": "The first line contains `n`. The second line contains the `n` integers. The third line contains `T`.",
        "output_format": "Print each subset on its own line, with the numbers separated by spaces. If there is no subset with sum `T`, print `-1`.",
        "constraints": "1 <= n <= 15. Every number is between 1 and 100, and the numbers are distinct. 1 <= T <= 200.",
        "starter_code": (
            "n = int(input())\n"
            "nums = list(map(int, input().split()))\n"
            "target = int(input())\n\n"
            "# Write your program here.\n"
            "# Store the subsets in the list answer, in the required order.\n"
            "# Each subset is a list of integers in increasing order.\n\n"
            "if len(answer) == 0:\n"
            "    print(-1)\n"
            "for subset in answer:\n"
            "    print(*subset)  # prints list entries without brackets"
        ),
        "judge_mode": "exact",
        "sample_tests": [
            {"input": "4\n2 3 5 7\n10", "output": "2 3 5\n3 7"},
            {"input": "6\n3 34 4 12 5 2\n9", "output": "2 3 4\n4 5"},
            {"input": "3\n4 6 8\n5", "output": "-1"},
        ],
        "hidden_tests": [
            {"input": "1\n5\n5", "output": "5"},
            {"input": "5\n10 1 2 7 6\n8", "output": "1 2 5\n1 7\n2 6".replace("1 2 5\n", "")},
            {"input": "4\n1 2 3 4\n6", "output": "1 2 3\n2 4"},
            {"input": "3\n2 4 6\n1", "output": "-1"},
        ],
        "hints": [
            "Sort `nums` first! When `nums` is sorted, iterating from index `start` to `n - 1` and choosing `nums[i]` before skipping it naturally generates subsets in dictionary order.",
            "In `backtrack(start, remaining, path)`: if `remaining == 0`, append `path.copy()` to `answer` and return. Loop `i` from `start` to `n - 1`: if `nums[i] > remaining`, break early (since `nums` is sorted).",
        ],
        "solution_steps": [
            "Sort `nums` in ascending order so elements within any subset are increasing and backtracking explores smaller elements first (dictionary order).",
            "Define `backtrack(start, remaining, path)`: if `remaining == 0`, append `path.copy()` to `answer` and return.",
            "Loop `i` from `start` to `n - 1`: if `nums[i] > remaining`, break early since all remaining numbers are positive and larger.",
            "Append `nums[i]` to `path`, recurse with `(i + 1, remaining - nums[i], path)`, then `path.pop()`.",
            "Time Complexity: O(2^n) worst case with pruning. Space Complexity: O(n) recursion depth.",
        ],
        "solution_code": (
            "n = int(input())\n"
            "nums = list(map(int, input().split()))\n"
            "target = int(input())\n\n"
            "nums.sort()\n"
            "answer = []\n\n"
            "def backtrack(start, remaining, path):\n"
            "    if remaining == 0:\n"
            "        answer.append(path.copy())\n"
            "        return\n"
            "    for i in range(start, n):\n"
            "        if nums[i] > remaining:\n"
            "            break\n"
            "        path.append(nums[i])\n"
            "        backtrack(i + 1, remaining - nums[i], path)\n"
            "        path.pop()\n\n"
            "backtrack(0, target, [])\n\n"
            "if len(answer) == 0:\n"
            "    print(-1)\n"
            "for subset in answer:\n"
            "    print(*subset)"
        ),
    },
    {
        "id": 9,
        "slug": "queens-on-a-board",
        "title": "Queens on a Board",
        "difficulty": "Hard",
        "difficulty_tier": "Hard",
        "statement": (
            "A queen attacks every square in its row, its column, and both of its diagonals. "
            "Place `n` queens on an `n x n` board so that no two queens attack each other. Count the number of different ways to do this. "
            "Place the queens one row at a time. If a queen cannot be placed safely in the current row, go back and move the queen in an earlier row."
        ),
        "worked_example": (
            "For `n = 4` there are exactly `2` ways. In one of them the queens are in columns `2, 4, 1, 3` of rows 1 to 4. "
            "The other way is its mirror image, with columns `3, 1, 4, 2`."
        ),
        "input_format": "A single line containing the integer `n`.",
        "output_format": "Print the number of ways to place the `n` queens.",
        "constraints": "1 <= n <= 9.",
        "starter_code": (
            "n = int(input())\n\n"
            "# Write your program here.\n"
            "# Store your final answer in the variable answer.\n\n"
            "print(answer)"
        ),
        "judge_mode": "exact",
        "sample_tests": [
            {"input": "4", "output": "2"},
            {"input": "6", "output": "4"},
            {"input": "8", "output": "92"},
        ],
        "hidden_tests": [
            {"input": "1", "output": "1"},
            {"input": "2", "output": "0"},
            {"input": "3", "output": "0"},
            {"input": "9", "output": "352"},
        ],
        "hints": [
            "Place one queen per row `r` from `0` to `n - 1`. Track which columns `cols`, main diagonals `(r - c)`, and anti-diagonals `(r + c)` are already occupied using three sets.",
            "When `r == n`, you have placed all `n` queens safely, so return `1`. Otherwise sum the recursive results for every valid column `c` in row `r`.",
        ],
        "solution_steps": [
            "Maintain three sets: `cols`, `diag1` (`r - c`), and `diag2` (`r + c`) for O(1) attack checks.",
            "Define `solve(r)`: if `r == n`, return `1` (valid placement found).",
            "For each column `c` in `0..n-1`: if `c` not in `cols`, `r - c` not in `diag1`, and `r + c` not in `diag2`, add them, recurse `solve(r + 1)`, and remove them (backtrack).",
            "Time Complexity: O(n!). Space Complexity: O(n).",
        ],
        "solution_code": (
            "n = int(input())\n\n"
            "cols = set()\n"
            "diag1 = set()\n"
            "diag2 = set()\n\n"
            "def solve(r):\n"
            "    if r == n:\n"
            "        return 1\n"
            "    total = 0\n"
            "    for c in range(n):\n"
            "        if c in cols or (r - c) in diag1 or (r + c) in diag2:\n"
            "            continue\n"
            "        cols.add(c)\n"
            "        diag1.add(r - c)\n"
            "        diag2.add(r + c)\n"
            "        total += solve(r + 1)\n"
            "        cols.remove(c)\n"
            "        diag1.remove(r - c)\n"
            "        diag2.remove(r + c)\n"
            "    return total\n\n"
            "answer = solve(0)\n"
            "print(answer)"
        ),
    },
    {
        "id": 10,
        "slug": "kth-move-tower-of-hanoi",
        "title": "The k-th Move of the Tower of Hanoi",
        "difficulty": "Hard",
        "difficulty_tier": "Hard",
        "statement": (
            "There are three pegs, `A`, `B` and `C`, and `n` disks numbered `1` to `n`, where disk `1` is the smallest. "
            "At the start all disks are on peg `A`, with the largest disk at the bottom. In one move you take the top disk of one peg and put it on another peg. "
            "A disk can never be placed on a smaller disk. The goal is to move all disks to peg `C`.\n\n"
            "Use this method to move `m` disks from peg `X` to peg `Y` with the help of peg `Z`: first move `m - 1` disks from `X` to `Z`, "
            "then move disk `m` from `X` to `Y`, then move `m - 1` disks from `Z` to `Y`. This takes `2^n - 1` moves in total.\n\n"
            "Print the `k`-th move of this method. For large `n` there are far too many moves to list them all, so find the `k`-th move without generating the others."
        ),
        "worked_example": (
            "For `n = 3` the seven moves are: disk 1 from A to C, disk 2 from A to B, disk 1 from C to B, disk 3 from A to C, "
            "disk 1 from B to A, disk 2 from B to C, disk 1 from A to C. So for `k = 4` the answer is `3 A C`."
        ),
        "input_format": "A single line containing two integers `n` and `k`.",
        "output_format": "Print the disk number, the peg it is taken from, and the peg it is moved to, separated by spaces.",
        "constraints": "1 <= n <= 60. 1 <= k <= 2^n - 1.",
        "starter_code": (
            "n, k = map(int, input().split())\n\n"
            "# Write your program here.\n"
            "# Store the disk number in the variable disk,\n"
            "# the peg it moves from in src, and the peg it moves to in dst.\n\n"
            "print(disk, src, dst)"
        ),
        "judge_mode": "exact",
        "sample_tests": [
            {"input": "3 4", "output": "3 A C"},
            {"input": "5 10", "output": "2 C A"},
            {"input": "60 576460752303423488", "output": "60 A C"},
        ],
        "hidden_tests": [
            {"input": "1 1", "output": "1 A C"},
            {"input": "3 1", "output": "1 A C"},
            {"input": "3 7", "output": "1 A C"},
            {"input": "4 8", "output": "4 A C"},
        ],
        "hints": [
            "Moving `m - 1` disks takes `half = 2**(m - 1) - 1` moves. Compare `k` to `half + 1` (the middle move).",
            "If `k == half + 1`, the `k`-th move is `(m, X, Y)`. If `k <= half`, recurse on `(m - 1, k, X, Z, Y)`. Otherwise recurse on `(m - 1, k - half - 1, Z, Y, X)`.",
        ],
        "solution_steps": [
            "Define `hanoi(m, k, src, dst, aux)` which returns `(disk, from_peg, to_peg)` for the `k`-th move.",
            "Compute `mid = 1 << (m - 1)` (which equals `2^(m-1)`, the exact move index of disk `m`).",
            "If `k == mid`: return `(m, src, dst)`.",
            "If `k < mid`: the move happens in the first half, so return `hanoi(m - 1, k, src, aux, dst)`.",
            "If `k > mid`: the move happens in the second half, so return `hanoi(m - 1, k - mid, aux, dst, src)`.",
            "Time Complexity: O(n). Space Complexity: O(n) (or O(1) iteratively).",
        ],
        "solution_code": (
            "n, k = map(int, input().split())\n\n"
            "def hanoi(m, k, src, dst, aux):\n"
            "    mid = 1 << (m - 1)\n"
            "    if k == mid:\n"
            "        return m, src, dst\n"
            "    elif k < mid:\n"
            "        return hanoi(m - 1, k, src, aux, dst)\n"
            "    else:\n"
            "        return hanoi(m - 1, k - mid, aux, dst, src)\n\n"
            "disk, src, dst = hanoi(n, k, 'A', 'C', 'B')\n"
            "print(disk, src, dst)"
        ),
    },
    {
        "id": 11,
        "slug": "recursive-star-pattern",
        "title": "Recursive Star Pattern",
        "difficulty": "Medium",
        "difficulty_tier": "Medium",
        "statement": (
            "Complete the recursive function `pattern(n, indent)` so that it prints a symmetric pattern using stars and spaces. "
            "For `n = 0`, the function prints nothing. For `0 < n <= 3`, the output is given in the samples. "
            "Fill in the four blanks in the starter code so that its output matches the sample output. "
            "You must not use loops or additional functions. String multiplication is allowed."
        ),
        "worked_example": (
            "For `n = 2`, the function first prints one star preceded by two spaces (`  *`). "
            "It then prints three stars with no leading spaces (`***`). Finally, it prints one star preceded by two spaces again (`  *`)."
        ),
        "input_format": "A single line containing the integer `n`.",
        "output_format": "Print the required pattern, preserving the leading spaces. Do not print spaces between stars or any extra blank lines.",
        "constraints": "1 <= n <= 8.",
        "starter_code": (
            "def pattern(n, indent=0):\n"
            "    if n == 0:\n"
            "        return  # Blank 1\n"
            "    # pattern(...)  # Blank 2\n"
            "    # print(...)    # Blank 3\n"
            "    # pattern(...)  # Blank 4\n\n"
            "n = int(input())\n"
            "pattern(n)"
        ),
        "judge_mode": "exact_preserve_leading",
        "sample_tests": [
            {"input": "3", "output": "    *\n  ***\n    *\n*****\n    *\n  ***\n    *"},
            {"input": "2", "output": "  *\n***\n  *"},
            {"input": "1", "output": "*"},
        ],
        "hidden_tests": [
            {"input": "4", "output": "      *\n    ***\n      *\n  *****\n      *\n    ***\n      *\n*******\n      *\n    ***\n      *\n  *****\n      *\n    ***\n      *"},
        ],
        "hints": [
            "Notice the symmetry: `pattern(n, indent)` prints `pattern(n - 1, indent + 2)`, then the middle line with `2 * n - 1` stars indented by `indent` spaces, then `pattern(n - 1, indent + 2)` again!",
            "Blank 1: `return`. Blank 2 & 4: `pattern(n - 1, indent + 2)`. Blank 3: `print(' ' * indent + '*' * (2 * n - 1))`.",
        ],
        "solution_steps": [
            "Base case (Blank 1): when `n == 0`, `return` immediately without printing anything.",
            "Top half (Blank 2): call `pattern(n - 1, indent + 2)` so smaller sub-patterns are indented 2 more spaces to the right.",
            "Middle bar (Blank 3): `print(' ' * indent + '*' * (2 * n - 1))`.",
            "Bottom half (Blank 4): call `pattern(n - 1, indent + 2)` again for symmetry.",
            "Time Complexity: O(2^n) lines printed. Space Complexity: O(n) recursion stack.",
        ],
        "solution_code": (
            "def pattern(n, indent=0):\n"
            "    if n == 0:\n"
            "        return\n"
            "    pattern(n - 1, indent + 2)\n"
            "    print(' ' * indent + '*' * (2 * n - 1))\n"
            "    pattern(n - 1, indent + 2)\n\n"
            "n = int(input())\n"
            "pattern(n)"
        ),
    },
    {
        "id": 12,
        "slug": "in-place-partitioning",
        "title": "In-Place Partitioning",
        "difficulty": "Medium",
        "difficulty_tier": "Medium",
        "statement": (
            "Complete the function `partition(L, x)` so that it rearranges the elements of `L` in place: "
            "all integers less than or equal to `x` must appear before all integers greater than `x`. "
            "The integers in `L` are distinct. The integer `x` need not occur in the list. The relative order of elements within either group does not matter.\n\n"
            "**In-Place Requirement:** You must modify the original list `L`. You may use only a constant number of additional variables, independent of the length of `L`. "
            "You must not create another list or any other collection, copy or slice the list, or use recursion. Swapping two elements using `L[i], L[j] = L[j], L[i]` is allowed. "
            "Do not use `sort()` or `sorted()`. Return the number of elements less than or equal to `x`."
        ),
        "worked_example": (
            "Suppose `L = [8, 3, 7, 1, 6, 2]` and `x = 3`. One valid rearrangement is `[3, 1, 2, 8, 6, 7]`. "
            "The first three elements are at most 3, and all remaining elements are greater than 3. The function returns `3`."
        ),
        "input_format": "The first line contains distinct integers separated by spaces, representing `L`. The second line contains the integer `x`.",
        "output_format": "The supplied driver code prints two lines: the count `k`, and `True` if the modified list is a valid partition.",
        "constraints": "1 <= n <= 10^5. Every element of L, and x, lies between -10^9 and 10^9.",
        "starter_code": (
            "def partition(L, x):\n"
            "    # Write your code here.\n"
            "    # Modify L in place and return the partition index.\n"
            "    pass\n\n"
            "L = list(map(int, input().split()))\n"
            "x = int(input())\n\n"
            "# The copy below is used only to check your answer.\n"
            "# You must not create a copy inside partition().\n"
            "original = L.copy()\n\n"
            "k = partition(L, x)\n"
            "print(k)\n\n"
            "valid = (\n"
            "    type(k) is int\n"
            "    and 0 <= k <= len(L)\n"
            "    and sorted(L) == sorted(original)\n"
            "    and all(L[i] <= x for i in range(k))\n"
            "    and all(L[i] > x for i in range(k, len(L)))\n"
            ")\n"
            "print(valid)"
        ),
        "judge_mode": "exact",
        "sample_tests": [
            {"input": "8 3 7 1 6 2\n3", "output": "3\nTrue"},
            {"input": "4 9 6\n2", "output": "0\nTrue"},
            {"input": "-3 5 0 2\n5", "output": "4\nTrue"},
        ],
        "hidden_tests": [
            {"input": "10\n10", "output": "1\nTrue"},
            {"input": "10\n5", "output": "0\nTrue"},
            {"input": "-10 -5 0 5 10\n0", "output": "3\nTrue"},
            {"input": "100 50 25 75 10 90\n50", "output": "3\nTrue"},
        ],
        "hints": [
            "Use Lomuto's partition pointer `k = 0`, which marks the boundary of elements `<= x`.",
            "Loop `i` from `0` to `len(L) - 1`: whenever `L[i] <= x`, swap `L[k]` and `L[i]`, then increment `k += 1`. Finally return `k`.",
        ],
        "solution_steps": [
            "Initialize `k = 0`, representing the number of elements `<= x` placed at the front so far.",
            "Scan `i` from `0` to `len(L) - 1`: if `L[i] <= x`, swap `L[k], L[i] = L[i], L[k]` and increment `k`.",
            "After the loop finishes, all elements in `L[:k]` are `<= x` and all elements in `L[k:]` are `> x`.",
            "Return `k`. Time Complexity: O(n). Space Complexity: O(1).",
        ],
        "solution_code": (
            "def partition(L, x):\n"
            "    k = 0\n"
            "    for i in range(len(L)):\n"
            "        if L[i] <= x:\n"
            "            L[k], L[i] = L[i], L[k]\n"
            "            k += 1\n"
            "    return k\n\n"
            "L = list(map(int, input().split()))\n"
            "x = int(input())\n\n"
            "original = L.copy()\n\n"
            "k = partition(L, x)\n"
            "print(k)\n\n"
            "valid = (\n"
            "    type(k) is int\n"
            "    and 0 <= k <= len(L)\n"
            "    and sorted(L) == sorted(original)\n"
            "    and all(L[i] <= x for i in range(k))\n"
            "    and all(L[i] > x for i in range(k, len(L)))\n"
            ")\n"
            "print(valid)"
        ),
    },
    {
        "id": 13,
        "slug": "merging-two-sorted-lists",
        "title": "Merging Two Sorted Lists",
        "difficulty": "Medium",
        "difficulty_tier": "Medium",
        "statement": (
            "Complete the function `merge(A, B)` that takes two lists of integers, each sorted in non-decreasing order, "
            "and returns a new sorted list containing all elements from both lists. "
            "Repeated elements must be preserved. Do not modify the original lists `A` and `B`. "
            "Do not use `sort()` or `sorted()`. You may create a new list to store the result."
        ),
        "worked_example": (
            "For `A = [1, 4, 7]` and `B = [2, 4, 8]`, the function returns `[1, 2, 4, 4, 7, 8]`. "
            "Both occurrences of `4` are included."
        ),
        "input_format": "The first line contains the elements of `A`, separated by spaces. The second line contains the elements of `B`, separated by spaces. An empty line represents an empty list.",
        "output_format": "Print the merged list as a Python list, as shown in the samples. The supplied driver code handles printing.",
        "constraints": "0 <= n, m <= 10^5. Every element lies between -10^9 and 10^9. Both input lists are sorted in non-decreasing order.",
        "starter_code": (
            "def merge(A, B):\n"
            "    # Write your code here.\n"
            "    # Return a new sorted list.\n"
            "    pass\n\n"
            "A = list(map(int, input().split()))\n"
            "B = list(map(int, input().split()))\n\n"
            "answer = merge(A, B)\n"
            "print(answer)"
        ),
        "judge_mode": "exact",
        "sample_tests": [
            {"input": "1 4 7\n2 4 8", "output": "[1, 2, 4, 4, 7, 8]"},
            {"input": "-5 -1 3\n-4 0 2 9", "output": "[-5, -4, -1, 0, 2, 3, 9]"},
            {"input": "1 1 5\n1 2 2", "output": "[1, 1, 1, 2, 2, 5]"},
        ],
        "hidden_tests": [
            {"input": "\n1 2 3", "output": "[1, 2, 3]"},
            {"input": "1 2 3\n\n", "output": "[1, 2, 3]"},
            {"input": "\n\n", "output": "[]"},
            {"input": "-10 0 10\n-10 0 10", "output": "[-10, -10, 0, 0, 10, 10]"},
        ],
        "hints": [
            "Use two indices `i = 0` (for `A`) and `j = 0` (for `B`) and an empty result list `res = []`.",
            "While `i < len(A)` and `j < len(B)`, append the smaller of `A[i]` and `B[j]` and advance that pointer. Afterward, extend `res` with whichever tail remains.",
        ],
        "solution_steps": [
            "Initialize `i = 0`, `j = 0`, and `res = []`.",
            "While both `i < len(A)` and `j < len(B)`, compare `A[i]` and `B[j]`. Append the smaller value to `res` and increment its index.",
            "Once one list is exhausted, append the remaining elements (`res.extend(A[i:])` and `res.extend(B[j:])`).",
            "Time Complexity: O(n + m). Space Complexity: O(n + m).",
        ],
        "solution_code": (
            "def merge(A, B):\n"
            "    i, j = 0, 0\n"
            "    res = []\n"
            "    while i < len(A) and j < len(B):\n"
            "        if A[i] <= B[j]:\n"
            "            res.append(A[i])\n"
            "            i += 1\n"
            "        else:\n"
            "            res.append(B[j])\n"
            "            j += 1\n"
            "    res.extend(A[i:])\n"
            "    res.extend(B[j:])\n"
            "    return res\n\n"
            "A = list(map(int, input().split()))\n"
            "B = list(map(int, input().split()))\n\n"
            "answer = merge(A, B)\n"
            "print(answer)"
        ),
    },
    {
        "id": 14,
        "slug": "strongest-stock-price-rally",
        "title": "Strongest Stock Price Rally",
        "difficulty": "Medium",
        "difficulty_tier": "Medium",
        "statement": (
            "A list `prices` contains the price of a stock on a sequence of days. The element `prices[i]` is the price on day `i`, with days numbered starting from 0. "
            "The strength of a rally from day `i` to day `j` is `prices[j] - prices[i]`, `i < j`. "
            "Prices may rise or fall between these two days; only the starting and ending prices determine the strength. "
            "Complete the function `strongest_rally(prices)` that returns the largest positive rally strength. If no positive rally exists, return `0`.\n\n"
            "Your function must use only a constant number of additional variables. Do not modify the input list, create another collection, or use sorting."
        ),
        "worked_example": (
            "For `prices = [120, 100, 115, 90, 130, 125]`, the strongest rally starts on day 3, at price 90, "
            "and ends on day 4, at price 130. Its strength is `130 - 90 = 40`. "
            "In `[150, 100, 120]`, the answer is `20`, not `50`, because 150 occurs before 100."
        ),
        "input_format": "A single line containing the daily prices as space-separated integers.",
        "output_format": "Print one integer: the strength of the strongest rally, or `0` if there is no positive rally. The supplied driver code handles printing.",
        "constraints": "1 <= n <= 10^5. Each price is an integer between 1 and 10^9. Prices may repeat.",
        "starter_code": (
            "def strongest_rally(prices):\n"
            "    # Write your code here.\n"
            "    # Return the largest positive price increase.\n"
            "    pass\n\n"
            "prices = list(map(int, input().split()))\n\n"
            "answer = strongest_rally(prices)\n"
            "print(answer)"
        ),
        "judge_mode": "exact",
        "sample_tests": [
            {"input": "120 100 115 90 130 125", "output": "40"},
            {"input": "150 100 120", "output": "20"},
            {"input": "100 90 80 70", "output": "0"},
            {"input": "75", "output": "0"},
        ],
        "hidden_tests": [
            {"input": "5 5 5 5", "output": "0"},
            {"input": "1 2 3 4 5", "output": "4"},
            {"input": "10 2 8 1 9", "output": "8"},
            {"input": "1000000000 1 1000000000", "output": "999999999"},
        ],
        "hints": [
            "As you scan `prices` from left to right, track the minimum price seen so far (`min_price`).",
            "For each price `p`, the best rally ending today is `p - min_price`. Update `best = max(best, p - min_price)` and `min_price = min(min_price, p)`.",
        ],
        "solution_steps": [
            "Initialize `min_price = prices[0]` and `best = 0`.",
            "For each `p` in `prices[1:]` (or all `p` in `prices`): update `best = max(best, p - min_price)` and `min_price = min(min_price, p)`.",
            "Return `best`. If prices only decrease, `best` remains `0`.",
            "Time Complexity: O(n). Space Complexity: O(1).",
        ],
        "solution_code": (
            "def strongest_rally(prices):\n"
            "    min_price = prices[0]\n"
            "    best = 0\n"
            "    for p in prices:\n"
            "        if p - min_price > best:\n"
            "            best = p - min_price\n"
            "        if p < min_price:\n"
            "            min_price = p\n"
            "    return best\n\n"
            "prices = list(map(int, input().split()))\n\n"
            "answer = strongest_rally(prices)\n"
            "print(answer)"
        ),
    },
    {
        "id": 15,
        "slug": "distinct-permutations",
        "title": "Distinct Permutations",
        "difficulty": "Hard",
        "difficulty_tier": "Hard",
        "statement": (
            "Complete the recursive function `permutations(L, i)` that prints all distinct permutations of a list of integers. "
            "The list may contain repeated integers, but each distinct permutation must be printed exactly once.\n\n"
            "The parameter `i` marks the position currently being filled. Elements before position `i` have already been chosen. The initial call is `permutations(L, 0)`. "
            "Use backtracking: choose an element for position `i`, recursively fill the remaining positions, and then undo your choice. "
            "When all positions have been filled, print the list using `print(L)`.\n\n"
            "You may use loops and a local set in each recursive call to keep track of values already tried at the current position. "
            "You must not use `itertools.permutations` or store all generated permutations in a collection to remove duplicates afterwards. "
            "The list must be restored to its original order when the function finishes."
        ),
        "worked_example": (
            "For `L = [1, 1, 2]`, there are three distinct permutations: `[1, 1, 2]`, `[1, 2, 1]`, and `[2, 1, 1]`. "
            "At any position, choosing different occurrences of the same value would generate duplicate results."
        ),
        "input_format": "A single line containing the elements of `L`, separated by spaces.",
        "output_format": "Print each distinct permutation as a Python list on a separate line. The permutations may be printed in any order.",
        "constraints": "1 <= |L| <= 8. Each element is an integer between -9 and 9. Elements may repeat.",
        "starter_code": (
            "def permutations(L, i):\n"
            "    # Write your recursive code here.\n"
            "    # Print each distinct permutation exactly once.\n"
            "    pass\n\n"
            "L = list(map(int, input().split()))\n"
            "permutations(L, 0)"
        ),
        "judge_mode": "unordered_lines",
        "sample_tests": [
            {"input": "1 1 2", "output": "[1, 1, 2]\n[1, 2, 1]\n[2, 1, 1]"},
            {"input": "4 4 4", "output": "[4, 4, 4]"},
            {"input": "-1 2", "output": "[-1, 2]\n[2, -1]"},
        ],
        "hidden_tests": [
            {"input": "7", "output": "[7]"},
            {"input": "1 2 3", "output": "[1, 2, 3]\n[1, 3, 2]\n[2, 1, 3]\n[2, 3, 1]\n[3, 1, 2]\n[3, 2, 1]"},
            {"input": "0 1 0 1", "output": "[0, 1, 0, 1]\n[0, 1, 1, 0]\n[0, 0, 1, 1]\n[1, 0, 0, 1]\n[1, 0, 1, 0]\n[1, 1, 0, 0]"},
        ],
        "hints": [
            "Base case: when `i == len(L)`, call `print(L)` and `return`.",
            "In the recursive step, create `used = set()`. Loop `j` from `i` to `len(L) - 1`: if `L[j]` is in `used`, skip it; otherwise add `L[j]` to `used`, swap `L[i]` and `L[j]`, call `permutations(L, i + 1)`, and swap back.",
        ],
        "solution_steps": [
            "If `i == len(L)`, all positions are filled: `print(L)` and `return`.",
            "Initialize `used = set()` local to this recursive call.",
            "For `j` from `i` to `len(L) - 1`: if `L[j] in used`, `continue` so the same value is never placed at index `i` twice.",
            "Add `L[j]` to `used`, swap `L[i], L[j] = L[j], L[i]`, recurse `permutations(L, i + 1)`, and swap back `L[i], L[j] = L[j], L[i]` to restore `L`.",
            "Time Complexity: O(n * n!). Space Complexity: O(n^2) due to local sets across recursion depth.",
        ],
        "solution_code": (
            "def permutations(L, i):\n"
            "    if i == len(L):\n"
            "        print(L)\n"
            "        return\n"
            "    used = set()\n"
            "    for j in range(i, len(L)):\n"
            "        if L[j] in used:\n"
            "            continue\n"
            "        used.add(L[j])\n"
            "        L[i], L[j] = L[j], L[i]\n"
            "        permutations(L, i + 1)\n"
            "        L[i], L[j] = L[j], L[i]\n\n"
            "L = list(map(int, input().split()))\n"
            "permutations(L, 0)"
        ),
    },
    {
        "id": 16,
        "slug": "integer-logarithm",
        "title": "Integer Logarithm",
        "difficulty": "Easy to Medium",
        "difficulty_tier": "Easy",
        "statement": (
            "Complete the recursive function `integer_log(n)` that returns `floor(log2(n))` for a positive integer `n`. "
            "Equivalently, return the largest nonnegative integer `k` such that `2^k <= n`.\n\n"
            "Your function must use recursion and integer arithmetic. Do not use loops, logarithm functions, floating-point arithmetic, "
            "`bit_length()`, or conversion to binary. You may use integer division (`//`)."
        ),
        "worked_example": (
            "For `n = 20`, we have `2^4 = 16 <= 20 < 32 = 2^5`. Therefore, the function returns `4`. "
            "For `n = 1`, it returns `0`, since `2^0 = 1`."
        ),
        "input_format": "A single line containing a positive integer `n`.",
        "output_format": "Print one integer: `floor(log2(n))`. The supplied driver code handles printing.",
        "constraints": "1 <= n <= 10^18.",
        "starter_code": (
            "def integer_log(n):\n"
            "    # Write your recursive code here.\n"
            "    # Return floor(log base 2 of n).\n"
            "    pass\n\n"
            "n = int(input())\n\n"
            "answer = integer_log(n)\n"
            "print(answer)"
        ),
        "judge_mode": "exact",
        "sample_tests": [
            {"input": "20", "output": "4"},
            {"input": "32", "output": "5"},
            {"input": "1", "output": "0"},
        ],
        "hidden_tests": [
            {"input": "2", "output": "1"},
            {"input": "31", "output": "4"},
            {"input": "1000000000000000000", "output": "59"},
            {"input": "1024", "output": "10"},
        ],
        "hints": [
            "What is `integer_log(1)`? It is `0`. That's your base case: `if n < 2: return 0`.",
            "Notice that `floor(log2(n)) = 1 + floor(log2(n // 2))` for `n >= 2`!",
        ],
        "solution_steps": [
            "Base case: if `n < 2` (i.e. `n == 1`), return `0`.",
            "Recursive step: dividing `n` by 2 reduces its base-2 logarithm by 1, so return `1 + integer_log(n // 2)`.",
            "Time Complexity: O(log n). Space Complexity: O(log n) recursion stack (at most ~60 frames for `n <= 10^18`).",
        ],
        "solution_code": (
            "def integer_log(n):\n"
            "    if n < 2:\n"
            "        return 0\n"
            "    return 1 + integer_log(n // 2)\n\n"
            "n = int(input())\n\n"
            "answer = integer_log(n)\n"
            "print(answer)"
        ),
    },
    {
        "id": 17,
        "slug": "counting-ones-in-binary",
        "title": "Counting Ones in Binary",
        "difficulty": "Easy to Medium",
        "difficulty_tier": "Easy",
        "statement": (
            "Complete the recursive function `count_ones(n)` that returns the number of 1s in the binary representation of a nonnegative integer `n`.\n\n"
            "Your function must use recursion and integer arithmetic. Do not use loops, `bin()`, `bit_count()`, bitwise operators, or conversion to a string. "
            "You may use integer division (`//`) and remainder (`%`)."
        ),
        "worked_example": (
            "The binary representation of `13` is `1101`, which contains three 1s. Therefore, the function returns `3`. "
            "The binary representation of `8` is `1000`, so the function returns `1`."
        ),
        "input_format": "A single line containing a nonnegative integer `n`.",
        "output_format": "Print one integer: the number of 1s in the binary representation of `n`. The supplied driver code handles printing.",
        "constraints": "0 <= n <= 10^18.",
        "starter_code": (
            "def count_ones(n):\n"
            "    # Write your recursive code here.\n"
            "    # Return the number of ones in binary.\n"
            "    pass\n\n"
            "n = int(input())\n\n"
            "answer = count_ones(n)\n"
            "print(answer)"
        ),
        "judge_mode": "exact",
        "sample_tests": [
            {"input": "13", "output": "3"},
            {"input": "8", "output": "1"},
            {"input": "0", "output": "0"},
        ],
        "hidden_tests": [
            {"input": "1", "output": "1"},
            {"input": "1023", "output": "10"},
            {"input": "1000000000000000000", "output": "24"},
            {"input": "255", "output": "8"},
        ],
        "hints": [
            "Base case: if `n == 0`, there are `0` ones in binary.",
            "The last binary bit of `n` is `n % 2`, and the remaining bits are `n // 2`. So return `(n % 2) + count_ones(n // 2)`.",
        ],
        "solution_steps": [
            "Base case: if `n == 0`, return `0`.",
            "Recursive step: `n % 2` gives the least significant bit (0 or 1), and `count_ones(n // 2)` counts the ones in all higher bits.",
            "Return `(n % 2) + count_ones(n // 2)`.",
            "Time Complexity: O(log n). Space Complexity: O(log n) recursion stack.",
        ],
        "solution_code": (
            "def count_ones(n):\n"
            "    if n == 0:\n"
            "        return 0\n"
            "    return (n % 2) + count_ones(n // 2)\n\n"
            "n = int(input())\n\n"
            "answer = count_ones(n)\n"
            "print(answer)"
        ),
    },
    {
        "id": 18,
        "slug": "lab-slots-for-students",
        "title": "Lab Slots for Students",
        "difficulty": "Medium to Hard",
        "difficulty_tier": "Medium",
        "statement": (
            "We want to divide `n` COL1000 students into `k` lab slots so that **every slot has at least one student**. "
            "Count the number of ways (Stirling numbers of the second kind, `S(n, k)`)."
        ),
        "worked_example": (
            "For `n = 3` students `[1, 2, 3]` and `k = 2` slots, the valid divisions are `([1], [2, 3])`, `([1, 2], [3])`, `([1, 3], [2])`, so `ways(3, 2) = 3`."
        ),
        "input_format": "Two integers `n` and `k` on separate lines.",
        "output_format": "Print `ways(n, k)`.",
        "constraints": "1 <= k <= n <= 20 (or k > n gives 0).",
        "starter_code": (
            "def ways(n, k):\n"
            "    # Write your recursive code here\n"
            "    pass\n\n"
            'n = int(input("Enter n: "))\n'
            'k = int(input("Enter k: "))\n\n'
            "print(ways(n, k))"
        ),
        "judge_mode": "strip_prompts",
        "sample_tests": [
            {"input": "3\n2", "output": "3"},
            {"input": "4\n2", "output": "7"},
            {"input": "4\n1", "output": "1"},
        ],
        "hidden_tests": [
            {"input": "5\n3", "output": "25"},
            {"input": "5\n5", "output": "1"},
            {"input": "2\n4", "output": "0"},
            {"input": "6\n3", "output": "90"},
        ],
        "hints": [
            "Suppose we already know how to distribute `n - 1` students. Either the `n`-th student joins one of `k` already non-empty slots (`k * ways(n - 1, k)`), or goes into its own new slot (`ways(n - 1, k - 1)`).",
            "Base cases: if `k == 0` or `k > n` return `0`; if `k == 1` or `k == n` return `1`.",
        ],
        "solution_steps": [
            "Base cases: if `k <= 0` or `k > n`, return `0`. If `k == 1` or `k == n`, there is only `1` way, so return `1`.",
            "Recursive relation: `ways(n, k) = k * ways(n - 1, k) + ways(n - 1, k - 1)`.",
            "Optionally memoize with `@functools.lru_cache` or a dict for larger inputs.",
            "Time Complexity: O(n * k) with memoization (exponential without).",
        ],
        "solution_code": (
            "def ways(n, k):\n"
            "    if k <= 0 or k > n:\n"
            "        return 0\n"
            "    if k == 1 or k == n:\n"
            "        return 1\n"
            "    return k * ways(n - 1, k) + ways(n - 1, k - 1)\n\n"
            'n = int(input("Enter n: "))\n'
            'k = int(input("Enter k: "))\n\n'
            "print(ways(n, k))"
        ),
    },
    {
        "id": 19,
        "slug": "seating-arrangement-for-students",
        "title": "Seating Arrangement for Students",
        "difficulty": "Medium to Hard",
        "difficulty_tier": "Medium",
        "statement": (
            "During the exam, we ensure that no two COL1000 students are seated next to each other. "
            "We have `n` people sitting in a **straight line**, numbered `1, 2, ..., n`. "
            "We want to choose exactly `k` people so that **no two chosen people are adjacent** (i.e., no two chosen people sit next to each other). "
            "Count the number of ways."
        ),
        "worked_example": (
            "For `n = 4` people in a line and `k = 2`, the valid choices are `[1, 3]`, `[1, 4]`, `[2, 4]`, so `ways(4, 2) = 3`."
        ),
        "input_format": "Two integers `n` and `k` on separate lines.",
        "output_format": "Print `ways(n, k)`.",
        "constraints": "n, k >= 1.",
        "starter_code": (
            "# assume n, k >= 1\n"
            "def ways(n, k):\n"
            "    # Write your recursive code here\n"
            "    pass\n\n"
            'n = int(input("Enter n: "))\n'
            'k = int(input("Enter k: "))\n\n'
            "print(ways(n, k))"
        ),
        "judge_mode": "strip_prompts",
        "sample_tests": [
            {"input": "4\n2", "output": "3"},
            {"input": "5\n3", "output": "1"},
            {"input": "5\n2", "output": "6"},
        ],
        "hidden_tests": [
            {"input": "6\n3", "output": "4"},
            {"input": "4\n3", "output": "0"},
            {"input": "1\n1", "output": "1"},
            {"input": "7\n3", "output": "10"},
        ],
        "hints": [
            "Look at person `n`: either person `n` is NOT chosen (`ways(n - 1, k)`), or person `n` IS chosen, so person `n - 1` cannot be chosen (`ways(n - 2, k - 1)`).",
            "Base cases: if `k == 0`, return `1`. If `n < 2 * k - 1` (not enough seats to space `k` non-adjacent people), return `0`. If `k == 1`, return `n`.",
        ],
        "solution_steps": [
            "Base cases: if `k == 0`, return `1`; if `n <= 0` or `n < 2 * k - 1`, return `0`; if `k == 1`, return `n`.",
            "Recursive step: `ways(n, k) = ways(n - 1, k) + ways(n - 2, k - 1)`.",
            "This handles both the case where person `n` is skipped and where person `n` is selected (forcing person `n - 1` to be skipped).",
            "Time Complexity: O(n * k) with memoization.",
        ],
        "solution_code": (
            "# assume n, k >= 1\n"
            "def ways(n, k):\n"
            "    if k == 0:\n"
            "        return 1\n"
            "    if n <= 0 or n < 2 * k - 1:\n"
            "        return 0\n"
            "    if k == 1:\n"
            "        return n\n"
            "    return ways(n - 1, k) + ways(n - 2, k - 1)\n\n"
            'n = int(input("Enter n: "))\n'
            'k = int(input("Enter k: "))\n\n'
            "print(ways(n, k))"
        ),
    },
    {
        "id": 20,
        "slug": "power-of-a-matrix",
        "title": "Power of a Matrix",
        "difficulty": "Medium to Hard",
        "difficulty_tier": "Hard",
        "statement": (
            "Neo has just discovered he lives in a simulation. To reach the exit, he must learn to compute the power of a matrix `M` (`n x n`). Implement three functions:\n"
            "1. `row_col_prod(A, B, i, j)` — return the dot product of row `i` of `A` with column `j` of `B`.\n"
            "2. `mat_mul(A, B)` — return `C = A x B` as a **new matrix**, computed by calling `row_col_prod` for each entry. Do not modify `A` or `B`.\n"
            "3. `mat_pow(M, k)` — return `M^k` for a square matrix `M` and integer `k >= 0`, with `M^0 = I` (identity matrix). Must be **recursive**, must not modify `M`, and `k = 1` must return a **fresh copy** of `M` (no aliasing)."
        ),
        "worked_example": (
            "For `A = [[1, 2], [3, 4]]` and `B = [[5, 6], [7, 8]]`, `mat_mul(A, B)` returns `[[19, 22], [43, 50]]`. "
            "For `F = [[1, 1], [1, 0]]`, `mat_pow(F, 5)` returns `[[8, 5], [5, 3]]`."
        ),
        "input_format": "Automated driver evaluates `row_col_prod`, `mat_mul`, and `mat_pow` directly on test expressions from stdin.",
        "output_format": "Prints the evaluated result of the test expression.",
        "constraints": "Square matrix M of size n x n, integer k >= 0. No aliasing allowed.",
        "starter_code": (
            "def row_col_prod(A, B, i, j):\n"
            "    # Return the dot product of row i of A and column j of B.\n"
            "    # TODO\n"
            "    pass\n\n"
            "def mat_mul(A, B):\n"
            "    # Return A x B as a new matrix (use row_col_prod).\n"
            "    # TODO\n"
            "    pass\n\n"
            "def mat_pow(M, k):\n"
            "    # Return M^k for a square M, k >= 0 and integer.\n"
            "    # Recursive\n"
            "    # TODO\n"
            "    pass"
        ),
        "judge_mode": "driver",
        "test_driver": (
            "\nimport sys as _sys\n"
            "_expr = _sys.stdin.read().strip()\n"
            "if _expr:\n"
            "    A = [[1, 2], [3, 4]]\n"
            "    B = [[5, 6], [7, 8]]\n"
            "    F = [[1, 1], [1, 0]]\n"
            "    print(eval(_expr))\n"
        ),
        "sample_tests": [
            {"input": "row_col_prod([[1, 2], [3, 4]], [[5, 6], [7, 8]], 0, 0)", "output": "19"},
            {"input": "mat_mul([[1, 2], [3, 4]], [[5, 6], [7, 8]])", "output": "[[19, 22], [43, 50]]"},
            {"input": "mat_pow([[1, 1], [1, 0]], 5)", "output": "[[8, 5], [5, 3]]"},
            {"input": "mat_pow([[1, 2], [3, 4]], 0)", "output": "[[1, 0], [0, 1]]"},
        ],
        "hidden_tests": [
            {"input": "row_col_prod([[1, 2], [3, 4]], [[5, 6], [7, 8]], 1, 1)", "output": "50"},
            {"input": "(lambda Q: Q == A and id(Q) != id(A) and id(Q[0]) != id(A[0]))(mat_pow(A, 1))", "output": "True"},
            {"input": "mat_pow([[2, 0], [0, 3]], 4)", "output": "[[16, 0], [0, 81]]"},
            {"input": "mat_mul([[1, 2, 3], [4, 5, 6]], [[7, 8], [9, 10], [11, 12]])", "output": "[[58, 64], [139, 154]]"},
        ],
        "hints": [
            "For `row_col_prod(A, B, i, j)`, return `sum(A[i][t] * B[t][j] for t in range(len(B)))`. For `mat_mul(A, B)`, build a new `len(A) x len(B[0])` list of lists calling `row_col_prod`.",
            "For `mat_pow(M, k)`: if `k == 0`, return the `n x n` identity matrix. If `k == 1`, return `[row[:] for row in M]` (a fresh deep copy!). Otherwise use binary exponentiation or `mat_mul(M, mat_pow(M, k - 1))`.",
        ],
        "solution_steps": [
            "`row_col_prod(A, B, i, j)` sums `A[i][t] * B[t][j]` for `t` in `0..len(B)-1`.",
            "`mat_mul(A, B)` constructs `[[row_col_prod(A, B, i, j) for j in range(len(B[0]))] for i in range(len(A))]`.",
            "`mat_pow(M, k)` handles `k == 0` (identity matrix), `k == 1` (fresh row-copied matrix `[r[:] for r in M]`), and for `k > 1` uses recursive fast exponentiation: `half = mat_pow(M, k // 2)`, `sq = mat_mul(half, half)`, returning `sq` if `k % 2 == 0` else `mat_mul(sq, M)`.",
            "Time Complexity: O(n^3 log k) for `mat_pow`.",
        ],
        "solution_code": (
            "def row_col_prod(A, B, i, j):\n"
            "    total = 0\n"
            "    for t in range(len(B)):\n"
            "        total += A[i][t] * B[t][j]\n"
            "    return total\n\n"
            "def mat_mul(A, B):\n"
            "    rows = len(A)\n"
            "    cols = len(B[0])\n"
            "    return [[row_col_prod(A, B, i, j) for j in range(cols)] for i in range(rows)]\n\n"
            "def mat_pow(M, k):\n"
            "    n = len(M)\n"
            "    if k == 0:\n"
            "        return [[1 if i == j else 0 for j in range(n)] for i in range(n)]\n"
            "    if k == 1:\n"
            "        return [row[:] for row in M]\n"
            "    half = mat_pow(M, k // 2)\n"
            "    sq = mat_mul(half, half)\n"
            "    if k % 2 == 0:\n"
            "        return sq\n"
            "    return mat_mul(sq, M)"
        ),
    },
    {
        "id": 21,
        "slug": "grid-paths-with-obstacles",
        "title": "Grid Paths with Obstacles",
        "difficulty": "Medium",
        "difficulty_tier": "Medium",
        "statement": (
            "You are given an `m x n` grid. You start at the top-left cell `(0, 0)` and want to reach the bottom-right cell `(m - 1, n - 1)`. "
            "You may only move right or down. Cells containing `1` are obstacles and cannot be entered; cells containing `0` are free. "
            "Count the number of valid paths."
        ),
        "worked_example": (
            "For the 3x3 grid `[[0, 0, 0], [0, 1, 0], [0, 0, 0]]`, there are exactly `2` valid paths from the top-left to the bottom-right."
        ),
        "input_format": "The first line contains two integers `m` and `n`. The next `m` lines each contain `n` integers, either `0` or `1`.",
        "output_format": "Print the number of valid paths.",
        "constraints": "1 <= m, n <= 10.",
        "starter_code": (
            "m, n = map(int, input().split())\n"
            "grid = [list(map(int, input().split())) for _ in range(m)]\n\n"
            "def count_paths(grid, i, j):\n"
            "    # write your code here\n"
            "    pass\n\n"
            "answer = count_paths(grid, 0, 0)\n"
            "print(answer)"
        ),
        "judge_mode": "exact",
        "sample_tests": [
            {"input": "3 3\n0 0 0\n0 1 0\n0 0 0", "output": "2"},
            {"input": "2 2\n0 0\n0 0", "output": "2"},
            {"input": "2 3\n0 0 0\n0 1 0", "output": "1"},
        ],
        "hidden_tests": [
            {"input": "1 1\n0", "output": "1"},
            {"input": "1 1\n1", "output": "0"},
            {"input": "3 3\n1 0 0\n0 0 0\n0 0 0", "output": "0"},
            {"input": "4 4\n0 0 0 0\n0 1 0 0\n0 0 1 0\n0 0 0 0", "output": "4"},
        ],
        "hints": [
            "Check bounds and obstacles first: if `i >= len(grid)` or `j >= len(grid[0])` or `grid[i][j] == 1`, return `0`.",
            "If `(i, j)` is `(len(grid) - 1, len(grid[0]) - 1)`, return `1`. Otherwise return `count_paths(grid, i + 1, j) + count_paths(grid, i, j + 1)`.",
        ],
        "solution_steps": [
            "Out-of-bounds or obstacle base case: if `i >= len(grid) or j >= len(grid[0]) or grid[i][j] == 1`, return `0`.",
            "Destination base case: if `i == len(grid) - 1 and j == len(grid[0]) - 1`, return `1`.",
            "Recursive step: sum paths moving down (`i + 1, j`) and moving right (`i, j + 1`).",
            "Memoize `(i, j)` (or use DP) for larger grids. Time Complexity: O(m * n) with memoization.",
        ],
        "solution_code": (
            "m, n = map(int, input().split())\n"
            "grid = [list(map(int, input().split())) for _ in range(m)]\n\n"
            "memo = {}\n"
            "def count_paths(grid, i, j):\n"
            "    if i >= len(grid) or j >= len(grid[0]) or grid[i][j] == 1:\n"
            "        return 0\n"
            "    if i == len(grid) - 1 and j == len(grid[0]) - 1:\n"
            "        return 1\n"
            "    if (i, j) in memo:\n"
            "        return memo[(i, j)]\n"
            "    memo[(i, j)] = count_paths(grid, i + 1, j) + count_paths(grid, i, j + 1)\n"
            "    return memo[(i, j)]\n\n"
            "answer = count_paths(grid, 0, 0)\n"
            "print(answer)"
        ),
    },
    {
        "id": 22,
        "slug": "combination-sum",
        "title": "Combination Sum",
        "difficulty": "Medium",
        "difficulty_tier": "Medium",
        "statement": (
            "Given `n` distinct positive integers (candidates) and a target `T`, find all unique combinations in which the chosen candidates sum to `T`. "
            "Each candidate may be used an unlimited number of times."
        ),
        "worked_example": (
            "For candidates `{2, 3, 6, 7}` and `T = 7`, the valid combinations are `[2, 2, 3]` and `[7]`."
        ),
        "input_format": "The first line contains two integers `n` and `T`. The second line contains `n` distinct positive integers.",
        "output_format": "Print each combination on its own line, integers separated by spaces. If no combination exists, print `NONE`.",
        "constraints": "1 <= n <= 20, 1 <= T <= 30.",
        "starter_code": (
            "n, T = map(int, input().split())\n"
            "cands = sorted(map(int, input().split()))\n\n"
            "res = []  # collect your answers in res\n\n"
            "def backtrack(start, remaining, path):\n"
            "    # write your code here\n"
            "    pass\n\n"
            "backtrack(0, T, [])\n"
            "answer = res\n\n"
            "if not answer:\n"
            '    print("NONE")\n'
            "else:\n"
            "    for combo in answer:\n"
            "        print(*combo)"
        ),
        "judge_mode": "exact",
        "sample_tests": [
            {"input": "4 7\n2 3 6 7", "output": "2 2 3\n7"},
            {"input": "3 5\n2 3 5", "output": "2 3\n5"},
            {"input": "2 1\n2 3", "output": "NONE"},
        ],
        "hidden_tests": [
            {"input": "1 4\n2", "output": "2 2"},
            {"input": "3 8\n2 3 5", "output": "2 2 2 2\n2 3 3\n3 5"},
            {"input": "2 6\n4 5", "output": "NONE"},
            {"input": "1 5\n5", "output": "5"},
        ],
        "hints": [
            "Since candidates can be reused unlimited times, when you pick `cands[i]`, pass `i` (not `i + 1`) as the next `start` index!",
            "Because `cands` is sorted, if `cands[i] > remaining`, you can `break` out of the loop early.",
        ],
        "solution_steps": [
            "Base case: if `remaining == 0`, append `path.copy()` to `res` and return.",
            "Loop `i` from `start` to `len(cands) - 1`: if `cands[i] > remaining`, break early.",
            "Append `cands[i]` to `path`, recurse `backtrack(i, remaining - cands[i], path)` (passing `i` to allow reuse), then `path.pop()`.",
            "Time Complexity: O(N^(T/min_cand)). Space Complexity: O(T/min_cand).",
        ],
        "solution_code": (
            "n, T = map(int, input().split())\n"
            "cands = sorted(map(int, input().split()))\n\n"
            "res = []\n\n"
            "def backtrack(start, remaining, path):\n"
            "    if remaining == 0:\n"
            "        res.append(path.copy())\n"
            "        return\n"
            "    for i in range(start, len(cands)):\n"
            "        if cands[i] > remaining:\n"
            "            break\n"
            "        path.append(cands[i])\n"
            "        backtrack(i, remaining - cands[i], path)\n"
            "        path.pop()\n\n"
            "backtrack(0, T, [])\n"
            "answer = res\n\n"
            "if not answer:\n"
            '    print("NONE")\n'
            "else:\n"
            "    for combo in answer:\n"
            "        print(*combo)"
        ),
    },
]
