import numpy as np

def ward_distance(cl1, cl2):
    """
    Calcule la distance de Ward entre deux clusters.
    Parameters:
    cl1 (np.ndarray): Un tableau de taille (n1, n) représentant les points du premier cluster.
    cl2 (np.ndarray): Un tableau de taille (n2, n) représentant les points du deuxième cluster.
    Returns:
    float: La distance de Ward entre les deux clusters.
    """
    # Nombre de points dans chaque cluster
    n1 = cl1.shape[0]
    n2 = cl2.shape[0]
    # Calcul des centroïdes des clusters
    mu_cl1 = np.mean(cl1, axis=0)
    mu_cl2 = np.mean(cl2, axis=0)
    # Distance euclidienne entre les centroïdes
    euclidean_distance = np.linalg.norm(mu_cl1 - mu_cl2)
    # Distance de Ward
    ward_dist = (n1 * n2) / (n1 + n2) * euclidean_distance**2
    return ward_dist
def variance_distance(cl1, cl2):
    """
    Calcule la variance intraclasse du cluster fusionné (Cl1 ∪ Cl2).
    Parameters:
    cl1 (np.ndarray): Un tableau de taille (n1, n) représentant les points du premier cluster.
    cl2 (np.ndarray): Un tableau de taille (n2, n) représentant les points du deuxième cluster.
    Returns:
    float: La variance intraclasse du cluster fusionné.
    """
    # Fusionner les deux clusters
    combined_cluster = np.vstack((cl1, cl2))
    # Calculer le centroïde du cluster fusionné
    mu_combined = np.mean(combined_cluster, axis=0)
    # Calculer la variance intraclasse du cluster fusionné
    variance = np.mean(np.linalg.norm(combined_cluster - mu_combined, axis=1)**2)
    return variance
def camille_distance(index_cl1,index_cl2,dem) :
    index_cluster_theorique=index_cl1 + index_cl2
    moy_cluster=np.array([])
    Matrice_cluster_therorique=[]
    for i in index_cluster_theorique :
        Matrice_cluster_therorique=Matrice_cluster_therorique + [dem[i]]
    moy_cluster=np.mean(Matrice_cluster_therorique, axis=0)
    moy_distance=0
    for i in index_cluster_theorique :
        moy_distance += np.linalg.norm(dem[i] - moy_cluster)
    similarity=moy_distance/len(index_cluster_theorique)
    return(similarity)









