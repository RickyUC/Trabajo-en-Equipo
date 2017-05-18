__author__ = "cotehidalgov"
__coauthor__ = "Diego Andai"
# -*- coding: utf-8 -*-
import random

###############################################################################
#Solo puedes escribir código aquí, cualquier modificación fuera de las lineas
#será penalizada con nota 1.0


def eat(self, plate):
    food = isinstance(plate.food, Food)
    drink = isinstance(plate.drink, Drink)
    if food and drink:
        if plate.food.quality + plate.drink.quality > 50:
            print("Qué delicia!")
        else:
            print("Esto no es digno de mi paladar")
    elif food and not drink:
        print("Mi plato tiene dos comidas")
    else:
        print("Mi plato tiene dos bebidas")


def cook(self):
    plate = Plate()
    self.choose_food(plate)
    self.choose_drink(plate)
    return plate


class MetaPerson(type):
    def __new__(cls, name, bases, dic):
        if name == "Chef":
            dic['cook'] = cook
        elif name == "Client":
            dic["eat"] = eat
        dic["restaurant"] = str()
        if not isinstance(cls, Person):
            print("\nLa clase {0} no está heredando de Person!".format(name))
            bases = (Person,)
            print("La clase {0} está ahora heredando de Person".format(name))
        return super().__new__(cls, name, bases, dic)


def llega_cliente(self, cliente):
    if isinstance(cliente, Client):
        self.clients.append(cliente)
        print("El cliente llamado {0} se ha agregado a la lista del restaurant".format(cliente.name))
    else:
        print("El cliente a añadir no es una instancia válida de Client!")


def cliente_se_va(self, client_name):
    for client in self.clients:
        name = client.name
        if name == client_name:
            self.clients.remove(client)
            print("El cliente llamado {0} ha sido removido exitosamente!".format(client_name))


def start(self):
    if len(self.clients) != 0:
        for i in range(1):  # Se hace el estudio por 5 dias
            print("\n----- Día {} -----".format(i + 1))
            plates = []
            for chef in self.chefs:
                for j in range(3):  # Cada chef cocina 3 platos
                    plates.append(chef.cook())  # Retorna platos de comida y bebida

            for client in self.clients:
                for plate in plates:
                    client.eat(plate)
    else:
        print("\n{0} no tiene clientes, que pena".format(self.name))


class MetaRestaurant(type):
    restaurants = []
    def __new__(meta, name, bases, dic):
        dic["llega_cliente"] = llega_cliente
        dic["cliente_se_va"] = cliente_se_va
        dic["start"] = start
        return super().__new__(meta, name, bases, dic)

    def __call__(cls, name, chefs=None, clients=None):
        chefs = chefs if chefs else []
        clients = clients if clients else []
        nuevos_chefs = []
        for chef in chefs:
            #Revisa si el chef pertenece a otro restaurant
            if chef.restaurant:
                #Busca el restaurant en la lista de restaurants
                pos = MetaRestaurant.restaurants.index(chef.restaurant)
                restaurant = MetaRestaurant.restaurants[pos]
                # Si el restaurant tiene más de un chef
                if MetaRestaurant.se_puede_quitar(restaurant):
                    MetaRestaurant.quitar_chef(restaurant, chef)
                    nuevos_chefs.append(chef)
                    chef.restaurant = name
            else:
                nuevos_chefs.append(chef)
                chef.restaurant = name
        if nuevos_chefs:
            instancia = super().__call__(name, nuevos_chefs, clients)
            MetaRestaurant.restaurants.append(instancia)
            print("\nInstanciación exitosa!")
            print("Los chefs contratados por {0} son los siguientes:\n".format(name))
            for chef in chefs:
                print("* {0}".format(chef.name))
            return instancia


    def se_puede_quitar(cls, restaurant):
        if len(restaurant.chefs) > 1:
            return True
        return False

    def quitar_chef(cls, restaurant, chef):
        pos = restaurant.chefs.index(chef)
        restaurant.chefs.pop(pos)


###############################################################################
#De aquí para abajo no puedes cambiar ABSOLUTAMENTE NADA


class Person:
    def __init__(self, name):
        self.name = name


class Food:
    def __init__(self, ingredients):
        self._quality = random.randint(50, 200)
        self.preparation_time = 0
        self.ingredients = ingredients


    @property
    def quality(self):
        return self._quality * random.random()


class Drink:
    def __init__(self):
        self._quality = random.randint(5, 15)

    @property
    def quality(self):
        return self._quality * random.random()


class Restaurant(metaclass = MetaRestaurant):
    def __init__(self, name, chefs, clients):
        self.name = name
        self.chefs = chefs
        self.clients = clients


    def start(self):
        for i in range(1):  # Se hace el estudio por 5 dias
            print("----- Día {} -----".format(i + 1))
            plates = []
            for chef in self.chefs:
                for j in range(3):  # Cada chef cocina 3 platos
                    plates.append(chef.cook())  # Retorna platos de comida y bebida

            for client in self.clients:
                for plate in plates:
                    client.eat(plate)


class Pizza(Food):
    def __init__(self, ingredients):
        super(Pizza, self).__init__(ingredients)
        self.preparation_time = random.randint(5, 100)


class Salad(Food):
    def __init__(self, ingredients):
        super(Salad, self).__init__(ingredients)
        self.preparation_time = random.randint(5, 60)


class Coke(Drink):
    def __init__(self):
        super(Coke, self).__init__()
        self._quality -= 5


class Juice(Drink):
    def __init__(self):
        super(Juice, self).__init__()
        self._quality += 5


class Plate:
    def __init__(self):
        self.food = None
        self.drink = None


class Chef(Pizza, metaclass=MetaPerson):
    def __init__(self, name):
        super(Chef, self).__init__(name)

    def choose_food(self, plate):
        food_choice = random.randint(0, 1)
        ingredients = []
        if food_choice == 0:
            for i in range(3):
                ingredients.append(random.choice(["pepperoni", "piña", "cebolla", "tomate", "jamón", "pollo"]))
            plate.food = Pizza(ingredients)
        else:
            for i in range(2):
                ingredients.append(random.choice(["crutones", "espinaca", "manzana", "zanahoria", "palta"]))
            plate.food = Salad(ingredients)

    def choose_drink(self, plate):
        drink_choice = random.randint(0, 1)
        if drink_choice == 0:
            plate.drink = Coke()
        else:
            plate.drink = Juice()


class Client(Pizza, metaclass=MetaPerson):
    def __init__(self, name):
        super(Client, self).__init__(name)


if __name__ == '__main__':

    chefs = [Chef("Enzo"), Chef("Nacho"), Chef("Diego")]
    clients = [Client("Bastian"), Client("Flori"),
                Client("Rodolfo"), Client("Felipe")]
    McDollars = Restaurant("Mc", chefs, clients)

    BurgerPimp = Restaurant("BK")

    KFK = Restaurant("KFK", [Chef("Enzo")])

    McDollars.start()
    KFK.start()
