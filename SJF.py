class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0


def calculate_sjf(processes):
    n = len(processes)
    completed = 0
    current_time = 0
    is_completed = [False] * n

    # Store final execution sequence
    execution_order = []

    print("\n--- Execution Order ---")

    while completed < n:
        # Find the process with the minimum burst time among the processes
        # that have already arrived and are not completed yet.
        min_index = -1
        min_burst = float('inf')

        for i in range(n):
            if processes[i].arrival_time <= current_time and not is_completed[i]:
                if processes[i].burst_time < min_burst:
                    min_burst = processes[i].burst_time
                    min_index = i
                # Tie-breaker: If burst times are equal, pick the one that arrived first
                elif processes[i].burst_time == min_burst:
                    if processes[i].arrival_time < processes[min_index].arrival_time:
                        min_index = i

        # If no process has arrived yet, advance time to the next closest arrival
        if min_index == -1:
            # Find the minimum arrival time among uncompleted processes
            next_arrival = min([p.arrival_time for idx, p in enumerate(processes) if not is_completed[idx]])
            current_time = next_arrival
            continue

        # Execute the selected process
        p = processes[min_index]
        current_time += p.burst_time
        p.completion_time = current_time
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time

        is_completed[min_index] = True
        completed += 1
        execution_order.append(p.pid)

    # Calculate averages
    total_tat = sum(p.turnaround_time for p in processes)
    total_wt = sum(p.waiting_time for p in processes)

    # Print results in a neat table format
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
    # Defining a list of processes (PID, Arrival Time, Burst Time)
    process_list = [
        Process(1, 1, 3),
        Process(2, 2, 4),
        Process(3, 1, 2),
        Process(4, 4, 4)
    ]

    calculate_sjf(process_list)
