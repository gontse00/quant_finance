class positions(object):
    """
    class to model derivatives positions
    """

    def __init__(self, name, quantity, underlying, mar_env, otype, payoff_func):
        self.name = name
        self.quantity = quantity
        self.underlying = underlying
        self.mar_env = mar_env
        self.otype = otype
        self.payoff_func = payoff_func

    def get_info(self):
        print("NAME:", self.name)
        print("QUANTITY:", self.quantity)
        print("UNDERLYING:", self.underlying)
        print("MARKET ENVIROMENT:", self.mar_env)

        print("**Constants**")
        for key, value in self.mar_env.constants.items():
            print(key+":", value)

        print("**Lists**")
        for key, value in self.mar_env.lists.items():
            print(key+":", value)

        print("**Curves**")
        for key, value in self.mar_env.curves.items():
            print(key+":", value)

        print("OPTION TYPE:", self.otype)
        print("PAYOFF FUNCTION:", self.payoff_func)
