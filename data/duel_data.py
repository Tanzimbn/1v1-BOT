import pandas as pd

DUEL_DB = "data/duels.csv"

def duel_exists(user_id: int) -> bool:
    df = pd.read_csv(DUEL_DB)
    if ((df["user1"] == user_id) | (df["user2"] == user_id)).any():
        return True
    else :
        return False

def new(uid1: int, uid2: int, rating: int, tag: str):
    df = pd.read_csv(DUEL_DB)
    new_duel = pd.DataFrame([{"user1": uid1, "user2": uid2, "rating": rating, "tag": tag}])
    df = pd.concat([df, new_duel])
    df.to_csv(DUEL_DB, index=False)

def get_duel_details( user_id: int):
    df = pd.read_csv(DUEL_DB)
    if (df["user1"] == user_id).any():
        return df.loc[df["user1"] == user_id].to_dict("records")[0]
    else:
        return df.loc[df["user2"] == user_id].to_dict("records")[0]

def drop(user_id: int):
    """Drop the challenge if it exists and is not ongoing"""
    df = pd.read_csv(DUEL_DB)
    df = df.loc[((df["user1"] != user_id) & (df["user2"] != user_id))]
    df.to_csv(DUEL_DB, index=False)

def duel_start(uid: int, contestId: int, index: str, start: int):
    """Adds problem and time to the duel"""
    df = pd.read_csv(DUEL_DB)
    df.loc[
        ((df["user1"] == uid) | (df["user2"] == uid)), ["contestId", "index", "start"]
    ] = [contestId, index, start]
    df.to_csv(DUEL_DB, index=False)

def duel_is_ongoing(uid: int) -> bool:
    df = pd.read_csv(DUEL_DB)
    return (
            duel_exists(user_id=uid)
            and str(df.loc[((df["user1"] == uid) | (df["user2"] == uid)), "start"].to_list()[0])
            != "nan"
        )
        


# print(duel_is_ongoing(1179623913639137290))