from dataclasses import dataclass

@dataclass
class Transaction:
    transaction_id: int
    ticket_number:  str
    txn_type:       str
    seat_id:        int
    performance_id: int
    employee_id:    int