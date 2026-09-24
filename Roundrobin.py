from collections import deque


class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time  # Track leftover burst time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0


def calculate_round_robin(processes, time_quantum):
    n = len(processes)
    current_time = 0
    completed = 0

    # Sort processes by arrival time initially to track entries correctly
    processes.sort(key=lambda x: (x.arrival_time, x.pid))

    ready_queue = deque()
    execution_order = []

    # Track if a process has already entered the ready queue
    is_in_queue = [False] * n

    # Push the first process that arrives into the queue
    current_time = processes[0].arrival_time
    ready_queue.append(processes[0])
    is_in_queue[0] = True

    while completed < n:
        if not ready_queue:
            # CPU is idle; advance time to the next closest arriving process
            next_arrival_idx = next(i for i, p in enumerate(processes) if p.remaining_time > 0 and not is_in_queue[i])
            current_time = processes[next_arrival_idx].arrival_time
            ready_queue.append(processes[next_arrival_idx])
            is_in_queue[next_arrival_idx] = True

        current_p = ready_queue.popleft()
        execution_order.append(current_p.pid)

        # Execute the process for the time quantum or its remaining time (whichever is smaller)
        time_spent = min(current_p.remaining_time, time_quantum)
        current_time += time_spent
        current_p.remaining_time -= time_spent

        # Check and add newly arrived processes to the queue during this execution time
        for i in range(n):
            if processes[i].arrival_time <= current_time and processes[i].remaining_time > 0 and not is_in_queue[i]:
                ready_queue.append(processes[i])
                is_in_queue[i] = True

        # If the current process still has work left, push it to the back of the queue
        if current_p.remaining_time > 0:
            ready_queue.append(current_p)
        else:
            # Process is fully executed
            current_p.completion_time = current_time
            current_p.turnaround_time = current_p.completion_time - current_p.arrival_time
            current_p.waiting_time = current_p.turnaround_time - current_p.burst_time
            completed += 1

    # Calculate averages
    total_tat = sum(p.turnaround_time for p in processes)
    total_wt = sum(p.waiting_time for p in processes)

    # Print results in a neat table format
    print("\n--- Round Robin Execution Results ---")
    print(f"Time Quantum: {time_quantum}")
    print(f"Gantt Chart Sequence: {' -> '.join(map(str, execution_order))}\n")
    print(f"{'PID':<5}{'Arrival':<10}{'Burst':<10}{'Completion':<15}{'Turnaround':<15}{'Waiting':<10}")
    print("-" * 70)

    for p in sorted(processes, key=lambda x: x.pid):
        print(
            f"{p.pid:<5}{p.arrival_time:<10}{p.burst_time:<10}{p.completion_time:<15}{p.turnaround_time:<15}{p.waiting_time:<10}")

    print("-" * 70)
    print(f"Average Turnaround Time: {total_tat / n:.2f}")
    print(f"Average Waiting Time: {total_wt / n:.2f}")


# Example Usage
if __name__ == "__main__":
    process_list = [
        Process(1, 1, 3),
        Process(2, 2, 4),
        Process(3, 1, 2),
        Process(4, 4, 4)
    ]

    time_quantum = 2
    calculate_round_robin(process_list, time_quantum)
