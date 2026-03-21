class ValidateIP:
    def __init__(self, ip):
        self.ip = ip
    def validate(self):
        for x in self.ip.split('.'):
            if not x.isdigit():
                return False
            if not 0 <= int(x) <= 255:
                return False
        return len(self.ip) > 0 and self.ip.count('.') > 2 and len(self.ip.split('.')) == 4
