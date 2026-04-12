import random
from collections import deque
from dataclasses import dataclass


@dataclass
class Worker:
    name: str
    pond: deque
    graveyard: deque = None
    period: int = 1
    spread_factor: float = 0.0
    timer: int = 0

    fish_counter: int = 0 


def get_delay(period: int, spread_factor: float) -> int:
    return max(1, int(random.gauss(period, period * spread_factor)))


def worker_tick(worker: Worker) -> None:
    if worker.timer > 1:
        worker.timer -= 1
    else:
        num_fish = len(worker.pond)
        
        if num_fish >= 10000:
            deaths = min(num_fish, 50) 
            for _ in range(deaths):
                dead_fish = worker.pond.popleft()
                if worker.graveyard is not None:
                    worker.graveyard.append(dead_fish)
                    
        elif num_fish >= 1000:
            for _ in range(10):
                worker.fish_counter += 1
                worker.pond.append(f"Ryba_{worker.name}_{worker.fish_counter}")
                
        elif num_fish >= 100:
            for _ in range(2):
                worker.fish_counter += 1
                worker.pond.append(f"Ryba_{worker.name}_{worker.fish_counter}")
                

        worker.timer = get_delay(worker.period, worker.spread_factor)


def print_snapshot(day: int, queues: list[tuple[str, deque]]) -> None:
    print(f"Den simulace: {day}")
    for name, queue in queues:
        print(f"{name}: {len(queue)} ryb")


def main() -> None:
    # 1. Vytvoření front
    pond_1 = deque([f"Ryba_start_P1_{i}" for i in range(100)])    # Začíná na 100
    pond_2 = deque([f"Ryba_start_P2_{i}" for i in range(1200)])   # Začíná na 1200
    graveyard = deque()

    queues_to_observe : list[tuple[str, deque]] = [
        ("Rybník 1 (Start 100)", pond_1),
        ("Rybník 2 (Start 1200)", pond_2),
        ("Rybí hřbitov (uhynulé)", graveyard)
    ]

    # 2. Vytvoření pracovníků
    nature_1 = Worker("Příroda_1", pond=pond_1, graveyard=graveyard, period=1, fish_counter=100)
    nature_2 = Worker("Příroda_2", pond=pond_2, graveyard=graveyard, period=1, fish_counter=1200)

    # 3. Hlavní smyčka simulace 
    #Místo sekund teď počítáme dny
    total_days = 2000
    current_day = 0
    
    while current_day <= total_days:
        for worker in [nature_1, nature_2]:
            worker_tick(worker)

        if current_day % 200 == 0:
            print_snapshot(current_day, queues_to_observe)

        current_day += 1


if __name__ == "__main__":
    main()