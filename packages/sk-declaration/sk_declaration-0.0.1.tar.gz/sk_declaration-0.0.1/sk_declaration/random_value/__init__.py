import random
from nltk.corpus import words
import string

class RandomValue:

    def __init__(self):
        self.functions = [item for index,item in enumerate(dir(self)) if '__' not in item and item != 'generate' and item != 'random_data']


    def random_data(self):

        determiner = random.randint(0,len(self.functions)-1)

        function = getattr(self,self.functions[determiner])

        return function()

    def random_object(self):

        return {"name": ''.join(random.choices(string.ascii_lowercase, k=5)), "age": random.randint(18, 65)}


    def random_nested_object(self,keys = random.choices(words.words(), k=random.randint(1,5)) ,values =  random.choices(range(0,100), k=random.randint(1,5))):

        if len(keys) ==0:
            return random.choice(values)


        determiner = random.randint(0,1)
        if len(keys) ==1:
            determiner = 1


        if determiner:
            nested_dict = {keys[0]  : self.random_nested_object(keys[1:],values)}
        else:
            nested_dict = {keys[0]  :  random.choice(values), keys[1]  :  self.random_nested_object(keys[2:],values)}

        return nested_dict

    def random_json(self,depth=random.randint(1,3), max_list_length=random.randint(1,5), max_dict_length=random.randint(1,5)):
        if depth == 0:
            return random.choice([None, random.randint(0, 100), random.random(), str(random.random())])

        data_type = random.choice(["dict", "list"])

        if data_type == "dict":
            json_data = {}
            dict_length = random.randint(1, max_dict_length)
            for _ in range(dict_length):
                key = self.random_word()
                value = self.random_json(depth - 1, max_list_length, max_dict_length)
                json_data[key] = value

        else:  # data_type == "list"
            json_data = []
            list_length = random.randint(1, max_list_length)
            for _ in range(list_length):
                value = self.random_json(depth - 1, max_list_length, max_dict_length)
                json_data.append(value)

        return json_data




    def random_list(self,start=0,end=100,length=5):
        return random.choices(range(start,end+1), k=length)

    def random_nested_list(self,dimensions=[3,3,3],start=0,end=100):

        if len(dimensions) == 0:
            return None

        # Get the size of the first dimension
        size = dimensions[0]

        # Create the array with the specified dimensions
        array = [None] * size

        # Base case: if there's only one dimension, assign index values to the elements
        if len(dimensions) == 1:
            for i in range(size):
                array[i] = random.randint(start,end)
            return array

        # Recursive case: create nested arrays for each element in the first dimension
        for i in range(size):
            array[i] = self.random_nested_list(dimensions[1:])

        return array

    def random_word(self):

        word_list = words.words()
        random_word = random.choice(word_list)
        return random_word

    def random_randint(self,start =0,end = 100):
        return random.randint(start,end)

    def random_digit(self):
        return random.randint(-10000,+10000)
