# Discussão Técnica – Parte 1
## Relação entre Teoria e Simulações

**Disciplina:** Processamento Digital de Sinais  

---

## Simulação 1 – Sequências Elementares

### Objetivo
Visualizar e comparar as sequências fundamentais do PDS: impulso, degrau, exponenciais e senoide discreta.

### Análise dos Resultados

**Impulso unitário δ[n]:** A simulação confirma a definição matemática — valor unitário apenas em $n=0$, nulo para todo $n \neq 0$. A importância física é imediata: todo sinal discreto pode ser expresso como combinação linear de impulsos deslocados e ponderados (propriedade de sifting).

**Degrau unitário u[n]:** Visualiza-se claramente a transição em $n=0$. A relação $\delta[n] = u[n] - u[n-1]$ é verificável nos gráficos: a diferença entre u[n] e sua versão atrasada reproduz exatamente o impulso.

**Exponencial real:** O contraste entre $a = 0.85$ (decaimento) e $a = 1.15$ (crescimento) evidencia como o parâmetro $|a|$ determina a estabilidade da sequência. Um sistema cujo $h[n] = a^n u[n]$ com $|a| \geq 1$ seria BIBO-instável, pois $\sum |h[n]| \rightarrow \infty$.

**Exponencial complexa e senoide:** As partes real e imaginária de $e^{j\omega_0 n}$ são, respectivamente, $\cos(\omega_0 n)$ e $\sin(\omega_0 n)$, confirmando a fórmula de Euler. Essa dualidade é a base da análise espectral via DFT/FFT (Parte 3).

---

## Simulação 2 – Operações com Sinais

### Objetivo
Demonstrar como deslocamento, inversão e escalonamento transformam um sinal base.

### Análise dos Resultados

**Deslocamento temporal ($n_0 = 5$):** O sinal original reaparece inteiramente deslocado 5 amostras à direita, sem qualquer distorção de amplitude. Este comportamento é exatamente o exigido por um sistema invariante no tempo: a relação entrada-saída não muda conforme o instante de operação.

**Inversão temporal:** A sequência é espelhada em torno de $n=0$. Graficamente, o que era à direita do eixo aparece à esquerda. Esta operação é central no cálculo da convolução discreta $y[n] = \sum x[k] h[n-k]$, que envolve inverter $h$ e deslizá-lo sobre $x$.

**Escalonamento ($\alpha = 2$):** Todas as amostras são multiplicadas por 2, preservando a forma do sinal. Este resultado valida a propriedade de homogeneidade, um dos dois requisitos para linearidade.

---

## Simulação 3 – Energia e Potência

### Objetivo
Classificar sinais quanto à sua natureza energética e calcular energia acumulada.

### Análise dos Resultados

**Exponencial decrescente ($a = 0.90$):** A energia acumulada cresce rapidamente nos primeiros instantes e converge para um valor finito ($E \approx 4.76$ para $N=60$). Conforme $N \rightarrow \infty$, $E = A^2 / (1 - a^2)$ para $|a| < 1$. É um **sinal de energia**. A potência média $P \rightarrow 0$, pois a energia se "dilui" em um intervalo infinito.

**Senoide:** A energia acumulada cresce indefinidamente (linearmente em $N$), confirmando $E = \infty$. Porém, a potência média converge para $P = A^2/2 = 0.5$, caracterizando um **sinal de potência**.

**Rampa $x[n] = n$:** Tanto energia quanto potência divergem. É um exemplo de sinal que não pertence a nenhuma das duas classes — matematicamente relevante, fisicamente corresponde a um sinal que cresce sem limites (e.g., velocidade de um objeto em aceleração constante sem saturação).

**Conexão prática:** Em manutenção preditiva, a energia acumulada por janela temporal é usada como indicador de severidade de vibração. Um aumento brusco sugere falha iminente no equipamento.

---

## Simulação 4 – Classificação de Sistemas

### Objetivo
Verificar numericamente as propriedades de linearidade, invariância, causalidade e estabilidade BIBO para quatro sistemas.

### Análise dos Resultados

| Sistema | Linear | Inv. Tempo | Causal | BIBO-Estável |
|---|:---:|:---:|:---:|:---:|
| S1: $y[n] = 3x[n] - x[n-2]$ | ✓ | ✓ | ✓ | ✓ |
| S2: $y[n] = x^2[n]$ | ✗ | ✓ | ✓ | ✓ |
| S3: $y[n] = n \cdot x[n]$ | ✓ | ✗ | ✓ | ✓ |
| S4: Acumulador $\Sigma x[k]$ | ✓ | ✓ | ✓ | ✗ |

**S1 – LTI, causal, estável:** Verificação por superposição confirma linearidade numericamente (erro < $10^{-9}$). É um filtro de diferenças de segunda ordem. A resposta ao impulso é $h[n] = 3\delta[n] - \delta[n-2]$, com $\sum|h[n]| = 4 < \infty$ — estável.

**S2 – Não linear:** A saída de $(\alpha x_1 + \beta x_2)^2 \neq \alpha x_1^2 + \beta x_2^2$ (há termos cruzados $2\alpha\beta x_1 x_2$). Os gráficos mostram que a saída sempre é não-negativa (quadrado), quebrando a homogeneidade para $\alpha < 0$.

**S3 – Variante no tempo:** O coeficiente $n$ que multiplica $x[n]$ muda a cada amostra. Se aplicarmos $x[n-n_0]$, obteremos $n \cdot x[n-n_0]$, mas $y[n-n_0] = (n-n_0) \cdot x[n-n_0]$. Como $n \neq n-n_0$, o sistema é variante. Graficamente, a amplitude da saída cresce com $n$ mesmo para entrada de amplitude constante.

**S4 – Acumulador marginalmente instável:** $h[n] = u[n]$, portanto $\sum_{n=0}^{\infty}|h[n]| = \infty$. A entrada senoidal de amplitude unitária produz saída de amplitude crescente — instabilidade BIBO demonstrada graficamente pela curva que cresce monotonicamente.

---

## Simulação 5 – Sensor de Vibração (Problema Norteador PBL)

### Cenário Modelado
Motor industrial com acelerômetro, $F_s = 1000$ Hz, componentes em 50 Hz (1ª harmônica) e 100 Hz (desequilíbrio mecânico), mais ruído gaussiano.

### Análise dos Resultados

**Modelagem do sinal:** O sinal $x[n] = A_1\sin(2\pi f_1 n/F_s) + A_2\sin(2\pi f_2 n/F_s) + \text{ruído}$ representa fielmente a equação de amostragem $x[n] = x_a(nT_s)$. A escolha $F_s = 1000$ Hz garante $F_s \geq 2 \times 100 = 200$ Hz, atendendo o critério de Nyquist com ampla margem.

**Espectro de frequência (FFT):** O espectro do sinal original exibe dois picos proeminentes em 50 Hz e 100 Hz, exatamente como esperado. O ruído aparece como um "patamar" distribuído ao longo de todas as frequências. Esta análise confirma que a amostragem preservou corretamente as componentes do sinal analógico.

**Filtro de média móvel (M = 10):** O filtro aplicado é $h[n] = \frac{1}{10}$ para $0 \leq n \leq 9$ e zero caso contrário. Suas propriedades:
  - **LTI:** coeficientes constantes, operação linear
  - **Causal:** usa apenas as 10 amostras mais recentes ($n, n-1, \ldots, n-9$) — implementável em tempo real
  - **BIBO-estável:** $\sum|h[n]| = 10 \times \frac{1}{10} = 1 < \infty$
  
  O espectro do sinal filtrado mostra atenuação do ruído de alta frequência, com os picos em 50 Hz e 100 Hz preservados. Há leve redução na amplitude de 100 Hz, esperada pois filtros MA têm resposta não-plana — assunto aprofundado na Parte 4 (Filtros Digitais).

**Energia por janela (50 ms):** O gráfico de barras mostra energia média estável ao longo do tempo, confirmando que o sinal é estacionário (para este modelo sintético). Em aplicações reais, picos de energia indicariam impactos mecânicos ou início de falhas.

### Conclusão do Problema Norteador

A Simulação 5 responde de forma integrada ao problema PBL:

1. O sinal do sensor é **modelado** como $x[n] = x_a(n/F_s)$ com $F_s$ satisfazendo Nyquist;
2. As **propriedades estruturais** fundamentais para processamento correto são: linearidade, invariância no tempo, causalidade e estabilidade BIBO;
3. O filtro de média móvel, verificado nas Simulações 1–4, satisfaz todos esses requisitos e é diretamente aplicável em sistemas embarcados (microcontroladores) por ser causal e de baixo custo computacional ($M$ multiplicações por amostra).

---

## Considerações Finais
 
Esta etapa consolidou os fundamentos matemáticos e práticos essenciais para o Processamento Digital de Sinais. Por meio das cinco simulações, foi possível observar na prática como sinais discretos são construídos a partir de sequências elementares, como operações básicas transformam esses sinais sem perda de informação, e como a classificação energética distingue comportamentos transientes de sinais de duração indefinida.
 
A classificação de sistemas revelou-se especialmente relevante: a verificação numérica de linearidade, invariância, causalidade e estabilidade BIBO demonstrou que essas propriedades não são apenas formalismos matemáticos, mas condições concretas que determinam se um sistema pode ser implementado, analisado e operado de forma segura em aplicações reais.
 
A aplicação ao sensor de vibração (Simulação 5) integrou todos os conceitos em um cenário de engenharia real, evidenciando que a escolha correta de $F_s$, a modelagem matemática do sinal e a seleção de um sistema com propriedades adequadas são etapas indissociáveis de qualquer projeto de processamento digital de sinais.

---

*Referências: OPPENHEIM & SCHAFER (2010); PROAKIS & MANOLAKIS (2006); LATHI (1998)*