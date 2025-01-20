import re

from error import *
import const
import assign as ass
import ifttt as ifelse
import loop
import printer
import const


class CompoundStatement(object):

    def __init__(self, text):
        self.text = text
        self.statements = []

        self.parse()

    def parse(self):

        while self.text != "":
            if self.text[0:2] == const.IF_OPEN:
                self.parseIf()
            elif self.text[0:5] == const.WHILE_OPEN:
                self.parseWhile()
            elif self.text[0:4] == const.COMMENT_OPEN:
                self.parseComment()
            elif self.text[0:5] == const.PRINT:
                self.parsePrint()
            else:
                self.parseAssign()

    def parseIf(self):

        count = 0
        index = 0
        for i in range(len(self.text) - 1):
            if self.text[i : i + 2] == const.IF_OPEN:
                count += 1
            elif self.text[i : i + 2] == const.IF_CLOSE:
                count -= 1

            if count == 0:
                index = i
                break

        if index == None:
            raise IfElseError(
                self.text,
                f"number of {const.IF_OPEN} and {const.IF_CLOSE} are not the same :(",
            )
        else:
            try:
                ifstatement = ifelse.IfElse(self.text[0 : index + 2])
                self.statements.append(ifstatement)
            except IfElseError:
                print("Error in Parsing : ", self.text)

            if len(self.text) >= index + 3 and self.text[index + 2] == const.EOL_SYMBOL:
                self.text = self.text[index + 3 :]
            else:
                raise IfElseError(self.text, "no semicolon after fi...")

    def parseAssign(self):
        # Parsing Assignment Statement Block
        pos = self.text.find(const.EOL_SYMBOL)

        if pos == -1:
            raise ass.AssignmentError(self.text, "semicolon missing")

        statement = self.text[0:pos]
        self.text = self.text[pos + 1 :]

        try:
            ass_obj = ass.Assignment(statement)
            self.statements.append(ass_obj)
        except AssignmentError:
            print(statement, "assignment syntax error")

    def parseWhile(self):

        count = 0
        index = None
        for i in range(len(self.text) - 4):
            if i <= len(self.text) - 5 and self.text[i : i + 5] == const.WHILE_OPEN:
                count += 1
            elif self.text[i : i + 4] == const.DONE:
                count -= 1
            if count == 0:
                index = i
                break

        if index == None:
            raise LoopError(self.text, "Unbalanced 'while' and 'done'")
        else:
            try:
                loop_statement = loop.WhileStatement(self.text[0 : index + 4])
                self.statements.append(loop_statement)
            except LoopError:
                print("Error in Parsing Loop Statement: ", self.text)

            if len(self.text) >= index + 5 and self.text[index + 4] == const.EOL_SYMBOL:
                self.text = self.text[index + 5 :]
            else:
                raise LoopError(self.text, "Semi colon missing after 'done'")

    def parseComment(self):

        end_pos = self.text.find(const.COMMENT_CLOSE)

        if end_pos == -1:
            raise CommentError(self.text, "Unfinished Comment.")
        else:
            self.text = self.text[end_pos + 3 :]

    def parsePrint(self):

        close_pos = self.text.find(const.PARAN_CLOSE)

        if close_pos == -1:
            raise PrintError(self.text, "No Opening bracket at the end of statement.")
        else:
            try:
                print_statement = printer.PrintStatement(self.text[6:close_pos])
            except PrintError:
                print("Error in parsing pring statement : ", self.text)

            self.statements.append(print_statement)

            if len(self.text) >= close_pos + 2 and self.text[close_pos + 1] == const.EOL_SYMBOL:
                self.text = self.text[close_pos + 2 :]
            else:
                raise PrintError(
                    self.text, "Semi colon missing after the end of the statement"
                )

    def eval(self, state):
        try:
            for x in self.statements:
                x.eval(state)
        except EvaluationError:
            print(self.text, "Error in evaluation of Compound Statement")
