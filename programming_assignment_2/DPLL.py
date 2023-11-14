import sys
from typing import List, Set, Dict, Tuple
import datetime


class CNFConverter:
    def __init__(self):
        self.var_to_int_map = {}
        self.int_to_var_map = {}
        self.next_var_index = 1

    def literal_to_int(self, literal: str) -> int:
        is_negative = literal.startswith('-')
        base_literal = literal[1:] if is_negative else literal

        if base_literal not in self.var_to_int_map:
            self.var_to_int_map[base_literal] = self.next_var_index
            self.int_to_var_map[self.next_var_index] = base_literal
            self.next_var_index += 1

        return -self.var_to_int_map[base_literal] if is_negative else self.var_to_int_map[base_literal]

    def int_to_literal(self, integer: int) -> str:
        literal = self.int_to_var_map[abs(integer)]
        return ('-' + literal) if integer < 0 else literal


def print_model(assignment: Dict[int, bool], converter: CNFConverter):
    # print 1 if true, -1 if false 0 if not assigned
    model = {converter.int_to_literal(
        var): '1' if val else '-1' if val == False else '0' for var, val in assignment.items()}
    print("Model:", model)


def read_cnf_file(file_path: str, converter: CNFConverter) -> List[Set[int]]:
    clauses = []
    with open(file_path, 'r', encoding='utf-16') as file:
        for line in file:
            trimmed_line = line.strip()
            if not trimmed_line or trimmed_line.startswith('#'):
                continue

            clause = {converter.literal_to_int(literal)
                      for literal in trimmed_line.split()}
            clauses.append(clause)
    return clauses


def dpll(clauses: List[Set[int]], assignment: Dict[int, bool], converter: CNFConverter, visited_paths: Set[Tuple[int, ...]], use_uch: bool, total_calls: int) -> Tuple[bool, Dict[int, bool]]:
    total_calls += 1
    # Convert current assignment to a tuple for immutability and easy storage
    current_path = tuple(sorted(assignment.items()))

    # Check if the current path has been visited and failed
    if current_path in visited_paths:
        print("returns false because of visited paths")
        return total_calls, False, {}
    all_satisfied = True
    # All satisfied check
    for clause in clauses:
        if (satisfies(clause, assignment) == False):
            all_satisfied = False
        if (satisfies(clause, assignment) == None):
            all_satisfied = False

    if (all_satisfied):
        print("returns true, all satisfied")
        return total_calls, True, assignment

    # Any clause is false check
    for clause in clauses:
        if (satisfies(clause, assignment) == False):
            print("false assignment")
            return total_calls, False, assignment

    print_model(assignment, converter)
    if use_uch:
        for clause in clauses:
            unassigned_vars = [
                var for var in clause if abs(var) not in assignment]
            if len(unassigned_vars) == 1:
                var = unassigned_vars[0]
                assignment[abs(var)] = var > 0
                print(
                    f"forcing {converter.int_to_literal(var)}={'1' if var > 0 else '-1'} by UCH")
                total_calls, result, final_assignment = dpll(
                    clauses, assignment, converter, visited_paths, use_uch, total_calls)
                if result:
                    print("returns true within uch")
                    return total_calls, True, final_assignment
                del assignment[abs(var)]  # backtrack

    unassigned_vars = get_unassigned_vars(clauses, assignment)
    if not unassigned_vars:
        print("returns at unassigned vars check")
        return total_calls, False, {}

    var = unassigned_vars.pop()

    for value in [True, False]:
        print(
            f"trying {converter.int_to_literal(var)}={'1' if value else '-1'}")
        assignment[var] = value
        total_calls, result, final_assignment = dpll(
            clauses, assignment, converter, visited_paths, False, total_calls)
        if result:
            return total_calls, True, final_assignment

        # Update visited paths with the failed assignment
        visited_paths.add(tuple(sorted(assignment.items())))

    # If neither True nor False works, remove the variable from the assignment and backtrack
    del assignment[var]
    print("returns false at end")
    return total_calls, False, {}


def satisfies(clause: Set[int], assignment: Dict[int, bool]) -> bool:
    unassigned_exists = False
    for var in clause:
        if var in assignment:
            if assignment[var]:
                # print("assignment", assignment)
                # print("satisfied", clause, var)
                # If any variable in the clause is true, the clause is satisfied
                return True
        elif -var in assignment:
            if not assignment[-var]:
                # If the negation of any variable in the clause is false, the clause is satisfied
                return True
        else:
            # If a variable is not in the assignment, we can't determine if the clause is satisfied or not
            # print("assignment", assignment)
            # print("not assigned", clause, var)
            unassigned_exists = True
    if (unassigned_exists):
        return None
    else:
        return False


def get_unassigned_vars(clauses: List[Set[int]], assignment: Dict[int, bool]) -> Set[int]:
    return {abs(var) for clause in clauses for var in clause if abs(var) not in assignment}


def main(cnf_file_path: str, facts: List[str], use_uch: bool):
    converter = CNFConverter()
    clauses = read_cnf_file(cnf_file_path, converter)

    assignments = {}
    for fact in facts:
        var = converter.literal_to_int(fact)
        assignments[abs(var)] = var > 0
# Modify the main function or wherever the dpll is called to initialize visited_paths
    visited_paths = set()
# result, final_assignment = dpll(clauses, initial_assignment, converter, visited_paths)
    total_calls = 0
    total_calls, result, final_assignment = dpll(
        clauses, assignments, converter, visited_paths, use_uch, total_calls)
    if result:
        print("solution:")
        for var in sorted(final_assignment):
            print(
                f"{converter.int_to_literal(var)}: {'1' if final_assignment[var] else '-1'}")
        print(datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p"))
        print("just the Satisfied (true) propositions:")
        print(" ".join([converter.int_to_literal(var)
              for var in final_assignment if final_assignment[var]]))
        # If you're tracking the number of DPLL calls
        print(f"total DPLL calls: {total_calls}")
        print(f"UCH={'True' if use_uch else 'False'}")
    else:
        print("UNSATISFIABLE")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python DPLL.py <cnf-file> [facts...] [+uch]")
        sys.exit(1)

    cnf_file_path = sys.argv[1]
    facts = [arg for arg in sys.argv[2:] if arg != "+uch"]
    use_uch = "+UCH" in sys.argv

    main(cnf_file_path, facts, use_uch)
