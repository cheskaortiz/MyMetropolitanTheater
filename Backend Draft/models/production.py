from dataclasses import dataclass
from datetime import date

@dataclass
class Production:
    production_num: int
    title:          str
    start_date:     date
    end_date:       date