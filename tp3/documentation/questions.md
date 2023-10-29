## Pourquoi lancer le greedy algorithm 10 fois ? Il est déterministique normalement

## Est-ce que je dois noter qqp la configuration des 5 problèmes générés aléatoirement ?

## C'est quoi le metropolis rule ?

## Est-ce que la fonction random.shuffle() est impur (ne retourne rien)

---------------------------------------

## Si je crée une fonction avec un type lié, changer avec le type d'origine ne donnera pas d'erreur

Réponse: ça ne change rien

```python
A = int

def add(a: A, b: A) -> A:
    return a + b

trois: int = 3
quatre: int = 4

res = add(trois, quatre)
print("res:", res)
```

---------------------------------------

## Est-ce que je peux conserver une structure mutable dans une fonction (= le stocker dans un générateur)


```python

class MyClass():
    counter = 0

    def incr(self):
        self.counter += 1

    def __str__(self):
        return f"counter: {self.counter}"


def keep_count(f, mc: MyClass):
    def new_f():
        mc.incr()
        return f()
    return new_f


def my_function():
    return "my_function"


a = MyClass()
f = keep_count(my_function, a)

print(f())  # my_function
print(f())  # my_function
print(f())  # my_function
print(a)  # 3 


```

---------------------------------------
