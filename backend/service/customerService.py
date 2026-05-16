from repository.customerRepo import CustomerRepo


class CustomerService:
    def __init__(self, conn):
        self.customerRepo = CustomerRepo(conn)

    # Needed attributes from customer object: name, email, mobileNumber
    def createCustomer(self, customer):
        validation = self.__checkCustomer(customer)

        if validation is True:
            self.customerRepo.createCustomer(customer)
            return "Successfully created customer."

        return validation
    
    # Needed attributes from customer object: customerId, name, email, mobileNumber
    def updateCustomer(self, customer):
        if customer is None:
            return "Customer data is required."

        if customer.customerId is None or str(customer.customerId).strip() == "":
            return "Customer ID is required."

        try:
            customer.customerId = int(customer.customerId)
        except (ValueError, TypeError):
            return "Invalid customer ID. Must be a number."

        if self.customerRepo.locateCustomerId(customer.customerId) is None:
            return "Customer does not exist."

        validation = self.__checkCustomer(customer, isUpdate=True)

        if validation is True:
            self.customerRepo.updateCustomer(customer)

            updated_customer = self.customerRepo.locateCustomerId(customer.customerId)

            return {
                "message": "Successfully updated customer.",
                "customer": self.__format_customer(updated_customer)
            }

        return validation

    # Retrieves all customer records.
    def viewAllCustomer(self):
        customers = self.customerRepo.getAllCustomers()

        if customers is None:
            return "No customers available."

        return self.__format_customer_list(customers)

    # Locates one customer using customer ID.
    # Needed input: custoemer id
    def locateCustomerId(self, customerId):
        if customerId is None or str(customerId).strip() == "":
            return "Customer ID is required."

        try:
            customerId = int(customerId)
        except (ValueError, TypeError):
            return "Invalid customer ID. Must be a number."

        customer = self.customerRepo.locateCustomerId(customerId)

        if customer:
            return self.__format_customer(customer)

        return "Customer does not exist."

    # Needed input: customerMobileNumber
    def locateCustomerMobileNumber(self, customerMobileNumber):
        if customerMobileNumber is None or str(customerMobileNumber).strip() == "":
            return "Customer mobile number is required."

        customerMobileNumber = str(customerMobileNumber).strip()

        customer = self.customerRepo.locateCustomerMobileNumber(customerMobileNumber)

        if customer:
            return self.__format_customer(customer)

        return "Customer does not exist."

    # Needed input: customerName
    def locateCustomerName(self, customerName):
        if customerName is None or str(customerName).strip() == "":
            return "Customer name is required."

        customerName = str(customerName).strip()

        customer = self.customerRepo.locateCustomerName(customerName)

        if customer:
            return self.__format_customer(customer)

        return "Customer does not exist."

    # Locates one customer using email.
    # Needed input: customerEmail
    def locateCustomerEmail(self, customerEmail):
        if customerEmail is None or str(customerEmail).strip() == "":
            return "Customer email is required."

        customerEmail = str(customerEmail).strip()

        customer = self.customerRepo.locateCustomerEmail(customerEmail)

        if customer:
            return self.__format_customer(customer)

        return "Customer does not exist."

    def __checkCustomer(self, customer, isUpdate=False):
        if customer is None:
            return "Customer data is required."

        if customer.name is None or str(customer.name).strip() == "":
            return "Customer name is required."

        if customer.mobileNumber is None or str(customer.mobileNumber).strip() == "":
            return "Customer mobile number is required."

        if customer.email is None or str(customer.email).strip() == "":
            return "Customer email is required."

        customer.name = str(customer.name).strip()
        customer.mobileNumber = str(customer.mobileNumber).strip()
        customer.email = str(customer.email).strip()

        if len(customer.mobileNumber) != 11:
            return "Mobile number must be 11 digits."

        if not customer.mobileNumber.isdigit():
            return "Mobile number must contain numbers only."

        if "@" not in customer.email or "." not in customer.email:
            return "Invalid email format."

        existingEmail = self.customerRepo.locateCustomerEmail(customer.email)

        if existingEmail:
            existingCustomerId = existingEmail[0]

            if not isUpdate or existingCustomerId != customer.customerId:
                return "Customer email already exists."

        existingMobileNumber = self.customerRepo.locateCustomerMobileNumber(customer.mobileNumber)

        if existingMobileNumber:
            existingCustomerId = existingMobileNumber[0]

            if not isUpdate or existingCustomerId != customer.customerId:
                return "Customer mobile number already exists."

        return True
    
    def __format_customer(self, customer):
        """
        Converts one customer row into dictionary format.

        Expected row from CustomerRepo:
        customer_id, name, email, mobile_number
        """

        if not customer:
            return None

        return {
            "customer_id": customer[0],
            "name": customer[1],
            "email": customer[2],
            "mobile_number": customer[3]
        }

    def __format_customer_list(self, customers):
        """
        Converts a list of customer rows into a list of dictionaries.
        """

        if not customers:
            return []

        customer_list = []

        for customer in customers:
            customer_list.append(self.__format_customer(customer))

        return customer_list
