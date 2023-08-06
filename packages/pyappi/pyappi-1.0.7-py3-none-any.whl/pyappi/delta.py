def changes_since(document, tsx):
    result = {}

    def _recursive_changes(current):
        vmt,cmt = (current.get("_cmt",-1),current.get("_vmt",-1))

        if cmt <= tsx or vmt <= tsx:
            return None

        delta = {}

        if cmt > tsx:
            for key,value in current.items():
                if not isinstance(key,dict):
                    continue

                _delta = _recursive_changes(value)
                if _delta:
                    delta[key] = _delta

        if vmt > tsx:
            for key,value in current.items():
                if isinstance(key,dict):
                    continue

                delta[key] = value
            
        return delta

    result = _recursive_changes(document.__dict__["__document"])

    return result

