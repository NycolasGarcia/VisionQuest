<div align="center">

<img src="https://img.shields.io/badge/VisionQuest-v2.0.0-00FFFB?style=for-the-badge&labelColor=1e1e2e" alt="VisionQuest v2.0.0" />

# VisionQuest

**Jogo educacional de matematica controlado por gestos das maos via webcam**

[Funcionalidades](#funcionalidades) · [Quick Start](#quick-start) · [Como Jogar](#como-jogar) · [Estrutura](#estrutura-do-projeto) · [Colaboradores](#colaboradores)

Ferramentas:

  <img src="https://skills.syvixor.com/api/icons?perline=15&i=python,pygame,opencv" width="">
  
  *Python • Pygame • OpenCV*

Detalhes:

![Version](https://img.shields.io/badge/version-1.0-grey?style=flat&color=darkgrey)
![Stars](https://img.shields.io/github/stars/NycolasGarcia/EDA-Speeder?style=flat&color=darkgrey)
![Repo Views](https://komarev.com/ghpvc/?username=NycolasGarcia&repo=EDA-Speeder&color=lightgrey)

[![License: MIT](https://img.shields.io/badge/License-MIT-a6e3a1.svg?style=flat-square)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-00FFFB.svg?style=flat-square)](https://github.com/eoLucasS/VisionQuest/pulls)



</div>

---

## Sobre

O **VisionQuest** utiliza visao computacional para transformar a webcam em um controle de jogo. O jogador responde questoes matematicas usando gestos das maos - juntando o indicador com o polegar (gesto de pinca) para selecionar respostas.

O projeto foi desenvolvido como ferramenta educacional alinhada ao **ODS 4 da ONU** (educacao de qualidade), promovendo aprendizagem interativa e acessivel.

> [!NOTE]
> Originalmente criado como projeto academico em 2024, foi completamente reestruturado em 2026 com arquitetura modular, novo sistema de UI/UX e mecanicas de jogo aprimoradas.

---

## Funcionalidades

<details>
<summary><strong>Deteccao de Maos em Tempo Real</strong></summary>

- Deteccao de ate 2 maos simultaneamente via MediaPipe Tasks API
- Cursor visual seguindo o dedo indicador em tempo real
- Gesto de pinca (indicador + polegar) para interacao
- Esqueleto da mao desenhado sobre a interface
- Cursor muda de cor ao realizar a pinca (azul → verde)

</details>

<details>
<summary><strong>Sistema de Questoes Matematicas</strong></summary>

- **Facil:** soma e subtracao com numeros de 1 a 20
- **Medio:** multiplicacao, divisao e potencias
- **Dificil:** logaritmos, raizes quadradas, equacoes de 1o grau e expressoes com ordem de operacoes
- Plano cartesiano interativo - toque no ponto correto com a mao
- Distratores inteligentes (opcoes erradas plausíveis, sem respostas obvias)

</details>

<details>
<summary><strong>Mecanicas de Jogo</strong></summary>

- **3 vidas** - erros tem consequencia real
- **Sistema de streak** - bonus a cada 3 acertos consecutivos
- **Barra de progresso** com contador de pontos (ex: 7/10)
- **Feedback sonoro** - sons distintos para acerto e erro
- **Resposta correta revelada ao errar** - aprendizado pelo erro
- **Tela de fim de jogo** com estatisticas completas (acertos, erros, pontuacao)

</details>

<details>
<summary><strong>Interface e UX</strong></summary>

- HUD com pontuacao, streak, vidas (coracoes) e dificuldade
- Botoes com hover highlight - mudam de cor ao passar o dedo
- Mao sempre visivel por cima de overlays (dicas, fim de jogo)
- Tema escuro com contraste otimizado para leitura sobre webcam
- Instrucoes visuais de como interagir em cada tela

</details>

---

## Quick Start

> [!TIP]
> Pre-requisitos: [Python](https://python.org) 3.9+ e uma webcam.

```bash
# 1. Clone o repositorio
git clone https://github.com/NycolasGarcia/VisionQuest.git
cd VisionQuest

# 2. Crie e ative um ambiente virtual
python -m venv venv
    venv/Scripts/activate   # Windows (Git Bash)
    source venv/bin/activate # Linux/macOS

# 3. Instale as dependencias
pip install -r requirements.txt

# 4. Execute o jogo
     py main.py
     python3 main.py
```

> [!IMPORTANT]
> Na primeira execucao o MediaPipe carrega o modelo de deteccao de maos, o que pode levar alguns segundos.

---

## Como Jogar

| Acao | Gesto |
|------|-------|
| **Mover cursor** | Mova a mao - o dedo indicador controla o cursor |
| **Selecionar/Clicar** | Junte o indicador com o polegar (pinca) |
| **Sair** | Pressione a tecla `Q` a qualquer momento |

### Fluxo do Jogo

```
Tela Inicial → Selecao de Dificuldade → Questoes → Fim de Jogo
     │                                      │            │
     └─ Sair                                └─ Dicas     └─ Jogar Novamente
```

1. **Tela inicial** - selecione "Jogar" com o gesto de pinca
2. **Dificuldade** - escolha entre Facil, Medio ou Dificil
3. **Questoes** - responda fazendo pinca sobre a opcao correta ou tocando o ponto no plano cartesiano
4. **Fim** - ao atingir 10 pontos (vitoria) ou perder 3 vidas (derrota), veja suas estatisticas

---

## Estrutura do Projeto

```
VisionQuest/
├── main.py                    # Ponto de entrada
├── requirements.txt           # Dependencias
├── assets/
│   ├── hand_landmarker.task   # Modelo MediaPipe de deteccao de maos
│   ├── preview.png            # Screenshot do jogo
│   ├── images/                # Fotos dos colaboradores, icones
│   └── sounds/                # Efeitos sonoros (acerto/erro)
└── src/
    ├── config.py              # Constantes e configuracoes centralizadas
    ├── game.py                # State machine principal do jogo
    ├── hand_tracker.py        # Deteccao de maos (MediaPipe Tasks API)
    ├── button.py              # Botoes interativos com hover
    ├── cartesian_plane.py     # Renderizacao do plano cartesiano
    ├── question_generator.py  # Gerador de questoes matematicas
    ├── score_system.py        # Pontuacao, vidas e streaks
    └── screens/
        ├── title.py           # Tela inicial
        ├── difficulty.py      # Selecao de dificuldade
        ├── gameplay.py        # Tela principal do jogo + HUD
        ├── game_over.py       # Tela de fim de jogo com estatisticas
        └── hint.py            # Overlay de dicas
```

---

## Stack Tecnica

| Tecnologia | Uso |
|-----------|-----|
| [Python 3](https://python.org) | Linguagem principal |
| [OpenCV](https://opencv.org) | Captura de video e renderizacao da interface |
| [MediaPipe](https://github.com/google/mediapipe) | Deteccao de maos em tempo real (Tasks API) |
| [Pygame CE](https://pyga.me) | Sistema de audio |
| [NumPy](https://numpy.org) | Operacoes numericas |

---

## Topicos Matematicos

O projeto abrange os seguintes topicos, alinhados a ementa academica:

- Aritmetica (soma, subtracao, multiplicacao, divisao)
- Potenciacao e raizes quadradas
- Logaritmos
- Equacoes de 1o grau
- Expressoes com ordem de operacoes
- Plano cartesiano e coordenadas

---

## Colaboradores
<div align=center>
<table>
  <tr>
    <td align="center">
      <a href="https://www.linkedin.com/in/lucaslopesdasilva/">
        <img src="https://avatars.githubusercontent.com/u/119815116?v=4" width="100px;" /><br>
        <sub><b>Lucas Silva</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://www.linkedin.com/in/nycolasagrgarcia/">
        <img src="https://avatars.githubusercontent.com/u/127459801?v=4" width="100px;" /><br>
        <sub><b>Nycolas Garcia</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://www.linkedin.com/in/danilodoes/">
        <img src="https://avatars.githubusercontent.com/u/110133245?v=4" width="100px;" /><br>
        <sub><b>Danilo Santos</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://www.linkedin.com/in/breno-melo-53822a20a/">
        <img src="https://avatars.githubusercontent.com/u/44868973?v=4" width="100px;" /><br>
        <sub><b>Breno Melo</b></sub>
      </a>
    </td>
  </tr>
</table>
</div>

## Contato

<div align="center">

| Plataforma | Link |
|------------|------|
| <img src="https://skills.syvixor.com/api/icons?i=linkedin" width="20"> LinkedIn | <a href="https://www.linkedin.com/in/NycolasAGRGarcia/" target="_blank">Acessar</a> |
| <img src="https://skills.syvixor.com/api/icons?i=github" width="20"> GitHub | <a href="https://github.com/NycolasGarcia" target="_blank">Acessar</a> |
| <img src="https://skills.syvixor.com/api/icons?i=gmail" width="20"> Gmail | <a href="mailto:nycolasagrg@gmail.com">Enviar</a> |
| <img src="https://skills.syvixor.com/api/icons?i=vercel" width="20"> Vercel | <a href="https://dev-nycolas-garcia.vercel.app/" target="_blank">Visitar</a> |

</div>


---

## Licenca

MIT. Veja [LICENSE](LICENSE) para detalhes.

