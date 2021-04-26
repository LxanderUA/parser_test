import enum


class Operators(enum.Enum):
    """
    Math operators list
    ('symbol' :str , priority:int 0-9 higher is bigger)
    """
    PLUS = ('+', 1)
    MINUS = ('-', 1)
    ASTERISK = ('*', 2)
    SLASH = ('/', 2)
    POWER = ('^', 3)
    PARENTHESIS_LEFT = ('(', 0)
    PARENTHESIS_RIGHT = (')', 0)

    def __init__(self, sign, priority):
        self.sign = sign
        self.priority = priority

    @staticmethod
    def is_math_operator(char):
        if char in [item.sign for item
                    in [Operators.PLUS, Operators.MINUS, Operators.ASTERISK, Operators.SLASH, Operators.POWER]]:
            return True
        return False

    @staticmethod
    def get_priority(char):
        for item in Operators:
            if item.sign == char:
                return item.priority
        return 0


class Stack:
    """
    push(item) - move item to stack
    pop - get item from stack
    peek - look at upper item
    """

    def __init__(self):
        self.__stack = list()

    def push(self, item):
        self.__stack.append(item)

    def pop(self):
        if len(self.__stack) > 0:
            return self.__stack.pop()
        return None

    def peek(self):
        if len(self.__stack) > 0:
            return self.__stack[len(self.__stack) - 1]
        return None

    def __len__(self):
        return len(self.__stack)

    def __str__(self):
        return str(self.__stack)


class Parser:
    """
    on init takes str with int digits, math operators and parenthesis
    Method .execute() return result of expression
    """
    def __init__(self, code: str):
        self.__code = '(' + code.strip() + ')'
        if not self._checkparenthesis(self.__code):
            raise Exception('Error on check parenthesis')

    def _checkparenthesis(self, code):
        par = Stack()
        for char in code:
            if char == Operators.PARENTHESIS_LEFT.sign:
                par.push(Operators.PARENTHESIS_LEFT)
            elif char == Operators.PARENTHESIS_RIGHT.sign:
                if len(par) > 0:
                    par.pop()
                else:
                    return False
        if len(par) == 0:
            return True
        return False

    def execute(self):
        return self._parse(self.__code)

    def _parse(self, code):
        digits = Stack()
        operation = Stack()
        digit = ''
        priority = 0
        for char in code:
            if char.isdigit():
                digit += char
                continue
            elif digit != '':
                digits.push(int(digit))
                digit = ''
            if char == Operators.PARENTHESIS_LEFT.sign:
                priority += 10
            elif char == Operators.PARENTHESIS_RIGHT.sign:
                self._solve(digits, operation, priority)
                priority -= 10
            elif Operators.is_math_operator(char):
                if len(operation) > 0 and priority + Operators.get_priority(char) < operation.peek()[1]:
                    self._solve(digits, operation, priority + Operators.get_priority(char))
                operation.push((char, priority + Operators.get_priority(char)))
        return digits.pop()


    def _solve(self, digits, operation, priority):
        while len(operation) > 0 and operation.peek()[1] > priority:
            operator = operation.pop()
            elem2 = digits.pop()
            elem1 = digits.pop()
            operation_tmp = Stack()
            digits_tmp = Stack()
            while len(operation) > 0 and operation.peek()[1] == operator[1]:
                operation_tmp.push(operator)
                digits_tmp.push(elem2)
                operator = operation.pop()
                elem2 = elem1
                elem1 = digits.pop()
            while len(operation_tmp) >= 0:
                if operator[0] == Operators.PLUS.sign:
                    elem1 += elem2
                elif operator[0] == Operators.MINUS.sign:
                    elem1 -= elem2
                elif operator[0] == Operators.ASTERISK.sign:
                    elem1 *= elem2
                elif operator[0] == Operators.SLASH.sign:
                    elem1 //= elem2
                elif operator[0] == Operators.POWER.sign:
                    elem1 **= elem2
                if len(operation_tmp) == 0:
                    break
                elem2 = digits_tmp.pop()
                operator = operation_tmp.pop()
            digits.push(elem1)


my = Parser('1+2*(2+10)/(5-2^2)-12+3^2*2')
print(my.execute())
