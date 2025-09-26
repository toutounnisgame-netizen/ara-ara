"""
PerformanceMonitor - Monitoring performance mémoire/temps
"""

import time
import tracemalloc
from typing import Dict, List, Any

class PerformanceMonitor:
    def __init__(self):
        self.session_start = 0.0
        self.loop_times = []
        self.memory_snapshots = []
        self.max_memory = 0.0

    def start_session(self):
        self.session_start = time.perf_counter()
        tracemalloc.start()

    def record_loop_time(self, loop_time_ms: float):
        self.loop_times.append(loop_time_ms)

        # Limite historique pour mémoire
        if len(self.loop_times) > 100:
            self.loop_times = self.loop_times[-50:]

    def end_session(self):
        if tracemalloc.is_tracing():
            current, peak = tracemalloc.get_traced_memory()
            self.max_memory = peak / 1024 / 1024  # MB
            tracemalloc.stop()

    def get_session_stats(self) -> Dict[str, Any]:
        duration = time.perf_counter() - self.session_start if self.session_start > 0 else 0
        avg_loop_time = sum(self.loop_times) / len(self.loop_times) if self.loop_times else 0

        return {
            "duration_seconds": duration,
            "max_memory_mb": self.max_memory,
            "avg_response_ms": avg_loop_time,
            "total_loops": len(self.loop_times)
        }
