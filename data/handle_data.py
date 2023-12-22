import pandas as pd

HANDLES_DB = "data/handles.csv"


def set_or_update_handle(handle: str, uid: int):
    """Update handle if uid exists. Otherwise, add new handle"""
    df = pd.read_csv(HANDLES_DB)
    
    if (df["user_id"] == uid).any():
        df.loc[df["user_id"] == uid, "handle"] = handle
    else:
        new_handle_df = pd.DataFrame([{"user_id": uid, "handle": handle}])
        df = pd.concat([df, new_handle_df])
    df.to_csv(HANDLES_DB, index=False)

def handle_owner(handle: str):
    df = pd.read_csv(HANDLES_DB)
    id = df.loc[ df["handle"] == handle, "user_id"].to_list()
    return id

def all_user_info():
    df = pd.read_csv(HANDLES_DB)
    return df.values.tolist()

def uid_exists(user_id: int) -> bool:
    """Returns true if uid exists. Otherwise, false"""
    df = pd.read_csv(HANDLES_DB)
    return (df["user_id"] == user_id).any()

def user_handle(user_id: int) -> str:

    df = pd.read_csv(HANDLES_DB)
    handle = df.loc[df["user_id"] == user_id, "handle"].to_list()
    return handle[0]


# print(all_user_info())
# print(handle_owner("beszero"))
# print(user_handle(722076634257162271))