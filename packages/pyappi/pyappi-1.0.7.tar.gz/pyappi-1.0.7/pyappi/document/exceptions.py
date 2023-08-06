class DocumentNotLocked(Exception):
    "Raised when access to a document is attempted outside of its lifetime."
    pass

class PathDoesntExist(Exception):
    "Raised when access to a document is attempted outside of its lifetime."
    pass

class ReadOnlyDocument(Exception):
    "Raised when access to a document is attempted outside of its lifetime."
    pass

class NoPrepopulatedObjects(Exception):
    "Raised when assigned objects have values or subkeys, as this bypasses the preprocessor."
    pass