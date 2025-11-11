import json
from pathlib import Path

#---------------------------------------------------#
# Data model                                        #
#---------------------------------------------------#

class FileDetail:
    """
        One fw source/header file
        holds file path and components by kind
    """
    def __init__(self, path):
        self.path = path
        self.components = {
            "functions": [],
            "structs": [],
            "enums": [],
            "macros": [],
            "includes": [],
            #include bodies with function name as keys
        }

        def to_dic(self):
            return {
                "path": self.path,
                "components": self.components
            }

        @staticmethod
        def from_dic(d):
            file_detail = FileDetail(d["path"])
            components = d.get("componenets", {})
            for k in ["functions", "structs", "enums", "macros", "includes"]:
                file_detail.components[k] = list(components.get(k, []))
            return file_detail

class ComponentDetail:
    """
        One component from [function, structs, enemus, macros, indluces...]
        Stores defn site, body text, and reference to other symboles
    """
    def __init__(self, comp_name, kind, file_path, line, body, references=None):
        self.comp_name = comp_name      # InitAclk
        self.kind = kind                # "function"
        self.file_path = file_path      # ""mp1/src/app/aclk_dpm.h" FileDetail.path
        self.line = int(line)
        self.body = body
        self.references - list(references or [])

    def to_dict(self):
        return {
            "comp_name": self.comp_name,
            "kind": self.kind,
            "file_path": self.file_path,
            "line": self.line,
            "body": self.body,
            "references": self.references
        }

    @staticmethod
    def from_dict(d):
        return ComponentDetail(
            d["name"],
            d["kind"],
            d["file"],
            d.get("line", 0),
            d.get("body", ""),
            d.get("references", [])
        )
