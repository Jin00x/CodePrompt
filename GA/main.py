
from data_types import *
from typing import List, Union, Tuple
import subprocess
from llm_api import *
import math
import random
import numpy as np


class Solution:
    def __init__(
        self, 
        prompt: str = "", 
        code_string: str = "", 
        fitness: float = float('inf'), 
        run_fitness: bool = False
    ):
        self.prompt = prompt
        self.code_string = code_string
        self.fitness = fitness

        if run_fitness is True:
            self.eval_fitness()
    
    # runs the test file on given rust code, and returns output and error
    def run_code(self) -> Tuple[str, str]:
        # Write the code_string to test.rs
        with open('test.rs', 'w') as file:
            file.write(self.code_string)

        # run the code, set capture_output to True to get the output and error msg
        res = subprocess.run(['cargo', 'run'], cwd='linked_list/src', capture_output=True, text=True)
        res_output, res_err = res.stdout, res.stderr

        # clean the test.rs file
        with open('test.rs', 'w') as file:
            file.write('')

        return res_output, res_err

    # calculate the fitness
    def eval_fitness(self) -> float:
        # prompt llm, and set the code string field
        self.generate_code()

        # run the code, and get the output and error
        output, error = self.run_code()
        
        # set fitness
        self.fitness = self.calc_fitness(output, error)
        return self.fitness
    
    # call prompt to get code from llm
    def generate_code(self) -> str:
        llm_output = call_openai_api(self.prompt)
        self.code_string = llm_output
        return llm_output
    
    # TODO: Implement the fitness calculation logic
    # fitness calc logic
    def calc_fitness(self, output: str, error: str) -> float:
        return float('inf')


def GA(
    initial_population_size: int = 50,
    mating_pool_size: int = 20,
    selection_type: NextGenSelectionType = NextGenSelectionType.TRS,
    selection_type_prob_type: Union[RBSType, FPSType] = RBSType.LINEAR_RANKING,
    tournament_selection_size_k: int = 4,
    mutation_rate: float = 0.05,
    new_population_selection_type: SelectionType = SelectionType.GRADUAL_REPLACEMENT,
    generation_limit: int = 20,
    s_in_ranking_based_selection: float = 1.5,
    probability_based_sample_method_type: ProbabilityBasedSampleMethodType = ProbabilityBasedSampleMethodType.ROULETTE_WHEEL,
    cross_over_type: CrossOverType = CrossOverType.SINGLE_POINT
) -> Solution:
    # create initial population
    population = []
    for i in range(initial_population_size):
        solution = Solution()
        # solution.randomize()
        population.append(solution)

    # mutate population for initial population
    apply_mutation_to_population(population, mutation_rate)

    # derive best current solution
    best_solution = min(population, key=eval_fitness)

    for generation_num in range(generation_limit):
        mating_pool = []

        #  if tournament based selection
        if selection_type == NextGenSelectionType.TRS:
            mating_pool = tournament_selection(
                population, 
                tournament_selection_size_k, 
                mating_pool_size
            )
        else:
            # probability based selection: (RBS or FPS)
            mating_pool = solver_probability_based(
                population,
                selection_type_prob_type,
                s_in_ranking_based_selection,
                probability_based_sample_method_type,
                mating_pool_size
            )
        
        # crossover
        new_population = crossover_on_population(mating_pool, cross_over_type)

        # mutation
        apply_mutation_to_population(new_population, mutation_rate)

        # selection from pools
        population = general_selection_based_on_type(
            population,
            new_population,
            new_population_selection_type
        )

        # update best solution
        best_solution = min(best_solution, min(population, key=eval_fitness), key=eval_fitness)

    return best_solution


# custom fitness evaluation function
def eval_fitness(x: Solution) -> float:
    return x.fitness


def solver_probability_based(
    population: List[Solution], 
    type: Union[RBSType, FPSType],
    s: float,
    probability_based_sample_method_type: ProbabilityBasedSampleMethodType,
    mating_pool_size: int
) -> List[Solution]:

    ranked_population = []
    if isinstance(type, RBSType):  # RBS
        # returns List of tuple of (probability, solution)
        ranked_population = ranking_based_selection(
            population,
            type,
            s
        )
    else:   # FPS
        ranked_population = improved_fps(
            population,
            type
        )
    
    # select new population based on probability
    mating_pool = probability_based_selection(
        ranked_population,
        probability_based_sample_method_type,
        mating_pool_size
    )

    return mating_pool


def general_selection_based_on_type(
    population: List[Solution], 
    new_population: List[Solution],
    type: SelectionType
) -> List[Solution]:

    if type == SelectionType.GENERAL_REPLACEMENT:
        # replace all population with new population
        return new_population

    new_population.sort(key=eval_fitness, reverse=True)
    population.sort(key=eval_fitness, reverse=True)
    M_BEST = len(population) // 5

    if type == SelectionType.ELITISM:
        # replace worst solutions with new population
        combined_population = population[-M_BEST:] + new_population[M_BEST:]
        return combined_population

    # GRADUAL_REPLACEMENT
    combined_population = population[M_BEST: ] + new_population[-M_BEST:]
    return combined_population


def apply_mutation_to_population(
    population: List[Solution],
    mutation_rate: float
) -> None:
    # mutation
    # TODO: Implement the mutation logic
    pass


def crossover_on_population(
    mating_pool: List[Solution], 
    cross_over_type: CrossOverType
) -> List[Solution]:
    # TODO: Implement the crossover logic

    return None

def crossover_between_parents(
    parent1: Solution, 
    parent2: Solution,
    cross_over_type: CrossOverType
) -> Solution:

    if cross_over_type == CrossOverType.SINGLE_POINT:
        cross_index = random.sample(range(1, parent1.size() - 1), 1)[0]
        child = parent1.copy()
        
        for i in range(cross_index, parent1.size()):
            child.solution[i] = parent2.solution[i]
        
        return child

    if cross_over_type == CrossOverType.TWO_POINT:
        indexes = random.sample(range(1, parent1.size() - 2), k=2)
        child = parent1.copy()

        for i in range(indexes[0], indexes[1] + 1):
            child.solution[i] = parent2.solution[i]

        return child

    # UNIFORM crossover
    k = 5
    indexes = random.sample(range(parent1.size()), k)
    child = parent1.copy()

    for i in indexes:
        child.solution[i] = parent2.solution[i]

    return child

# needs valid population under budget
def tournament_selection(
    population: List[Solution], 
    k: int, 
    mating_pool_size: int
) -> List[Solution]:
    # tournament selection
    # select k random solutions from population
    mating_pool = set()
    while len(mating_pool) < mating_pool_size:
        while True:
            k_sample = random.sample(population, k)
            best_one = min(k_sample, key=eval_fitness)
            if best_one not in mating_pool:
                mating_pool.add(best_one)
                break

    return list(mating_pool)


def probability_based_selection(
    ranked_population: List[Solution],
    type: ProbabilityBasedSampleMethodType,
    mating_pool_size: int
) -> List[Solution]:
    # roulette wheel selection
    if type == ProbabilityBasedSampleMethodType.ROULETTE_WHEEL:
        return roulette_wheel_selection(ranked_population, mating_pool_size)

    # Stochastic Universal Sampling
    return stochastic_universal_sampling(ranked_population)


def roulette_wheel_selection(
    ranked_population: List[Tuple[float, Solution]],
    mating_pool_size: int
) -> List[Solution]:
    mating_pool = set()
    while len(mating_pool) < mating_pool_size:
        # pick random number uniformly from 0 to 1
        # print(mating_pool_size, len(ranked_population))
        while True:
            random_number = random.random()
            index = 0
            total_probability = ranked_population[0][0]
            while total_probability < random_number:
                index += 1
                total_probability += ranked_population[index][0]
            
            # print(total_probability)
            # print(ranked_population )
            
            if ranked_population[index][1] not in mating_pool:
                mating_pool.add(ranked_population[index][1])
                break

    return list(mating_pool)


def stochastic_universal_sampling(
    ranked_population: List[Tuple[float, Solution]],
) -> List[Solution]:

    pointer_distance = sum([
        sol.value() for _, sol in ranked_population
    ]) / len(ranked_population)

    start_point = random.uniform(0, pointer_distance)
    pointers = [
        start_point + i * pointer_distance for i in range(len(ranked_population) - 1)
    ]

    accum_probs = 0
    curr_index = 0
    mating_pool = []
    for pointer in pointers:
        while curr_index < len(ranked_population) - 1 and accum_probs < pointer:
            accum_probs += ranked_population[curr_index][0]
            curr_index += 1
        mating_pool.append(ranked_population[curr_index][1])

    return mating_pool


# returns List[(probability, solution)]
def ranking_based_selection(
    population: List[Solution], 
    type: RBSType, 
    s: int = 1.5
) -> List[Tuple[float, Solution]]:

    # sort in ascending order of fitness
    population.sort(key=eval_fitness)
    population_size = len(population)

    if type == RBSType.LINEAR_RANKING:
        # calculate the rank sum
        # TODO: implement linear ranking
        return []

    # EXPONENTIAL_RANKING
    # TODO: implement EXPONENTIAL_RANKING ranking
    return []


# returns List[(probability, solution)]
def improved_fps(
    population: List[Solution], 
    type: FPSType
) -> List[Tuple[float, Solution]]:
    if type == FPSType.WINDOWING:
        # get b(t) for linear scaling
        # TODO: implement windowing
        return []
    
    # SIGNAL_SCALING
    # TODO: implement signal scaling, and debug
    # find mean value of population using np
    mean = np.mean([sol.fitness for sol in population])

    # find standard deviation of population using np
    std = np.std([sol.fitness for sol in population])
    c = 2

    # scaling using f(i) = max(f(i) - (mean - c * std), 0)
    ranked_population = [[max(sol.fitness - (mean - c * std), 0), sol] for sol in population]
    total_fitness = sum([updated_fitness for updated_fitness, _ in ranked_population])
    for i in range(len(ranked_population)):
        ranked_population[i][0] /= total_fitness
    return ranked_population