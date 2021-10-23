from qboard import Solver


def create_solver_connection():
    PARAMS = {
        "remote_addr": "https://remote.qboard.tech",
        "access_key": "8a9c6702-ee8c-4cdc-a857-801f06cbd886"
    }
    s = Solver(mode="remote:simcim", params=PARAMS)
    return s
