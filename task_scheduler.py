# task_scheduler.py

class Task:
    def __init__(self, name, duration, priority, max_duration=None, dependencies=[]):
        self.name = name
        self.duration = duration
        self.priority = priority
        self.max_duration = max_duration
        self.dependencies = dependencies
        self.assigned_to = None
        self.start_time = None
        self.end_time = None

    def __repr__(self):
        return f"Task(name={self.name}, duration={self.duration}, priority={self.priority})"


class Resource:
    def __init__(self, name):
        self.name = name
        self.available_at = 0

    def __repr__(self):
        return f"Resource(name={self.name})"


# Algorithmes gloutons

def greedy_by_duration(tasks, resources):
    tasks_sorted = sorted(tasks, key=lambda x: x.duration)  # Trier par durée
    schedule = []

    for task in tasks_sorted:
        available_resource = min(resources, key=lambda r: r.available_at)
        task.start_time = available_resource.available_at
        task.end_time = task.start_time + task.duration
        task.assigned_to = available_resource
        available_resource.available_at = task.end_time
        schedule.append(task)

    return schedule


def greedy_by_priority(tasks, resources):
    tasks_sorted = sorted(tasks, key=lambda x: x.priority, reverse=True)
    schedule = []

    for task in tasks_sorted:
        available_resource = min(resources, key=lambda r: r.available_at)
        task.start_time = available_resource.available_at
        task.end_time = task.start_time + task.duration
        task.assigned_to = available_resource
        available_resource.available_at = task.end_time
        schedule.append(task)

    return schedule


def greedy_by_duration_and_priority(tasks, resources):
    tasks_sorted = sorted(tasks, key=lambda x: (x.priority, x.duration), reverse=True)
    schedule = []

    for task in tasks_sorted:
        available_resource = min(resources, key=lambda r: r.available_at)
        task.start_time = available_resource.available_at
        task.end_time = task.start_time + task.duration
        task.assigned_to = available_resource
        available_resource.available_at = task.end_time
        schedule.append(task)

    return schedule
