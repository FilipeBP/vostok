from fastapi.exceptions import HTTPException

class NotMulipleError(HTTPException):
    def __init__(self, name, quantity, stack_size):
        detail_msg = f"The {name} quantity ({quantity}) has to be multiple of its stack size which is {stack_size}"

        super(NotMulipleError, self).__init__(status_code=412, detail=detail_msg)

class RentabilityError(HTTPException):
    def __init__(self):
        detail_msg = "Requested rentability is invalid"
        super(RentabilityError, self).__init__(status_code=406, detail=detail_msg)