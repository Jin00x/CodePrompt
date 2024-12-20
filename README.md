# EvoPrompt for Code: Extending EvoPrompt for the Rust Code generation
EvoPrompt paper: [Connecting Large Language Models with Evolutionary Algorithms Yields Powerful Prompt Optimizers](https://arxiv.org/abs/2309.08532)

## Abstract
EvoPrompt is a framework for optimizing discrete prompts by combining the language processing power of large language models (LLMs) with the efficient search capabilities of evolutionary algorithms (EAs). By starting with an initial population of prompts, EvoPrompt iteratively improves them using LLM-based generation and EA-inspired selection, achieving state-of-the-art performance on tasks across 31 datasets. This approach automates prompt creation and significantly outperforms human-engineered and existing automatic methods, showcasing the potential of integrating LLMs with conventional algorithms for better optimization.

## Proposal
One of the most productive use of generative models is code generation. However, generating high quality code that satisfies all the requirements is a challenging task. EvoPrompt framework doesn't address this aspect of LLM generation; thus, our project aims to extend EvoPrompt to generate the best prompt for the Rust code generation. The project uses the Rust codebase for number of different functionalities as the source code and evolves the prompt to generate the best prompt for the Rust code generation.

## Implementation Details

This project implements a genetic algorithm (GA) to generate the best promptfor the Rust code for a singly linked list. The GA evolves solutions over multiple generations to optimize the prompt based on fitness values.

## Quick Start

### Setup Instructions

1. **Install the required dependencies:**

    ```sh
    pip install -r requirements.txt
    ```
2. **Add you OpenAI Key to .env file in root directory:**

    ```sh
    LLM_API_KEY=<your_key_here>
    ```

### Running the Genetic Algorithm

1. **Navigate to the  directory:**

    ```sh
    cd GA
    ```

2. **Run the genetic algorithm:**

    ```sh
    python ga.py --file <file_name>
    ```

### Code Details

- **GA/ga.py:** Contains the main implementation of the genetic algorithm, including functions for selection, crossover, mutation, and fitness evaluation.
- **GA/error_message_parser.py:** Parses the output of Rust compiler errors and test results.
- **GA/llm_api.py:** Interfaces with the OpenAI API to generate and mutate code prompts.
- **initial_prompts/init_prompts.json:** Contains the initial prompts used to generate the initial population of solutions.
- **rust_examples/src/{project}/{project.rs} Contains the source code of the project 
- **rust_examples/src/{project}/{test_project.rs} Contains the test cases for project

### Testing the source rust code

1. **Navigate to the  directory:**

    ```sh
    cd ../linked_list
    ```

2. **Run the tests:**

    ```sh
    cargo test
    ```

### Additional Information

- **GA/test_capture.py:** Captures and parses the output of to extract error codes.
- **GA/test.py:** Runs the Rust tests and prints the output.
