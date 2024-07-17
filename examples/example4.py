import sys

class Pet:
    def __init__(self, animal_type):
        self.animal_type = animal_type
        self.supported = {"dog", "cat", "duck", "pig"}

    def is_supported(self):
        return self.animal_type in self.supported

    def make_sound(self):
        if self.animal_type == "dog":
            return "Woof!"
        elif self.animal_type == "cat":
            return "Meaw!"
        elif self.animal_type == "duck":
            return "Quack!"
        elif self.animal_type == "pig":
            return "Oink!"

animals = sys.argv[1:]

for animal in animals:
    pet = Pet(animal)
    if not pet.is_supported():
        break
    else:
        print(pet.make_sound())
