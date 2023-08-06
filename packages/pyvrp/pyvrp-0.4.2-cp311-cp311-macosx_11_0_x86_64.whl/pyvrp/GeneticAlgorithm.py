import time
from dataclasses import dataclass
from typing import Callable, Collection, Tuple

from pyvrp.search.LocalSearch import LocalSearch
from pyvrp.stop import StoppingCriterion

from .PenaltyManager import PenaltyManager
from .Population import Population
from .Result import Result
from .Statistics import Statistics
from ._CostEvaluator import CostEvaluator
from ._ProblemData import ProblemData
from ._Solution import Solution
from ._XorShift128 import XorShift128

_Parents = Tuple[Solution, Solution]
CrossoverOperator = Callable[
    [_Parents, ProblemData, CostEvaluator, XorShift128], Solution
]


@dataclass
class GeneticAlgorithmParams:
    repair_probability: float = 0.80
    collect_statistics: bool = False
    intensify_probability: float = 0.15
    intensify_on_best: bool = True
    nb_iter_no_improvement: int = 20_000

    def __post_init__(self):
        if not 0 <= self.repair_probability <= 1:
            raise ValueError("repair_probability must be in [0, 1].")

        if not 0 <= self.intensify_probability <= 1:
            raise ValueError("intensify_probability must be in [0, 1].")

        if self.nb_iter_no_improvement < 0:
            raise ValueError("nb_iter_no_improvement < 0 not understood.")


class GeneticAlgorithm:
    """
    Creates a GeneticAlgorithm instance.

    Parameters
    ----------
    data
        Data object describing the problem to be solved.
    penalty_manager
        Penalty manager to use.
    rng
        Random number generator.
    population
        Population to use.
    local_search
        Local search instance to use.
    crossover_op
        Crossover operator to use for generating offspring.
    initial_solutions
        Initial solutions to use to initialise the population.
    params
        Genetic algorithm parameters. If not provided, a default will be used.

    Raises
    ------
    ValueError
        When the population is empty.
    """

    def __init__(
        self,
        data: ProblemData,
        penalty_manager: PenaltyManager,
        rng: XorShift128,
        population: Population,
        local_search: LocalSearch,
        crossover_op: CrossoverOperator,
        initial_solutions: Collection[Solution],
        params: GeneticAlgorithmParams = GeneticAlgorithmParams(),
    ):
        if len(initial_solutions) == 0:
            raise ValueError("Expected at least one initial solution.")

        self._data = data
        self._pm = penalty_manager
        self._rng = rng
        self._pop = population
        self._ls = local_search
        self._op = crossover_op
        self._initial_solutions = initial_solutions
        self._params = params

        # Find best feasible initial solution if any exist, else set a random
        # infeasible solution (with infinite cost) as the initial best.
        self._best = min(initial_solutions, key=self._cost_evaluator.cost)

    @property
    def _cost_evaluator(self) -> CostEvaluator:
        return self._pm.get_cost_evaluator()

    def run(self, stop: StoppingCriterion):
        """
        Runs the genetic algorithm with the provided stopping criterion.

        Parameters
        ----------
        stop
            Stopping criterion to use. The algorithm runs until the first time
            the stopping criterion returns ``True``.

        Returns
        -------
        Result
            A Result object, containing statistics and the best found solution.
        """
        start = time.perf_counter()
        stats = Statistics()
        iters = 0
        iters_no_improvement = 1

        for sol in self._initial_solutions:
            self._pop.add(sol, self._cost_evaluator)

        while not stop(self._cost_evaluator.cost(self._best)):
            iters += 1

            if iters_no_improvement == self._params.nb_iter_no_improvement:
                iters_no_improvement = 1
                self._pop.clear()

                for sol in self._initial_solutions:
                    self._pop.add(sol, self._cost_evaluator)

            curr_best = self._cost_evaluator.cost(self._best)

            parents = self._pop.select(self._rng, self._cost_evaluator)
            offspring = self._op(
                parents, self._data, self._cost_evaluator, self._rng
            )
            self._search(offspring)

            new_best = self._cost_evaluator.cost(self._best)

            if new_best < curr_best:
                iters_no_improvement = 1
            else:
                iters_no_improvement += 1

            if self._params.collect_statistics:
                stats.collect_from(self._pop, self._cost_evaluator)

        end = time.perf_counter() - start
        return Result(self._best, stats, iters, end)

    def _search(self, sol: Solution):
        def is_new_best(sol):
            cost = self._cost_evaluator.cost(sol)
            best_cost = self._cost_evaluator.cost(self._best)
            return cost < best_cost

        def add_and_register(sol):
            self._pop.add(sol, self._cost_evaluator)
            self._pm.register_load_feasible(not sol.has_excess_load())
            self._pm.register_time_feasible(not sol.has_time_warp())

        intensify_prob = self._params.intensify_probability
        should_intensify = self._rng.rand() < intensify_prob

        sol = self._ls.run(sol, self._cost_evaluator, should_intensify)

        if is_new_best(sol):
            self._best = sol

            # Only intensify feasible, new best solutions. See also the repair
            # step below. TODO Refactor to on_best callback (see issue #111)
            if self._params.intensify_on_best:
                sol = self._ls.intensify(
                    sol, self._cost_evaluator, overlap_tolerance_degrees=360
                )

                if is_new_best(sol):
                    self._best = sol

        add_and_register(sol)

        # Possibly repair if current solution is infeasible. In that case, we
        # penalise infeasibility more using a penalty booster.
        if (
            not sol.is_feasible()
            and self._rng.rand() < self._params.repair_probability
        ):
            should_intensify = self._rng.rand() < intensify_prob
            sol = self._ls.run(
                sol, self._pm.get_booster_cost_evaluator(), should_intensify
            )

            if is_new_best(sol):
                self._best = sol

                if self._params.intensify_on_best:
                    sol = self._ls.intensify(
                        sol,
                        self._pm.get_booster_cost_evaluator(),
                        overlap_tolerance_degrees=360,
                    )

                    if is_new_best(sol):
                        self._best = sol

            if sol.is_feasible():
                add_and_register(sol)
