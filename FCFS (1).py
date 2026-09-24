class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0


def calculate_fcfs(processes):
    n = len(processes)
    current_time = 0

    # Sort processes primarily by Arrival Time, and by PID as a tie-breaker
    processes.sort(key=lambda x: (x.arrival_time, x.pid))

    execution_order = []

    for p in processes:
        # If the CPU is idle (process hasn't arrived yet), advance time to its arrival
        if current_time < p.arrival_time:
            current_time = p.arrival_time

        # Execute the process
        current_time += p.burst_time
        p.completion_time = current_time
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time

        execution_order.append(p.pid)

    # Calculate averages
    total_tat = sum(p.turnaround_time for p in processes)
    total_wt = sum(p.waiting_time for p in processes)

    # Print results in a neat table format
    print("\n--- FCFS Execution Results ---")
    print(f"Gantt Chart Sequence: {' -> '.join(map(str, execution_order))}\n")
    print(f"{'PID':<5}{'Arrival':<10}{'Burst':<10}{'Completion':<15}{'Turnaround':<15}{'Waiting':<10}")
    print("-" * 70)

    # Print sorted by PID for clean presentation
    for p in sorted(processes, key=lambda x: x.pid):
        print(
            f"{p.pid:<5}{p.arrival_time:<10}{p.burst_time:<10}{p.completion_time:<15}{p.turnaround_time:<15}{p.waiting_time:<10}")

    print("-" * 70)
    print(f"Average Turnaround Time: {total_tat / n:.2f}")
    print(f"Average Waiting Time: {total_wt / n:.2f}")


# Example Usage (Using the same values from the SJF example)
if __name__ == "__main__":
    process_list = [
        Process(1, 1, 3),
        Process(2, 2, 4),
        Process(3, 1, 2),
        Process(4, 4, 4)
    ]

    calculate_fcfs(process_list)
