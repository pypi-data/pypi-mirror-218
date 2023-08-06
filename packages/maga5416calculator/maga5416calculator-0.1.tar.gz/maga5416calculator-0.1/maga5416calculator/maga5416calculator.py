class Calculator:
    """
    A simple calculator class that can perform addition, subtraction,
    multiplication, division, and nth root calculations.
    It also has a memory that holds the result of the calculations.
    """

    def __init__(self):
        """
        Initializes a new instance of the Calculator class and sets the memory to 0.
        """
        self.memory = 0


    def add(self, number):
        """
        Adds the provided number to the memory.
        
        Parameters:
        number (float): The number to be added to the memory.

        Returns:
        float: The new memory value after the addition.
        """
        self.memory += number
        return self.memory

    def subtract(self, number):
        """
        Subtracts the provided number from the memory.
        
        Parameters:
        number (float): The number to be subtracted from the memory.

        Returns:
        float: The new memory value after the subtraction.
        """
        self.memory -= number
        return self.memory

    def multiply(self, number):
        """
        Multiplies the memory by the provided number.
        
        Parameters:
        number (float): The number to multiply the memory by.

        Returns:
        float: The new memory value after the multiplication.
        """
        self.memory *= number
        return self.memory

    def divide(self, number):
        """
        Divides the memory by the provided number.
        
        Parameters:
        number (float): The number to divide the memory by.

        Returns:
        float: The new memory value after the division.
        """
        if number != 0:
            self.memory /= number
            return self.memory
        else:
            return 'Error: Division by zero is not allowed'

    def root(self, n):
        """
        Takes the nth root of the memory.
        
        Parameters:
        n (float): The root to take of the memory.

        Returns:
        float: The new memory value after taking the nth root.
        """
        if n != 0:
            self.memory **= (1 / n)
            return self.memory
        else:
            return 'Error: Division by zero is not allowed'

    def reset_memory(self):
        """
        Resets the memory to 0.

        Returns:
        float: The new memory value after the reset (should always be 0).
        """
        self.memory = 0
        return self.memory
