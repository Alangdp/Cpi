Observações:

Os commits com o nome de pr são para indicar progresso em futuras atualizações.

Futuras Atualizações:

1. Criação de uma homepage para o site [ ]
2. Implementação do uso de threads para compensar a lentidão da biblioteca (Beautiful Soup) [ x ]
3. Coleta de dados à página e atualização dinâmica /detalhes [ ] - pr1, 
4. Pagina do usuário (mudar senha, email, nome de usuário) [ ]

Correções:

1. Possiveis falhas no sistema de login [  ] - algumas falhas,
2. Implementar a criptografia no sistema de login usando md5 [ x ] - usado sha256
3. Dinamização das páginas [ x ] - todas as páginas até o momento

Demais correções feitas:

1. Refatorado código da página de registro/login (estava bagunçado) 
2. Otimizações em algumas funções do "routes.py"
3. Sistema de CSRF token