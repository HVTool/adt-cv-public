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


def get_delay(period: int, spread_factor: float) -> int:
    return int(random.gauss(period, period * spread_factor))



def worker_tick(worker: Worker) -> None:
    if worker.timer > 1:
        worker.timer -= 1
    elif len(worker.source) > 0:
        next_customer = worker.source.popleft()
        worker.dest.append(next_customer)
        worker.timer = get_delay(worker.period, worker.spread_factor)


def print_snapshot(time: int, queues: list[tuple[str, deque]]) -> None:
    print(f"Actual time:{time}")
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
    gate_m = 15  # Gate keeper každého odbavuje 5s
    vege_m = 45  # Vážení zeleniny trvá 45s
    final_m = 2 * 60  # Pokladna zabere 2 minuty

    # 2. Vytvoření pracovníků (Worker)
    # Worker(jméno, zdroj, cíl, perioda, spread_factor)
    generator = Worker("Generator", people_in_the_city, gate_q, day_m)
    gatekeeper = Worker("GateKeeper", gate_q, vege_q, gate_m)
    vegeman = Worker("VegeMan", vege_q, cashier_q, vege_m)
    cashier = Worker("Cashier", cashier_q, final_q, final_m)
    # 3. Hlavní smyčka simulace
    time = 7200
    while time > 0:
        for worker in [generator, gatekeeper, vegeman, cashier]:
            worker_tick(worker)

        if time % 60 == 0:
            print_snapshot(time, queues_to_observe)

        time -= 1




if __name__ == "__main__":
    main()

#otázky k testu:
#1. jak bychom zjistili kdy vejde člověk do fronty?
#řešení: vytvořit dataclass pro člověka, kde bude jeho id, čas atd.
#lepší řešení: udělat list záznamů a tam zaznamenat pokud se něco událo (nezapisujeme, když je worker zaneprázdněn)

#2. jak udělat kdyby si člověk chtěl vybrat kam jít?
# v dataclass worker bychom neměli jednu destination, ale list destinací
# nevadí když dva workers posílají lidi na cashier zároveň

#3. jak upravit kód tak, aby jsme implemetovali jiné téma
# názorné příklady:
# jak bychom udělali půjčovnu aut, kde jsou zákazníci opět na ulici a budou si vybírat auta podle popularity
# rybník, když mám 100 ryb budou se množit při 100 rybách 2/den, 1000 ryb 10/den, 10000 ryb - začnou umírat. případně tam bude víc rybníků

#v testu bude buď dnešní nebo zítřejší cvičení, jinak už nic
