class Treatment:
    prices = {
        "Check-up": 50.00,
        "Cleaning": 75.00,
        "Filling": 120.00,
        "Tooth Extraction": 150.00,
        # ... add all your other treatments here
    }

    @classmethod
    def get_price(cls, name):
        return cls.prices.get(name, 0.0)

    @classmethod
    def list_all(cls):
        return list(cls.prices.keys())