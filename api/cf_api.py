from os import path

import requests

def cf_query(path: str, params=None):
    API_BASE_URL = "https://codeforces.com/api/"
    res = requests.get(url=API_BASE_URL + path, params=params)
    return res.json()["result"]

def handle_exists(handle: str):
    
    params = {"handles": [handle]}
    try:
        cf_query("user.info", params=params)
    except KeyError:
        return False
    return True

def all_ac_problem(handle: str):
    params = {"handle": handle}
    submissions = cf_query("user.status", params=params)
    problems = set()
    for submission in submissions:
        problems.add((submission.get("contestId"), submission.get("problem").get("index")))
    return problems

def all_ac_problem_detail(handle: str):
    params = {"handle": handle}
    submissions = cf_query("user.status", params=params)
    problems = dict()
    for submission in submissions:
        if submission.get("verdict") == "OK":
            prob = (
                submission.get("contestId"),
                submission.get("problem").get("index"),
            )
            creationTime = submission.get("creationTimeSeconds")
            problems[prob] = creationTime
    return problems

def all_problem(rating: int):
    problems = cf_query("problemset.problems")["problems"]
    select_prob = set()
    for _prob in problems:
        _rating = _prob.get("rating")
        if rating in [None, _rating]:
            select_prob.add((_prob.get("contestId"), _prob.get("index"), _prob.get("name")))
    return select_prob

# print(all_ac_problem_detail("tanzim_bn"))
