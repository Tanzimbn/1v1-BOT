from os import path
import matplotlib.pyplot as plt
from datetime import datetime
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

def user_info(handle: str):
    params = {"handles": [handle]}
    return cf_query("user.info", params=params)[0]

def all_ac_problem(handle: str):
    params = {"handle": handle}
    submissions = cf_query("user.status", params=params)
    problems = set()
    for submission in submissions:
        problems.add((submission.get("contestId"), submission.get("problem").get("index"), submission.get("problem").get("name")))
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

def all_problem(rating: int, tag: str):
    params = {"tags": tag}
    problems = cf_query("problemset.problems", params)["problems"]
    select_prob = set()
    for _prob in problems:
        _rating = _prob.get("rating")
        if rating in [None, _rating]:
            select_prob.add((_prob.get("contestId"), _prob.get("index"), _prob.get("name")))
    return select_prob

def compiler_error_check(handle: str, contestId: int, index: str, submit_time: int):
    params = {"handle": handle, "from":'1', "count": '60'}
    submissions = cf_query("user.status", params)
    # print(submissions)
    for submission in submissions:
        if submission.get("verdict") == "COMPILATION_ERROR" and submission.get("contestId") == contestId and submission.get("problem").get("index") == index:
            creationTime = submission.get("creationTimeSeconds")
            if creationTime >= submit_time:
                return True
            
    return False

def rating_graph(handle: str):
    params = {"handle":handle}
    rating_changes = cf_query("user.rating", params)
    update_times = [datetime.fromtimestamp(change['ratingUpdateTimeSeconds']) for change in rating_changes]
    new_ratings = [change['newRating'] for change in rating_changes]

    plt.plot(update_times, new_ratings, label='New Rating', marker='o')
    
    plt.xlabel('Update Time')
    plt.ylabel('Rating')
    plt.title('Codeforces Rating Changes')
    plt.legend()
    plt.xticks(rotation=45)

    # Save the plot as an image file
    image_path = 'rating_plot.png'
    plt.savefig(image_path)
    plt.close()  
    return image_path


# print(rating_graph("tanzim_bn"))
# print(compiler_error_check("tanzim_bn", 4, "A", 1703223102))
# print(user_info("tanzim_bn")['handle'])
# print(all_problem(3500, "implementation"))
# print(all_ac_problem_detail("tanzim_bn"))
