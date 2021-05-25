class Vessel:
    """
    Data oriented class for the vessel.
    """
    def __init__(self, bay, stack, tier):
        self.nBays = bay
        self.nStacks = stack
        self.nTiers = tier
