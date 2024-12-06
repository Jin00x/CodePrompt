
from data_types import *
from typing import List, Union, Tuple
from llm_api import *
import random
import numpy as np
import json

from error_message_parser import RustCompilerErrorParser
from compiler_error import CompilerError


class Solution:
    def __init__(
        self, 
        prompt: str = "",
        code_string: str = "",
        source_code: str = "",
        fitness: float = float('inf'), 
        run_fitness: bool = False,
        err_parser: RustCompilerErrorParser = None
    ):
        self.prompt = prompt
        self.code_string = code_string
        self.source_code = source_code
        self.fitness = fitness
        self.err_parser = err_parser

        if run_fitness is True:
            self.eval_fitness()
    

    # calculate the fitness
    def eval_fitness(self) -> float:
        # generate the code from llm
        self.generate_code()

        # write the code to the linked_list_src.rs file
        with open('../linked_list/src/linked_list.rs', 'w') as file:
            file.write(self.code_string)

        # run the code, collect the errors from parser
        errors: List[CompilerError] = self.err_parser.parse_cargo_test_output()
        score = sum([err.score for err in errors])

        # print(len(errors), "errors found")
        # print(self.code_string)

        # for err in errors:
        #     print(err.ERROR_CODE, err.message, err.score)

        # clean the test file
        with open('../linked_list/src/linked_list.rs', 'w') as file:
            file.write('')

        # set fitness
        self.fitness = score
        return self.fitness
    
    # call prompt to get code from llm
    def generate_code(self) -> str:
        print("Calling OpenAI API in Solution")
        llm_output = call_openai_api(self.prompt)
        print("OpenAI API call finished in Solution")
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
) -> Solution:
    
    current_file_path = os.path.dirname(__file__)
    folder_path = os.path.join(current_file_path, '../linked_list')
    project_path = os.path.abspath(folder_path)

    # create instance of Rust error parser
    err_parser = RustCompilerErrorParser(project_path)

    # read from the initial prompts json file
    initial_prompts = []
    with open('../initial_prompts/init_prompts.json', 'r') as file:
        initial_prompts = json.load(file)
        initial_prompts = initial_prompts['prompts']

    source_code = ""
    with open('../linked_list/src/linked_list.rs', 'r') as file:
        source_code = file.read()

    # create initial population
    population = []
    for prompt in [initial_prompts[0]]:
        solution = Solution(
            prompt=prompt + source_code,
            code_string="",
            source_code=source_code,
            fitness=float('inf'),
            run_fitness=True,
            err_parser=err_parser
        )
        population.append(solution)
    print("Initial Population Created")

    # derive best current solution
    best_solution = min(population, key=eval_fitness)
    print(f"Initial Best Solution: {best_solution.fitness}\n")

    for generation_num in range(generation_limit):
        print(f"Generation: {generation_num + 1}")
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
        print("Mating Pool Created")
        
        # crossover
        new_population = crossover_on_population(mating_pool)
        print("Crossover Done")

        # mutation
        apply_mutation_to_population(new_population, mutation_rate)
        print("Mutation Done")

        # selection from pools
        population = general_selection_based_on_type(
            population,
            new_population,
            new_population_selection_type
        )
        print("Selection Done")

        # update best solution
        best_solution = min(best_solution, min(population, key=eval_fitness), key=eval_fitness)
        print(f"Best Solution: {best_solution.fitness}\n")

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

    # TODO: Implement the mutation logic

    for sol in population:
        mutation_prompt = f"""
<prompt_here>
Mutation Rate: {mutation_rate}
"""
    
        mutated_prompt = call_openai_api(mutation_prompt)
        sol.prompt = mutated_prompt


def crossover_on_population(
    mating_pool: List[Solution], 
) -> List[Solution]:
    
    new_population = []
    for i in range(len(mating_pool) - 1):
        for j in range(i + 1, len(mating_pool)):
            new_population.append(
                crossover_between_parents(
                    mating_pool[i],
                    mating_pool[j],
                )
            )

    return new_population


def crossover_between_parents(
    parent1: Solution, 
    parent2: Solution,
) -> Solution:
    
    cross_over_prompt = f"""
<prompt_here>

Parent 1: {parent1.prompt}
Parent 2: {parent2.prompt}
"""
    
    child_prompt = call_openai_api(cross_over_prompt)
    child = Solution(
        prompt=child_prompt,
        code_string="",
        source_code=parent1.source_code,
        fitness=float('inf'),
        run_fitness=False,
        err_parser=parent1.err_parser
    )
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


if __name__ == "__main__":
    solution = GA()
    print(f"Best Solution: {solution.prompt}\n")
    print(f"Best Fitness: {solution.fitness}\n")
    print(f"Best Code: {solution.code_string}\n")