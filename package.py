class Package():
    
    def __init__(self, id: str() = "?", text: str() or [str()] = "",
                 error: bool() = False, lost: bool() = False,
                 npackages: int() = 1, multpackages: bool() = False, passkey: str() = "3301"):
        self.id = id
        self.text = text
        self.error = error
        self.lost = lost
        self.npackages = npackages
        self.multpackages = multpackages
        self.passkey = passkey