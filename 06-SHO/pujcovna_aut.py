import random
from collections import deque
from dataclasses import dataclass


@dataclass
class Worker:
    name: str
    source: deque
    dest: deque = None
    period: int = 0
    spread_factor: float = 0.0
    timer: int = 0
    
    destinations: list[tuple[deque, int]] = None


def get_delay(period: int, spread_factor: float) -> int:
    return max(1, int(random.gauss(period, period * spread_factor)))


def worker_tick(worker: Worker) -> None:
    if worker.timer > 1:
        worker.timer -= 1
    elif len(worker.source) > 0:
        next_customer = worker.source.popleft()
        
        if worker.destinations:

            dests = [d[0] for d in worker.destinations]
            weights = [d[1] for d in worker.destinations]
            
            chosen_dest = random.choices(dests, weights=weights, k=1)[0]
            chosen_dest.append(next_customer)
            
        elif worker.dest is not None:
            worker.dest.append(next_customer)
            
        worker.timer = get_delay(worker.period, worker.spread_factor)


def print_snapshot(time: int, queues: list[tuple[str, deque]]) -> None:
    print(f"Aktuální čas: {time}")
    for name, queue in queues:
        print(f"{name}: {len(queue)}")


def main() -> None:
    people_number = 1000
    street_q = deque(list(range(people_number)))

    # 1. Vytvoření front (stavy v půjčovně)
    reception_q = deque()
    economy_q = deque()
    suv_q = deque()
    luxury_q = deque()

    # Seznam pro výpis (jméno, fronta)
    queues_to_observe : list[tuple[str, deque]] = [
        ("Ulice", street_q),
        ("Čekárna na recepci", reception_q),
        ("Vypůjčeno - Economy", economy_q),
        ("Vypůjčeno - SUV", suv_q),
        ("Vypůjčeno - Luxury", luxury_q)
    ]

    # Parametry simulace 
    arrival_m = 60  # Každých 60s přijde někdo z ulice
    reception_m = 120  # Vyřízení papírů trvá průměrně 2 minuty

    # 2. Vytvoření pracovníků (Worker)
    generator = Worker("Příchody", street_q, dest=reception_q, period=arrival_m, spread_factor=0.2)
    
    car_popularity = [
        (economy_q, 60),  #60% lidí chce Economy
        (suv_q, 30),      #30% lidí chce SUV
        (luxury_q, 10)    #10% lidí chce Luxury
    ]
    
    #Recepční přiděluje auta podle popularity
    receptionist = Worker("Recepční", reception_q, period=reception_m, spread_factor=0.1, destinations=car_popularity)

    # 3. Hlavní smyčka simulace
    time = 7200
    while time > 0:
        for worker in [generator, receptionist]:
            worker_tick(worker)

        if time % 1800 == 0:
            print_snapshot(7200 - time, queues_to_observe)

        time -= 1


if __name__ == "__main__":
    main()