
class CrossoverDeniedException(Exception):
    "Raised when a crossover is denied"
    pass


class InvalidArgumentsException(Exception):
    "Raised when not the right number of arguments are provided"
    pass


class InvalidSelectionType(Exception):
    "Raised the provided selection does not exist"
    pass


class InvalidCrossoverType(Exception):
    "Raised the provided crossover type does not exist"
    pass
