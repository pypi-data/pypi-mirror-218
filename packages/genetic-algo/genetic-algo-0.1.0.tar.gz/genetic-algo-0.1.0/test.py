# test.py

from genetic_algo.attributes import FloatAttribute
from genetic_algo.solution import Template, Solution
from genetic_algo.driver import DriverDefinition, Driver
from genetic_algo.environment import (
    Environment, EnvironmentDefinition, Fitness, History
)

class Parameter(FloatAttribute):
    """A class to represent an attribute of a solution."""

    FLOOR = -5
    ROOF = 5
    STEP = 0.1

    EXCLUDED = [0]
# end Parameter

class CombinationSolution(Solution):
    """A class to represent a solution of a problem."""
# end CombinationSolution

class FormulaTemplate(Template):
    """A class to represent a template for solution attributes."""

    SOLUTION = CombinationSolution
    ATTRIBUTES = [Parameter, Parameter, Parameter]
# end FormulaTemplate

class MeanAbsoluteError(Fitness):
    """A class to represent a fitness function."""

    variables = list(range(-1000, 1000))

    def call(self, solution: CombinationSolution) -> float:
        """
        Calls the fitness function on the solution.

        :param solution: The solution object.

        :return: The fitness value.
        """

        # a * x ^ 2 + b * x + c = 0
        # Finds a function with the minima of 1.

        return round(
            sum(
                abs(
                    (
                        (
                            solution.attributes[0].value * (value ** 2) +
                            solution.attributes[1].value * value +
                            solution.attributes[2].value
                        ) - 1
                    ) / (value if value != 0 else 1)
                )
                for value in self.variables
            ) / len(self.variables), 5
        )
    # end call
# end MeanAbsoluteError

def main() -> None:
    """The main function to run the test."""

    environment_definition = EnvironmentDefinition(
        size=100,
        ascending=False,
        repetitions=False,
        padding=True,
        parents=2,
        eliminations=0.05,
        successors=0.5,
        continuers=0.05,
        mutations=0.01
    )

    template = FormulaTemplate()
    fitness = MeanAbsoluteError()
    history = History()

    environment = Environment(
        definition=environment_definition,
        template=template,
        fitness=fitness,
        history=history
    )

    deriver_definition = DriverDefinition(
        fitness_limit=1,
        max_generations=100,
        min_improvement=0.001,
        min_count=1
    )

    driver = Driver(
        definition=deriver_definition,
        environment=environment
    )

    generations = driver.run()

    print(generations[-1])
    print(len(generations))
# end main

if __name__ == "__main__":
    main()
# end if