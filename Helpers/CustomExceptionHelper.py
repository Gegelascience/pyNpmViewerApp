

class UnpublishedPackage(Exception):

    def __init__(self, packageName:str,message:str ="Package déplublié") -> None:
        self.packageName = packageName
        self.message = message
        super().__init__(self.message)