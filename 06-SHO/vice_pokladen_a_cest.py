import random
from collections import deque
from dataclasses import dataclass


@dataclass
class Worker:
    name: str
    source: deque
    dest: deque
    period: int
    spread_factor: float = 0.0
    timer: int = 0
    
    dest2: deque = None
    prob_dest: float = 1.0


def get_delay(period: int, spread_factor: float) -> int:
    return max(1, int(random.gauss(period, period * spread_factor)))


def worker_tick(worker: Worker) -> None:
    if worker.timer > 1:
        worker.timer -= 1
    elif len(worker.source) > 0:
        next_customer = worker.source.popleft()

        if worker.dest2 is not None and random.random() > worker.prob_dest:
            worker.dest2.append(next_customer)
        else:
            worker.dest.append(next_customer)

        worker.timer = get_delay(worker.period, worker.spread_factor)


def print_snapshot(time: int, queues: list[tuple[str, deque]]) -> None:
    print(f"Actual time: {time}")
    for i in range(len(queues)):
        name, queue = queues[i]
        print(f"{name}({len(queue)})")


def main() -> None:
    people_number = 1000
    people_in_the_city = deque(list(range(people_number)))

    # 1. Vytvoření front
    gate_q = deque()
    vege_q = deque()
    cashier_q = deque()
    final_q = deque()

    # Seznam pro výpis (jméno, fronta)
    queues_to_observe : list[tuple[str, deque]] = [
        ("Street", people_in_the_city),
        ("Gate", gate_q),
        ("Vege", vege_q),
        ("Cashier", cashier_q),
        ("Final", final_q)
    ]

    # Parametry simulace (střední hodnoty časů v sekundách)
    day_m = 30  # Každých 30s přijde někdo z ulice
    gate_m = 15  # Gate keeper každého odbavuje 15s
    vege_m = 45  # Vážení zeleniny trvá 45s
    final_m = 2 * 60  # Pokladna zabere 2 minuty

    # 2. Vytvoření pracovníků (Worker)
    generator = Worker("Generator", people_in_the_city, gate_q, day_m)
    gatekeeper = Worker("GateKeeper", gate_q, vege_q, gate_m, dest2=cashier_q, prob_dest=0.4)
    vegeman = Worker("VegeMan", vege_q, cashier_q, vege_m)
    
    num_cashiers = 3
    cashiers = [
        Worker(f"Cashier_{i+1}", cashier_q, final_q, final_m, spread_factor=0.1) 
        for i in range(num_cashiers)
    ]

    all_workers = [generator, gatekeeper, vegeman] + cashiers

    # 3. Hlavní smyčka simulace
    time = 7200
    while time > 0:
        for worker in all_workers:
            worker_tick(worker)

        if time % 60 == 0: 
            print_snapshot(time, queues_to_observe)

        time -= 1


if __name__ == "__main__":
    main()