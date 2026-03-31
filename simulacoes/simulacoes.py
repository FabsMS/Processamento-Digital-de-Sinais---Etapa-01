"""
=============================================================================
PDS – Estudo Dirigido | Parte 1: Modelagem de Sinais e Sistemas Discretos
=============================================================================
Simulações:
  1. Sequências Elementares (impulso, degrau, exponenciais)
  2. Operações com Sinais (deslocamento, inversão, escalonamento)
  3. Energia e Potência de Sinais
  4. Classificação de Sistemas Discretos
  5. Sinal de Sensor de Vibração – Aplicação Real (PBL)
=============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os

# ---------------------------------------------------------------------------
# Configuração de estilo
# ---------------------------------------------------------------------------
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "#f9f9f9",
    "axes.grid": True,
    "grid.linestyle": "--",
    "grid.alpha": 0.5,
    "axes.titlesize": 12,
    "axes.labelsize": 10,
    "font.family": "DejaVu Sans",
})

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "resultados")
os.makedirs(RESULTS_DIR, exist_ok=True)


# ===========================================================================
# SIMULAÇÃO 1 – Sequências Elementares
# ===========================================================================
def simulacao_1():
    n = np.arange(-10, 21)

    # --- Impulso unitário ---
    delta = (n == 0).astype(float)

    # --- Degrau unitário ---
    degrau = (n >= 0).astype(float)

    # --- Exponenciais reais ---
    a_dec = 0.85          # decaimento estável
    a_cre = 1.15          # crescimento instável
    exp_dec = np.where(n >= 0, a_dec ** n, 0.0)
    exp_cre = np.where(n >= 0, a_cre ** n, 0.0)

    # --- Exponencial complexa ---
    omega0 = 2 * np.pi * 0.08   # ω₀ = 0.08 × 2π rad/amostra
    exp_cx = np.exp(1j * omega0 * n)

    # --- Senoide discreta ---
    senoide = np.cos(omega0 * n)

    # ----- Plotagem -----
    fig = plt.figure(figsize=(14, 10))
    fig.suptitle("Simulação 1 – Sequências Elementares", fontsize=14, fontweight="bold")
    gs = gridspec.GridSpec(3, 2, figure=fig, hspace=0.55, wspace=0.35)

    specs = [
        (gs[0, 0], n, delta,          "Impulso Unitário  δ[n]",              "k"),
        (gs[0, 1], n, degrau,         "Degrau Unitário  u[n]",               "#1f77b4"),
        (gs[1, 0], n, exp_dec,        f"Exponencial Real  a={a_dec}  (|a|<1)", "#2ca02c"),
        (gs[1, 1], n, exp_cre,        f"Exponencial Real  a={a_cre}  (|a|>1)", "#d62728"),
        (gs[2, 0], n, exp_cx.real,    "Exp. Complexa – Parte Real  cos(ω₀n)", "#9467bd"),
        (gs[2, 1], n, senoide,        "Senoide Discreta  cos(ω₀n)",           "#8c564b"),
    ]

    for pos, nx, sig, titulo, cor in specs:
        ax = fig.add_subplot(pos)
        ax.stem(nx, sig, linefmt=cor, markerfmt=f"o", basefmt="gray")
        ax.set_title(titulo)
        ax.set_xlabel("n  (amostras)")
        ax.set_ylabel("x[n]")

    plt.savefig(os.path.join(RESULTS_DIR, "sim1_sequencias_elementares.png"),
                dpi=150, bbox_inches="tight")
    plt.close()
    print("✔ Simulação 1 salva.")


# ===========================================================================
# SIMULAÇÃO 2 – Operações com Sinais
# ===========================================================================
def simulacao_2():
    n = np.arange(-15, 16)

    # Sinal base: senoide janelada (simula pulso de sensor)
    x = np.where((n >= 0) & (n <= 8), np.sin(2 * np.pi * 0.15 * n), 0.0)

    n0 = 5          # atraso
    alpha = 2.0     # escalonamento

    x_atrasado  = np.where((n - n0 >= 0) & (n - n0 <= 8),
                            np.sin(2 * np.pi * 0.15 * (n - n0)), 0.0)
    x_invertido = np.where((-n >= 0) & (-n <= 8),
                            np.sin(2 * np.pi * 0.15 * (-n)), 0.0)
    x_escalado  = alpha * x

    fig, axes = plt.subplots(2, 2, figsize=(13, 8))
    fig.suptitle("Simulação 2 – Operações com Sinais Discretos",
                 fontsize=14, fontweight="bold")

    dados = [
        (axes[0, 0], x,           "Sinal original  x[n]",              "#1f77b4"),
        (axes[0, 1], x_atrasado,  f"Deslocamento  x[n − {n0}]",         "#ff7f0e"),
        (axes[1, 0], x_invertido, "Inversão temporal  x[−n]",           "#2ca02c"),
        (axes[1, 1], x_escalado,  f"Escalonamento  {alpha} · x[n]",     "#d62728"),
    ]

    for ax, sig, titulo, cor in dados:
        ax.stem(n, sig, linefmt=cor, markerfmt="o", basefmt="gray")
        ax.set_title(titulo)
        ax.set_xlabel("n  (amostras)")
        ax.set_ylabel("x[n]")

    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "sim2_operacoes_sinais.png"),
                dpi=150, bbox_inches="tight")
    plt.close()
    print("✔ Simulação 2 salva.")


# ===========================================================================
# SIMULAÇÃO 3 – Energia e Potência de Sinais
# ===========================================================================
def simulacao_3():
    N = 60
    n = np.arange(0, N)

    # Sinais
    a = 0.90
    exp_sig  = a ** n                          # sinal de energia
    senoide  = np.cos(2 * np.pi * 0.1 * n)    # sinal de potência
    rampa    = n.astype(float)                  # nem/nem

    def energia_acumulada(x):
        return np.cumsum(x ** 2)

    def potencia_media(x):
        return np.mean(x ** 2)

    E_exp  = np.sum(exp_sig ** 2)
    E_seno = np.sum(senoide ** 2)   # finito para N finito; diverge com N→∞
    P_seno = potencia_media(senoide)
    P_exp  = potencia_media(exp_sig)

    fig = plt.figure(figsize=(14, 10))
    fig.suptitle("Simulação 3 – Energia e Potência de Sinais", fontsize=14, fontweight="bold")
    gs = gridspec.GridSpec(3, 2, figure=fig, hspace=0.6, wspace=0.35)

    # ---- linha 1: sinais ----
    for (pos, sig, titulo, cor) in [
        (gs[0, 0], exp_sig, f"Exponencial  a={a}  (sinal de energia)", "#2ca02c"),
        (gs[0, 1], senoide, "Senoide  (sinal de potência)",            "#1f77b4"),
    ]:
        ax = fig.add_subplot(pos)
        ax.stem(n, sig, linefmt=cor, markerfmt="o", basefmt="gray")
        ax.set_title(titulo); ax.set_xlabel("n"); ax.set_ylabel("x[n]")

    # ---- linha 2: energia acumulada ----
    for (pos, sig, titulo, cor) in [
        (gs[1, 0], exp_sig, f"Energia acumulada  (E_total ≈ {E_exp:.2f})", "#2ca02c"),
        (gs[1, 1], senoide, f"Energia acumulada  (P_média ≈ {P_seno:.2f})", "#1f77b4"),
    ]:
        ax = fig.add_subplot(pos)
        ax.plot(n, energia_acumulada(sig), color=cor, linewidth=2)
        ax.set_title(titulo); ax.set_xlabel("n"); ax.set_ylabel("E[n]")

    # ---- linha 3: rampa ----
    ax_rampa = fig.add_subplot(gs[2, :])
    ax_rampa.stem(n[:20], rampa[:20], linefmt="#d62728", markerfmt="o", basefmt="gray")
    ax_rampa.set_title("Rampa  x[n] = n  (E = ∞, P = ∞ — nem energia nem potência)")
    ax_rampa.set_xlabel("n"); ax_rampa.set_ylabel("x[n]")

    plt.savefig(os.path.join(RESULTS_DIR, "sim3_energia_potencia.png"),
                dpi=150, bbox_inches="tight")
    plt.close()
    print("✔ Simulação 3 salva.")


# ===========================================================================
# SIMULAÇÃO 4 – Classificação de Sistemas Discretos
# ===========================================================================
def simulacao_4():
    n = np.arange(0, 40)
    x1 = np.sin(2 * np.pi * 0.05 * n)
    x2 = np.cos(2 * np.pi * 0.12 * n)
    alpha, beta = 1.5, 0.8

    # --- Definição dos sistemas ---
    def S1(x):
        """y[n] = 3x[n] − x[n−2]  (LTI, causal, BIBO-estável)"""
        y = np.zeros_like(x)
        for i in range(len(x)):
            y[i] = 3 * x[i] - (x[i - 2] if i >= 2 else 0)
        return y

    def S2(x):
        """y[n] = x²[n]  (não linear)"""
        return x ** 2

    def S3(x, n_arr):
        """y[n] = n · x[n]  (variante no tempo — coeficiente muda com n)"""
        return n_arr * x

    def S4(x):
        """y[n] = Σ_{k≤n} x[k]  (acumulador — marginalmente estável)"""
        return np.cumsum(x)

    # --- Verificação numérica de linearidade ---
    def verifica_linearidade(sistema, *args):
        """Retorna True se T{αx1 + βx2} ≈ αT{x1} + βT{x2}."""
        entrada_combo = alpha * x1 + beta * x2
        if args:
            saida_combo = sistema(entrada_combo, *args)
            saida_sup   = alpha * sistema(x1, *args) + beta * sistema(x2, *args)
        else:
            saida_combo = sistema(entrada_combo)
            saida_sup   = alpha * sistema(x1) + beta * sistema(x2)
        return np.allclose(saida_combo, saida_sup, atol=1e-9)

    resultados = {
        "S1: y=3x[n]−x[n−2]":  {"linear": verifica_linearidade(S1),
                                   "causal": True, "estavel": True,
                                   "invariante": True},
        "S2: y=x²[n]":          {"linear": verifica_linearidade(S2),
                                   "causal": True, "estavel": True,
                                   "invariante": True},
        "S3: y=n·x[n]":         {"linear": verifica_linearidade(S3, n),
                                   "causal": True, "estavel": True,
                                   "invariante": False},
        "S4: Acumulador":        {"linear": verifica_linearidade(S4),
                                   "causal": True, "estavel": False,
                                   "invariante": True},
    }

    # ----- Plotagem -----
    fig, axes = plt.subplots(2, 2, figsize=(13, 8))
    fig.suptitle("Simulação 4 – Classificação de Sistemas Discretos",
                 fontsize=14, fontweight="bold")
    axes = axes.flatten()

    entradas = [x1, x1, x1, x1]
    funcoes  = [S1, S2, lambda x: S3(x, n), S4]
    cores    = ["#1f77b4", "#d62728", "#ff7f0e", "#9467bd"]

    for idx, (nome, props) in enumerate(resultados.items()):
        saida = funcoes[idx](entradas[idx])
        ax = axes[idx]
        ax.plot(n, entradas[idx], "k--", alpha=0.5, linewidth=1, label="x[n]")
        ax.plot(n, saida, color=cores[idx], linewidth=2, label="y[n]")
        status = (f"Linear: {'✓' if props['linear'] else '✗'}  |  "
                  f"Inv.Tempo: {'✓' if props['invariante'] else '✗'}  |  "
                  f"Causal: {'✓' if props['causal'] else '✗'}  |  "
                  f"BIBO: {'✓' if props['estavel'] else '✗'}")
        ax.set_title(f"{nome}\n{status}", fontsize=9)
        ax.set_xlabel("n"); ax.set_ylabel("Amplitude")
        ax.legend(fontsize=8)

    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "sim4_classificacao_sistemas.png"),
                dpi=150, bbox_inches="tight")
    plt.close()
    print("✔ Simulação 4 salva.")


# ===========================================================================
# SIMULAÇÃO 5 – Sensor de Vibração: Aplicação Real (Problema Norteador PBL)
# ===========================================================================
def simulacao_5():
    np.random.seed(42)

    Fs   = 1000          # Hz — frequência de amostragem
    T    = 1.0           # s  — duração do sinal
    N    = int(Fs * T)   # número de amostras
    n    = np.arange(N)
    t    = n / Fs        # eixo de tempo (s)

    # Composição do sinal de vibração
    f1, f2 = 50, 100              # Hz
    A1, A2 = 1.0, 0.4            # amplitudes
    ruido  = 0.25 * np.random.randn(N)

    x = A1 * np.sin(2 * np.pi * f1 * t) + \
        A2 * np.sin(2 * np.pi * f2 * t) + ruido

    # Filtro de média móvel: h[n] = 1/M para 0 ≤ n ≤ M-1
    M = 10   # comprimento do filtro
    h = np.ones(M) / M
    # convolução (modo 'same' preserva tamanho; causal → usa apenas passado)
    x_filtrado = np.convolve(x, h, mode="same")

    # Energia por janela de 50 ms
    janela    = int(0.05 * Fs)    # 50 amostras
    n_janelas = N // janela
    energia_janela = np.array([
        np.sum(x[i * janela:(i + 1) * janela] ** 2) / janela
        for i in range(n_janelas)
    ])
    t_janela = np.arange(n_janelas) * (janela / Fs) + (janela / Fs) / 2

    # ----- Plotagem -----
    fig = plt.figure(figsize=(14, 10))
    fig.suptitle(
        "Simulação 5 – Sensor de Vibração (Problema Norteador PBL)\n"
        f"Motor industrial  |  Fs = {Fs} Hz  |  f₁ = {f1} Hz, f₂ = {f2} Hz",
        fontsize=13, fontweight="bold"
    )
    gs = gridspec.GridSpec(3, 2, figure=fig, hspace=0.55, wspace=0.35)

    # Sinal original (primeiros 200 ms)
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(t[:200], x[:200], color="#1f77b4", alpha=0.7, linewidth=0.8, label="x[n] — com ruído")
    ax1.plot(t[:200], x_filtrado[:200], color="#d62728", linewidth=2, label=f"Filtro MA  M={M}")
    ax1.set_title("Sinal de vibração — domínio do tempo (200 ms)")
    ax1.set_xlabel("Tempo (s)")
    ax1.set_ylabel("Aceleração (u.a.)")
    ax1.legend()

    # FFT do sinal original
    ax2 = fig.add_subplot(gs[1, 0])
    freq = np.fft.rfftfreq(N, d=1 / Fs)
    Xf   = np.abs(np.fft.rfft(x)) / N
    ax2.plot(freq, Xf, color="#1f77b4", linewidth=1)
    ax2.set_xlim(0, 200)
    ax2.axvline(f1, color="#ff7f0e", linestyle="--", alpha=0.8, label=f"f₁={f1} Hz")
    ax2.axvline(f2, color="#2ca02c", linestyle="--", alpha=0.8, label=f"f₂={f2} Hz")
    ax2.set_title("Espectro de frequência  |X(f)|  (sinal original)")
    ax2.set_xlabel("Frequência (Hz)")
    ax2.set_ylabel("|X(f)|")
    ax2.legend()

    # FFT do sinal filtrado
    ax3 = fig.add_subplot(gs[1, 1])
    Xf_filt = np.abs(np.fft.rfft(x_filtrado)) / N
    ax3.plot(freq, Xf_filt, color="#d62728", linewidth=1)
    ax3.set_xlim(0, 200)
    ax3.axvline(f1, color="#ff7f0e", linestyle="--", alpha=0.8, label=f"f₁={f1} Hz")
    ax3.axvline(f2, color="#2ca02c", linestyle="--", alpha=0.8, label=f"f₂={f2} Hz")
    ax3.set_title("Espectro de frequência  |X(f)|  (sinal filtrado)")
    ax3.set_xlabel("Frequência (Hz)")
    ax3.set_ylabel("|X(f)|")
    ax3.legend()

    # Energia por janela
    ax4 = fig.add_subplot(gs[2, :])
    ax4.bar(t_janela, energia_janela, width=janela / Fs * 0.85,
            color="#9467bd", alpha=0.8, label="Energia / janela (50 ms)")
    ax4.set_title("Energia média por janela temporal (50 ms)")
    ax4.set_xlabel("Tempo (s)")
    ax4.set_ylabel("Energia média (u.a.²)")
    ax4.legend()

    plt.savefig(os.path.join(RESULTS_DIR, "sim5_sensor_vibracao.png"),
                dpi=150, bbox_inches="tight")
    plt.close()
    print("✔ Simulação 5 salva.")


# ===========================================================================
# EXECUÇÃO PRINCIPAL
# ===========================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("PDS – Parte 1: Modelagem de Sinais e Sistemas Discretos")
    print("=" * 60)
    simulacao_1()
    simulacao_2()
    simulacao_3()
    simulacao_4()
    simulacao_5()
    print("-" * 60)
    print(f"Resultados salvos em: {os.path.abspath(RESULTS_DIR)}")
    print("=" * 60)