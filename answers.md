# CMPS 6610 Problem Set 04
## Answers

**Name:** Khoa Le


Place all written answers from `problemset-04.md` here for easier grading.




- **1d. (3 pts)**

File | Fixed-Length Coding | Huffman Coding | Huffman vs. Fixed-Length
---|---|---|---
f1.txt | 1340 | 826 | 0.616
alice29.txt | 1039367 | 676374 | 0.651
asyoulik.txt | 876253 | 606448 | 0.692
grammar.lsp | 26047 | 17356 | 0.666
fields.c | 78050 | 56206 | 0.720

Yes, there is a consistent trend. Huffman is always cheaper than fixed-length.

Base on the ratio, Huffman saves roughly 30% of the bits.

The reason is that character frequencies are very skewed. Common characters like spaces get short codes. Fixed-length spends the same number of bits on every character.


- **1e. (3 pts)** Equal frequency Huffman encoding cost.

Let $n$ be the number of characters in the document.

If every character has the same frequency, no character is more common than another. So Huffman builds a balanced tree. Every character gets a code of about $\log_2 |\Sigma|$ bits.

$$\text{cost} \approx n \log_2 |\Sigma|$$

This is the same as fixed-length coding. So Huffman gives no real savings.


- **2a. (5 pts)** Construct a binary min-heap algorithm

I treat the array $A$ as an almost-complete binary tree. The children of index $i$ are $2i+1$ and $2i+2$.

I go from $i = \lfloor n/2 \rfloor - 1$ down to $0$ and call sift-down on $i$. Sift-down swaps $A[i]$ with its smaller child while that child is smaller.

Correctness: leaves (indexes $\ge \lfloor n/2 \rfloor$) are already heaps. When I reach $i$, its children have larger indexes, so they are already heaps. Sift-down on $i$ then makes the subtree at $i$ a heap.

Work: sift-down on a node of height $h$ costs $O(h)$. There are at most $\lceil n / 2^{h+1} \rceil$ nodes of height $h$.
$$W(n) = \sum_{h=0}^{\log n} \left\lceil\frac{n}{2^{h+1}}\right\rceil O(h) = O\left(n \sum_{h} \frac{h}{2^h}\right) = O(n)$$
This works because $\sum_h h/2^h = 2$.

- **2b. (2 pts)** Span of your algorithm

Nodes on the same level have disjoint subtrees. So their sift-downs don't depend on each other.

I run all sift-downs of one level in parallel, from the bottom level to the top. There are $\log n$ levels, and each sift-down takes $O(\log n)$.
$$S(n) = O(\log^2 n)$$

- **3a. (3 pts)** Greedy algorithm for making change

Take the largest coin $2^i$ (with $i \le k$) that is at most the amount left. Subtract it. Repeat until the amount is $0$.

Another way to say it: use $\lfloor N / 2^k \rfloor$ coins of $2^k$. The rest is just the binary representation of the remainder.

- **3b. (3 pts)** Optimality proof

Greedy choice: let $2^i$ be the largest coin with $2^i \le N$. I claim some optimal solution uses $2^i$.

In an optimal solution, no coin $2^j$ with $j < k$ appears twice. Otherwise I could swap the two coins for one $2^{j+1}$ and use fewer coins.

So the coins smaller than $2^i$ are used at most once each. They add up to at most $2^0 + \dots + 2^{i-1} = 2^i - 1 < N$. That is not enough to make $N$.

So the solution needs a coin of value at least $2^i$. Coins bigger than $N$ can't be used. So the solution contains $2^i$.

Optimal substructure: let $S$ be an optimal solution for $N$ that contains coin $c$. Then $S \setminus \{c\}$ is optimal for $N - c$.

If not, there is a better solution for $N - c$. Adding $c$ to it gives fewer coins than $S$ for $N$. That contradicts $S$ being optimal.

Together: take the largest coin, then solve the smaller problem optimally. This gives an optimal solution.

- **3c. (2 pts)** Work and span of your algorithm

I assume arithmetic is $O(1)$. The number of denominations $k$ is fixed.

I get $q = \lfloor N / 2^k \rfloor$ coins of $2^k$ with one division. The remainder $N \bmod 2^k$ is less than $2^k$. I write it in binary with the $k$ smaller coins, one check per coin.

If I return a count per denomination, it is a loop over $k$ denominations.
$$W = S = O(k)$$
If every coin must be listed one by one, the output has $N/2^k$ coins. Then the work is $O(k + N/2^k)$.

- **4a. (2 pts)** Fortuito counter example proof

Take denominations $\{1, 3, 4\}$ and $N = 6$.

Greedy takes $4$, then $1$, then $1$. That is $3$ coins.

But $3 + 3 = 6$ uses only $2$ coins. So greedy is not optimal.

- **4b. (3 pts)** Optimal substructure property

Let $OPT(N)$ be the fewest coins that make $N$ ($\infty$ if impossible).
$$OPT(0) = 0, \qquad OPT(N) = 1 + \min_{i : D_i \le N} OPT(N - D_i)$$
If no $D_i \le N$, then $OPT(N) = \infty$.

Proof: say an optimal solution for $N$ uses coin $D_i$. The other coins make $N - D_i$.

If they were not optimal for $N - D_i$, I could replace them with fewer coins. Adding $D_i$ back gives fewer than $OPT(N)$ coins. That is a contradiction.

So the rest is optimal for $N - D_i$. I don't know which $D_i$ is used, so I try all of them and take the min.

- **4c. (2 pts)** Fortuito dynamic programming algorithm

I fill a table $OPT[0..N]$ bottom-up. Set $OPT[0] = 0$. For $n = 1, \dots, N$, compute $OPT[n]$ with the recurrence from 4b.

The answer is $OPT[N]$. If it is $\infty$, change is impossible.

I also store which coin gave the min at each $n$. Then I walk back from $N$ to list the coins.

Work: there are $N$ subproblems, and each looks at $k$ coins.
$$W = O(Nk)$$
Span: $OPT[n]$ needs smaller entries, so the $N$ entries form a chain. The min over $k$ coins is a reduce with span $O(\log k)$.
$$S = O(N \log k)$$

- **5a. (4 pts)** Weighted task selection: Optimal substructure?

Yes. Sort the tasks by finish time, so $f_0 \le \dots \le f_{n-1}$.

For task $j$, let $p(j)$ be the largest $i < j$ with $f_i \le s_j$ ($-1$ if none). Let $OPT(j)$ be the max value using only tasks $0..j$.
$$OPT(-1) = 0, \qquad OPT(j) = \max\left(v_j + OPT(p(j)),\ OPT(j-1)\right)$$

Proof: look at an optimal solution for tasks $0..j$. There are two cases.

Case 1: it doesn't use $a_j$. Then it is a solution for tasks $0..j-1$. It must be optimal there, or I could swap in a better one.

Case 2: it uses $a_j$. The other tasks can't overlap $a_j$, so they finish by $s_j$. Since tasks are sorted by finish time, they are among tasks $0..p(j)$. They must be optimal for $0..p(j)$, or I could swap in a better set.

So the optimal value is the max of the two cases.

- **5b. (4 pts)** Does the greedy choice property hold?

No. Here are two greedy rules that fail:

1. Earliest finish time (the greedy from class). Tasks $a = (0, 1, v=1)$ and $b = (0, 10, v=100)$. Greedy picks $a$ and gets $1$. But $b$ alone is worth $100$.
2. Highest value first. Tasks $a = (0, 10, v=10)$, $b = (0, 5, v=9)$, $c = (5, 10, v=9)$. Greedy picks $a$ and gets $10$. But $b$ and $c$ together give $18$.

- **5c. (4 pts)** Dynamic programming algorithm for Weighted Task Selection

1. Sort tasks by finish time.
2. Compute $p(j)$ for every $j$ with binary search on the finish times. These are independent, so they run in parallel.
3. Fill $OPT[0..n-1]$ left to right with the recurrence from 5a.
4. The answer is $OPT[n-1]$. I remember which case was chosen at each $j$, so I can walk back to get the tasks.

Work: sorting is $O(n \log n)$, the binary searches are $O(n \log n)$, and the table is $O(n)$.
$$W = O(n \log n)$$
Span: sorting is $O(\log^2 n)$ and the parallel binary searches are $O(\log n)$. The table is a chain of $n$ steps, $O(1)$ each.
$$S = O(n)$$
