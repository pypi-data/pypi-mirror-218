"""Код должен быть по PEP8 чтобы все работало!"""

from typing import List


class CodeParse:
    def __init__(self, file):
        self._file = file
        self.code_strings: List[str] = file.read().split("\n")

        self.imports_parse = None
        self.functions_parse = None
        self.classes_parse = None

    def search(self, text: str) -> List:
        return [(num, string) for num, string in enumerate(self.code_strings) if text in string]
    
    def _get_imports(self, code_strings):
        pass

    def add_code_line(self, string: str, index: int = 0) -> None:
        self.code_strings.insert(index, string)

    def add_import_from(self, from_: str, import_: str) -> None:
        self.add_code_line(f"from {from_} import {import_}")

    def add_import_from_as(self, from_: str, import_: str, as_: str) -> None:
        self.add_code_line(f"from {from_} import {import_} as {as_}")

    def add_import(self, import_: str) -> None:
        self.add_code_line(f"import {import_}")

    def add_import_as(self, import_: str, as_: str) -> None:
        self.add_code_line(f"import {import_} as {as_}")

    def append_in_lists(self, var: str, value: str):
        strings = self._search(var + " = ")

        for num, string in strings:
            var_values = string[string.find("[")+1:string.find("]")]
            self.code_strings[num] = f"{var} = [{var_values}, {value}]"

        return self.code_strings

    def save(self):
        self._file.seek(0)
        self._file.write("\n".join(self.code_strings))
