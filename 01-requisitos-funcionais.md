# Requisitos Funcionais

Sistema: Biblioteca Escolar

Os requisitos abaixo descrevem o que o sistema deve fazer para controlar livros, usuários e empréstimos da biblioteca da escola.

| ID | Requisito | Prioridade |
| --- | --- | --- |
| RF01 | O sistema deve autenticar usuários por e-mail e senha, liberando o acesso somente a quem tiver cadastro válido. | Alta |
| RF02 | O sistema deve validar os campos obrigatórios do login e exibir mensagem quando o e-mail ou a senha estiverem incorretos. | Alta |
| RF03 | O sistema deve permitir cadastrar livros informando título, autor, categoria e quantidade disponível. | Alta |
| RF04 | O sistema deve permitir consultar livros por título, autor ou categoria. | Alta |
| RF05 | O sistema deve permitir alterar os dados de um livro já cadastrado. | Alta |
| RF06 | O sistema deve permitir excluir livros, bloqueando a exclusão quando houver empréstimos registrados para o livro. | Média |
| RF07 | O sistema deve registrar empréstimos associando um usuário a um livro, com data do empréstimo e data prevista de devolução. | Alta |
| RF08 | O sistema deve impedir o empréstimo de livros sem exemplares disponíveis. | Alta |
| RF09 | O sistema deve atualizar automaticamente a quantidade disponível do livro a cada empréstimo e a cada devolução. | Alta |
| RF10 | O sistema deve registrar devoluções, preenchendo a data de devolução e impedindo que o mesmo empréstimo seja devolvido duas vezes. | Alta |
| RF11 | O sistema deve exibir o histórico de empréstimos com a situação de cada um (ativo, devolvido ou atrasado). | Média |
| RF12 | O sistema deve exibir na página principal a quantidade de livros cadastrados, de empréstimos ativos e de usuários. | Média |
| RF13 | O sistema deve gerar relatório de empréstimos com filtro por período e situação. | Média |
| RF14 | O sistema deve gerar relatório dos livros mais emprestados (desafio extra). | Baixa |
| RF15 | O sistema deve permitir encerrar a sessão do usuário e exigir autenticação para acessar qualquer tela interna. | Alta |

## Regras de negócio associadas

- A quantidade de um livro nunca pode ser negativa.
- Um empréstimo é considerado ativo enquanto a data de devolução estiver vazia.
- Um empréstimo é considerado atrasado quando está ativo e a data prevista de devolução já passou.
- A data prevista de devolução não pode ser anterior à data do empréstimo.
- O e-mail de cada usuário deve ser único no sistema.
