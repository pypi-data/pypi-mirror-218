import regex as re
from .random_value import RandomValue

class DeclarationGenerator:

    def __init__(self):
        self.reandom_value = RandomValue()
        self.functions = self.reandom_value.functions


    def process(self,template):

        declaraion_list = self.get_declaration_list(template)

        declaraion_list = self.call_random_functions(declaraion_list)

        declaraion_text = self.process_list(declaraion_list)
        return  declaraion_text



    def get_declaration_list(self,template):
        pattern = r'(?:\n)?(.*?)(?:=)(.*)'

        declaration_list = re.findall(pattern,template)
        temp = []
        for variable,expression in declaration_list:
            temp += [(variable.replace(' ',''),expression)]

        declaration_list = temp
        return declaration_list

    def call_random_functions(self,declaration_list):
        temp = []
        for variable,expression in declaration_list:
            pattern = r'([a-zA-z]+)\s*(\((?:[^()]+|(?R))*\))'
            functions = re.findall(pattern,expression)
            value = expression

            for function_call in functions:
                if function_call[0] in self.functions or function_call[0]=='random_data':

                    function,arguments = function_call

                    result  = eval(f"self.reandom_value.{function}{arguments}")
                    pattern = re.escape(function)+r'(\s|\b)*'+re.escape(arguments)

                    value = re.sub(pattern,str(result),expression)

            temp += [(variable,value)]
        return temp

    def process_list(self,declaration_list):
        declarations_text =''
        for variable,expression in declaration_list:
            variable = variable if variable.startswith('$')  else '$'+variable

            for v,e in declaration_list:
                v = v.replace('$','') if v.startswith('$')  else v
                expression = re.sub(r'(?=\b|\s|^)([^\$])'+re.escape(v)+r'(?=\b|\s|$)',f'${v}',expression)



            declarations_text += f"{variable} = {expression};\n"
        return declarations_text
    def get_help(self):

        text ='''The program generates random data using various functions you can  assign them to variables. Here is a description of the program and how the functions are called with their arguments:

1. `random_data()`:
   - Function: Generates random data.
   - No arguments provided.
   - Returns: Random data.

2. `random_word()`:
   - Function: Generates a random word.
   - No arguments provided.
   - Returns: Random word.

3. `random_list()`:
   - Function: Generates a random list of numbers within a specified range or with a specified length.
   - Arguments:
     - Optional arguments:
       - `start` (default: 0): Starting value of the range.
       - `end` (default: 100): Ending value of the range.
       - `length` (default: None): Length of the list. If specified, overrides the range.
   - Returns: Random list of numbers.

4. `random_nested_list()`:
   - Function: Generates a random nested list of numbers with specified dimensions.
   - Arguments:
     - `dimensions`: A list specifying the dimensions of the nested list.
   - Returns: Random nested list of numbers.

5. `random_nested_object()`:
   - Function: Generates a random nested object with specified keys and corresponding values.
   - Arguments:
     - `keys`: A list of keys for the nested object.
     - `values`: A list of values corresponding to the keys.
   - Returns: Random nested object.

6. `random_json()`:
   - Function: Generates random JSON data with optional depth.
   - Arguments:
     - Optional argument:
       - `depth` (default: 1): Specifies the depth of the nested JSON structure.
   - Returns: Random JSON data.
Example:
    input:
x = random_data()

y = random_word()

z = random_list()

a = random_nested_list()

b = random_nested_object()

c = random_json()

k = random_list(0,1,5)

q = random_list(start =1,end = 10, length = 3)
w = random_nested_list(dimensions = [2,3,3])
r = random_nested_object(keys = ['x','y','z','a','b','c'],values = [2,3,4,5,6])
t = random_json(depth=2)

$a = 1+ random_json   ();
x =1+ random_digit()

output :
$x =  {'nosewheel': [None, None]};
$y =  sequestrectomy;
$z =  [14, 98, 98, 32, 42];
$a =  [[[5, 14, 52], [17, 39, 34], [24, 88, 29]], [[96, 74, 72], [45, 20, 51], [50, 85, 67]], [[68, 63, 97], [42, 86, 26], [65, 63, 83]]];
$b =  {'rookie': {'trunkfish': 57, 'infracostalis': 57}};
$c =  {'overpartially': {'homotatic': 0.023304651717117153}};
$k =  [0, 1, 1, 0, 1];
$q =  [6, 7, 2];
$w =  [[[97, 42, 71], [26, 54, 59], [20, 60, 82]], [[26, 96, 87], [9, 53, 12], [90, 18, 2]]];
$r =  {'x': {'y': 2, 'z': {'a': 5, 'b': {'c': 4}}}};
$t =  [[None, '0.5497858420290839'], [0.08433649013358602]];
$a =  1+ [{'tuskish': '0.7731976907294389'}];
$x = 1+ -1390
The program assigns the generated random data to variables using the assignment operator (`=`). The variables are named `x`, `y`, `z`, `a`, `b`, `c`, `k`, `q`, `w`, `r`, and `t`. The dollar sign (`$`) is prefixed to the variable names in the output for clarity.
 '''

        return text

##declaration = DeclarationGenerator()
##declaration.generate
##('''
##
##x = random_data()
##
##y = random_word()
##
##z = random_list()
##
##a = random_nested_list()
##
##b = random_nested_object()
##
##c = random_json()
##
##k = random_list(0,1,5)
##
##q = random_list(start =1,end = 10, length = 3)
##w = random_nested_list(dimensions = [2,3,3])
##r = random_nested_object(keys = ['x','y','z','a','b','c'],values = [2,3,4,5,6])
##t = random_json(depth=2)
##
##$a = 1+ random_json   ();
##x =1+ random_digit()

##''')




