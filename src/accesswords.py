from enum import Enum

class AccessWords(Enum):
    access =        ["access",      "edit"]
    append =        ["append",      "edit"]
    change =        ["change",      "edit"]
    edit =          ["edit",        "edit"]
    examine =       ["examine",     "read"]
    manipulate =    ["manipulate",  "edit"]
    modify =        ["modify",      "edit"]
    read =          ["read",        "read"]
    see =           ["see",         "read"]
    update =        ["update",      "edit"]
    use =           ["use",         "edit"]
    view =          ["view",        "read"]
    write =         ["write",       "edit"]