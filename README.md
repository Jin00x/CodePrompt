# CS454 Team Project
CS454 | Team 8 | Project

## Implementation Details

This project implements a genetic algorithm (GA) to generate the best promptfor the Rust code for a singly linked list. The GA evolves solutions over multiple generations to optimize the prompt based on fitness values.

### Project Structure
````markdown
The project is organized as follows:

CS454---Team-project/
├── GA/
│   ├── __init__.py
│   ├── error_message_parser.py
│   ├── ga.py
│   ├── llm_api.py
│   ├── test_capture.py
│   └── test.py
├── initial_prompts/
│   └── init_prompts.json
├── rust_examples/
│   ├── Cargo.lock
│   ├── Cargo.toml
│   └── src/
│       └── linked_list/
│           ├── linked_list.rs
│           ├── linked_list_src.rs
│           └── test_linked_list.rs
│       └── graph/
│           ├── graph.rs
│           ├── graph_src.rs
│           └── test_graph.rs
│       ...
├── .gitignore
├── README.md
└── requirements.txt
````

### Setup Instructions

1. **Create a virtual environment:**

    ```sh
    python -m venv venv
    ```

2. **Activate the virtual environment:**

    - On Windows:

        ```sh
        .\venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```sh
        source venv/bin/activate
        ```

3. **Install the required dependencies:**

    ```sh
    pip install -r requirements.txt
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

This project leverages the OpenAI API to generate and evolve prompts for the Rust code, ensuring that the generated code adheres to Rust's strict ownership and borrowing rules.

