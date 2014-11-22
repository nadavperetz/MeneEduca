from random import shuffle
from timeout import timeout, TimeoutError
from math import factorial


def bigger_groups_number(npeople, ngroups):
    return npeople % ngroups


def smaller_groups_number(npeople, ngroups):
    return ngroups - npeople % ngroups


def bigger_groups_size(npeople, ngroups):
    return npeople // ngroups + 1


def smaller_groups_size(npeople, ngroups):
    return npeople // ngroups


def bruteforce_group_formation(people, ngroups):
    groups = []
    for i in range(ngroups):
        groups.append([])

    return bruteforce_group_formation2(people, groups, 0)[1]


def bruteforce_group_formation2(people, groups, count):
    npeople = len(people)
    ngroups = len(groups)

    bigger_number = bigger_groups_number(npeople, ngroups)
    smaller_number = smaller_groups_number(npeople, ngroups)
    bigger_size = bigger_groups_size(npeople, ngroups)
    smaller_size = smaller_groups_size(npeople, ngroups)

    best_solution = (0.0, None)

    # base case - all people have been added to a group
    if count == len(people):
        groups_copy = []
        for group in groups:
            groups_copy.append(list(group))
        return (rate_formation(groups), groups_copy)

    # takes the first person
    person = people[count]

    # tries to put the person in the bigger groups
    for i in xrange(bigger_number):

        # avoids groups that are already full
        if len(groups[i]) >= bigger_size:
            continue

        groups[i].append(person)
        sol = bruteforce_group_formation2(people, groups, count + 1)
        if sol[0] > best_solution[0]:
            best_solution = sol
        groups[i].pop()

        # avoids adding the person to several empty groups
        if len(groups[i]) == 0:
            break

    # tries to put the person in the smaller groups
    for i in xrange(bigger_number, smaller_number + bigger_number):

        # avoids groups that are already full
        if len(groups[i]) >= smaller_size:
            continue

        groups[i].append(person)
        sol = bruteforce_group_formation2(people, groups, count + 1)
        if sol[0] > best_solution[0]:
            best_solution = sol
        groups[i].pop()

        # avoids adding the person to several empty groups
        if len(groups[i]) == 0:
            break

    return best_solution


def rate_group(group):
    ntraits = len(grop[0].get_traits())
    max_traits = [0.0] * ntraits
    min_traits = [1.0] * ntraits

    if len(group) == 1:
        return 1.0

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
        rate *= rate_group(group)
    rate **= (1.0 / len(groups))

    return rate


@timeout(10)
def random_group_formation(people, ngroups):
    npeople = len(people)
    best_score = 0.0
    best_formation = None

    try:
        tmp = list(people)

        while True:
            shuffle(tmp)
            formation = stupid_group_formation(tmp, ngroups)
            score = rate_formation(formation)

            if score > best_score:
                best_score = score
                best_formation = formation

    except TimeoutError:
        pass

    # gives a sorted answer (not required, but nice)
    bigger_number = bigger_groups_number(npeople, ngroups)
    smaller_number = smaller_groups_number(npeople, ngroups)
    for group in best_formation:
        group.sort()
    best_formation = sorted(best_formation[0 : bigger_number]) + sorted(best_formation[bigger_number : bigger_number + smaller_number])

    return best_formation


def stupid_group_formation(people, ngroups):
    npeople = len(people)

    bigger_number = bigger_groups_number(npeople, ngroups)
    smaller_number = smaller_groups_number(npeople, ngroups)
    bigger_size = bigger_groups_size(npeople, ngroups)
    smaller_size = smaller_groups_size(npeople, ngroups)

    bigger_groups = []
    smaller_groups = []

    for x in range(bigger_number):
        bigger_groups.append(people[(x * bigger_size):((x + 1) * bigger_size)])

    for x in range(smaller_number):
        smaller_groups.append(people[x * smaller_size +
                                     bigger_number * bigger_size :
                                     (x + 1) * smaller_size +
                                     bigger_number * bigger_size])

    return bigger_groups + smaller_groups


def total_solutions(npeople, ngroups):
    bigger_number = bigger_groups_number(npeople, ngroups)
    smaller_number = smaller_groups_number(npeople, ngroups)
    bigger_size = bigger_groups_size(npeople, ngroups)
    smaller_size = smaller_groups_size(npeople, ngroups)

    ans = factorial(npeople)
    ans //= factorial(smaller_size) ** smaller_number
    ans //= factorial(bigger_size) ** bigger_number
    ans //= factorial(bigger_number) * factorial(smaller_number)

    return ans


def smart_group_formation(people, ngroups):
    npeople = len(people)

    if total_solutions(npeople, ngroups) > 500000:
        return random_group_formation(people, ngroups)
    else:
        return bruteforce_group_formation(people, ngroups)
