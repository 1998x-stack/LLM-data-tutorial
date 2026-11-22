"""Simple file/task/worker planning estimates for DataTrove pipelines."""
from math import ceil


def plan_tasks(file_count: int, tasks: int, workers: int) -> dict[str, int]:
    """Estimate non-empty tasks, concurrency and average file shard size.

    This does not model file-size skew or DataTrove's exact sharding order.
    """
    for name, value in (("file_count", file_count), ("tasks", tasks), ("workers", workers)):
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ValueError(f"{name} must be a positive integer")
    active_tasks = min(file_count, tasks)
    return {
        "file_count": file_count,
        "tasks": tasks,
        "workers": workers,
        "active_tasks_upper_bound": active_tasks,
        "concurrent_tasks_upper_bound": min(active_tasks, workers),
        "estimated_files_per_task_ceiling": ceil(file_count / tasks),
        "empty_tasks_lower_bound": max(0, tasks - file_count),
    }
