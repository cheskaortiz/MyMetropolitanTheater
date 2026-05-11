from typing import Final

class Commissioned:
    def __init__(self, staff_id=None):
        self.staff_id = staff_id
        self.commission_rate:Final= 0.25
