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
            print(e, p, d)
            tasks.append([e, p, d])
    return tasks

def simulate_rm(tasks):
    hyperperiod = reduce(lcm, [int(task[1]) for task in tasks])
    preemptions = [0] * len(tasks)
    remaining_time = [0] * len(tasks)
    next_release = [0] * len(tasks)
    current_task = None
    
    for t in range(hyperperiod):
        # Check for new task releases
        for i, task in enumerate(tasks):
            if t == next_release[i]:
                if remaining_time[i] > 0:  # Task missed its deadline
                    return False, preemptions
                remaining_time[i] = task[0]
                next_release[i] += task[1]
        
        # Find the highest priority task that needs to execute
        highest_priority = None
        for i, task in enumerate(tasks):
            if remaining_time[i] > 0:
                if highest_priority is None or task[1] < tasks[highest_priority][1]:
                    highest_priority = i
        
        # Check for preemption and execute the task
        if highest_priority is not None:
            if current_task is not None and current_task != highest_priority:
                if remaining_time[current_task] > 0:
                    preemptions[current_task] += 1
            current_task = highest_priority
            remaining_time[current_task] -= 1
        else:
            current_task = None
        
        # Check for missed deadlines
        for i, task in enumerate(tasks):
            if t % int(task[1]) == int(task[2]) - 1:  # At deadline
                if remaining_time[i] > 0:
                    return False, preemptions
    
    # Final check for unfinished tasks
    if any(remaining_time[i] > 0 for i in range(len(tasks))):
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