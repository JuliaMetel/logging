import types

class A:
    def __init__(self):
        self.a = 4

B = A()

def function1():
    pass

print(function1.__name__)
print(A.__name__)
print(B.__class__)

int1 = 89
float1 = 6.9
str1 = 'Wow'
bool1 = True
tuple1 = (6,7,8,9,0)
list1 = [3,2,1]
set1 = {1,2,3,4,5}
dict1 = {'key1': 1, 'key2':2}
func1 = function1


print('Int:' + str(isinstance(int1, object)))
print('Float:' + str(isinstance(float1,float)))
print('String:' + str(isinstance(str1,str)))
print('Bool:' + str(isinstance(bool1,bool)))
print('Tuple:' + str(isinstance(tuple1,tuple)))
print('List:' + str(isinstance(list1,list)))
print('Set:' + str(isinstance(set1,set)))
print('Dict:' + str(isinstance(dict1,dict)))
print('Function:' + str(isinstance(range(1),types.FunctionType)))
print('Object:' + str(isinstance(B,object)))
print('Class:' + str(isinstance(A,object)))
