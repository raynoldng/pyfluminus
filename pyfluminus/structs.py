from typing import List, Dict

class Module:
    def __init__(self, id: str, code: str, name: str, teaching: bool, term: str):
        """
        * `:id` - id of the module in the LumiNUS API
        * `:code` - code of the module, e.g. `"CS1101S"`
        * `:name` - name of the module, e.g. `"Programming Methodology"`
        * `:teaching?` - `true` if the user is teaching the module, `false` if the user is taking the module
        * `:term` - a string identifier used by the LumiNUS API to uniquely identify a term (semester), e.g. `"1820"`
        is invalid
        """
        self.id = id
        self.code = code
        self.name = name
        self.teaching = teaching
        self.term = term

    def __eq__(self, other):
        return (
            self.id == other.id
            and self.code == other.code
            and self.name == other.name
            and self.teaching == other.teaching
            and self.term == other.term
        )


class Lesson:
    def __init__(self, id: str, name: str, week: str, module_id: str):
        """
        Provides an abstraction over a lesson plan in LumiNUS, and operations possible on them using
        LumiNUS API.

        Struct fields:
        * `:id` - id of the lesson plan
        * `:name` - name of the lesson plan
        * `:week` - which week the lesson plan is for
        * `:module_id` - the module id to which the lesson plan is from.
        """
        self.id = id
        self.name = name
        self.week = week
        self.module_id = module_id


class File:
    def __init__(
        self,
        id: str,
        name: str,
        directory: bool,
        children: List,
        allow_upload: bool,
        multimedia: bool,
    ):
        """
        Provides an abstraction over a file/directory in LumiNUS, and operations possible on them using
        LumiNUS API.

        Struct fields:
        * `:id` - id of the file
        * `:name` - the name of the file
        * `:directory?` - whether this file is a directory
        * `:children` - `nil` indicated the need to fetch, otherwise it contains a list of its children.
        if `directory?` is `false`, then this field contains an empty list.
        * `:allow_upload?` - whether this is a student submission folder.
        * `:multimedia?` - whether this is a multimedia file.
        """
        self.id = id
        self.name = name
        self.directory = directory
        self.children = children
        self.allow_upload = allow_upload
        self.multimedia = multimedia

    @classmethod
    def from_module(cls, auth: Dict, module: Module):
        pass
