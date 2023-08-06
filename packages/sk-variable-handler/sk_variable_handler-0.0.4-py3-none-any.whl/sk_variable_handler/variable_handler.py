import regex as re

import json


class VariableHandler:
    def __init__(self):
        self.calculator = None

    def set_calculator(self, calculator):

        self.calculator = calculator

    def remove_comments(self, declarations):

        single_line_comment = r'\#.*+($)?'
        declarations = re.sub(single_line_comment, '', declarations)

        multiline_comment = r'\/\*[\s\S]*?\*\/'
        declarations = re.sub(multiline_comment, '', declarations)

        extra_space = r'\n\s*'
        declarations = re.sub(extra_space, '', declarations)

        declarations = declarations.strip()
        return declarations

    def declare(self, declarations):

        pattern = '\$[^=]+=[^;]+'

        declarations = re.findall(pattern, declarations)
        declaration_list = {}

        for declaration in declarations:
            variable, expression = re.split(r'\s*(\$[^=]+)\s*=\s*', declaration)[1:]
            variable = variable.replace(' ', '')
            if re.search(re.escape(variable) + r'(\s|\b)', expression):
                if type(declaration_list[variable]) == list:
                    declaration_list[variable] = declaration_list[variable] + [expression]
                else:
                    declaration_list[variable] = [declaration_list[variable]] + [expression]
            else:
                declaration_list[variable] = expression
        return declaration_list

    def solve_expressions(self, declaration_list):

        temp = {}
        temp2 = {}
        for variable, expression in declaration_list.items():
            if '$' not in expression:
                value = str(self.calculator.evaluate(str(expression)))
                if not re.search(r'Unsupported', str(value)):
                    try:
                        temp[variable] = eval(value)
                    except:
                        temp[variable] = value
                else:
                    try:
                        temp[variable] = eval(expression)
                    except:
                        temp[variable] = expression

        declaration_list.update(temp)
        temp = {}

        for key, value in self.declaration_list.items():

            if '$' not in str(value):

                value = str(value)
                pattern = r'eval(\((?>[^()]|(?1))*\))'
                expression_list = [item for index, item in enumerate(re.findall(pattern, value)) if item != ' ']

                for expression in expression_list:
                    expression_value = str(self.calculator.evaluate(expression))
                    pattern = r'eval' + re.escape(expression)
                    value = re.sub(pattern, expression_value, value)
                try:
                    temp[key] = eval(value)
                except:
                    temp[key] = value

        declaration_list.update(temp)

        return declaration_list

    def evaluate_expression(self, expression):
        value = ''

        value = str(self.calculator.evaluate(str(expression)))
        if '[' not in value and not '{' in value:
            return value
        try:
            expression = eval(expression)
        except:
            pass
        return expression

    def solve_nested_variables(self, declaration_list):

        resolved_variables = {}
        nested_variables = {}

        for variable, expression in declaration_list.items():
            if '$' not in str(expression):
                resolved_variables[variable] = expression
            else:
                nested_variables[variable] = expression

        temp_resolved = {}

        nested = True

        while nested_variables:
            nested = False
            for variable, expression in nested_variables.items():
                for resolved_variable, resolved_expression in resolved_variables.items():
                    pattern = re.escape(resolved_variable) + r'(?>=\s|\b|$)'
                    if re.search(pattern, expression):
                        try:
                            resolved_expression = eval(str(resolved_expression))
                        except:
                            resolved_expression = f"'{resolved_expression}'"

                        expression = re.sub(pattern, str(resolved_expression), str(expression))

                if '$' not in expression:
                    temp_resolved[variable] = self.evaluate_expression(expression)
                    nested = True

            for variable, expression in temp_resolved.items():
                try:
                    resolved_variables[variable] = eval(str(expression))
                except:
                    resolved_variables[variable] = expression

                del nested_variables[variable]
            temp_resolved = {}

            if not nested:
                break
        declaration_list.update(resolved_variables)

        return declaration_list

    def resolve_recursive_variables(self, declaration_list):
        resolved_variables = {}
        recursive_variables = {}
        temp = {}

        for variable, expression in declaration_list.items():

            if re.search(re.escape(variable) + r'(\s|\b)', str(expression)):
                recursive_variables[variable] = expression
            else:
                resolved_variables[variable] = expression

        for recursive_variable, recursive_expression in recursive_variables.items():

            recursive_reverse_value = recursive_expression[::-1]
            value = recursive_reverse_value[0]
            for item in recursive_reverse_value[1:]:
                value = re.sub(re.escape(recursive_variable) + r'(\s|\b)', '(' + item + ')', value)
            try:
                temp[recursive_variable] = eval(self.evaluate_expression(value))
            except:
                temp[recursive_variable] = self.evaluate_expression(value)

        resolved_variables.update(temp)

        return resolved_variables

    def get_result(self, declarations):

        declarations = self.remove_comments(declarations)

        self.declaration_list = self.declare(declarations)

        self.declaration_list = self.solve_expressions(self.declaration_list)

        self.declaration_list = self.resolve_recursive_variables(self.declaration_list)
        self.declaration_list = self.solve_nested_variables(self.declaration_list)

        return self.declaration_list
