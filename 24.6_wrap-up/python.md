- [Python](#python)
  - [A Compiled Language](#a-compiled-language)
  - [Type Hints](#type-hints)
  - [Generators](#generators)
  - [Operator Overloading](#operator-overloading)
- [Python Libraries](#python-libraries)
  - [Beautiful Soup](#beautiful-soup)
  - [Data science libraries](#data-science-libraries)
- [Jupyter](#jupyter)

## Python

Python is:

- a **high-level** language -> _low-level_ refers to binary
- **dynamic** -> running script can create its own funcs/classes
- dynamically-typed -> vars can swap values of different types
- strongly-typed -> language doesn't soft convert -> 'a' + 3 != 'a3' like JS
- compiled

### A Compiled Language

Python is compiled into 'bytecode' -> still a level higher than binary

### Type Hints

```py
def add(x:int,y:int) -> int:
  return x + y
```

This does not enforce types, but will give hints

```py
-> int:
# type hints the output -> python will auto-complete int methods
```

### Generators

Easy way of creating iterators in Python
Summing first 10,000 nums!  
Old way create a list:

```py
def firstn(n):
  num,nums = 0,[]
  while num < n:
    nums.append(num)
    num +=1
  return num
  sum firstn(10,000)
```

A big list like this can be memory intensive when we're not using ints!  
Here's an equivalent generator

```py
def firstngen(n):
  num = 0
  while num < n:
    yield num
    num +=1
```

Yield is like return -> but it also retains its value  
running this creates a **generator object** -> iterable

```py
#next method
it = firstngen(10)
next(it) -> 0
next(it) -> 1
next(it) -> 2
```

Python calls this itself:

```py
for n in firstngen(20):
  print(n)
```

Same return as before, but not a single massive list!

```py
sum(firstngen(1000))
```

of course we would use range() to do something like this  
but there are definitely instances where things are too big to hold in a list

### Operator Overloading

```py
3 + 3 = 6
'3' + '3' = '33'
```

This behavior is controlled by _dunder methods_ on our type objects  
We can override these methods to get special functionality

```py
def __eq__(self,other):
  return self.lower() == other.lower()
```

Now we can compare mix-case strings

## Python Libraries

Standard library is huge:

- queues and stacks
- binary search trees
- statistics
- copy operations
- regular expressions
- *data persistance*
  - pickling - **outputing data to files**
- file formats
- multiprocessing
- complex numbers, fractions, cool math stuff
- functional programming helpers

### Beautiful Soup

A lot of sites have APIs that return data.

Many don’t, and you need to **scrape** HTML to get data.

Beautiful Soup is a terrific library for this.

### Data science libraries
Numpy
- fast linear and matrix algebra
Pandas
- data slicing, grouping, etc
SciKit-Learn
- common machine learning algos
**Scipy**
## Jupyter
Jupter creates interactive reports and documentation  
Publishable in to the web!  
**Jupter notebook** is can be ran in the command line  
opens up web interface compatible with markdown, interactive codeblocks, **the works**  
