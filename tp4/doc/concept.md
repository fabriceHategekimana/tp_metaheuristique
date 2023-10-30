Il y a m fourmis qui vont traverser un chemin.
Ces fourmis laissent des phéromones en passant.
Ces phéromones pousseront plus les autres fourmis à suivre s'ils sont plus fort.

Pour chaque choix, une fourmi caclule la probabilité d'aller dans un point par ces deux critères:
- Distance
- Puissance des phéromones

Ant System algorithm (AS)
t = iteration
k = ant
ant_k (city_i to city_j)
p_kij 
J = set of cities not yet visited by ant K
eta(i,j) = 1/distance(i,j)
tau(i,j,t) = intensity of the path between i and j at iteration t.
tau(i,j) = pheromone associated with the edge joining cities i and j
alpha and beta = relative importance control
*1 : tau(i,j,t+1) = (1-rho) tau(i,j,t) + sum(delta(tau(k, i, j, t)))
rho = evaporation_rate
quantity_of_pheromone_laid_on_edge(i, j) by ant k = {
	if ant k used edge (i, j) in its tour
		return Q/L(k, t)
	else:
		return 0
}
Q = constant (nothing else)
L(k, t) = length of the tour constructed by ant k.
tau(0) >= 0 
L(n,n) = possible solution determined by using the nearest neighbour algorithm
function =  AS(m, t_max)
# initialisation
alpha = 1
beta = 5
rho = 0.1
Q = L(n,n)
tau = 1/L(n,n)
For each iteration:
	update_pheromones(ants) : *1
tau = pheromone
