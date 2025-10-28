import time
from collections import deque
from queue import PriorityQueue
from typing import List, Callable, Dict, Optional 

def printPuzzle(puzzle: str, n: int) -> None:
    ''' 
    Print the puzzle as an n x n grid 
    '''

    for i in range(n):
        row = puzzle[i*n : (i+1)*n]  
        print(" ".join(row))         
    print()  

def swap(puzzle: str, i: int, j: int) -> str:
    ''' Swaps characters at indices i and j in puzzle string '''
    new_puzzle = [*puzzle]
    new_puzzle[i] = puzzle[j]
    new_puzzle[j] = puzzle[i]
    return "".join(new_puzzle)

def getNodeRowCol(node: str, n: int) -> Dict[str, tuple]:
    ''' 
    Return mapping from index in string to (row, col) positions 
    '''

    res = {}

    for c in node:
        if c == '_': 
            continue
        i = node.index(c)
        row, col = divmod(i, n)
        res[c] = (row, col)

    return res

def calcManhattanDist(node: str, goal: str) -> int:
    '''
    Calculates the Manhattan distance between node and goal
    '''

    nodeRowCol = getNodeRowCol(node)
    goalRowCol = getNodeRowCol(goal)
    
    manhattanDist = 0
    for num in nodeRowCol:
        nodeR, nodeC = nodeRowCol[num]
        goalR, goalC = goalRowCol[num]
        manhattanDist += abs(nodeR - goalR) + abs(nodeC - goalC)
    
    return manhattanDist


def getNeighbors(p: str) -> List[str]:
    '''
    Given the current state, returns a list of the valid neighboring puzzle states
    '''

    i = p.index('_')
    row = i//n
    col = i%n
    nbrs = []
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for dr, dc in dirs:
        newR, newC = row + dr, col + dc
        if (0 <= newR < n and 0 <= newC < n):
            new_i = newR * n + newC
            new_p = swap(p, i, new_i)
            nbrs.append(new_p)
    return nbrs

def reconstructPath(visited: Dict[str, str], start: str, goal: str) -> str:
    path = []
    node = goal

    while node != '$':
        path.append(node)
        node = visited[node]
    
    path.reverse()
    
    print(f"Solution found in {len(path)-1} moves:\n")
    for step, state in enumerate(path):
        print(f"Step {step}:")
        printPuzzle(state, n)  # print each puzzle as a grid

    return " -> ".join(path)

def solvePuzzleAStar(p: str, goal: str, neighborFn: Callable=getNeighbors) -> str:
    pq = PriorityQueue()
    visited = {p:'$'}
    g = {p: 0}
    f = g[p] + calcManhattanDist(p, goal)
    pq.put((f, p))

    while not pq.empty():
        f, node = pq.get()

        if node == goal: 
            # print("Goal found!!")
            path = reconstructPath(visited, p, goal)
            # print(path)
            return path
        
        for nbr in neighborFn(node):
            currG = g[node] + 1
            if nbr not in g or currG < g[nbr]:
                if nbr in visited: continue
                g[nbr] = currG
                visited[nbr] = node
                f = currG + calcManhattanDist(nbr, goal)
                pq.put((f, nbr))

def solvePuzzleBFS(p: str, goal: str, neighborFn: Callable=getNeighbors) -> str:
    q = deque()
    q.append(p)
    visited = {p:'$'}
    while q:
        node = q.popleft()
        if node == goal:
            print("Goal found!!")
            path = reconstructPath(visited, p, goal)
            print(path)
            return path
        for nbr in neighborFn(node):
            if nbr not in visited:
                visited[nbr] = node # store parent as key to track path
                q.append(nbr)




def benchmarkSolver(solver_fn: Callable, puzzles: List[str], goal: str) -> List[str]:
    results = []
    for i, puzzle in enumerate(puzzles):
        start_time = time.time()
        nodes_explored = 0

        # counts nodes
        def countingGetNeighbors(node):
            nonlocal nodes_explored
            nodes_explored += 1
            return getNeighbors(node)

        # run solver
        path = solver_fn(puzzle, goal, neighborFn=countingGetNeighbors)
        end_time = time.time()
        results.append({
            "puzzle": i+1,
            "time_s": end_time - start_time,
            "nodes_explored": nodes_explored,
            "path_length": len(path.split(" -> ")) if path else None
        })
    return results

if __name__ == "__main__":
    goal = "ABCDEFGHIJKLMNO_"
    puzzles = [
        "BECDA_FGMJNKOILH",
        "AG_BECLDJFHKIMNO",
        "AFDHIECK_JLBMGNO",
        "BEAHGJICND_KMFOL",
        "BCDGIEH_JAFKMNOL"
    ]
    n = int(len(goal) ** 0.5)

    results = benchmarkSolver(solvePuzzleAStar, puzzles, goal)

    print("--------------Results---------------")
    for r in results:
        print(f"Puzzle {r['puzzle']}: Time={r['time_s']:.4f}s, Nodes={r['nodes_explored']}, Path length={r['path_length']}")
