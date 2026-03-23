class ValidateIP:
    def __init__(self, ip):
        self.ip = ip
    def validate(self):
        for char in self.ip.split('.'):
            if not char.isdigit():
                return False
            if not 0 <= int(char) <= 255:
                return False
        return len(self.ip) > 0 and self.ip.count('.') > 2 and len(self.ip.split('.')) == 4
