import numpy as np
import matplotlib.pyplot as plt

# L'anomalie moyenne M (en radian), proportionnelle au temps, permet
# d'obtenir l'anomalie excentrique E (en radian)
# (résolution itérative de l'équation de Kepler M=E-e*sin(E))
# puis l'anomalie vraie V (en radian)


def eq_kepler(M, e):
    E = np.pi
    M = np.remainder(M, 2*np.pi)
    for n in range(5):
        E = (M-e*(E*np.cos(E)-np.sin(E)))/(1-e*np.cos(E))
    return E


def calc_anom_vraie(E, e):
    V = 2*np.arctan(np.sqrt((1+e)/(1-e))*np.tan(E/2))
    return V

# S0 : constante solaire (en W/m^2)
# Epsilon : inclinaison de l'axe de rotation terrestre (en degré)
# W : longitude écliptique du Soleil au périhélie (en degré)
# M0 : anomalie moyenne au 1er janvier (en degré)
# e : excentricité de l'orbite terrestre
# Les paramètres par défaut sont ceux permettant de décrire
# le mouvement apparent du Soleil au cours d'une année.


def calcul_eclairement(S0=1365, Epsilon=23.44, W=282.99, M0=356.83, e=0.0167):
    Epsilon = Epsilon*np.pi/180.0
    W = W*np.pi/180.0
    pas_calc = 0.2
    M_liste = np.pi*(np.arange(0, 360, pas_calc)+M0)/180
    E = [eq_kepler(M_liste[k], e) for k in range(len(M_liste))]
    V = np.array([calc_anom_vraie(E[k], e) for k in range(len(E))])
    Lambda, Phi = np.meshgrid(V+W, np.pi*np.arange(-90, 90, pas_calc)/180)
    M, Phi = np.meshgrid(M_liste, np.pi*np.arange(-90, 90, pas_calc)/180)
    Delta = np.arcsin(np.sin(Lambda)*np.sin(Epsilon))
    un_sur_r = (1+e*np.cos(Lambda-W))/(1-e**2)
    cosH0 = -np.tan(Phi)*np.tan(Delta)
    cosH0[np.where(cosH0 > 1)] = 1
    cosH0[np.where(cosH0 < -1)] = -1
    H0 = np.arccos(cosH0)
    PM = S0*un_sur_r**2 * (H0*np.sin(Phi)*np.sin(Delta) +
                           np.cos(Phi)*np.cos(Delta)*np.sin(H0))/np.pi
    H0 = H0*180/np.pi
    M = M*180/np.pi
    Phi = Phi*180/np.pi
    return PM, H0, M, Phi, M0


def trace_resultat(PM, H0, M, Phi, M0):

    fig, ax = plt.subplots(figsize=(10, 5))
    CS = ax.contour((M-M0)*365.25/360, Phi, PM,
                    np.arange(0, np.max(PM)+100, 50), cmap='plasma')
    ax.clabel(CS, CS.levels, inline=True, fontsize=8)
    ax.set_xlabel('Temps (en jours depuis le 1er janvier 2024)')
    ax.set_ylabel('Latitude (en degré)')
    ax.set_title('Eclairement moyen journalier (en $W/m^2$)')
    plt.axis('equal')
    plt.xticks(np.arange(0, 361, 30))
    plt.yticks(np.arange(-90, 91, 10))
    plt.grid('on')

    fig, ax = plt.subplots(figsize=(10, 5))
    CS = ax.contour((M-M0)*365.25/360, Phi, 24*H0/180,
                    [0, 7, 8, 9, 10, 11, 11.5, 12, 12.5, 13, 14, 15, 16, 17, 23.99, 30], cmap='plasma')
    ax.clabel(CS, CS.levels, inline=True, fontsize=8)
    ax.set_xlabel('Temps (en jours depuis le 1er janvier 2024)')
    ax.set_ylabel('Latitude (en degré)')
    ax.set_title('Durée du jour (en h)')
    plt.axis('equal')
    plt.xticks(np.arange(0, 361, 30))
    plt.yticks(np.arange(-90, 91, 10))
    plt.grid('on')

    plt.show()
