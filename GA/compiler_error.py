class CompilerError:
    ERROR_CODE = 0

    def __init__(self, line, column, message):
        self.line = line
        self.column = column
        self.message = message
        self.score = 0

    @classmethod
    def class_code(cls):
        return f"E{cls.ERROR_CODE:04}"

    def __str__(self):
        return f"[E{self.ERROR_CODE:04}] at line {self.line}, column {self.column}: {self.message}"


class TypeMismatchError(CompilerError):
    ERROR_CODE = 308  # E0308: Mismatched types

    def __init__(self, line, column, message):
        super().__init__(line, column, message)
        self.score = 8
        self.name = "Type Mismatch Error"


class OwnershipError(CompilerError):
    ERROR_CODE = 382  # E0382: Use of moved value

    def __init__(self, line, column, message):
        super().__init__(line, column, message)
        self.score = 10
        self.name = "Ownership Error"


class BorrowCheckerError(CompilerError):
    ERROR_CODE = 499  # E0499: Cannot borrow as mutable more than once at a time

    def __init__(self, line, column, message):
        super().__init__(line, column, message)
        self.score = 9
        self.name = "Borrow Checker Error"


class TraitImplementationError(CompilerError):
    ERROR_CODE = 277  # E0277: Trait not implemented

    def __init__(self, line, column, message):
        super().__init__(line, column, message)
        self.score = 7
        self.name = "Trait Implementation Error"


class UndefinedValueError(CompilerError):
    ERROR_CODE = 425  # E0425: Cannot find value in this scope

    def __init__(self, line, column, message):
        super().__init__(line, column, message)
        self.score = 6
        self.name = "Undefined Value Error"

class UndeclaredType(CompilerError):
    ERROR_CODE = 433
    def __init__(self, line, column, message):
        super().__init__(line, column, message)
        self.score = 10
        self.name = "Undeclared Type Error"
class MethodNotFoundError(CompilerError):
    ERROR_CODE = 599  # E0599: No method named X found for type Y

    def __init__(self, line, column, message):
        super().__init__(line, column, message)
        self.score = 7
        self.name = "Method Not Found Error"


class OperatorTypeError(CompilerError):
    ERROR_CODE = 369  # E0369: Cannot apply binary operator to types

    def __init__(self, line, column, message):
        super().__init__(line, column, message)
        self.score = 5
        self.name = "Operator Type Error"


class MutableBorrowError(CompilerError):
    ERROR_CODE = 502  # E0502: Cannot borrow as immutable because it is also borrowed as mutable

    def __init__(self, line, column, message):
        super().__init__(line, column, message)
        self.score = 8
        self.name = "Mutable Borrow Error"


class UndeclaredLifetimeError(CompilerError):
    ERROR_CODE = 261  # E0261: Use of undeclared lifetime name

    def __init__(self, line, column, message):
        super().__init__(line, column, message)
        self.score = 6
        self.name = "Undeclared Lifetime Error"


class DerefFieldError(CompilerError):
    ERROR_CODE = 609  # E0609: Attempt to access a field of a type that does not implement Deref

    def __init__(self, line, column, message):
        super().__init__(line, column, message)
        self.score = 5
        self.name = "Deref Field Error"
