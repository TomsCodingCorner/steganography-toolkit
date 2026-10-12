# Dit programma genereert unieke willekeurige coördinaten binnen een afbeelding.
# Het maakt gebruik van een wachtwoord en SHA-256 hashing om deze coördinaten te berekenen.
# De coördinaten zijn gegarandeerd uniek en liggen binnen de gegeven afmetingen van de afbeelding.
# Deze helper is aangepast uit extern aangeleverde code in het oorspronkelijke project.

#########################################################################

import hashlib

class RandomNumberGenerator:
    def __init__(self, image_width, image_height, password, num_coordinates):
        self.image_width = image_width
        self.image_height = image_height
        self.num_pixels = image_width * image_height
        self.password = password
        self.num_coordinates = num_coordinates
        self.generate_random_coordinates(num_coordinates)

    def generate_random_coordinates(self, count):
        if count > self.num_pixels:
            raise ValueError("Count cannot be greater than the total number of pixels")

        seed = f"{self.num_pixels}{self.password}"
        random_coordinates = set()
        ordered_coordinates = []

        for i in range(count):
            unique_seed = f"{seed}{i}"
            hash_object = hashlib.sha256(unique_seed.encode())
            hash_hex = hash_object.hexdigest()
            hash_int = int(hash_hex, 16)

            # Calculate the X and Y coordinates
            x = hash_int % self.image_width
            y = (hash_int // self.image_width) % self.image_height

            coordinate = (x, y)

            # Ensure the coordinate is unique
            while coordinate in random_coordinates:
                hash_int = (hash_int + 1) % self.num_pixels
                x = hash_int % self.image_width
                y = (hash_int // self.image_width) % self.image_height
                coordinate = (x, y)

            random_coordinates.add(coordinate)
            ordered_coordinates.append(coordinate)

        self.random_coordinates = ordered_coordinates
        return ordered_coordinates

    def getcoordinates(self):
        return self.random_coordinates

