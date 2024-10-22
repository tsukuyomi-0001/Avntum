# Welcome
avntum syntax is quite easy and similar to python and 
bit of static types language, journey will easy so relax and learn

## variables and comments
variables can be defined as place holder in memory, programmng language like python provides automatically declare types of variable so you don't need to declare type, same goes with avntum

```
x = 5 # see this is  easy you created variable
# oh and this is comment you can write notes ;)
```
in avm (Avntum) you can create defined datatype var (variables) here's how
```
int x = 5 # easy
float y = 5.3
string z = "wow"
char a = 'a'
```

although you create static variable you can't put value of different datatype to different datatye var

```
int x = 45
x = 3 # this is valid

int z = 23
z = "hello" # this isn't valid
```

but you can do this with dynamic variables
```
a = 4
a = "a"
a = 3.1 # all are valid
```

like all other programming language avm has same naming rules

1) shouldn't start with number
2) only alpha, number and underscore

## printing and inputs
wana see what you variables stored down?
```
a = 4
print(a) # should have outputed 4
```
and what about to take inputs?
```
b = input("give me input")
print(b) # this should print out value you gave in
```

## to run script
now how do we run avm script? just run this command in powershell or terminal
```
avntum xyz.avm
```
and boom! if should do that task you writen in avm.. if you are c++ users and want to see .c++ code use
```
avntum xyz.avm -c
```

##  Conditions
want to check if some kid is 18 above or not, can do
```
a = input("age? ")
if (a>18):
    print("lets have some beer")
elif (b==18):
    print("lol you are still kid")
else:
    print("no babies are allowed")
```

## Loops
sometime you wana do repetitive task like running code until you school computer crashes than learn loops
```
i = 0
while(i<1000):
    print(i)

```
altough this script doesn't make computer crash but you can make script of your own, understand avntum and crash that computer goo boys

below is also a type of loop
```
for i in range(1000):
    print(i)
```

up till now it was easy write?
## Functions
function are block of code that can be used again and again without writing code again and again
```
func add(a,b):
    return a+b

a = 4
b = 5
print(add(a,b)) # should output 9
```

for static function
```
int add(a,b)
    return a+b
int a = 4   # remember static function will take static value and dynamic will take encoded values
int b = 5
print(add(a,b)) # should out output same 9
```

## import statement
splitting code to multiple files is always a good thing,
to do so create a file called game.avm and then create a new file called assests.avm
open game.avm and write

```
import assests
import_obj() # suppose there's a function called import_obj in assets
```

<!-- if want to import all functions, var everything than do
```
from assests import *
```
and for specific functions
```
from assests import function1
```
and to use alias name instead of original library name
```
import assests as ats # WHAT? YOU THOUGHT I WOULD WRITE SOMETHING DIFFERENT HUH?
``` -->

## In-built functions
there a few in-built functions like
1) type()
2) len()

and also for c++ coders who also want to customize generated code there are few in-built function to convert encoded value to decode 
1) decoded_string()
2) decoded_int()
3) decoded_float()

# END
as this is just version 2.0 alpha there are still version beta, gamma, delta version left to make avntum proper programable language so i wish you will suppose this language...