**How To Execute**
First line tells how many tasks are present in the current task set, let's say n. Next 'n' lines contain period 'P' and computation time 'C' for each task.
**Sample Input**

```
3
4 1
6 2
8 3

```

**Sample Output**

```
This task set consists of 3 tasks. They are:
Task 0:
	Period: 4
	Computation Time: 1
Task 1:
	Period: 6
	Computation Time: 2
Task 2:
	Period: 8
	Computation Time: 3


##Note that this task set does not satisfy the schedulability check,
therefore there are chances of deadline misses.
=========================================================
The Execution Begins:
=========================================================
At time 0, task 0 has started execution
At time 1, task 0 has been completely executed.
At time 1, task 1 has started execution
At time 3, task 1 has been completely executed.
At time 3, task 2 has started execution
At time 4, task 2 has been preempted.
At time 4, task 0 has started execution
At time 5, task 0 has been completely executed.
At time 5, task 2 has started execution
At time 6, task 2 has been preempted.
At time 6, task 1 has started execution
At time 8, task 1 has been completely executed.
At time 8, task 2 has been preempted.
At time 8, task 0 has started execution
At time 9, task 0 has been completely executed.
At time 9, task 2 has started execution
Task 2 finished at time 10 thus, missing it's deadline of time 8.

Process finished with exit code 0my input and ouput is bit different but its for you to just get idea and maybe you could provide correct solution now also remmeber you can only use librraries comes with python 3.10 builtin
```