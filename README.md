
# CPI - Controle Produtivo de Investimentos

O site é um projeto de portfólio que tem como objetivo fornecer informações e recomendações sobre investimentos em bolsa de valores. Com base em análises e estudos de mercado, o site oferece sugestões de investimentos em renda variável para ajudar os usuários a tomar decisões financeiras mais informadas.

Por meio de uma interface simples e intuitiva, os usuários podem acessar informações sobre diferentes empresas, setores e tendências do mercado de ações. Além disso, o site também oferece ferramentas e recursos para ajudar os usuários a entender melhor o mercado financeiro e tomar decisões mais inteligentes sobre seus investimentos.

As recomendações de investimentos são baseadas em análises cuidadosas e em estudos de mercado rigorosos, com o objetivo de fornecer aos usuários informações precisas e atualizadas sobre as melhores oportunidades de investimento em renda variável.

Em resumo, o site é uma plataforma completa para quem deseja investir em bolsa de valores e busca informações precisas e confiáveis para tomar decisões financeiras mais informadas e lucrativas.

| Aviso: Em desenvolvimento, não levar os dados como recomendação!! |
| ---|

# Correções
- Possíveis falhas no sistema de login 
- Implementação de criptografia sha256 no sistema de login
- Dinamização das páginas
- Refatoração do código da página de registro/login
- Otimizações em algumas funções do "routes.py"

# Funcionalidades
- Coleta de dados de páginas da web usando a biblioteca Beautiful Soup  
- Sistema de registro e login  
- Página do usuário para atualizar informações de conta  
- Implementação de criptografia sha256 para senha  
- Uso de middlewares para autenticação de login  
- Implementação de CSRF token  
- Homepage dinâmica 
- Uso de threads para otimização

## Quanto há implementação da carteira, Ficaram disponíveis os seguintes ativos
| Ativo                                             | Situação      | Em Desenvolvimento |
|---------------------------------------------------|---------------|--------------------|
| Ações                                             | Em andamento  | Sim                |
| Fundos Imobiliários (FII)                         | Em andamento  | Não                |
| Exchange Traded Funds (ETF)                       | Em andamento  | Não                |
| Debêntures                                        | Em andamento  | Não                |
| Certificados de Depósito Bancário (CDB)           | Em andamento  | Não                |
| Letras de Crédito Imobiliário (LCI)               | Em andamento  | Não                |
| Letras de Crédito do Agronegócio (LCA)            | Em andamento  | Não                |
| Fundos de Investimento em Ações (FIA)             | Em andamento  | Não                |
| Fundos de Investimento em Renda Fixa (FIRF)       | Em andamento  | Não                |
| Fundos Multimercado                               | Em andamento  | Não                |
| Fundos Cambiais                                   | Em andamento  | Não                |


# Futuras Atualizações 
- Coleta de dados à página e atualização dinâmica /detalhes - pr1
- Página para montar carteira
- Calculo imposto de renda
- Refatoração da classe BasicData
- Refazer filtros

# Como executar:

### Clone este repositório executando o comando abaixo em seu terminal:

``` git clone git@github.com:Alangdp/Cpi.git ```

## Crie e ative um ambiente virtual:

### Windows

Instale o virtualenv com o comando: pip install virtualenv  
Crie um ambiente virtual com o comando: virtualenv venv  
Ative o ambiente virtual com o comando: venv\Scripts\activate  

### Linux

Instale o virtualenv com o comando: sudo apt install python3-venv  
Crie um ambiente virtual com o comando: python3 -m venv venv  
Ative o ambiente virtual com o comando: source venv/bin/activate  

### Instale as dependências usando o comando:

``` pip install -r requirements.txt ```

### Execute o servidor usando no terminal:

``` flask run ```

### acesse através de:

``` localhost:5000  ```

| Aviso: A muitas bibliotecas no arquivo de ``` requirements.txt ``` que não são usadas realmente no projeto, isso sera corrigido futuramente!! |
| ---|