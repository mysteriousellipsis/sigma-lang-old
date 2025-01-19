from error import *
from expression import *
from keywords import *
import const
            
class Assignment(object):
    '''
    handles assignment statements
    '''
    
    def __init__(self, statement):
        self.statement = statement
        self.lhs = None
        self.rhs = None

        self.parse()
        
    def parse(self):
        '''
        parses assignment statements:
        splits up into left and right
        throws an error when 
        '''
        count = self.statemnent.count(const.ASSIGNMENT_OPERATOR)
        if count == 1:
            # split the statement into the left and right of the equal sign
            index = self.statement.index('=')
            self.lhs = self.statement[0:index]
            self.rhs = self.statement[index+1:]
            
            if self.lhs == '':
                raise AssignmentError(self.statement, "you need to assign a name to your variable!")
            
            if self.lhs[0].isdigit():
                raise AssignmentError(self.statement, "variable cannot begin with a number!!")
            
            # evaluate right hand side
            self.rhs = Expression(self.rhs)
            
            return True
        
        elif count == 0:
            raise AssignmentError(self.statement, f"you need to use '{const.ASSIGNMENT_OPERATOR}' to assign a variable!")
        
        else:
            raise AssignmentError(self.statement, "more than one assignment operator...")
    
    def eval(self, state):
        try:
            # assigns lhs to rhs
            state[self.lhs] = self.rhs.eval(state)
        
        except EvaluationError:
            print(self.statement, "unknown error :(")