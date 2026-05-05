from dataclasses import dataclass
from datetime import date

@dataclass
class Performance:
    performance_id: int
    production_num: int
    perf_date:      date
    perf_time:      str