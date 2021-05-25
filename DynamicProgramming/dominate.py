def dominate(l):
    """
    Checks if a given label, l, is dominated
    """
    NumberDominated = []
    for i in range(len(l) - 1):
        if l[-1]["Path"][-1] == l[i]["Path"][-1]:
            if l[-1]["Cost"] == l[i]["Cost"] and l[-1]["Time"] == l[i]["Time"] and l[-1]["Inco"] == l[i][
                "Inco"] and check_visits(l[i], l[-1]) and check_pair(l[i], l[-1]):
                l[-1]["Done"] = True
                NumberDominated.append(len(l) - 1)
                break
            elif l[-1]["Cost"] <= l[i]["Cost"] and l[-1]["Time"] <= l[i]["Time"] and l[-1]["Inco"] <= l[i][
                "Inco"] and check_visits(l[-1], l[i]) and check_pair(l[i], l[-1]):

                if not l[i]["Done"]:
                    l[i]["Done"] = True
                    NumberDominated.append(i)
            elif l[-1]["Cost"] >= l[i]["Cost"] and l[-1]["Time"] >= l[i]["Time"] and l[-1]["Inco"] >= l[i][
                "Inco"] and check_visits(l[i], l[-1]) and check_pair(l[i], l[-1]):
                l[-1]["Done"] = True
                NumberDominated.append(len(l) - 1)
                break
    return NumberDominated


def check_visits(label1, label2):
    """
    Checks if label2 has visited more cities
    than label2 (according to the resource).
    Used to enforce elementary paths.
    """
    for i in range(len(label1['Visit'])):
        v1 = label1['Visit'][i]
        v2 = label2['Visit'][i]
        if v1 > v2:
            return False
    return True


def check_pair(label1, label2):
    """
    Checks if both 'Pair' resources are the same for label1 and label2.
    Used to enforce pairing.
    """
    return label1['Pair'] == label2['Pair']
