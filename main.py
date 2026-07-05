import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d

# =====================================================================
# SIMULADOR DE AUTÔMATOS CELULARES: FEBRE AMARELA URBANA
# Baseado em Coupled Map Lattices (CA para densidades populacionais)
# =====================================================================

def init_grid(size=50):
    """
    Inicializa a malha espacial (grid) representando a cidade.
    """
    Sh = np.ones((size, size)) * 100.0  
    Ih = np.zeros((size, size))
    Rh = np.zeros((size, size))
    
    Sv = np.ones((size, size)) * 50.0   
    Iv = np.zeros((size, size))
    
    # CRIANDO O EFEITO (A): Foco Localizado num bairro específico
    Iv[5:10, 5:10] = 20.0 
    
    return {'Sh': Sh, 'Ih': Ih, 'Rh': Rh, 'Sv': Sv, 'Iv': Iv}

def run_ca_simulation(grid, days, beta_vh, beta_hv, gamma, mu_v, vector_diffusion, human_mobility_rate):
    """
    Executa a simulação discreta temporal e espacial.
    """
    size = grid['Sh'].shape[0]
    history = {'Ih': [], 'Iv': []}
    
    Sh = grid['Sh'].copy()
    Ih = grid['Ih'].copy()
    Rh = grid['Rh'].copy()
    Sv = grid['Sv'].copy()
    Iv = grid['Iv'].copy()
    
    # Matriz de convolução (Vizinhança de Moore)
    kernel_diffusion = np.array([[0.05, 0.1, 0.05],
                                 [0.1,  0.4, 0.1 ],
                                 [0.05, 0.1, 0.05]])
    
    for t in range(days):
        history['Ih'].append(Ih.copy())
        history['Iv'].append(Iv.copy())
        
        Nh = Sh + Ih + Rh
        Nh[Nh == 0] = 1.0 
        
        # Equações Diferenciais Discretas (Sistema Acoplado SIR-SI)
        new_Ih = beta_vh * Sh * (Iv / Nh)
        new_Iv = beta_hv * Sv * (Ih / Nh) # Aqui está o beta_hv atuando!
        rec_Ih = gamma * Ih
        
        Sh = np.maximum(Sh - new_Ih, 0)
        Ih = Ih + new_Ih - rec_Ih
        Rh = Rh + rec_Ih
        
        Sv = np.maximum(Sv - new_Iv + (mu_v * 50.0) - (mu_v * Sv), 0)
        Iv = np.maximum(Iv + new_Iv - (mu_v * Iv), 0)
        
        # Convolução - Difusão do Mosquito
        Iv = convolve2d(Iv, kernel_diffusion, mode='same', boundary='wrap') * vector_diffusion + Iv * (1 - vector_diffusion)
        
        # Mobilidade Humana (Saltos Espaciais)
        if human_mobility_rate > 0:
            traveling_Ih = Ih * human_mobility_rate
            Ih = Ih - traveling_Ih
            
            flat_travelers = traveling_Ih.flatten()
            np.random.shuffle(flat_travelers)
            traveling_Ih = flat_travelers.reshape((size, size))
            
            Ih = Ih + traveling_Ih

    return history

def plot_progression(history_no_mob, history_with_mob, days_to_plot):
    """
    Gera um painel visual mostrando a PROGRESSÃO TEMPORAL da doença.
    Ideal para publicações científicas mostrando o alastramento.
    """
    num_plots = len(days_to_plot)
    fig, axes = plt.subplots(2, num_plots, figsize=(5 * num_plots, 9))
    
    # Garantir que axes é bidimensional mesmo se for apenas 1 dia
    if num_plots == 1:
        axes = axes.reshape(2, 1)

    for i, day in enumerate(days_to_plot):
        # Linha Superior: Sem Mobilidade (Apenas Mosquito)
        im1 = axes[0, i].imshow(history_no_mob['Ih'][day], cmap='hot', interpolation='nearest', vmin=0, vmax=10)
        axes[0, i].set_title(f'DIA {day} - Voo Restrito do Vetor\n(Mobilidade Humana = 0%)')
        axes[0, i].axis('off')
        
        # Linha Inferior: Com Mobilidade (Saltos Humanos)
        im2 = axes[1, i].imshow(history_with_mob['Ih'][day], cmap='hot', interpolation='nearest', vmin=0, vmax=10)
        axes[1, i].set_title(f'DIA {day} - Saltos Populacionais\n(Mobilidade Humana = 5%)')
        axes[1, i].axis('off')

    # Adicionar barra de cores geral na figura
    cbar = fig.colorbar(im2, ax=axes.ravel().tolist(), fraction=0.015, pad=0.04)
    cbar.set_label('Densidade de Humanos Infectados')

    plt.suptitle("Evolução Espaço-Temporal da Febre Amarela Urbana: Contágio Focal vs. Mobilidade Global", fontsize=16)
    plt.show()

def main():
    days_to_simulate = 60
    beta_vh = 0.6    
    beta_hv = 0.5    
    gamma = 1.0/7.0  
    mu_v = 1.0/14.0  
    vector_diffusion = 0.3 
    
    # 1. Sem mobilidade humana
    history_no_mob = run_ca_simulation(
        init_grid(), days_to_simulate, beta_vh, beta_hv, gamma, mu_v, vector_diffusion, 0.0
    )
    
    # 2. Com mobilidade humana (5%)
    history_with_mob = run_ca_simulation(
        init_grid(), days_to_simulate, beta_vh, beta_hv, gamma, mu_v, vector_diffusion, 0.05
    )
    
    # AGORA PLOTAMOS UMA SÉRIE TEMPORAL: Dias 10, 25 e 50.
    plot_progression(history_no_mob, history_with_mob, days_to_plot=[10, 25, 50])

if __name__ == '__main__':
    main()