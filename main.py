import numpy as np


def read_file(file):
    """ input: txt file
        output: n = Dimensions
                m = Number of pizzerias
                m_info = Information of pizzerias, location and maximum delivery distance"""

    lines = open(file).readlines()

    # First line
    n = int(lines[0].split()[0])
    m = int(lines[0].split()[1])

    if n < 1 or n > 1000:
        raise ValueError('Dimension should be on interval [1, 1000]')

    # Pizzerias information
    m_info = []
    for line in range(1, m + 1):

        x = int(lines[line].split()[0])
        y = int(lines[line].split()[1])
        k = int(lines[line].split()[2])
        info = [(x, y), k]
        m_info.append(info)

        # Errors if exceeded limits
        if (x < 1 or x > n) or (y < 1 or y > n):
            raise ValueError("Location should be within town's dimensions {}x{}".format(n, n))

        if k < 1 or k > 1000:
            raise ValueError("Delivery distance should be on interval [1, 1000]")

    return n, m, m_info


class Town:

    def __init__(self, N, M, M_info):

        self.size = N
        self.town = np.zeros((N, N), dtype=np.int8)
        self.n_pizzerias = M
        self.pizzerias = M_info

    def add_route(self):
        """Adds delivery route for each pizzeria"""
        for pizzeria in self.pizzerias:
            x_loc = pizzeria[0][0] - 1
            y_loc = pizzeria[0][1] - 1
            k = pizzeria[1]

            # Adding delivery route to the south of the pizzeria
            for i in range(k + 1):
                # Boundaries below the map
                if x_loc + k - i >= N:
                    pass
                # Boundaries left of the map
                elif y_loc - i <0:
                    self.town[x_loc + k - i, 0:pizzeria[0][1] + i] += 1
                # Boundaries right of the map
                elif pizzeria[0][1] + i >= N:
                    self.town[x_loc + k - i, y_loc - i:N] += 1
                else:
                    self.town[x_loc + k - i, y_loc - i:pizzeria[0][1]+ i] += 1

            # Adding delivery route to the north of the pizzeria
            for i in range(k + 1):
                # Boundaries above the map
                if x_loc - k + i < 0:
                    pass
                # Boundaries left of the map
                elif y_loc - i <0:
                    self.town[x_loc - k + i, 0:pizzeria[0][1] + i] += 1
                # Boundaries right of the map
                elif pizzeria[0][1] + i >= N:
                    self.town[x_loc - k + i, y_loc - i:N] += 1
                else:
                    self.town[x_loc - k + i, y_loc - i:pizzeria[0][1]+ i] += 1

            # Erasing duplicated centre delivery route
            if y_loc - i < 0:
                self.town[x_loc, 0:pizzeria[0][1] + i] -= 1
            elif pizzeria[0][1] + i >= N:
                self.town[x_loc, y_loc - i:N] -= 1
            else:
                self.town[x_loc, y_loc - i:pizzeria[0][1] + i] -= 1

    def display(self):
        print(self.town.copy())

    def max_pizzas(self):
        return np.max(self.town.copy())


if __name__ == '__main__':
    # Read file
    N, M, M_info = read_file('input.txt')
    town = Town(N, M, M_info)
    town.add_route()
    town.display()
    best_loc = town.max_pizzas()
    print("Maximum selection of pizzas are {}".format(best_loc))

