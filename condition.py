import const
from error import *
from expression import *


class GenericCondition(object):
    """
    generic conditional statements
    """

    def __init__(self, left, right):
        self.right = Expression(right)
        self.left = Expression(left)


class GreaterThanEqualTo(GenericCondition):
    """
    conditional for >=
    """

    def eval(self, state):
        return self.left.eval(state) >= self.right.eval(state)


class LessThanEqualTo(GenericCondition):
    """
    conditional for <=
    """

    def eval(self, state):
        return self.left.eval(state) <= self.right.eval(state)


class EqualTo(GenericCondition):
    """
    conditional for ==
    """

    def eval(self, state):
        return self.left.eval(state) == self.right.eval(state)


class GreaterThan(GenericCondition):
    """
    conditional for >
    """

    def eval(self, state):
        return self.left.eval(state) > self.right.eval(state)


class LessThan(GenericCondition):
    """
    conditional for <
    """

    def eval(self, state):
        return self.left.eval(state) < self.right.eval(state)


class NotEqual(GenericCondition):
    """
    conditional for !=
    """

    def eval(self, state):
        return self.left.eval(state) != self.right.eval(state)


class ConditionalStatement(object):
    """
    conditional statemnets
    """

    def __init__(self, expression):
        self.expression = expression
        self.expr_type = None

        self.parse()

    def parse(self):
        # Done for ease in implementation
        # Can be optimized for better performance
        # By checking and finding sequentially.
        gtesymbol = self.expression.find(">=")
        ltesymbol = self.expression.find("<=")
        equalsymbol = self.expression.find("==")
        greatersymbol = self.expression.find(">")
        lesssymbol = self.expression.find("<")
        notequalsymbol = self.expression.find("!=")

        if gtesymbol != -1:
            self.expr_type = GreaterThanEqualTo(
                self.expression[:gtesymbol], self.expression[gtesymbol + 2 :]
            )
        elif ltesymbol != -1:
            self.expr_type = LessThanEqualTo(
                self.expression[:ltesymbol], self.expression[ltesymbol + 2 :]
            )
        elif equalsymbol != -1:
            self.expr_type = EqualTo(
                self.expression[:equalsymbol], self.expression[equalsymbol + 2 :]
            )
        elif greatersymbol != -1:
            self.expr_type = GreaterThan(
                self.expression[:greatersymbol], self.expression[greatersymbol + 1 :]
            )
        elif lesssymbol != -1:
            self.expr_type = LessThan(
                self.expression[:lesssymbol], self.expression[lesssymbol + 1 :]
            )
        elif notequalsymbol != -1:
            self.expr_type = NotEqual(
                self.expression[:notequalsymbol], self.expression[notequalsymbol + 2 :]
            )
        else:
            raise IfElseError(
                self.expression, "logic operators must be surrounded by values"
            )

    def eval(self, state):
        try:
            return self.expr_type.eval(state)
        except IfElseError:
            print(self.expression, "Error in Evaluation of conditional Statement")
