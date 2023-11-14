def generate_n_queens_kb(n):
    kb = []

    # Generate clauses for at least one queen in each row and column
    for i in range(1, n + 1):
        # Rows
        row_clause = '(or ' + \
            ' '.join([f'Q{i}{j}' for j in range(1, n + 1)]) + ')'
        kb.append(row_clause)

        # Columns
        col_clause = '(or ' + \
            ' '.join([f'Q{j}{i}' for j in range(1, n + 1)]) + ')'
        kb.append(col_clause)

    # Generate clauses for no two queens in the same row or column
    for i in range(1, n + 1):
        for j in range(1, n):
            for k in range(j + 1, n + 1):
                # Rows
                kb.append(f'(or (not Q{i}{j}) (not Q{i}{k}))')
                # Columns
                kb.append(f'(or (not Q{j}{i}) (not Q{k}{i}))')

    # Generate clauses for no two queens in the same diagonal
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            for k in range(1, n + 1):
                for l in range(1, n + 1):
                    if abs(i - k) == abs(j - l) and (i != k and j != l):
                        kb.append(f'(or (not Q{i}{j}) (not Q{k}{l}))')

    return kb


if __name__ == "__main__":
    kb_4_queens = generate_n_queens_kb(6)
    for clause in kb_4_queens:
        print(clause)
