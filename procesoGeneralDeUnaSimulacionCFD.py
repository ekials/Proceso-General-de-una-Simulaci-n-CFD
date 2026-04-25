
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from scipy.linalg import solve_banded
import warnings
warnings.filterwarnings('ignore')

plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.titlesize': 12,
    'axes.labelsize': 11,
    'legend.fontsize': 9,
    'figure.dpi': 150,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'savefig.bbox': 'tight',
})

AZUL   = '#1a6eb5'
ROJO   = '#e05a2b'
VERDE  = '#27a060'
GRIS   = '#555555'
MORADO = '#7b2d8b'


def _guardar(nombre, dpi=150, mostrar=False, tight=True):
    """Guarda la figura actual en PNG y la cierra.

    nombre: nombre de archivo sin extensión
    dpi: resolución de la imagen
    mostrar: si True llama a `plt.show()` antes de cerrar
    tight: si True aplica `plt.tight_layout()` antes de guardar
    """
    if tight:
        try:
            plt.tight_layout()
        except Exception:
            pass
    fname = f"{nombre}.png"
    plt.savefig(fname, dpi=dpi)
    print(f"Guardado: {fname}")
    if mostrar:
        plt.show()
    plt.close()

#  SIM 1 — Proceso CFD: Geometría → Mallado → Condiciones de frontera

def sim1_proceso_mallado():
    """
    Visualiza los pasos del proceso CFD usando una tubería 2D como ejemplo.
    Muestra: (a) geometría, (b) malla estructurada, (c) condiciones de frontera.
    """
    fig, axes = plt.subplots(1, 3, figsize=(13, 4))

    #geometria
    ax = axes[0]
    ax.set_xlim(-0.1, 2.1); ax.set_ylim(-0.6, 0.6)
    ax.set_aspect('equal')
    rect = mpatches.FancyBboxPatch((0, -0.4), 2, 0.8,
                                   boxstyle="round,pad=0.02",
                                   fc='#ddeeff', ec=AZUL, lw=2)
    ax.add_patch(rect)
    ax.text(1, 0, 'Dominio fluido', ha='center', va='center',
            fontsize=10, color=AZUL)
    ax.text(1, -0.53, 'Tubería circular — sección 2D', ha='center',
            fontsize=9, color='gray')
    ax.axis('off')
    ax.set_title('Paso 1: Geometría', fontweight='bold')

    #malla
    ax = axes[1]
    Nx, Ny = 16, 8
    x = np.linspace(0, 2, Nx + 1)
    y = np.linspace(-0.4, 0.4, Ny + 1)
    for xi in x:
        ax.plot([xi, xi], [-0.4, 0.4], color='#6699cc', lw=0.8)
    for yi in y:
        ax.plot([0, 2], [yi, yi], color='#6699cc', lw=0.8)
    # Nodos
    xg, yg = np.meshgrid(x, y)
    ax.plot(xg, yg, 'o', color=AZUL, ms=2.5, alpha=0.7)
    ax.set_xlim(-0.1, 2.1); ax.set_ylim(-0.55, 0.55)
    ax.set_aspect('equal')
    ax.text(1, -0.51,
            f'Malla estructurada: {Nx}×{Ny} = {Nx*Ny} celdas',
            ha='center', fontsize=9, color='gray')
    ax.axis('off')
    ax.set_title('Paso 2: Mallado', fontweight='bold')

#cond frontera
    ax = axes[2]
    ax.set_xlim(-0.3, 2.4); ax.set_ylim(-0.65, 0.65)
    ax.set_aspect('equal')
    rect2 = mpatches.FancyBboxPatch((0, -0.4), 2, 0.8,
                                    boxstyle="round,pad=0.02",
                                    fc='#f5f5ff', ec='#aaa', lw=1.5)
    ax.add_patch(rect2)

    # Entrada: flechas de velocidad
    for y_arr in np.linspace(-0.3, 0.3, 5):
        ax.annotate('', xy=(0.25, y_arr), xytext=(-0.15, y_arr),
                    arrowprops=dict(arrowstyle='->', color=VERDE, lw=1.5))
    ax.text(-0.22, 0, 'Entrada\n$u = u_0$', ha='center',
            fontsize=8, color=VERDE, va='center')

    # Salida: presiom
    ax.annotate('', xy=(2.35, 0), xytext=(2.0, 0),
                arrowprops=dict(arrowstyle='->', color=ROJO, lw=1.5))
    ax.text(2.38, 0, 'Salida\n$p=0$', ha='left',
            fontsize=8, color=ROJO, va='center')

    # Paredes: 
    ax.plot([0, 2], [0.4, 0.4], color='#333', lw=3)
    ax.plot([0, 2], [-0.4, -0.4], color='#333', lw=3)
    ax.text(1, 0.47, 'Pared: $\\vec{u}=0$ (no deslizamiento)',
            ha='center', fontsize=8, color='#333')

    ax.axis('off')
    ax.set_title('Paso 3: Condiciones de frontera', fontweight='bold')

    fig.suptitle('Proceso CFD — Definición del problema', fontsize=13,
                 fontweight='bold', y=1.01)
    plt.tight_layout()
    _guardar('sim1_malla_cfd')



if __name__ == '__main__':
    print('\n' + '═'*60)
    print('  Simulaciones — Parte 5: Metodología Computacional (CFD)')
    print('  Física Computacional — UCSP')
    print('═'*60 + '\n')

    print('[1/7] Proceso CFD: geometría y mallado')
    sim1_proceso_mallado()
