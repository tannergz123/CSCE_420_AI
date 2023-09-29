Enter instructions and requirements for running your code here.
Command-Line Usage
Run the program with the following syntax:
python blocksworld.py <filename> [-H H0|H1|H2] [-MAX_ITERS <int>]
-H defaults to -H2, which is my own heuristic
H0 is a 0 heuristic, basically simulates BFS.
H1 is a basic heuristic that just checks for mismatched blocks
H2 is a advanced heuristic that attempts to implement weights, with blocks on the bottom being heavier along other conditions.

    -MAX_ITERS defaults to 100000 but can be changed to anything

Known Limitations and Constraints:
The program cannot solve B20 within 100000 iterations
