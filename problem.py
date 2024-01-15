import random

from data import handle_data
from api import cf_api

def give_problem(uid1: int, uid2: int, rating: int, tag: str):
    handle1 = handle_data.user_handle(uid1)
    handle2 = handle_data.user_handle(uid2)
    prob1 = cf_api.all_ac_problem(handle1)
    prob2 = cf_api.all_ac_problem(handle2)
    cancel_prob = prob1.union(prob2)
    problems = list(cf_api.all_problem(rating=rating, tag=tag))
    random.shuffle(problems)
    for prob in problems:
        if prob in cancel_prob:
            continue
        return prob
    return (-1, -1, -1)

def random_problem(rating: int, tag: str):
    problems = list(cf_api.all_problem(rating=rating, tag=tag))
    random.shuffle(problems)
    return problems[0]

# contestId, index, _ = give_problem(722076634257162271,1179623913639137290,900)
# print(random_problem(800, "implementation"))