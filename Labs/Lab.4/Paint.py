import math

class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Empty canvas is a matrix with element being the "space" character
        self.data = [[' '] * width for i in range(height)]

    def set_pixel(self, row, col, char='*'):
        if 0 <= row < self.height and 0 <= col < self.width:
            self.data[row][col] = char

    def get_pixel(self, row, col):
        return self.data[row][col]
    
    def clear_canvas(self):
        self.data = [[' '] * self.width for i in range(self.height)]
    
    def v_line(self, x, y, w, **kargs):
        for i in range(x,x+w):
            self.set_pixel(i,y, **kargs)

    def h_line(self, x, y, h, **kargs):
        for i in range(y,y+h):
            self.set_pixel(x,i, **kargs)
            
    def line(self, x1, y1, x2, y2, **kargs):
        slope = (y2-y1) / (x2-x1)
        for y in range(y1,y2):
            x= int(slope * y)
            self.set_pixel(x,y, **kargs)
            
    def display(self):
        print("\n".join(["".join(row) for row in self.data]))

class Shape():

    def area(self):
        pass

    def perimeter(self):
        pass

    def get_points_on_perimeter(self):
        pass

    def is_inside(self, x, y):
        pass

    def overlaps(self, other):
        pass

# Circle Class that inherits from Shape
class Circle(Shape):
    def __init__(self, radius, x, y):
        self.__radius = radius
        self.__x = x
        self.__y = y


    def get_radius(self):
        return self.__radius

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def area(self):
        pi = 3.14159
        return pi * (self.__radius ** 2)


    def perimeter(self):
        pi = 3.14159
        return 2 * pi * self.__radius

    def get_points_on_perimeter(self):
        points = []
        pi = 3.14159
        for i in range(16):
            theta = 2 * pi * i / 16
            x = self.__x + self.__radius * math.cos(theta)
            y = self.__y + self.__radius * math.sin(theta)
            points.append((x, y))
        return points


    def is_inside(self, x, y):
        distance_squared = (x - self.__x)**2 + (y - self.__y)**2
        return distance_squared <= self.__radius**2

    def overlaps(self, other):
        if isinstance(other, Circle):
            distance_between_centers = math.sqrt((self.__x - other.get_x())**2 + (self.__y - other.get_y())**2)
            return distance_between_centers <= (self.__radius + other.get_radius())
        return False 
    
    def draw(self, canvas):
        for i in range(self.__x - self.__radius, self.__x + self.__radius + 1):
            for j in range(self.__y - self.__radius, self.__y + self.__radius + 1):
                if (i - self.__x) ** 2 + (j - self.__y) ** 2 <= self.__radius ** 2:
                    if 0 <= i < canvas.width and 0 <= j < canvas.height:
                        canvas.set_pixel(j, i, '*')

# Rectangle Class that inherits from Shape
class Rectangle(Shape):
    def __init__(self, length, width, x, y):
        self.__length = length
        self.__width = width
        self.__x = x
        self.__y = y

    def get_length(self):
        return self.__length

    def get_width(self):
        return self.__width

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def area(self):
        return self.__length * self.__width

    def perimeter(self):
        return 2 * (self.__length + self.__width)

    def get_points_on_perimeter(self):
        points = []
        for i in range(4):
            if i == 0:  
                for j in range(4):
                    x = self.__x + j * (self.__length / 3)
                    y = self.__y
                    points.append((x, y))
            elif i == 1:
                for j in range(4):
                    x = self.__x + self.__length
                    y = self.__y + j * (self.__width / 3)
                    points.append((x, y))
            elif i == 2:
                for j in range(4):
                    x = self.__x + (3 - j) * (self.__length / 3)
                    y = self.__y + self.__width
                    points.append((x, y))
            elif i == 3:
                for j in range(4):
                    x = self.__x
                    y = self.__y + (3 - j) * (self.__width / 3)
                    points.append((x, y))
        return points

    def is_inside(self, x, y):
        return self.__x <= x <= self.__x + self.__length and self.__y <= y <= self.__y + self.__width

    def overlaps(self, other):
        if isinstance(other, Rectangle):
            if self.__x + self.__length < other.get_x() or other.get_x() + other.get_length() < self.__x:
                return False
            if self.__y + self.__width < other.get_y() or other.get_y() + other.get_width() < self.__y:
                return False
            return True
        return False
    
    def draw(self, canvas):
        for i in range(self.__x, self.__x + self.__width):
            if 0 <= i < canvas.width:
                if 0 <= self.__y < canvas.height:
                    canvas.set_pixel(self.__y, i, '*')  
                if 0 <= self.__y + self.__length - 1 < canvas.height:
                    canvas.set_pixel(self.__y + self.__length - 1, i, '*') 
        
        for i in range(self.__y, self.__y + self.__length):
            if 0 <= i < canvas.height:
                if 0 <= self.__x < canvas.width:
                    canvas.set_pixel(i, self.__x, '*')  
                if 0 <= self.__x + self.__width - 1 < canvas.width:
                    canvas.set_pixel(i, self.__x + self.__width - 1, '*')


class CompoundShape(Shape):
    def __init__(self):
        self.shapes = []

    def add_shape(self, shape):
        self.shapes.append(shape)

    def draw(self, canvas):
        for shape in self.shapes:
            shape.draw(canvas)

    def is_inside(self, x, y):
        return any(shape.is_inside(x, y) for shape in self.shapes)

    def overlaps(self, other):
        return any(shape.overlaps(other) for shape in self.shapes)