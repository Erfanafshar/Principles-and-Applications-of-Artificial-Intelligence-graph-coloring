import copy
import random
import math
import matplotlib.pyplot as plt

number_of_iterations = 1000


class City:
    def __init__(self):
        self.color_number = 0
        self.adjacent_cities_number = []

    def set_adjacent_cities(self, adjacent_cities_number):
        self.adjacent_cities_number = adjacent_cities_number

    def set_color(self, color_number):
        self.color_number = color_number


class Country:
    def __init__(self, cities):
        self.cities = cities


class Chromosome:
    def __init__(self, country, fitness):
        self.country = country
        self.fitness = fitness

    def set_fitness(self, fitness):
        self.fitness = fitness


def create_country():
    cities = []
    for i in range(31):
        cities.append(City())

    cities[0].set_adjacent_cities([1, 2, 13])
    cities[1].set_adjacent_cities([0, 19, 13])
    cities[2].set_adjacent_cities([0, 24, 13])
    cities[3].set_adjacent_cities([14, 18, 27, 25, 8, 22, 16, 30, 9])
    cities[4].set_adjacent_cities([26, 17, 27, 7])
    cities[5].set_adjacent_cities([21, 25, 12])
    cities[6].set_adjacent_cities([12, 22, 16, 28])
    cities[7].set_adjacent_cities([4, 26, 27, 18, 14])
    cities[8].set_adjacent_cities([12, 25, 3, 22])
    cities[9].set_adjacent_cities([10, 14, 3, 30, 20, 15])
    cities[10].set_adjacent_cities([9, 11, 14])
    cities[11].set_adjacent_cities([14, 10, 23])
    cities[12].set_adjacent_cities([5, 25, 22, 8, 6])
    cities[13].set_adjacent_cities([0, 1, 2, 19, 29, 24, 17])
    cities[14].set_adjacent_cities([18, 7, 23, 26, 9, 10, 11, 3])
    cities[15].set_adjacent_cities([9, 20, 28])
    cities[16].set_adjacent_cities([6, 3, 22, 30, 20, 28])
    cities[17].set_adjacent_cities([13, 24, 26, 27, 4, 29])
    cities[18].set_adjacent_cities([7, 27, 3, 14])
    cities[19].set_adjacent_cities([1, 13, 29, 21])
    cities[20].set_adjacent_cities([16, 30, 9, 15, 28])
    cities[21].set_adjacent_cities([19, 25, 29, 5])
    cities[22].set_adjacent_cities([12, 8, 3, 16, 6])
    cities[23].set_adjacent_cities([26, 14, 11])
    cities[24].set_adjacent_cities([2, 13, 17, 26])
    cities[25].set_adjacent_cities([21, 5, 27, 29, 3, 12, 8])
    cities[26].set_adjacent_cities([24, 17, 4, 7, 14, 23])
    cities[27].set_adjacent_cities([29, 17, 4, 7, 18, 3, 25])
    cities[28].set_adjacent_cities([16, 6, 20, 15])
    cities[29].set_adjacent_cities([19, 21, 17, 13, 27, 25])
    cities[30].set_adjacent_cities([3, 16, 9, 20])
    return Country(cities)


def get_random_chromosome():
    country = create_country()
    for city in country.cities:
        city.color_number = random.choice([1, 2, 3, 4])
    chromosome = Chromosome(copy.deepcopy(country), fitness_function(country))
    return chromosome


def fitness_function(country):
    fitness = 0
    edges_number = 0
    for city in country.cities:
        for number in city.adjacent_cities_number:
            edges_number += 1
            if country.cities[number].color_number != city.color_number:
                fitness += 1
    fitness = fitness / edges_number
    return fitness


def get_random_child(current_chromosome):
    chromosome = copy.deepcopy(current_chromosome)
    rand_number = random.randint(0, 30)
    color_number = chromosome.country.cities[rand_number].color_number
    while True:
        random_color = random.choice([1, 2, 3, 4])
        if random_color != color_number:
            break
    chromosome.country.cities[rand_number].set_color(random_color)
    country = copy.deepcopy(chromosome.country)
    chromosome.set_fitness(fitness_function(country))
    return chromosome


def set_temperature(method_number, T0, k, alpha):
    if method_number == 0:
        T = T0 * pow(alpha, k)
        return T
    if method_number == 1:
        T = T0 / (1 + alpha * math.log(1 + k))
        return T
    if method_number == 2:
        T = T0 / (1 + (alpha * k))
        return T
    if method_number == 3:
        T = T0 / (1 + (alpha * k * k))
        return T


def simulated_annealing(method_number, T0, alpha):
    information = []
    best_chromosome_fitness = -1
    best_chromosome = None
    current_chromosome = get_random_chromosome()
    for k in range(number_of_iterations):
        if current_chromosome.fitness > best_chromosome_fitness:
            best_chromosome_fitness = current_chromosome.fitness
            best_chromosome = copy.deepcopy(current_chromosome)
        information.append(current_chromosome.fitness)
        T = set_temperature(method_number, T0, k, alpha)
        if T == 0:
            return current_chromosome
        next_chromosome = get_random_child(current_chromosome)
        delta_E = next_chromosome.fitness - current_chromosome.fitness
        if delta_E > 0:
            current_chromosome = next_chromosome
        else:
            probability = math.exp(delta_E / T)
            if random.random() < probability:
                current_chromosome = next_chromosome
    return best_chromosome, information


def draw_chart(information):
    x = list(range(1, number_of_iterations + 1))
    plt.scatter(x, information, color="yellow")
    plt.show()


def print_result(result):
    if result.fitness == 1.0:
        print("result founded : ")
        for i in range(31):
            print("number " + str(i + 1) + " city color number is : " + str(result.country.cities[i].color_number))
    else:
        print("best result founded : ")
        print("number of conflicts = " + str(round((1 - result.fitness) * 74)))
        for i in range(31):
            print("number " + str(i + 1) + " city color number is : " + str(result.country.cities[i].color_number))


def main():
    print("start")

    method_number = 0
    T0 = 1.0
    alpha = 0.9
    result, information = simulated_annealing(method_number, T0, alpha)
    draw_chart(information)
    print_result(result)

    print("end")


main()
