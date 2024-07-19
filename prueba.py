import numpy as np
from scipy.optimize import fsolve

def calcular_coeficientes_actividad_nrtl(fracciones_liquidas, tau, alpha):
    n_componentes = len(fracciones_liquidas)
    G = np.exp(-alpha * tau)
    ln_gamma = np.zeros(n_componentes)
    
    for i in range(n_componentes):
        sum_G_ji_tau_ji_x_j = 0
        sum_G_jk_x_k = np.zeros(n_componentes)
        sum_G_ij_tau_ij_x_j = 0
        
        for j in range(n_componentes):
            sum_G_ji_tau_ji_x_j += fracciones_liquidas[j] * tau[j][i] * G[j][i]
            sum_G_jk_x_k[j] = np.sum(fracciones_liquidas * G[j])
            sum_G_ij_tau_ij_x_j += fracciones_liquidas[j] * G[i][j] * tau[i][j]
        
        ln_gamma[i] = sum_G_ji_tau_ji_x_j / np.sum(fracciones_liquidas * G[:, i]) + sum_G_ij_tau_ij_x_j / sum_G_jk_x_k[i] - np.sum(fracciones_liquidas * tau[i] * G[i] / sum_G_jk_x_k)
    
    return np.exp(ln_gamma)

def calcular_constantes_equilibrio(fracciones_liquidas, presiones_vapor_puros, matriz_coeficientes_actividad, presion_total):
    n_componentes = len(fracciones_liquidas)
    constantes_equilibrio = np.zeros(n_componentes)
    
    for i in range(n_componentes):
        constantes_equilibrio[i] = (matriz_coeficientes_actividad[i] * presiones_vapor_puros[i]) / presion_total
    
    return constantes_equilibrio

def balance_masa_energia(y, z, K, HF, HV, HL, Q, F):
    V = y[-2]
    L = y[-1]
    x = y[:-2]
    
    n_componentes = len(z)
    
    # Balances de masa de componentes
    balances_masa = np.zeros(n_componentes)
    for i in range(n_componentes):
        balances_masa[i] = F * z[i] - V * K[i] * x[i] - L * x[i]
    
    # Balance de energía
    balance_energia = Q + F * HF - V * HV - L * HL
    
    return np.append(balances_masa, balance_energia)

# Datos de entrada
fracciones_liquidas = np.array([0.2, 0.5, 0.3])  # Fracciones molares en la fase líquida
presiones_vapor_puros = np.array([100, 80, 60])  # Presiones de vapor de los componentes puros en kPa
presion_total = 101.3  # Presión total del sistema en kPa
z = np.array([0.4, 0.4, 0.2])  # Fracciones molares en la alimentación

# Parámetros NRTL (ejemplo)
tau = np.array([[0, 0.3, 0.4],
                [0.2, 0, 0.5],
                [0.1, 0.3, 0]])
alpha = np.array([[0, 0.2, 0.2],
                  [0.2, 0, 0.2],
                  [0.2, 0.2, 0]])

# Calor añadido o removido (Q en kJ)
Q = 500  # Ejemplo

# Flujos de alimentación y entalpías (HF, HV, HL en kJ/kg)
F = 100  # Flujo de alimentación (kg/h)
HF = 200  # Entalpía de la alimentación (kJ/kg)
HV = 250  # Entalpía del vapor (kJ/kg)
HL = 150  # Entalpía del líquido (kJ/kg)

# Calcular coeficientes de actividad usando el modelo NRTL
coeficientes_actividad = calcular_coeficientes_actividad_nrtl(fracciones_liquidas, tau, alpha)

# Calcular las constantes de equilibrio
constantes_equilibrio = calcular_constantes_equilibrio(fracciones_liquidas, presiones_vapor_puros, coeficientes_actividad, presion_total)

# Estimaciones iniciales para las fracciones molares en el líquido, flujo de vapor y flujo de líquido
# Asegúrate de que las fracciones sumen 1
x0 = np.array([0.3, 0.3, 0.4, 40.0, 60.0])

# Resolver balances de masa y energía
solucion = fsolve(balance_masa_energia, x0, args=(z, constantes_equilibrio, HF, HV, HL, Q, F))

# Separar las soluciones
x = solucion[:-2]
V = solucion[-2]
L = solucion[-1]

# Verificar sumas de fracciones
if not np.isclose(np.sum(x), 1):
    raise ValueError("Las fracciones molares en la fase líquida no suman 1.")

# Imprimir los resultados
print(f"Flujo de líquido L: {L:.2f} kg/h")
print(f"Flujo de vapor V: {V:.2f} kg/h")
for i, K_i in enumerate(constantes_equilibrio):
    print(f"Constante de equilibrio K_{i+1}: {K_i:.4f}")
print(f"Fracciones molares en la fase líquida: {x}")
