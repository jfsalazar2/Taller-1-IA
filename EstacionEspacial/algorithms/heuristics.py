from typing import Tuple

from django.db.migrations import state
from algorithms import utils
from algorithms.problems import SystemRepairProblem


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def manhattanHeuristic(state, problem):
    """
    The Manhattan distance heuristic.

    Baseline rule for this workshop: estimate the direct distance to the next
    mandatory target:
    - K if the robot does not have the kit yet.
    - the nearest pending T if the robot has the kit and systems remain.
    - C if all systems have been repaired.
    """
    position, hasKit, pendingSystems = state
    x1, y1 = position

    # si todavia no tiene el kit, el objetivo mas cercano es ir por el kit
    if not hasKit:
        x2, y2 = problem.kitPosition
        return abs(x1 - x2) + abs(y1 - y2)

    # si ya tiene el kit pero faltan sistemas por reparar,
    # calculamos la distancia al T mas cercano
    if len(pendingSystems) > 0:
        distancias = []
        for sistema in pendingSystems:
            x2, y2 = sistema
            distancias.append(abs(x1 - x2) + abs(y1 - y2))
        return min(distancias)

    # si ya reparo todo, lo unico que falta es volver al centro de control
    x2, y2 = problem.controlPosition
    return abs(x1 - x2) + abs(y1 - y2)


def euclideanHeuristic(state, problem):
    """
    The Euclidean distance heuristic.

    Baseline rule for this workshop: estimate the direct distance to the next
    mandatory target:
    - K if the robot does not have the kit yet.
    - the nearest pending T if the robot has the kit and systems remain.
    - C if all systems have been repaired.
    """
    position, hasKit, pendingSystems = state
    x1, y1 = position

    # si no tiene el kit, calculamos distancia en linea recta hasta K
    if not hasKit:
        x2, y2 = problem.kitPosition
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    # si ya tiene el kit pero faltan T's, buscamos el mas cercano
    if len(pendingSystems) > 0:
        distancias = []
        for sistema in pendingSystems:
            x2, y2 = sistema
            distancias.append(((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5)
        return min(distancias)

    # si ya reparo todo, falta volver a C
    x2, y2 = problem.controlPosition
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def systemRepairHeuristic(
    state: Tuple[Tuple, bool, Tuple], problem: SystemRepairProblem
):
    """
    Your heuristic for the SystemRepairProblem.

    state: (position, hasKit, pendingSystems)
    problem: SystemRepairProblem instance

    This must be admissible and preferably consistent.

    Hints:
    - Use problem.heuristicInfo to cache expensive computations
    - Go with some simple heuristics first, then build up to more complex ones
    - Consider the kit, pending systems, and the final return to control center
    - Balance heuristic strength vs. computation time (do experiments!)
    """
    position, hasKit, pendingSystems = state
    def manhattan(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    total = 0
    actual = position
    # si no tiene el kit, primero obligatoriamente debe llegar a K
    if not hasKit:
        total += manhattan(actual, problem.kitPosition)
        actual = problem.kitPosition
    if len(pendingSystems) > 0:
        # faltan sistemas obligatorios por visitar
        distancias = [
            manhattan(actual, sistema)
            for sistema in pendingSystems
        ]
        # tambien sabemos que eventualmente debemos terminar en C
        distanciaControl = manhattan(
            actual,
            problem.controlPosition
        )
        total += max(
            max(distancias),
            distanciaControl
        )
    else:
        # ya reparo todos los sistemas, solo falta C
        total += manhattan(
            actual,
            problem.controlPosition
        )
    return total
