import sys
from math import gcd
from functools import reduce

def lcm(a, b):
    return abs(a * b) // gcd(int(a), int(b))

def read_tasks(filename):
    tasks = []
    with open(filename, 'r') as f:
        for line in f:
            e, p, d = map(float, line.strip().split(','))
            tasks.append({'exec_time': e, 'period': p, 'deadline': d, 'remaining_time': 0.0, 'next_release': 0.0, 'preemptions': 0})
    return tasks

def compute_hyperperiod(tasks):
    periods = [task['period'] for task in tasks]
    return reduce(lcm, [int(period) for period in periods])

def simulate_rm(tasks):
    hyperperiod = compute_hyperperiod(tasks)
    current_task = None
    task_count = len(tasks)

    for t in range(int(hyperperiod)):
        # Check for new task releases
        for task in tasks:
            if t == int(task['next_release']):
                if task['remaining_time'] > 0:  # Task missed its deadline
                    return False, [task['preemptions'] for task in tasks]
                task['remaining_time'] = task['exec_time']
                task['next_release'] += task['period']

        # Find the highest priority task that needs to execute
        highest_priority_task = None
        for task in tasks:
            if task['remaining_time'] > 0:
                if highest_priority_task is None or task['period'] < highest_priority_task['period']:
                    highest_priority_task = task

        # Check for preemption and execute the task
        if highest_priority_task is not None:
            if current_task is not None and current_task != highest_priority_task and current_task['remaining_time'] > 0:
                current_task['preemptions'] += 1
            current_task = highest_priority_task
            current_task['remaining_time'] -= 1
        else:
            current_task = None

        # Check for missed deadlines
        for task in tasks:
            if (t + 1) % int(task['period']) == 0:  # At deadline
                if task['remaining_time'] > 0:  # More work than one execution time remains
                    return False, [task['preemptions'] for task in tasks]

    # Check if all tasks completed by the end of hyperperiod
    if any(task['remaining_time'] > 0 for task in tasks):
        return False, [task['preemptions'] for task in tasks]

    return True, [task['preemptions'] for task in tasks]

def main(filename):
    tasks = read_tasks(filename)
    schedulable, preemptions = simulate_rm(tasks)
    
    if schedulable:
        print(1)
        print(','.join(map(str, preemptions)))
    else:
        print(0)
        print()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 ece_455_final.py <input_file>")
        sys.exit(1)
    
    main(sys.argv[1])
