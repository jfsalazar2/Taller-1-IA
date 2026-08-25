from algorithms.problems import SearchProblem
import algorithms.utils as utils
from world.game import Directions
from algorithms.heuristics import nullHeuristic


def tinyDiagnosticSearch(problem: SearchProblem):
    """
    Returns a hard-coded sequence of moves for the tinyDiagnostic layout.
    For any other station layout, the sequence of moves will be incorrect.
    """
    s = Directions.SOUTH
    e = Directions.EAST
    return [s, e, s, e, e, e, e, s, e, e, s, s, e, s, s, e, s, e, e, e, e, e, e, e]


def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    # TODO: Add your code here
    pila = utils.Stack
    estado_inicial = problem.getStartState()
    pila.push((estado_inicial, []))
    visitados = set()
    while not pila.isEmpty():
        estado, acciones = pila.pop()
        if problem.isGoalState(estado):
            return acciones
        if estado not in visitados:
            visitados.add(estado)
            for sucesor, accion, _ in problem.getSuccessors(estado):
                pila.push((sucesor, acciones + [accion]))
                
    return []  

def breadthFirstSearch(problem: SearchProblem):
    """
    Search the shallowest nodes in the search tree first.
    """
    # TODO: Add your code here
    cola = utils.Queue()
    estado_inicial = problem.getStartState()
    cola.push((estado_inicial, []))
    visitados = set()
    while not cola.isEmpty():
        estado, acciones = cola.pop()
        if problem.isGoalState(estado):
                return acciones
        if estado not in visitados:
                visitados.add(estado)
                for sucesor, accion, _ in problem.getSuccessors(estado):
                    cola.push((sucesor, acciones + [accion]))
                    
    return []  


def uniformCostSearch(problem: SearchProblem):
    """
    Search the node of least total cost first.
    """

    # TODO: Add your code here
    prioridad = utils.PriorityQueue()
    estado_inicial = problem.getStartState()
    prioridad.push((estado_inicial, [], 0), 0)
    visitados = set()
    while not prioridad.isEmpty():
        estado, acciones, costo = prioridad.pop()
        if problem.isGoalState(estado):
            return acciones
        if estado not in visitados:
            visitados.add(estado)
            for sucesor, accion, costo_sucesor in problem.getSuccessors(estado):
                prioridad.push((sucesor, acciones + [accion], costo + costo_sucesor), costo + costo_sucesor)
    return []


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    # TODO: Add your code here
    utils.raiseNotDefined()


# Abbreviations (you can use them for the -f option in main.py)
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
