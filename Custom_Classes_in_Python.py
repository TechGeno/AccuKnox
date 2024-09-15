class Rectangle:
    # Constructor method to initialization
    def __init__(self, length: int, width: int):
        self.length = length  
        self.width = width    
   
    # Making object iterable
    def __iter__(self):
        yield {'length': self.length}
        yield {'width': self.width}


# Example usage:
rect = Rectangle(5, 3)  # Creating rectangle object
for item in rect:  # Iterate over the Rectangle object
    print(item)   

