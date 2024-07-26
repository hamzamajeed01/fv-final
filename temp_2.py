import sys
from math import gcd
from functools import reduce

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def read_tasks(filename):
    tasks = []
    with open(filename, 'r') as f:
        for line in f:
            e, p, d = map(float, line.strip().split(','))
            tasks.append([e, p, d])
    return tasks

def simulate_rm(tasks):
    hyperperiod = reduce(lcm, [int(task[1]) for task in tasks])
    schedule = [None] * hyperperiod
    preemptions = [0] * len(tasks)
    remaining_time = [0] * len(tasks)
    last_run = [-1] * len(tasks)
    
    for t in range(hyperperiod):
        # Reset execution time at the beginning of each period
        for i, task in enumerate(tasks):
            if t % int(task[1]) == 0:
                if remaining_time[i] > 0:  # Task missed its deadline
                    return False, preemptions
                remaining_time[i] = task[0]
        
        # Find the highest priority task that needs to execute
        active_task = None
        for i, task in enumerate(tasks):
            if remaining_time[i] > 0:
                if active_task is None or task[1] < tasks[active_task][1]:
                    active_task = i
        
        # Execute the task and check for preemptions
        if active_task is not None:
            if schedule[t-1] is not None and schedule[t-1] != active_task:
                if remaining_time[schedule[t-1]] > 0:  # The previous task was preempted
                    preemptions[schedule[t-1]] += 1
            
            if last_run[active_task] != -1 and last_run[active_task] != t - 1:
                # This task was preempted earlier and is now resuming
                preemptions[active_task] += 1
            
            schedule[t] = active_task
            remaining_time[active_task] -= 1
            last_run[active_task] = t
        
        # Check for missed deadlines
        for i, task in enumerate(tasks):
            if t % int(task[1]) == int(task[2]) - 1:  # At deadline
                if remaining_time[i] > 0:
                    return False, preemptions
    
    return True, preemptions

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