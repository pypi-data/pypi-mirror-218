"""
This test file is supposed to parse variables including scopes from AST.


Example:

Their usages could be searched without parsing the names first.
    module.class.method.variable
    module.module.function.variable

Definition creates a scope.
Usage increases usages of scope. Corner case is when a closure uses variables from another scope.
    Its hard to distinguish from which scope the variable is taken (is it closures or global space variable).


def hello_world():
    hello = "vienas"
    def closure():
        print(hello)


The solution is to use sequential analysis: if name is not defined search for it in higher scopes.
    Module scope is the highest one, hence the class function and variable names should be separated using different notation.


module.module notation:
    . <- folows a module
    >variable
    :function / method
    @class



How should this be done:
    feature_version=(3, 11)
"""

import ast
from typing import Dict
from unittest import TestCase
from inspect import cleandoc as d


ScopedVarNameStr = str
OccourenciesInt = int


class ParsingTests(TestCase):
    # TODO: What edge-cases are not resolved by the Vulture and other static checkers:
    # https://programming.dev/comment/464586

    # It seems that all these cases are already solved by the Vulture.
    #   I should take their core and improve the interface.

    def get_ast(self, code: str) -> str:
        return ast.dump(ast.parse(d(code)), indent=1)

    def parse_variables(self, code_ast: str) -> Dict[ScopedVarNameStr, OccourenciesInt]:
        """Notations used in the name by the parser:
            . <- module
            > <- variable / attribute
            : <- function / method
            @ <- class
        """
        return {}

    def test_variable_parsing(self):
        code = """
            foo = None
            print(foo)
        """
        code_ast = self.get_ast(code)
        variables = self.parse_variables(code_ast)
        assert variables == {
            ">foo": 2,
        }

    def test_function_parsing(self):
        code = """
            def foo():
                pass
            print(foo)
        """
        code_ast = self.get_ast(code)
        variables = self.parse_variables(code_ast)
        assert variables == {
            ":foo": 2,
        }

    def test_variable_in_function_parsing(self):
        code = """
            def foo():
                bar = None
            print(foo)
        """
        code_ast = self.get_ast(code)
        variables = self.parse_variables(code_ast)
        assert variables == {
            ":foo": 2,
            ":foo>bar": 1
        }

    def test_class_parsing(self):
        code = """
            class Foo:
                pass
            print(Foo())
        """
        code_ast = self.get_ast(code)
        variables = self.parse_variables(code_ast)
        assert variables == {
            "@Foo": 2,
        }

    def test_inheritance_parsing(self):
        code = """
            class Base:
                bar = None

            class Foo(Base):
                pass
            print(Foo().bar)
        """
        code_ast = self.get_ast(code)
        variables = self.parse_variables(code_ast)
        assert variables == {
            "@Base": 2,
            "@Foo": 2,
            "@Base>bar": 2,  # Usages in all subclasses should be counted
        }

    def test_method_and_attribute_parsing(self):
        code = """
            class Foo:
                bar = None

                def __init__(self):
                    self.spam = None

                def eggs(self):
                    pass
            print(Foo())
        """
        code_ast = self.get_ast(code)
        variables = self.parse_variables(code_ast)
        assert variables == {
            "@Foo": 2,
            "@Foo>bar": 1,
            "@Foo:__init__": 1,  # TODO: should be filtered out as reserved magic method
            "@Foo>spam": 1,
            "@Foo:eggs": 1,
        }

    def test_closure_parsing(self):
        code = """
            def hello_world():
                hello = "vienas"
                def closure():
                    print(hello)
        """
        code_ast = self.get_ast(code)
        variables = self.parse_variables(code_ast)
        assert variables == {
            "hello_world.hello": 2,
            "hello_world.closure": 1
        }

    def test_variable_in_walrus_expression_parsing(self):
        code = """
            if name := "hello":
                pass
        """
        code_ast = self.get_ast(code)
        variables = self.parse_variables(code_ast)
        assert variables == {
            ">name": 1,
        }
