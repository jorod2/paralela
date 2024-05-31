#kaggle data visualization esta bien, seaborn y matplotlib

import numpy as np

from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn import metrics
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
from sklearn.datasets import make_blobs

archivo1 = "/home/jorgedebian/Downloads/Personas_de_villa_laminera.txt"

##### APARTADO 1 #####

#cargamos los datos en X. Da un array de arrays de dim 2.
X = np.loadtxt(archivo1,skiprows=1)



#Graficamos los datos.
#plt.plot(X[:,0],X[:,1],'ro', markersize=1)
#plt.show()

#Vamos a almacenar los coefs de Silhouette en el vector v_sil
#y para graficarlos el numero de clusters en v_clus
v_clus = []
v_sil = []
for i in range(2, 16):

    n_clusters = i
    #aqui añado n_init ya que me salia un warning al ejecutar
    kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init = 10).fit(X)
    labels = kmeans.labels_
    silhouette = metrics.silhouette_score(X, labels)
    v_clus.append(n_clusters) 
    v_sil.append(silhouette)


#Hacemos una grafica. En esta observamos que el que mayor coeficiente de silhouette tiene es 
#el que tiene 3 clusters.
plt.plot(v_clus[:], v_sil[:],'ro')
plt.xlabel("Número de vecindades")
plt.ylabel("Coeficiente de Silhouette")
plt.show()

##Ahora hacemos Kmeans con 3 clusters.
n_clusters = 3
kmeans = KMeans(n_clusters=3, random_state=0, n_init = 10).fit(X)
labels = kmeans.labels_
silhouette = metrics.silhouette_score(X, labels)
print(f"El coeficiente de de Silhouette para Kmeans con la métrica euclidea es: {silhouette}")
centroides = kmeans.cluster_centers_ #Añado los centroides para el diagrama de Voronoi


##Añadimos aqui parte del apartado 3 para tenerlo en la grafica
problem = np.array([[1/2, 0], [0, -3]])#a y b
clases_pred = kmeans.predict(problem)
print(f"El punto a tendría la etiqueta {clases_pred[0]} y el punto b {clases_pred[1]}")
##############################################################

vor = Voronoi(centroides)

unique_labels = set(labels)
colors = [plt.cm.Spectral(each)
          for each in np.linspace(0, 1, len(unique_labels))]

fig, ax = plt.subplots(figsize=(8,4))

#plt.figure(figsize=(8,4))


for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = [0, 0, 0, 1]

    class_member_mask = (labels == k)

    xy = X[class_member_mask]
    ax.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=5)

ax.plot(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:,1],'o', markersize = 10,
            markeredgecolor='yellow', markerfacecolor = "purple")
ax.plot(problem[:,0],problem[:,1],'o', markersize=12, markerfacecolor="red")

voronoi_plot_2d(vor,show_vertices=False, show_points=False, ax = ax)

ax.axis([-4,4,-4,4])
plt.title('Numero fijo de vecindades en Kmeans: %d' % n_clusters)
plt.xlabel("Estrés")
plt.ylabel("Afición a los dulces")
plt.show()


##### APARTADO 2 #####

# Clasifiquemos ahora los datos mediante DBSCAN

#Voy a hacer 30 medidas para ver el coeficiente de Silhouette
epsilon = 0.1

l_eps = []
l_sil = []

for i in range(0,31):
    db = DBSCAN(eps=epsilon, min_samples=10, metric='euclidean').fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
    
    #Calculamos el numero de clustters y de ruido de haberlo
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)
    
    #añadimos nuestro epsilon y los coef de sil para graficar
    l_eps.append(epsilon)
    l_sil.append(metrics.silhouette_score(X, labels))
    
    #seguimos añadiendo epsion
    epsilon += 0.01

#Descomentar para ver datos exactos de la grafica
#for i in range(len(l_eps)):
#    print(f"epsilon: {l_eps[i]}, coef sil: {l_sil[i]}")

#El coeficiente de Silhouette se maximiza en eps = 0.32 con s = 0.5635701646775091
plt.plot(l_eps[:], l_sil[:])
plt.xlabel("Umbral mínimo de la distancia")
plt.ylabel("Coeficiente de Silhouette")
plt.show()


##Hacemos el DBSCANS con el mejor resultado
epsilon = 0.32

db = DBSCAN(eps=epsilon, min_samples=10, metric='euclidean').fit(X)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)



unique_labels = set(labels)
colors = [plt.cm.Spectral(each)
          for each in np.linspace(0, 1, len(unique_labels))]

plt.figure(figsize=(8,4))
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = [0, 0, 0, 1]

    class_member_mask = (labels == k)

    xy = X[class_member_mask & core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=5)

    xy = X[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=3)

plt.title('Estimated number of DBSCAN clusters: %d' % n_clusters_)
plt.xlabel("Estrés")
plt.ylabel("Afición a los dulces")
plt.show()


#### Metrica Manhattan

# Clasifiquemos ahora los datos mediante DBSCAN

#Voy a hacer 30 medidas para ver el coeficiente de Silhouette
epsilon = 0.1

l_eps = []
l_sil = []

for i in range(0,31):
    db = DBSCAN(eps=epsilon, min_samples=10, metric='manhattan').fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
    
    #Calculamos el numero de clustters y de ruido de haberlo
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)
    
    #añadimos nuestro epsilon y los coef de sil para graficar
    l_eps.append(epsilon)
    l_sil.append(metrics.silhouette_score(X, labels))
    
    #seguimos añadiendo a epsion
    epsilon += 0.01

#Descomentar para ver datos exactos de la grafica
#for i in range(len(l_eps)):
#    print(f"epsilon: {l_eps[i]}, coef sil: {l_sil[i]}")

#El coeficiente de Silhouette se maximiza en eps = 0.4 con s = 0.5665175865117323
plt.plot(l_eps[:], l_sil[:])
plt.xlabel("Umbral mínimo de la distancia")
plt.ylabel("Coeficiente de Silhouette")
plt.show()


## Hacemos el DBSCANS con el mejor resultado
epsilon = 0.4

db = DBSCAN(eps=epsilon, min_samples=10, metric='manhattan').fit(X)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)



unique_labels = set(labels)
colors = [plt.cm.Spectral(each)
          for each in np.linspace(0, 1, len(unique_labels))]

plt.figure(figsize=(8,4))
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = [0, 0, 0, 1]

    class_member_mask = (labels == k)

    xy = X[class_member_mask & core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=5)

    xy = X[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=3)

plt.title('Estimated number of DBSCAN clusters: %d' % n_clusters_)
plt.xlabel("Estrés")
plt.ylabel("Afición a los dulces")
plt.show()

