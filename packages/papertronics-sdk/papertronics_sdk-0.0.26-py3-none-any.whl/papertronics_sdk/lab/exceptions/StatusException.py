class StatusException(Exception):
    def __init__(self, code, detail):
        self.code = code
        self.detail = detail

    def __str__(self):
        return f"{self.code}: {self.detail}"

    @staticmethod
    def from_response(response):
        return StatusException(response.status_code, response.json().get("detail"))