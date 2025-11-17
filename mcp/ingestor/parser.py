import json
from pathlib import Path

#---------------------------------------------------#
# Data model                                        #
#---------------------------------------------------#
class ComponentDetail:
    """
    One component defined inside a file.

    Examples:
      - a function (kind="function")
      - a struct  (kind="struct")
      - an enum   (kind="enum")
      - a macro   (kind="macro")

    Fields:
      name       : component name (e.g. "InitAclk")
      kind       : "function" | "struct" | "enum" | "macro"
      file_path  : path of the file where it is defined
      line       : line number in that file (1-based)
      body       : signature or full definition text
      references : list of other component names it uses/calls
    """

    def __init__(self, name, kind, file_path, line, body, references=None):
        self.name       = name
        self.kind       = kind
        self.file_path  = file_path
        self.line       = int(line)
        self.body       = body
        self.references = list(references or [])

    def to_dict(self):
        return {
            "name":       self.name,
            "kind":       self.kind,
            "file_path":  self.file_path,
            "line":       self.line,
            "body":       self.body,
            "references": self.references
        }

    @staticmethod
    def from_dict(d):
        return ComponentDetail(
            d["name"],
            d["kind"],
            d["file_path"],
            d.get("line", 0),
            d.get("body", ""),
            d.get("references", [])
        )

class FileDetail:
    """
    One firmware source/header file.

    Fields:
      path       : file path (relative under firmware root)
      includes   : list of other file paths this file includes
      components : list of ComponentDetail objects defined in this file
    """
    
    def __init__(self, path):
        self.path = path
        self.includes = []
        self.componenets = []
        
    def add_include(self, include_path):
        """ Populate source file with include (paths)"""
        if include_path not in self.includes:
            self.includes.append(include_path)
            
    def add_component(self, component):
        """Populate source file with components (of componentdetail instance)"""
        for existing in self.componenets:
            if ((existing.name == component.name) and (existing.kind == component.kind)):
                return 
        self.componenets.append(component)
        
    def to_dict(self):
        """
        Convert to a JSON-friendly dict.
        Components are stored as a list of dicts.
        """
        return {
            "path":      self.path,
            "includes":  self.includes,
            "components": [c.to_dict() for c in self.components]
        }

    @staticmethod
    def from_dict(d):
        fd = FileDetail(d["path"])
        fd.includes = list(d.get("includes", []))
        comps = d.get("components", [])
        for c in comps:
            fd.components.append(ComponentDetail.from_dict(c))
        return fd
    
class ParsedFirmware:
    """"
    Central Container:
        files   : path -> FileDetails instance of FileDetails with path
        components: FileDetails
    """
    def __init__(self):
        self.files = {}
        self.components = {}
        
    def add_file(self, file_path:str):
        """ Create a FileDetail if missing and return it """
        if file_path not in self.files:
            self.files[file_path] = FileDetail(file_path)
            print(f"Populated Files with {file_path}")
        return self.files[file_path]
    
    def add_file_include(self, file_path:str, include_name:str):
        fd = self.add_file(file_path)
        if include_name not in fd.components["includes"]:
            fd.components["includes"].append(include_name)
    
    def create_component(self, comp_name, kind, file_path, line, body, references=None):
        self.components[comp_name] = ComponentDetail(
            comp_name, kind, file_path, line, body, references
        )