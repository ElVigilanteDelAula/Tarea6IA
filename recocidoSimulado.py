import random
import math
import timeit



def generate_knapsack_instance(num_items, max_value, max_weight):
    values = [random.randint(1, max_value) for _ in range(num_items)]
    weights = [random.randint(1, max_weight) for _ in range(num_items)]
    max_capacity = random.randint(sum(weights) // 2, sum(weights))
    return values, weights, max_capacity

# Función para evaluar la solución actual
def eval_solution(solution, values, weights, max_weight):
    total_value = 0
    total_weight = 0
    for i in range(len(solution)):
        if solution[i] == 1:
            total_value += values[i]
            total_weight += weights[i]
    if total_weight > max_weight:
        return 0
    else:
        return total_value

# Función para generar una solución aleatoria
def generate_random_solution(num_items):
    solution = [random.randint(0, 1) for _ in range(num_items)]
    return solution

# Función para generar una vecindad de soluciones
def generate_neighborhood(current_solution):
    neighborhood = []
    for i in range(len(current_solution)):
        neighbor = list(current_solution)
        neighbor[i] = 1 - neighbor[i]
        neighborhood.append(neighbor)
    return neighborhood

# Función para calcular la probabilidad de aceptar una solución peor
def acceptance_probability(old_value, new_value, temperature):
    if new_value > old_value:
        return 1.0
    else:
        return math.exp((new_value - old_value) / temperature)

# Función principal del algoritmo de recocido simulado
def simulated_annealing(values, weights, max_weight, initial_temperature, cooling_rate):
    # Inicialización
    current_solution = generate_random_solution(len(values))
    best_solution = list(current_solution)
    temperature = initial_temperature
    
    # Bucle principal
    while temperature > 1:
        # Generar vecindad
        neighborhood = generate_neighborhood(current_solution)
        
        # Evaluar vecinos y seleccionar uno al azar
        neighbor = random.choice(neighborhood)
        neighbor_value = eval_solution(neighbor, values, weights, max_weight)
        
        # Evaluar solución actual
        current_value = eval_solution(current_solution, values, weights, max_weight)
        
        # Calcular probabilidad de aceptar solución peor
        probability = acceptance_probability(current_value, neighbor_value, temperature)
        
        # Actualizar solución actual o aceptar una peor con cierta probabilidad
        if probability > random.random():
            current_solution = neighbor
            
        # Actualizar mejor solución encontrada
        if eval_solution(current_solution, values, weights, max_weight) > eval_solution(best_solution, values, weights, max_weight):
            best_solution = list(current_solution)
        
        # Enfriar temperatura
        temperature *= cooling_rate
    
    return best_solution, eval_solution(best_solution, values, weights, max_weight)
 
 # Ejemplo de uso
start = timeit.default_timer()
numeroDeItems = 500 
beneficioMaximo = 10000  
pesoMaximo = 5000
valoresDeItems, pesoDeItems, capacidadMochila = generate_knapsack_instance(numeroDeItems, beneficioMaximo, pesoMaximo)
initial_temperature = 6000
cooling_rate = 0.95

best_solution, best_value = simulated_annealing(valoresDeItems, pesoDeItems, capacidadMochila, initial_temperature, cooling_rate)
stop = timeit.default_timer()
print("Mejor solución encontrada:", best_solution)
print("Valor de la mejor solución encontrada:", best_value)
print('Time: ', stop - start)
