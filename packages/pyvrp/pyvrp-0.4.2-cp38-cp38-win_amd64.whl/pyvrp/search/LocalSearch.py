from typing import List

from pyvrp._CostEvaluator import CostEvaluator
from pyvrp._ProblemData import ProblemData
from pyvrp._Solution import Solution
from pyvrp._XorShift128 import XorShift128

from ._LocalSearch import LocalSearch as _LocalSearch

Neighbours = List[List[int]]


class LocalSearch:
    """
    Local search method. This search method explores a granular neighbourhood
    in a very efficient manner using user-provided node and route operators.
    This quickly results in much improved solutions.

    Parameters
    ----------
    data
        Data object describing the problem to be solved.
    rng
        Random number generator.
    neighbours
        List of lists that defines the local search neighbourhood.
    """

    def __init__(
        self, data: ProblemData, rng: XorShift128, neighbours: Neighbours
    ):
        self._ls = _LocalSearch(data, neighbours)
        self._rng = rng

    def add_node_operator(self, op):
        """
        Adds a node operator to this local search object. The node operator
        will be used by :meth:`~search` to improve a solution.

        Parameters
        ----------
        op
            The node operator to add to this local search object.
        """
        self._ls.add_node_operator(op)

    def add_route_operator(self, op):
        """
        Adds a route operator to this local search object. The route operator
        will be used by :meth:`~intensify` to improve a solution using more
        expensive route operators.

        Parameters
        ----------
        op
            The route operator to add to this local search object.
        """
        self._ls.add_route_operator(op)

    def set_neighbours(self, neighbours: Neighbours):
        """
        Convenience method to replace the current granular neighbourhood used
        by the local search object.

        Parameters
        ----------
        neighbours
            A new granular neighbourhood.
        """
        self._ls.set_neighbours(neighbours)

    def get_neighbours(self) -> Neighbours:
        """
        Returns the granular neighbourhood currently used by the local search.

        Returns
        -------
        list
            The current granular neighbourhood.
        """
        return self._ls.get_neighbours()

    def run(
        self,
        solution: Solution,
        cost_evaluator: CostEvaluator,
        should_intensify: bool,
    ) -> Solution:
        """
        This method uses the :meth:`~search` and :meth:`~intensify` methods to
        iteratively improve the given solution. First, :meth:`~search` is
        applied. Thereafter, if ``should_intensify`` is true,
        :meth:`~intensify` is applied. This process repeats until no further
        improvements are found. Finally, the improved solution is returned.

        Parameters
        ----------
        solution
            The solution to improve through local search.
        cost_evaluator
            Cost evaluator to use.
        should_intensify
            Whether to apply :meth:`~intensify`. Intensification can provide
            much better solutions, but is computationally demanding. By default
            intensification is applied.

        Returns
        -------
        Solution
            The improved solution. This is not the same object as the
            solution that was passed in.
        """
        # HACK We keep searching and intensifying to mimic the local search
        # implementation of HGS-CVRP and HGS-VRPTW
        # TODO separate load/export solution from c++ implementation
        # so we only need to do it once
        while True:
            solution = self.search(solution, cost_evaluator)

            if not should_intensify:
                return solution

            new_solution = self.intensify(solution, cost_evaluator)

            current_cost = cost_evaluator.penalised_cost(solution)
            new_cost = cost_evaluator.penalised_cost(new_solution)

            if new_cost < current_cost:
                solution = new_solution
                continue

            return solution

    def intensify(
        self,
        solution: Solution,
        cost_evaluator: CostEvaluator,
        overlap_tolerance_degrees: int = 0,
    ) -> Solution:
        """
        This method uses the intensifying route operators on this local search
        object to improve the given solution. To limit the computation
        demands of intensification, the  ``overlap_tolerance_degrees`` argument
        can be used to limit the number of route pairs that are evaluated.

        Parameters
        ----------
        solution
            The solution to improve.
        cost_evaluator
            Cost evaluator to use.
        overlap_tolerance_degrees
            This method evaluates improving moves between route pairs. To limit
            computational efforts, by default not all route pairs are
            considered: only those route pairs that share some overlap when
            considering their center's angle from the depot are evaluted.
            This parameter controls the amount of overlap needed before two
            routes are evaluated.

        Raises
        ------
        RuntimeError
            When this method is called before registering route operators.
            Operators can be registered using :meth:`~add_route_operator`.

        Returns
        -------
        Solution
            The improved solution. This is not the same object as the
            solution that was passed in.
        """
        self._ls.shuffle(self._rng)
        return self._ls.intensify(
            solution, cost_evaluator, overlap_tolerance_degrees
        )

    def search(
        self, solution: Solution, cost_evaluator: CostEvaluator
    ) -> Solution:
        """
        This method uses the node operators on this local search object to
        improve the given solution.

        Parameters
        ----------
        solution
            The solution to improve.
        cost_evaluator
            Cost evaluator to use.

        Raises
        ------
        RuntimeError
            When this method is called before registering node operators.
            Operators can be registered using :meth:`~add_node_operator`.

        Returns
        -------
        Solution
            The improved solution. This is not the same object as the
            solution that was passed in.
        """
        self._ls.shuffle(self._rng)
        return self._ls.search(solution, cost_evaluator)
