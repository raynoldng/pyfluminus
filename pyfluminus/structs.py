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

