#!/usr/bin/env python3

import ast
import astunparse


###############################################################################
# Patch functions
###############################################################################


def patch_ET_fromstring(node):
    """
    Replace `ET.fromstring()` with `etree.fromstring()`
    """
    if (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.value.id == "ET"
        and node.func.attr == "fromstring"
    ):
        # https://docs.python.org/3/library/ast.html#ast.Call
        return ast.Call(
            func=ast.Attribute(
                value=ast.Name(id="etree", ctx=ast.Load()),
                attr="fromstring",
                ctx=ast.Load(),
            ),
            args=node.args,
            keywords=node.keywords,
        )


def patch_ElementTree_import(node):
    """
    Replace `import xml.etree.ElementTree as ET` with `from lxml import etree`
    """
    if isinstance(node, ast.Import):
        # https://docs.python.org/3/library/ast.html#ast.ImportFrom
        return ast.ImportFrom(
            module="lxml",
            names=[ast.alias(name="etree", asname=None)],
            level=0,  # absolute import
        )


###############################################################################
# Patcher class
###############################################################################


class Patcher:
    """
    Apply a list of patch functions to a node
    """

    def __init__(self, patch_functions):
        self.patch_functions = patch_functions

    def patch(self, node):
        if not hasattr(node, "_fields"):
            return node

        for (name, field) in ast.iter_fields(node):
            if isinstance(field, list):
                for i in range(len(field)):
                    for patch_function in self.patch_functions:
                        updated_field = patch_function(field[i])
                        if updated_field:
                            field[i] = updated_field
                    self.patch(field[i])
            else:
                for patch_function in self.patch_functions:
                    updated_field = patch_function(field)
                    if updated_field:
                        setattr(node, name, updated_field)
                self.patch(field)


###############################################################################
# Main
###############################################################################

if __name__ == "__main__":
    patcher = Patcher(patch_functions=[patch_ET_fromstring, patch_ElementTree_import])

    with open("config.py", "r") as f:
        head = ast.parse(f.read())
        patcher.patch(head)

        with open("config-patched.py", "w") as config_patched_file:
            config_patched_file.write((astunparse.unparse(head)))
