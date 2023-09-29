import heapq
from itertools import zip_longest


class State:
    def __init__(self, stacks):
        self.stacks = stacks

    def __str__(self):
        return ' '.join([''.join(stack) for stack in self.stacks])


class Node:
    def __init__(self, state, parent=None, depth=0):
        self.state = state
        self.parent = parent
        self.depth = depth

    def __lt__(self, other):
        return self.depth < other.depth


def print_state(state):
    print(">>>>>>>>>>")
    for stack in state.stacks:
        print(''.join(stack))
    print(">>>>>>>>>>")


def zero_heuristic(state, goal):
    return 0


def basic_heuristic(state, goal):
    mismatch_count = 0
    for s_stack, g_stack in zip(state.stacks, goal.stacks):
        for s_block, g_block in zip_longest(s_stack, g_stack, fillvalue=None):
            if s_block != g_block:
                mismatch_count += 1
    return mismatch_count


def heuristic(state, goal):
    mismatch_count = 0

    # Map blocks to their respective goal positions
    block_goal_positions = {}
    for stack_idx, g_stack in enumerate(goal.stacks):
        for block_idx, block in enumerate(g_stack):
            block_goal_positions[block] = (stack_idx, block_idx)

    for s_stack_idx, s_stack in enumerate(state.stacks):
        for s_block_idx, s_block in enumerate(s_stack):
            goal_stack_idx, goal_block_idx = block_goal_positions.get(
                s_block, (None, None))

            # If the block is not in its goal stack, add 2 to the heuristic
            # (One for picking it up, one for placing it)
            if goal_stack_idx is not None and goal_stack_idx != s_stack_idx:
                mismatch_count += 2

            # If the block is in its goal stack but not in its goal position, add 1
            elif goal_block_idx is not None and goal_block_idx != s_block_idx:
                mismatch_count += 1

                # Weight the bottom blocks more
                if s_block_idx == 0:
                    mismatch_count += len(s_stack)

    return mismatch_count


def pairwise_distance_heuristic(state, goal):
    distance_count = 0

    # Map blocks to their respective goal positions
    block_goal_positions = {}
    for stack_idx, g_stack in enumerate(goal.stacks):
        for block_idx, block in enumerate(g_stack):
            block_goal_positions[block] = (stack_idx, block_idx)

    for s_stack_idx, s_stack in enumerate(state.stacks):
        for s_block_idx, s_block in enumerate(s_stack):
            goal_stack_idx, goal_block_idx = block_goal_positions.get(
                s_block, (None, None))

            # If the block is not in its goal stack, compute the vertical and horizontal distance
            if goal_stack_idx is not None and goal_stack_idx != s_stack_idx:
                vertical_distance = abs(goal_stack_idx - s_stack_idx)
                horizontal_distance = abs(goal_block_idx - s_block_idx)
                distance_count += vertical_distance + horizontal_distance

            # If the block is in its goal stack but not in its goal position, compute the vertical distance
            elif goal_block_idx is not None and goal_block_idx != s_block_idx:
                vertical_distance = abs(goal_block_idx - s_block_idx)
                distance_count += vertical_distance

    return distance_count


def print_solution_path(node, goal, iterations, selected_heuristic, max_q, filename):
    # Reconstruct path from end node to start node
    path = []
    while node:
        path.append(node)
        node = node.parent
    path = path[::-1]  # Reverse so it starts from the beginning

    # Iterate over the path and print each node's state and information
    for i, node in enumerate(path):
        print(f"move {i}, pathcost={node.depth}, heuristic={selected_heuristic(node.state, goal)}, f(n)=g(n)+h(n)={node.depth + heuristic(node.state, goal)}")
        print_state(node.state)

    # Print the final statistics (for the sake of the example, using dummy values for maxq)
    print(
        f"statistics: {filename} method Astar planlen {len(path)-1} iter {iterations} maxq {max_q}")


def successors(node):
    current_state = node.state
    successor_nodes = []

    for i, src_stack in enumerate(current_state.stacks):
        if not src_stack:  # Skip if source stack is empty.
            continue

        for j, dst_stack in enumerate(current_state.stacks):
            if i == j:  # Skip if source and destination are the same.
                continue

            # Create a new state by moving the block.
            # Deep copy.
            new_stacks = [list(stack) for stack in current_state.stacks]
            # Remove the block from source stack.
            block_to_move = new_stacks[i].pop()
            # Add the block to destination stack.
            new_stacks[j].append(block_to_move)
            new_state = State(new_stacks)

            # Create a new node with the new state and current node as parent.
            successor_node = Node(new_state, node, node.depth + 1)
            successor_nodes.append(successor_node)

    return successor_nodes


def AStarSearch(initial, goal, max_iters, heuristic_func):
    queue = []
    visited = set()

    max_queue_size = 0  # Initialize the maximum queue size tracker

    start_node = Node(initial)
    heapq.heappush(queue, (0, start_node))

    iterations = 0
    while queue and iterations < max_iters:
        _, current_node = heapq.heappop(queue)
        visited.add(str(current_node.state))

        # Update max_queue_size if the current queue size is larger
        max_queue_size = max(max_queue_size, len(queue))

        # Goal reached
        if states_equal(current_node.state, goal):
            return current_node, iterations, max_queue_size

        for successor in successors(current_node):
            if str(successor.state) not in visited:
                h = heuristic_func(successor.state, goal)
                f = h + successor.depth
                heapq.heappush(queue, (f, successor))

        iterations += 1

        # Print debug information
        if iterations % 1000 == 0:
            h_value = heuristic_func(current_node.state, goal)
            path_cost = current_node.depth
            print(
                f"Iteration: {iterations}, Queue Size: {len(queue)}, Heuristic: {h_value}, Path Cost: {path_cost}")
            print_state(current_node.state)

    return None, iterations, max_queue_size


def parse_input(filename):
    with open(filename, 'r') as file:
        line = file.readline().strip()
        if not line:
            raise ValueError("Empty or incorrectly formatted input file.")

        stacks_count, _, _ = map(int, line.split())
        file.readline()  # skip '>>>>>>>>>>'

        stacks = []
        for _ in range(stacks_count):
            stack_line = file.readline().strip()
            stacks.append(list(stack_line))
        initial_state = State(stacks)

        file.readline()  # skip '>>>>>>>>>>'

        goal_stacks = []
        for _ in range(stacks_count):
            stack_line = file.readline().strip()
            goal_stacks.append(list(stack_line))
        goal_state = State(goal_stacks)

    return initial_state, goal_state


def states_equal(node_state, goal_state):
    if len(node_state.stacks) != len(goal_state.stacks):
        return False

    for node_stack, goal_stack in zip(node_state.stacks, goal_state.stacks):
        if ''.join(node_stack) != ''.join(goal_stack):
            return False
    return True


HEURISTICS = {
    'H0': zero_heuristic,
    'H1': basic_heuristic,
    'H2': heuristic,
    'H3': pairwise_distance_heuristic
}

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print(
            "Usage: blocksworld.py <filename> [-H H0|H1|…] [-MAX_ITERS <int>]")
        sys.exit(1)

    filename = sys.argv[1]
    max_iters = 100000  # default value

    if "-MAX_ITERS" in sys.argv:
        index = sys.argv.index("-MAX_ITERS")
        max_iters = int(sys.argv[index + 1])

    heuristic_name = 'H2'  # default value
    if "-H" in sys.argv:
        heuristic_name = sys.argv[sys.argv.index("-H") + 1]
    selected_heuristic = HEURISTICS.get(heuristic_name, heuristic)

    initial, goal = parse_input(filename)
    result, iterations, max_q = AStarSearch(
        initial, goal, max_iters, selected_heuristic)

    if result:
        print("Solution found!")
        print_solution_path(result, goal, iterations,
                            selected_heuristic, max_q, filename)
    else:
        print(
            f"statistics: {filename} method Astar planlen FAILED iter {iterations} maxq {max_q}")

    # # Hardcoded initial state
    # initial_stacks = [
    #     [],
    #     ['C', 'F'],
    #     ['A', 'D', 'E'],
    #     ['G', 'H', 'I', 'J'],
    #     ['B']
    # ]
    # initial_state = State(initial_stacks)

    # # Hardcoded goal state
    # goal_stacks = [
    #     ['A'],
    #     ['C', 'F'],
    #     ['D', 'E'],
    #     ['G', 'H', 'I', 'J'],
    #     ['B']
    # ]
    # goal_state = State(goal_stacks)
    # print("heuristic test:", selected_heuristic(initial_state, goal_state))
