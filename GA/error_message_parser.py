import subprocess
from compiler_error import *
from collections import *  #FIXME this is not good practice 

import subprocess
import re
import json
import os


class RustCompilerErrorParser:
    def __init__(self, project_path):
        """
        Initialize the parser with the path to the Rust project
        @param: project_path: Path to the Rust project root directory
        """
        self.project_path = project_path
        self.errors = (
            OwnershipError,
            TypeMismatchError,
            LifetimeError,
            PatternMatchingError,
            TraitImplementationError,
            MutabilityError,
            BorrowCheckerError,
            GenericConstraintError
        )

    def parse_cargo_test_output(self):
        """
        Run cargo test and parse the output for compiler errors
        
        :return: List of CompilerError instances
        """
        try:
            # Change to the project directory
            original_dir = os.getcwd()
            os.chdir(self.project_path)

            # Run cargo test with JSON output
            result = subprocess.run(
                ['cargo', 'test', '--no-run', '--message-format=json'], 
                capture_output=True, 
                text=True
            )

            # Collect errors
            errors = []
            
            # Parse JSON output
            for line in result.stdout.split('\n'):
                if not line.strip():
                    continue
                try:
                    message = json.loads(line)
                    
                    # Check if it's a compiler error
                    if message.get('reason') == 'compiler-message':
                        error_details = message.get('message', {})
                        
                        # Extract error specifics
                        spans = error_details.get('spans', [{}])[0]
                        line = spans.get('line_start', 0)
                        column = spans.get('column_start', 0)
                        error_message = error_details.get('message', {})
                        code = error_details.get('code', {})

                        if code:
                            error_code = code.get('code', '')
                        else:
                            continue
                        
                        # Determine error type
                        error_class = CompilerError
                        for error_type in self.errors:
                            if error_code == error_type.class_code():
                                error_class = error_type
                                break
                        
                        # Create error instance
                        error = error_class(
                            line=line, 
                            column=column, 
                            message=error_message
                        )
                        errors.append(error)
                
                except json.JSONDecodeError:
                    # Skip lines that aren't valid JSON
                    continue
            
            # Change back to original directory
            os.chdir(original_dir)
            
            return errors

        except subprocess.CalledProcessError as e:
            print(f"Error running cargo test: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error: {e}")
            return []

    def generate_error_report(self):
        """
        Generate a comprehensive error report
        
        :return: Dictionary with error statistics
        """
        errors = self.parse_cargo_test_output()
        
        report = {
            'total_errors': len(errors),
            'errors_by_type': {},
            'total_score': 0
        }
        
        for error in errors:
            error_type = type(error).__name__
            if error_type not in report['errors_by_type']:
                report['errors_by_type'][error_type] = 0
            report['errors_by_type'][error_type] += 1
            
            report['total_score'] += error.score
        
        return report

# Example usage
def main():
    # Specify the path to your Rust project
    project_path = '/Users/coll1ns/CS454---Team-project/linked_list'
    
    # Create parser instance
    parser = RustCompilerErrorParser(project_path)
    
    # Parse errors
    errors = parser.parse_cargo_test_output()
    
    # Print individual errors
    for error in errors:
        print(error)
    
    # Generate error report
    report = parser.generate_error_report()
    print("\nError Report:")
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()