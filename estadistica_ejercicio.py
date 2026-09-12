import pandas as pd
import math
import matplotlib.pyplot as plt
from scipy.stats import kstest, norm, ttest_ind, t, f
import numpy as np

#primero cargamos los datos 
ruta_archivo = "datosejercicioevaluacionanchuras.xlsx"  # Cambia por la ruta de tu archivo
df = pd.read_excel(ruta_archivo)


#EJERCICIO 1
#apartado a)
epoca1 = df[df["Época histórica"]==1]
anchura_epoca1 = epoca1["Anchura del cráneo"]
#print(epoca1)

epoca2 = df[df["Época histórica"]==2]
anchura_epoca2 = epoca2["Anchura del cráneo"]
#print(epoca2)

#medidas de centralizacion: media, moda, mediana y cuartiles
def centralizacion_epoca(data):
    anchura_epoca = data["Anchura del cráneo"]
    media = anchura_epoca.mean()
    moda = anchura_epoca.mode()[0]
    mediana = anchura_epoca.median()
    cuartil1, cuartil2, cuartil3 = anchura_epoca.quantile([0.25,0.5, 0.75])
    return media, moda, mediana, cuartil1, cuartil2 , cuartil3

media1, moda1, mediana1, cuartil1_1, cuartil2_1, cuartil3_1 = centralizacion_epoca(epoca1)
media2, moda2, mediana2, cuartil1_2, cuartil2_2, cuartil3_2 = centralizacion_epoca(epoca2)
frecuencia_moda1 = anchura_epoca1.value_counts()[moda1]
frecuencia_moda2 = anchura_epoca2.value_counts()[moda2]
print(frecuencia_moda1)
print(frecuencia_moda2)
#medidas de dispersion
def dispersion_epoca(df):
    anchura_epoca = df["Anchura del cráneo"]
    rango = anchura_epoca.max() - anchura_epoca.min()
    varianza = anchura_epoca.var()
    desv_tipica = math.sqrt(varianza)
    coef_person = desv_tipica/anchura_epoca.mean()
    return rango, varianza, desv_tipica, coef_person

rango1, varianza1, desv_tipica1, coef_person1 = dispersion_epoca(epoca1)
rango2, varianza2, desv_tipica2, coef_person2 = dispersion_epoca(epoca2)

def asimetria_y_curtosis(df):
    anchura_epoca = df["Anchura del cráneo"]
    media = anchura_epoca.mean()
    desviacion_tipica = anchura_epoca.std() 
    n = len(anchura_epoca)

    suma_cubos = sum((elem - media) ** 3 for elem in anchura_epoca)
    suma_cuarta = sum((elem-media) **4 for elem in anchura_epoca)
    
    asimetria = suma_cubos / (n * desviacion_tipica ** 3)
    curtosis = suma_cuarta/ (n * desviacion_tipica ** 2) - 3
    
    return asimetria, curtosis

asimetria1, curtosis1 = asimetria_y_curtosis(epoca1)
asimetria2, curtosis2 = asimetria_y_curtosis(epoca2)

#otra sol para la asimetria: asimetria = filtro["Anchura del cráneo"].skew()
#curtosis = filtro["Anchura del cráneo"].kurt()
#cajas y bigotes
plt.boxplot([anchura_epoca1, anchura_epoca2], labels=["Época 1", "Época 2"])
plt.title("Diagramas de Cajas y Bigotes por Época Histórica")
plt.ylabel("Anchura del Cráneo")
plt.show()

#apartado b
# Realizar el test de Kolmogorov-Smirnov para cada submuestra
ks_epoca1 = kstest(anchura_epoca1, 'norm', args=(media1, desv_tipica1))
ks_epoca2 = kstest(anchura_epoca2, 'norm', args=(media2, desv_tipica2))

print("Test KS para Época 1:")
print(f"Estadístico KS: {ks_epoca1.statistic}, p-valor: {ks_epoca1.pvalue}\n")

print("Test KS para Época 2:")
print(f"Estadístico KS: {ks_epoca2.statistic}, p-valor: {ks_epoca2.pvalue}")

#Para la primera se rechaza H_{0}, para la segunda no. E.d la primera no sigue distribucion normal
#y para la segunda no tenemos evidencias suficientes para decir que no sigue la normal

###EJERCICIO 2
#apartado a: INTERVALOS DE CONFIANZA
niveles = [0.9, 0.95, 0.99]
m, n = len(anchura_epoca1), len(anchura_epoca2)
for nivel in niveles:
    alpha = 1 - nivel
    grados_libertad = m + n - 2
    t_alpha2 = t.ppf(1 - alpha / 2, grados_libertad)

    error_estandar = np.sqrt(varianza1 / m + varianza2 / n)
    dif_medias = media1 - media2
    limite_inferior = dif_medias - t_alpha2 * error_estandar
    limite_superior = dif_medias + t_alpha2 * error_estandar
    print(f"Intervalo de confianza al {nivel} para la diferencia de medias: ({limite_inferior:.2f}, {limite_superior:.2f})")
F = varianza1 / varianza2 if varianza1 > varianza2 else varianza2 / varianza1
p_valor = 2*(1 - f.cdf(F, m-1, n-1))
print(f"Estadístico F calculado: {F:.2f}")
print(f"p-valor: {p_valor:.4f}")


#apartado b 

# Realizar el test t de Student para muestras independientes
S_c = (m * varianza1 + n * varianza2) / (m + n - 2)

t_stat = abs(media1 - media2) / np.sqrt(S_c* (1/m + 1/n))


grados_libertad = m + n - 2

t_critical = t.ppf(1 - alpha/2, grados_libertad)

p_valor = 2 * (1 - t.cdf(t_stat, grados_libertad))


print(f"Estadístico t: {t_stat:.4f}")
print(f"Valor crítico t: {t_critical}")
print(f"p-valor: {p_valor:.6f}")

