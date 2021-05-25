def resource(label, wTime, wInco, nNodes=30):
    """
    Checks if a label is resource feasible.
    """
    for i in label["Visit"]:
        if i < 0 or i > 1:
            return False
    if label['Pair'] != 0 and label['Path'][-1] == nNodes:
        return False
    return label["Time"] <= wTime and label["Inco"] <= wInco
