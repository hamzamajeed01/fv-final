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
    schedule = []
    preemptions = [0] * len(tasks)
    remaining_time = [0] * len(tasks)
    next_release = [0] * len(tasks)
    
    t = 0
    while t < hyperperiod:
        # Check for new task releases
        for i, task in enumerate(tasks):
            if t == next_release[i]:
                if remaining_time[i] > 0:  # Task missed its deadline
                    return False, preemptions
                remaining_time[i] = task[0]
                next_release[i] += task[1]
        
        # Find the highest priority task that needs to execute
        active_task = None
        for i, task in enumerate(tasks):
            if remaining_time[i] > 0:
                if active_task is None or task[1] < tasks[active_task][1]:
                    active_task = i
        
        if active_task is not None:
            # Calculate how long this task can run
            run_duration = min(remaining_time[active_task], 
                               min((next_release[i] - t for i in range(len(tasks)) if i != active_task), default=hyperperiod-t))
            
            # Check for preemption
            if schedule and schedule[-1][0] != active_task and remaining_time[schedule[-1][0]] > 0:
                preemptions[schedule[-1][0]] += 1
            
            schedule.append((active_task, t, t + run_duration))
            remaining_time[active_task] -= run_duration
            t += run_duration
        else:
            t += 1
        
        # Check for missed deadlines
        for i, task in enumerate(tasks):
            if t % int(task[1]) == int(task[2]) and remaining_time[i] > 0:
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