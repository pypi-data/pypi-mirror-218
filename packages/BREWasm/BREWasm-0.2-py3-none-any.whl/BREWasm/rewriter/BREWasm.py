from BREWasm.rewriter.change_binary import ChangeBinary


class BREWasm:

    def __init__(self, file_name: str):
        self.binary = ChangeBinary(file_name)
