import subprocess
from compiler_error import *
from collections import *  #FIXME this is not good practice 
import re 
import subprocess
import json
import os

# FIXME class doesn't only parse the compiler errors now as well, it parses the normal test output as well
#so the name should be changed to RustTestOutputParser or something similar
class RustCompilerErrorParser:
    def __init__(self, project_path):
        """
        Initialize the parser with the path to the Rust project
        @param: project_path: Path to the Rust project root directory
        """
        self.project_path = project_path
        self.errors = (
            #TODO: Add more error classes
            OwnershipError,
            TypeMismatchError,
            BorrowCheckerError,
            TraitImplementationError,
            UndefinedValueError,
            MethodNotFoundError,
            OperatorTypeError,
            MutableBorrowError,
            UndeclaredLifetimeError,
            DerefFieldError,
            )
        self.list_of_errors = None
        self.passed = 0
        self.failed = 0 

    def parse_cargo_test_output(self):
        """
        Run cargo test and parse the output for compiler errors and run time result of the test. 
        @return: List of CompilerError instances
        """
        try:
            # Change to the project directory
            original_dir = os.getcwd()
            os.chdir(self.project_path)

            # Run cargo test with JSON output
            result = subprocess.run(
                ['cargo', 'test', '--message-format=json'], #enable running as well..  
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
                        code = error_details.get('code', {})

                        # if it is an actual error, we will have a code
                        if code:
                            error_code = code.get('code', '')
                        else:
                            continue
                        spans = error_details.get('spans', [{}])[0]
                        line = spans.get('line_start', 0)
                        column = spans.get('column_start', 0)
                        error_message = error_details.get('message', {})
                        
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
                    expr = r"(\d+)\s+passed;\s+(\d+)\s+failed;"
                    match = re.search(expr, line)
                    if match:
                        self.passed = int(match.group(1))
                        self.failed = int(match.group(2))
            
            # Change back to original directory
            os.chdir(original_dir)
            self.list_of_errors = errors
            return errors

        except subprocess.CalledProcessError as e:
            print(f"Error running cargo test: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error: {e}")
            return []

    def generate_report(self):
        """
        Generate a comprehensive error report
        @param: self
        @return: Dictionary with error statistics and unit test result
        """
        # if self.list_of_errors is None:
        errors = self.parse_cargo_test_output()
        # else:
            # errors = self.list_of_errors
        
        report = {
            'total_errors': len(errors),
            'errors_by_type': {},
            'total_score': 0,
            'passed': self.passed,
            'failed': self.failed
        }
        
        for error in errors:
            error_type = type(error).__name__
            if error_type not in report['errors_by_type']:
                report['errors_by_type'][error_type] = 0
            report['errors_by_type'][error_type] += 1
            
            report['total_score'] += error.score
        if not (self.passed == 0 and self.failed == 0):
            report['total_score'] = report['failed'] / (report['failed'] + report['passed'])
        
        return report

# Example usage
def main():
    # Specify the path to your Rust project
    current_file_path = os.path.dirname(__file__)

    # Construct the relative path
    folder2_path = os.path.join(current_file_path, '../linked_list')

    # Resolve to an absolute path
    project_path = os.path.abspath(folder2_path)

    print(project_path)    
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