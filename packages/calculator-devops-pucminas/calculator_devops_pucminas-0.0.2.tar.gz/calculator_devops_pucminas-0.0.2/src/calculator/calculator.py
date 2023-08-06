class cal():
    def __init__(self):
        pass

    def checking_consistence(self, x):
        x = str(x)
        if not x.replace('.', '', 1).isdigit():
            raise Exception('The information inputed is not a number. Closing Calculator!')

    def add(self, a, b):
        self.checking_consistence(a)
        self.checking_consistence(b)
        a = float(a)
        b = float(b)
        return a + b

    def sub(self, a, b):
        self.checking_consistence(a)
        self.checking_consistence(b)
        a = float(a)
        b = float(b)
        return a - b

    def multiply(self, a, b):
        self.checking_consistence(a)
        self.checking_consistence(b)
        a = float(a)
        b = float(b)
        return a * b

    def divide(self, a, b):
        self.checking_consistence(a)
        self.checking_consistence(b)
        a = float(a)
        b = float(b)
        return a / b
