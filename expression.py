import const
from error import *
import math

infinity = math.inf


class Var(object):
    '''
    variables
    '''

    def __init__(self, data):
        self.variable = data

    def eval(self, state):
        try:
            return state[self.variable]
        except NameError:
            print(f"{self.variable} does not exist... did you define it?")


class Constant(object):
    '''
    constant
    '''

    def __init__(self, data):
        try:
            if data[0] == const.MINUS:
                self.data = -int(data[1:])
            elif data[0] == const.PLUS:
                self.data = int(data[1:])
            else:
                self.data = int(data)
        except ValueError:
            print(f"could not evaluate {data}")

    def eval(self, state):
        return self.data


class Factor(object):

    def __init__(self, expression):
        self.expression = expression
        self.data_type = None

        self.parse()

    def parse(self):

        try:
            if (
                self.expression[0] == const.MINUS
                or self.expression[0] == const.PLUS
                or self.expression[0].isdigit()
            ):
                self.data_type = Constant(self.expression)
            else:
                self.data_type = Var(self.expression)
        except AssignmentError:
            print(self.expression)

    def eval(self, state):
        try:
            return self.data_type.eval(state)
        except EvaluationError:
            print(self.expression, "Unknown Error")


class GenericExpression(object):

    def __init__(self, expression):

        self.expression = expression
        self.left = None
        self.right = None

        self.parse()


class PlusExpression(GenericExpression):

    def parse(self):
        idx = self.expression.find(const.PLUS)

        self.right = Expression(self.expression[0:idx])
        self.left = Expression(self.expression[idx + 1 :])

    def eval(self, state):
        try:
            return self.left.eval(state) + self.right.eval(state)
        except EvaluationError:
            print(self.expression, "Unknown Error")


class MinusExpression(GenericExpression):

    def parse(self):
        idx = self.expression.find(const.MINUS)

        self.left = Expression(self.expression[0:idx])
        self.right = Expression(self.expression[idx + 1 :])

    def eval(self, state):
        try:
            return self.left.eval(state) - self.right.eval(state)
        except EvaluationError:
            print(self.expression, "Unknown Error")


class MulExpression(GenericExpression):

    def parse(self):
        idx = self.expression.find(const.MULTIPLY)

        self.left = Expression(self.expression[0:idx])
        self.right = Expression(self.expression[idx + 1 :])

    def eval(self, state):
        try:
            return self.left.eval(state) * self.right.eval(state)
        except EvaluationError:
            print(self.expression, "Unknown Error")


class DivExpression(GenericExpression):

    def parse(self):
        idx = self.expression.find(const.DIVIDE)

        self.left = Expression(self.expression[0:idx])
        self.right = Expression(self.expression[idx + 1 :])

    def eval(self, state):
        try:
            return self.left.eval(state) / self.right.eval(state)
        except EvaluationError:
            print(self.expression, "Unknown Error")


class Expression(object):

    def __init__(self, expression):
        self.expression = expression
        self.expr_type = None

        self.parse()

    def parse(self):

        add_index = self.expression.find(const.PLUS)
        sub_index = self.expression.find(const.MINUS)

        if add_index == -1:
            add_index = infinity
        if sub_index == -1:
            sub_index = infinity

        if add_index == 0 or sub_index == 0:
            self.expr_type = Factor(self.expression)
        elif add_index < sub_index:
            self.expr_type = PlusExpression(self.expression)
        elif sub_index < add_index:
            self.expr_type = MinusExpression(self.expression)
        else:
            div_index = self.expression.find(const.DIVIDE)
            mul_index = self.expression.find(const.MULTIPLY)

            if mul_index == -1:
                mul_index = infinity
            if div_index == -1:
                div_index = infinity

            if mul_index < div_index:
                self.expr_type = MulExpression(self.expression)
            elif div_index < mul_index:
                self.expr_type = DivExpression(self.expression)
            else:
                self.expr_type = Factor(self.expression)

    def eval(self, state):
        try:
            return self.expr_type.eval(state)
        except EvaluationError:
            print(self.expression, "Unknown Error")
