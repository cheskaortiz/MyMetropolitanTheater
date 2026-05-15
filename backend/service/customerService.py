from repository.customerRepo import CustomerRepo

class CustomerService:
    def __init__(self, conn):
        self.customerRepo = CustomerRepo(conn)

    # creates a new customer after validating all required fields
    # requirement: customers must exist before tickets can be purchased
    def createCustomer(self, customer):
        validation = self.__checkCustomer(customer)

        if validation is True:
            self.customerRepo.createCustomer(customer)
            return "successfully created production"
        
        return validation
    
    # updates customer information after verifying customer exists
    def updateCustomer(self, customer):
        if customer.customerId is None:
            return "Invalid customerId."

        try:
            customer.customerId = int(customer.customerId)
        except ValueError:
            return "Invalid customerId. Must be a number."

        if self.customerRepo.locateCustomerId(customer.customerId) is None:
            return "Customer id does not exist."

        validation = self.__checkCustomer(customer, isUpdate=True)

        if validation is True:
            self.customerRepo.updateCustomer(customer)
            return "Successfully updated customer."

        return validation
    
    # retrieves all customer records
    # requirement: supports Transaction Report and Names report
    def viewAllCustomer(self):
        return self.customerRepo.getAllCustomers()
    
    # locates a customer by ID — used before update operations
    def locateCustomerId(self, customerId):
        try:
            customerId = int(customerId)
        except ValueError:
            return "invalid customerId. must be number"
        
        customer = self.customerRepo.locateCustomerId(customerId)

        if customer:
            return customer
        return "Customer does not exist"
    
    # locates a customer by mobile number — used to prevent duplicate registrations
    def locateCustomerMobileNumber(self, customerMobileNumber):
        if customerMobileNumber is None or str(customerMobileNumber).strip() == "":
            return "Seat number is required."

        customerMobileNumber = str(customerMobileNumber).strip()

        customer = self.customerRepo.locateCustomerMobileNumber(customerMobileNumber)

        if customer:
            return customer

        return "customer does not exist."
    
    # locates a customer by name — supports customer search during ticket purchase
    def locateCustomerName(self, customerName):
        if customerName is None or str(customerName).strip() == "":
            return "customer name is required."

        customerName = str(customerName).strip()

        customer = self.customerRepo.locateCustomerName(customerName)

        if customer:
            return customer

        return "customer does not exist."
    
    # locates a customer by email — used to prevent duplicate registrations
    def locateCustomerEmail(self, customerEmail):
        if customerEmail is None or str(customerEmail).strip() == "":
            return "customer name is required."

        customerEmail = str(customerEmail).strip()

        customer = self.customerRepo.locateCustomerEmail(customerEmail)

        if customer:
            return customer

        return "customer does not exist."
    
    # validates all customer fields before create or update
    # checks: name, mobile number (11 digits, numeric), email format, duplicate email, duplicate mobile
    def __checkCustomer(self, customer, isUpdate=False):
        if customer.name is None or str(customer.name).strip() == "":
            return "name is required"

        if customer.mobileNumber is None or str(customer.mobileNumber).strip() == "":
            return "mobile number is required."
        
        if len(customer.mobileNumber) != 11:
            return "Mobile number must be 11 digits."

        if customer.email is None or str(customer.email).strip() == "":
            return "email is required."

        customer.name = str(customer.name).strip()
        customer.mobileNumber = str(customer.mobileNumber).strip()
        customer.email = str(customer.email).strip()

        if "@" not in customer.email or "." not in customer.email:
            return "invalid email format"
        
        if not customer.mobileNumber.isdigit():
            return "mobile number  only"
        
        existingEmail = self.customerRepo.locateCustomerEmail(customer.email)

        if existingEmail:
            existingCustomerId = existingEmail[0]

            if not isUpdate or existingCustomerId != customer.customerId:
                return "customer email already exists"

        existingMobileNumber = self.customerRepo.locateCustomerMobileNumber(customer.mobileNumber)

        if existingMobileNumber:
            existingCustomerId = existingMobileNumber[0]

            if not isUpdate or existingCustomerId != customer.customerId:
                return "Customer mobile number already exists."

        return True