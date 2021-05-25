class Container:
    """
    Data oriented class for keeping track of the containers.
    """
    def __init__(self, id, weight):
        self.id = id
        self.weight = weight

    @staticmethod
    def sort_array_weight_descending(b):
        """
        Sorts array according to weight, descending.
        :param b: dictionary of Container objects
        :return: the sorted list
        """
        a = list(b.values())
        a = sorted(a, key=lambda c: c.weight,
                   reverse=True)
        return [container.id for container in a]

    @staticmethod
    def sort_array_weight_ascending(b):
        """
        Sorts array according to weight, ascending.
        :param b: dictionary of Container objects
        :return: the sorted list
        """
        a = list(b.values())
        a = sorted(a, key=lambda c: c.weight,
                   reverse=False)

        return [container.id for container in a]
