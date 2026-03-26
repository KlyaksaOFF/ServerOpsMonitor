class ValidateIP:
    def __init__(self, ip):
        self.ip = ip

    def validate(self):
        parts_ip = self.ip.split('.')
        for part in parts_ip:
            if not part.isdigit():
                return False
            if not 0 <= int(part) <= 255:
                return False
        return (len(self.ip) > 0 and self.ip.count('.') > 2
                and len(parts_ip) == 4)
