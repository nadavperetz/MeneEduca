

def bigger_groups_number(npeople, ngroups):
    return npeople % ngroups


def smaller_groups_number(npeople, ngroups):
    return ngroups - npeople % ngroups


def bigger_groups_size(npeople, ngroups):
    return npeople // ngroups + 1


def smaller_groups_size(npeople, ngroups):
    return npeople // ngroups


def dfs_group_formation(people, ngroups):
    groups = []
    for i in range(ngroups):
        groups.append([])

    return dfs_group_formation2(len(people), people, groups)


def dfs_group_formation2(npeople, people, groups):
    bigger_number = bigger_groups_number(npeople, len(groups))
    smaller_number = smaller_groups_number(npeople, len(groups))
    bigger_size = bigger_groups_number(npeople, len(groups))
    smaller_size = smaller_groups_number(npeople, len(groups))

    best_solution = (0.0, None)

    # base of the recursion
    if not people:
        groups_copy = []
        for group in groups:
            groups_copy.append(list(group))
        return rate_formation(groups), list(groups_copy)

    # takes the first person
    person = people.pop()

    # tries to put the person in the bigger groups
    for i in range(bigger_number):
        if len(groups[i]) >= bigger_size:
            continue

        groups[i].append(person)
        sol = dfs_group_formation2(npeople, people, groups)
        if sol[0] > best_solution[0]:
            best_solution = sol
        groups[i].pop()

        if len(groups[i]) == 0:
            break

    # tries to put the person in the smaller groups
    for i in range(bigger_number, smaller_number + bigger_number):
        if len(groups[i]) >= smaller_size:
            continue

        groups[i].append(person)
        sol = dfs_group_formation2(npeople, people, groups)
        if sol[0] > best_solution[0]:
            best_solution = sol
        groups[i].pop()

        if len(groups[i]) == 0:
            break

    people.append(person)
    return best_solution


def rate_group(group):
    max_traits = [0.0, 0.0, 0.0, 0.0, 0.0]
    min_traits = [1.0, 1.0, 1.0, 1.0, 1.0]

    for person in group:
        traits = person.get_traits()

        for i in range(len(traits)):
            if traits[i] < min_traits[i]:
                min_traits[i] = traits[i]
            if traits[i] > max_traits[i]:
                max_traits[i] = traits[i]

    rate = 1.0
    for i in range(len(max_traits)):
        rate *= (max_traits[i] - min_traits[i])
    rate **= (1.0 / len(max_traits))
    return rate


def rate_formation(groups):
    rate = 1.0
    for group in groups:
        rate = rate * rate_group(group)
    rate **= (1.0 / len(groups))
    return rate