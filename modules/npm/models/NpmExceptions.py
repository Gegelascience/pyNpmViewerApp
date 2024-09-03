

class UnpublishedPackage(Exception):

    def __init__(self, packageName:str) -> None:
        self.packageName = packageName
        self.message = "Package déplublié"
        super().__init__(self.message)