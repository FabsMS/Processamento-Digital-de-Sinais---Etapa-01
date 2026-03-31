# Resumo Teórico – Parte 1
## Modelagem de Sinais e Sistemas Discretos

**Disciplina:** Processamento Digital de Sinais  

---

## 1. Sinais Contínuos e Discretos

### 1.1 Definições

Um **sinal** é uma função que representa a variação de alguma grandeza física ao longo do tempo (ou outra variável independente). Matematicamente:

- **Sinal contínuo:** $x(t)$, com $t \in \mathbb{R}$, definido para todo instante de tempo.
- **Sinal discreto:** $x[n]$, com $n \in \mathbb{Z}$, definido apenas para instantes inteiros — uma sequência numérica.

### 1.2 Processo de Amostragem

A conversão de um sinal contínuo para discreto é feita por **amostragem** com período $T_s$ e frequência $F_s = 1/T_s$:

$$x[n] = x_a(n T_s), \quad n \in \mathbb{Z}$$

O **Teorema de Nyquist-Shannon** estabelece a condição para reconstrução perfeita do sinal:

$$F_s \geq 2 F_{\max}$$

onde $F_{\max}$ é a maior frequência presente no sinal analógico. A violação dessa condição causa **aliasing**: frequências acima de $F_s/2$ são "dobradas" sobre frequências mais baixas, corrompendo irreversivelmente o sinal amostrado.

**Exemplo:** Um sensor de vibração com componentes até 500 Hz requer $F_s \geq 1000$ Hz. Na prática, adota-se $F_s = 2000$–$5000$ Hz para garantir margem de segurança e facilitar a filtragem anti-aliasing.

---

## 2. Sequências Elementares

As sequências elementares são os blocos fundamentais para representar qualquer sinal discreto.

### 2.1 Impulso Unitário (Delta de Kronecker)

$$\delta[n] = \begin{cases} 1, & n = 0 \\ 0, & n \neq 0 \end{cases}$$

**Propriedade de amostragem (sifting):**

$$x[n] = \sum_{k=-\infty}^{+\infty} x[k]\, \delta[n - k]$$

Essa propriedade é fundamental: qualquer sequência pode ser decomposta como soma ponderada de impulsos deslocados. É a base para a definição da resposta ao impulso de sistemas LTI.

### 2.2 Degrau Unitário

$$u[n] = \begin{cases} 1, & n \geq 0 \\ 0, & n < 0 \end{cases}$$

Relação com o impulso:

$$u[n] = \sum_{k=0}^{+\infty} \delta[n - k], \qquad \delta[n] = u[n] - u[n-1]$$

### 2.3 Exponencial Real

$$x[n] = A \cdot a^n, \quad n \geq 0$$

O comportamento depende de $|a|$:

| $|a|$ | Comportamento |
|-------|---------------|
| $|a| < 1$ | Decaimento exponencial (estável) |
| $|a| = 1$ | Amplitude constante |
| $|a| > 1$ | Crescimento exponencial (instável) |

### 2.4 Exponencial Complexa

$$x[n] = A e^{j\omega_0 n} = A[\cos(\omega_0 n) + j\,\sin(\omega_0 n)]$$

onde $\omega_0$ é a **frequência digital** (rad/amostra), relacionada à frequência analógica por $\omega_0 = 2\pi f_0 / F_s$. A exponencial complexa é autofunção dos sistemas LTI: se $x[n] = e^{j\omega n}$, então $y[n] = H(e^{j\omega}) e^{j\omega n}$, onde $H(e^{j\omega})$ é a resposta em frequência do sistema.

### 2.5 Senoide Discreta

$$x[n] = A \cos(\omega_0 n + \phi)$$

É periódica com período $N$ se $\omega_0 = 2\pi k / N$ para algum inteiro $k$.

---

## 3. Operações com Sinais Discretos

### 3.1 Deslocamento Temporal

$$y[n] = x[n - n_0]$$

Para $n_0 > 0$: atraso. Para $n_0 < 0$: avanço temporal.

### 3.2 Inversão Temporal (Reflexão)

$$y[n] = x[-n]$$

O sinal é refletido em torno de $n = 0$. Fundamental na operação de convolução.

### 3.3 Escalonamento de Amplitude

$$y[n] = \alpha \cdot x[n], \quad \alpha \in \mathbb{R}$$

Multiplicação de todos os valores da sequência por uma constante.

### 3.4 Soma e Produto

$$y[n] = x_1[n] + x_2[n], \qquad y[n] = x_1[n] \cdot x_2[n]$$

---

## 4. Energia e Potência de Sinais

### 4.1 Energia

$$E = \sum_{n=-\infty}^{+\infty} |x[n]|^2$$

### 4.2 Potência Média

$$P = \lim_{N \to \infty} \frac{1}{2N+1} \sum_{n=-N}^{N} |x[n]|^2$$

### 4.3 Classificação Energética

| Classificação | Condição | Exemplo |
|---|---|---|
| Sinal de energia | $0 < E < \infty$, $P = 0$ | Exponencial decrescente |
| Sinal de potência | $E = \infty$, $0 < P < \infty$ | Senoide periódica |
| Nem energia nem potência | $E = \infty$, $P = \infty$ | Rampa $x[n] = n$ |

**Interpretação física:** Sinais de energia são transientes (pulsos, respostas impulsivas). Sinais de potência são de duração infinita, como senoides e sinais estocásticos estacionários.

---

## 5. Classificação de Sistemas Discretos

Um **sistema discreto** é um operador $\mathcal{T}\{\cdot\}$ que mapeia uma entrada $x[n]$ em uma saída $y[n] = \mathcal{T}\{x[n]\}$.

### 5.1 Sistemas com e sem Memória

- **Sem memória:** $y[n]$ depende apenas de $x[n]$ no mesmo instante. Ex.: $y[n] = 2x[n]$
- **Com memória:** depende de amostras passadas ou futuras. Ex.: $y[n] = x[n] + x[n-1]$

### 5.2 Linearidade

Um sistema é **linear** se satisfaz o **princípio da superposição**:

$$\mathcal{T}\{\alpha x_1[n] + \beta x_2[n]\} = \alpha\, \mathcal{T}\{x_1[n]\} + \beta\, \mathcal{T}\{x_2[n]\}$$

- **Linear:** $y[n] = 3x[n] - x[n-2]$
- **Não linear:** $y[n] = x^2[n]$

### 5.3 Invariância no Tempo

Um sistema é **invariante no tempo** se:

$$x[n - n_0] \rightarrow y[n - n_0], \quad \forall\, n_0 \in \mathbb{Z}$$

**Variante:** $y[n] = n \cdot x[n]$ (o coeficiente $n$ muda com o tempo).

### 5.4 Sistemas LTI

Sistemas **Lineares e Invariantes no Tempo** são completamente caracterizados por sua **resposta ao impulso** $h[n] = \mathcal{T}\{\delta[n]\}$. A saída é obtida pela **convolução discreta**:

$$y[n] = x[n] * h[n] = \sum_{k=-\infty}^{+\infty} x[k]\, h[n-k]$$

### 5.5 Causalidade

Sistema **causal** se $y[n_0]$ depende apenas de $x[n]$ com $n \leq n_0$. Para LTI:

$$\text{Causal} \iff h[n] = 0, \quad \forall\, n < 0$$

**Importância:** Todo sistema implementado em tempo real deve ser causal.

### 5.6 Estabilidade BIBO

Sistema **BIBO-estável** (*Bounded Input, Bounded Output*) se:

$$|x[n]| \leq M_x < \infty \implies |y[n]| \leq M_y < \infty$$

Para sistemas LTI, condição necessária e suficiente:

$$\sum_{n=-\infty}^{+\infty} |h[n]| < \infty$$

**Consequência prática:** Um sistema instável amplifica indefinidamente qualquer perturbação, inviabilizando sua operação. Filtros para sensores industriais devem obrigatoriamente ser BIBO-estáveis.

### 5.7 Invertibilidade

Um sistema é **invertível** se existe $\mathcal{T}^{-1}\{\cdot\}$ tal que $\mathcal{T}^{-1}\{\mathcal{T}\{x[n]\}\} = x[n]$. Essencial em equalização de canais e deconvolução.

---

## 6. Interpretação Física de Sinais

| Grandeza Física | Sinal $x[n]$ | $F_s$ típico | Aplicação |
|---|---|---|---|
| Vibração (acelerômetro) | Aceleração (m/s²) | 1–50 kHz | Manutenção preditiva |
| Temperatura (termopar) | °C ou mV | 1–100 Hz | Controle industrial |
| Corrente (sensor Hall) | A ou mA | 10–100 kHz | Proteção de acionamentos |
| Velocidade angular (encoder) | RPM ou pulsos | 1–10 kHz | Controle de motores |
| Pressão (piezelétrico) | Pa ou bar | 1–100 kHz | Monitoramento estrutural |

---

## 7. Resposta ao Problema Norteador (PBL)

> *Como representar matematicamente o comportamento temporal de um sensor real e quais propriedades estruturais devem ser analisadas para garantir o correto processamento digital desse sinal?*

O sinal de um sensor real é modelado como sequência discreta $x[n] = x_a(nT_s)$, obtida respeitando $F_s \geq 2F_{\max}$ (Teorema de Nyquist-Shannon). Para garantir processamento correto, o sistema digital deve ser:

1. **Linear** – para que o princípio da superposição valha e a análise espectral seja possível;
2. **Invariante no tempo** – para que o comportamento não mude ao longo da operação;
3. **Causal** – para implementação em tempo real em sistemas embarcados;
4. **BIBO-estável** – para que ruídos limitados não causem divergência na saída.

O filtro de média móvel $y[n] = \frac{1}{M}\sum_{k=0}^{M-1} x[n-k]$ exemplifica esses requisitos: é LTI, causal (usa apenas amostras passadas) e BIBO-estável ($\sum|h[n]| = 1 < \infty$), sendo amplamente usado na suavização de sinais de sensores industriais.

---

## Referências

- OPPENHEIM, A. V.; SCHAFER, R. W. *Discrete-Time Signal Processing*. 3. ed. Pearson, 2010.
- PROAKIS, J. G.; MANOLAKIS, D. G. *Digital Signal Processing: Principles, Algorithms and Applications*. 4. ed. Pearson, 2006.
- LATHI, B. P. *Signal Processing and Linear Systems*. Oxford University Press, 1998.