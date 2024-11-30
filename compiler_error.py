class CompilerError:
    ERROR_CODE = 0

    def __init__(self, line, column, message):
        self.line = line
        self.column = column
        self.message = message
        self.score = 0

    @classmethod
    def class_code(cls):
        return f"E0{cls.ERROR_CODE}"
    
    @classmethod
    def class_code_for_debugging(cls):
        return f"E0{cls.ERROR_CODE}"
    def __str__(self):
        return f"[E0{self.ERROR_CODE}] at line {self.line}, column {self.column}: {self.message}"

class MovedValueError(CompilerError):
    ERROR_CODE = 382

    def __init__(self, line, column, message):
        super().__init__(line, column, message)
        self.score = 10
        self.name = "Moved Value Error"

    
class TypeMismatchError(CompilerError):
    ERROR_CODE = 308

    def __init__(self, line, column, message):
        super().__init__(line, column, message)
        self.score = 8
        self.name = "Type Mismatch Error"

    
class BorrowOneTimeError(CompilerError):
    ERROR_CODE = 499

    def __init__(self, line, column, message):
        super().__init__(line, column, message)
        self.score = 9
        self.name = "Borrow One Time Error"

    
class PatternMatchingError(CompilerError):
    ERROR_CODE = 504

    def __init__(self, line, column, message):
        super().__init__(line, column, message)
        self.score = 6
        self.name = "Pattern Matching Error"

    
class TraitImplementationError(CompilerError):
    ERROR_CODE = 277

    def __init__(self, line, column, message):
        super().__init__(line, column, message)
        self.score = 7
        self.name = "Trait Implementation Error"

    
class ValueNotFoundScopeError(CompilerError):
    ERROR_CODE = 425

    def __init__(self, line, column, message):
        super().__init__(line, column, message)
        self.score = 5
        self.name = "Value Not Found Scope Error"

    
class ConstStaticError(CompilerError):
    ERROR_CODE = 507

    def __init__(self, line, column, message):
        super().__init__(line, column, message)
        self.score = 6
        self.name = "Const/Static Error"

    
class VisibilityError(CompilerError):
    ERROR_CODE = 508

    def __init__(self, line, column, message):
        super().__init__(line, column, message)
        self.score = 4
        self.name = "Visibility Error"
   
    
    
class BorrowCheckerError(CompilerError):
    ERROR_CODE = 382

    def __init__(self, line, column, message):
        super().__init__(line, column, message)
        self.score = 9
        self.name = "Borrow Checker Error"

    
class GenericConstraintError(CompilerError):
    ERROR_CODE = 510

    def __init__(self, line, column, message):
        super().__init__(line, column, message)
        self.score = 7
        self.name = "Generic Constraint Error"

    