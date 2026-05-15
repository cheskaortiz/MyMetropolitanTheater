class CustomerRepo:
    def __init__(self, connect):
        self.connect = connect

    # retrieves all customers — supports Transaction Report and Purchase Tickets by Performance
    def getAllCustomers(self):
        with self.connect.cursor() as cur:
            cur.execute("SELECT * FROM customer")
            rows = cur.fetchall()
            return rows
    
    # creates a new customer record — required before a ticket can be purchased
    def createCustomer(self, newCustomer):
        with self.connect.cursor() as cur:
            cur.execute(
                "INSERT INTO customer (name, email, mobile_number) VALUES (%s, %s, %s)",
                (
                    newCustomer.name,
                    newCustomer.email,
                    newCustomer.mobileNumber
                )
            )
            self.connect.commit()
    
    # # updates customer contact details — name, email, mobile number
    def updateCustomer(self, updatedCustomer):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                UPDATE customer
                SET name = %s, email = %s, mobile_number = %s
                WHERE customer_id = %s
                """,
                (
                    updatedCustomer.name,
                    updatedCustomer.email,
                    updatedCustomer.mobileNumber,
                    updatedCustomer.customerId
                )
            )
            self.connect.commit()

    # locates a customer by their system-generated ID — used before update and for ticket lookup
    def locateCustomerId(self, customerId):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM customer
                WHERE customer_id = %s
                """,
                (customerId,)
            )

            row = cur.fetchone()

            if row:
                return row
            return None
        
    # locates a customer by name — supports customer search when purchasing tickets
    def locateCustomerName(self, customerName):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM customer
                WHERE name = %s
                """,
                (customerName,)
            )

            row = cur.fetchone()

            if row:
                return row
            return None

    # locates a customer by email — used to prevent duplicate customer records 
    def locateCustomerEmail(self, customerEmail):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM customer
                WHERE email = %s
                """,
                (customerEmail,)
            )

            row = cur.fetchone()

            if row:
                return row
            return None
        
    # locates a customer by mobile number — used to prevent duplicate customer records
    def locateCustomerMobileNumber(self, customerMobileNumber):
        with self.connect.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM customer
                WHERE mobile_number = %s
                """,
                (customerMobileNumber,)
            )

            row = cur.fetchone()

            if row:
                return row
            return None