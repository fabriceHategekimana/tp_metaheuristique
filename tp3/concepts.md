# objective function

Minimisation

of(x) = delta_energy() = E_next - E_current > 0
of(x) = delta_energy() = E_next - E_current < 0 // on veut accepter ça


P(accept Next) = exp(deltaE/Temperature)

- La température diminue la probalité
- L'énergie l'autmente 

```r
E = 1  # augmente
T = 1  # diminue
y = exp(E/T)
y

# E T
# 1 1 -> 2.71
# 2 1 -> 7.38
# 1 2 -> 1.64
```

Techniquement, la température nous permet de choisir lintensité entre:
- optimisation
- exploration

Comme pour le métale dans une forgerie, une forte température laisse beaucoup de maléabilité au métal.


