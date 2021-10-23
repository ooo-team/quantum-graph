from qboard import Solver


def create_solver_connection():  # инициализация солвера - ничего умного, код взят из документации
    PARAMS = {
        "remote_addr": "https://remote.qboard.tech",  # просто ремот наш, всё ок
        "access_key": "8a9c6702-ee8c-4cdc-a857-801f06cbd886"  # аксес кей, так то такое коммитить нельзя. oh well
    }
    s = Solver(mode="remote:simcim", params=PARAMS)  # remote:simcim с бесконечными попытками
    return s
