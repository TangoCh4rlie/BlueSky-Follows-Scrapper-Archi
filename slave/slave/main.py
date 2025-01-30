'''
    The main thread to run the collection of followers.
    ENVIRONMENT VARIABLES :
     - SLAVE_ID
     - MASTER_URL
     - REDIS_HOSTNAME
     - OUTPUT_PATH
     - SEED (optionnal)
'''

import io
import logging
import time

import redis
from construct import Int32ul
import requests

from slave.constants import MASTER_URL, REDIS_HOSTNAME, \
    SLAVE_ID, VERTICE_ID_BIT_SIZE, OUTPUT_PATH, MAX_NB_TREATED

logging.basicConfig(level=logging.DEBUG)

mappings : dict[str, int] = {}
edges : set[tuple[int, int]] = set()

r : redis.Redis = redis.Redis(host=REDIS_HOSTNAME, port=6379, db=0)
start_point : int = SLAVE_ID << VERTICE_ID_BIT_SIZE

def get_work() -> str:
    '''
        Gets from the server a username to process
    '''
    req = requests.post(
        MASTER_URL + f"/process/{SLAVE_ID}", params={
            "nbUser" : 1
        },
        json=[]
    )

    if not req.ok:
        logging.error(f"{req.status_code} - {req.text}")
        exit(1)
    return req.json()[0]


def answer_work(answer : set[str]) -> None:
    '''
        Returns to the server a list of the usernames found in the process
    '''
    req = requests.post(
        MASTER_URL + f"/process/{SLAVE_ID}", params={
            "nbUser" : 1
        },
        json=list(answer)
    )
    pass

def generate_new_id() -> int:
    global start_point # single-threaded so no mutex
    start_point += 1
    return start_point

def get_username_id(username : str) -> int:
    if username in mappings:
        return mappings[username]
    else:
        # Interrogate redis
        possible_id : bytes | None = r.get(username)
        if possible_id is None:
            possible_id = generate_new_id()
            r.set(username, possible_id)
        elif isinstance(possible_id, bytes):
            possible_id = int(possible_id)
        mappings[username] = possible_id
        
        return possible_id

def get_follows(user: str) -> list[str]:
    cursor : str | None = None
    follows  : list[str] = []

    while True:
        url = f"https://public.api.bsky.app/xrpc/app.bsky.graph.getFollows?actor={user}&limit=100"
        if cursor:
            url += f"&cursor={cursor}"

        res_ok = False
        while not res_ok:
            response = requests.get(url)
            res_ok = response.ok
            if not response.ok:
                logging.warning("Received a ")
                time.sleep(1)
        
        result = response.json()

        if not result.get("follows"): # None or len() == 0
            break

        follows.extend(follow.get("handle") for follow in result["follows"])
        cursor = result.get("cursor")

        if not cursor:
            break

    return follows

def work(username : str) -> set[str]:
    '''
        Given a `username`
    '''
    follows : list[str] = get_follows(username)
    follows_ids = [get_username_id(follower_username) for follower_username in follows]
    followed_id = get_username_id(username)

    for follower_id in follows_ids:
        edges.add((follower_id, followed_id))
    return set(follows)

def save_edges(f : io.BufferedWriter):
    for u, v in edges: # Todo optimize with bigger buffers
        f.write(Int32ul.build(u))
        f.write(Int32ul.build(v))

def save_mapping(f : io.BufferedWriter):
    for username, id in mappings.items():
        if (id >> VERTICE_ID_BIT_SIZE) != SLAVE_ID:
            continue
        f.write(Int32ul.build(id))
        f.write(username.encode(encoding="ascii"))

if __name__ == "__main__":
    logging.info(f"Starting the slave {SLAVE_ID}")

    for _ in range(MAX_NB_TREATED):
        try:
            answer_work(work(get_work()))
        except Exception as e:
            logging.error(e)
            break
    
    logging.info(f"Exited the work->solve->work loop, exporting to files")
    with open(OUTPUT_PATH + f"/{SLAVE_ID}.edges", "wb") as f:
        save_edges(f)
    
    with open(OUTPUT_PATH + f"/{SLAVE_ID}.mappings", "wb") as f:
        save_mapping(f)
    logging.info(f"Finished exporting, stopping slave {SLAVE_ID}")
