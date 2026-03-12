# ai_agents_validation

Este repositório contém código de exemplo e recursos para experimentar e validar um fluxo de trabalho composto por múltiplos agentes de inteligência artificial. O objetivo é construir uma prova de conceito de um sistema modular em que agentes especializados cooperam para planejar, desenvolver, validar e documentar software automaticamente.

## Visão Geral

O projeto alberga um conjunto pequeno de ficheiros Python e web (HTML, CSS, JavaScript) que servem como ponto de partida para implementar e testar cada agente do fluxo. Foi concebido como uma plataforma de experimentação onde novos agentes podem ser adicionados e seu comportamento observado.

## Agentes Planejados

O fluxo final esperado consiste nos seguintes agentes, cada um com um papel definido:

1. **Project Manager (PM)**
   - Interpreta requisitos de alto nível.
   - Cria e distribui tarefas para os outros agentes.

2. **Design UI**
   - Gera a interface de utilizador (frontend), incluindo HTML, CSS e Javascript.

3. **Full Dev**
   - Desenvolve o backend e integra componentes do sistema.

4. **Code Quality Agent**
   - Analisa o código produzido.
   - Valida conformidade com normas e tornações de qualidade.

5. **Testes**
   - Gera e executa testes automatizados contra o código.

6. **Documentação**
   - Cria documentação do projeto e do API.

## Estrutura do Repositório

```
ai_agents_validation/
  index.html        # Exemplo de frontend inicial
  README.md         # Este ficheiro
  requirements.txt  # Dependências Python
  script.js         # JavaScript de exemplo
  style.css         # Estilos de exemplo
  agent/
    main.py         # Ponto de entrada do agente ou orquestrador
```

## Como Usar

1. Defina as variáveis de ambiente num ficheiro `.env` na raiz do projeto. Um template mínimo é:
   ```ini
   # .env
   OPENAI_API_KEY=your_api_key_here
   GITHUB_TOKEN=your_github_token
   GITHUB_OWNER=github_user_name
   GITHUB_REPO=github_repo_name
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute o agente principal:
   ```bash
   python agent/main.py
   ```
4. Modifique e experimente com novos agentes ou tarefas no diretório `agent/`.

## Objetivo Final

Demonstrar um pipeline de desenvolvimento auto-orquestrado, no qual o PM inicializa o processo e os agentes subsequentes criam o software, verificam a sua qualidade e documentam-no, com o mínimo de intervenção humana.

---


tente testar e expandir este README conforme necessário para documentar novos avanços no projeto.
