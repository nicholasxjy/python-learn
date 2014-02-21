import pickle

class Transaction:

    def __init__(self, amount, date, currency="USD", usd_conversion_rate=1, description=None):
        """
        >>>t = Transaction(100, "2014-02-21")
        >>>t.amount, t.currency, t.usd
        """
        self.__amount = amount
        self.__date = date
        self.__currency = currency
        self.__usd_conversion_rate = usd_conversion_rate
        self.__description = description

        @property
        def amount(self):
            return self.__amount

        @property
        def date(self):
            return self.__date

        @property
        def currency(self):
            return self.__currency

        @property
        def usd_conversion_rate(self):
            return self.__usd_conversion_rate

        @property
        def description(self):
            return self.__description

        @property
        def usd(self):
            return self.__amount * self.__usd_conversion_rate

class Account:

    def __init__(self, number, name):
        """Creates a new account with the given number and name
        The number is used as the account's filename.
        """
        self.__number = number
        self.__name = name
        self.__transactions = []

    @property
    def number(self):
        "The read-only account number"
        return self.__number

    @property
    def name(self):
        """The account's name
        This can be changed since it is only for human convenience;
        the account number is the true identifier
        """
        return self.__name

    @name.setter
    def name(self, name):
        assert len(name) > 3, "account name must be at least 4 characters"
        self.__name = name

    def __len__(self):
        "Return the number of transactions"
        return len(self.__transactions)

    def apply(self, transaction):
        "Applies (adds) the given transaction to the account"
        self.__transactions.append(transaction)

    @property
    def balance(self):
        "Return the balance in USD"
        total = 0.0
        for transaction in self.__transactions:
            total += transaction.usd
        return total

    @property
    def all_usd(self):
        "Return True if all transactions are in USD"
        for tansaction in self.__transactions:
            if transaction.currency != "USD":
                return False
        return True

    def save(self):
        "Save the account's data in file number .acc"
        fh = None
        try:
            data = [self.number, self.name, self.__transactions]
            fh = open(self.number + ".acc", "wb")
            pickle.dump(data, fh, pickle.HIGHEST_PROTOCOL)
        except (EnvironmentError, pickle.PickleError) as err:
            raise SaveError(str(err))
        finally:
            if fh is not None:
                fh.close()

    def load(self):
        """Load the account's data from file number.acc
        All prvious data is lost
        """
        fh = None
        try:
            fh = open(self.number+".acc", "rb")
            data = pickle.load(fh)
            assert self.number == data[0], "account number doesnt match"
        except (EnvironmentError, pickle.UnpicklingError) as err:
            raise LoadError(str(err))
        finally:
            if fh is not None:
                fh.close()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
