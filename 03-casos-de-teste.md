# Casos de Teste de Software

Sistema: Biblioteca Escolar

Os testes abaixo cobrem autenticação, cadastro de livros, empréstimos e devoluções. Antes de executar, o banco deve estar populado com o script de dados iniciais.

## Resumo

| ID | Cenário | Resultado esperado |
| --- | --- | --- |
| CT01 | Login válido | Acesso liberado e página principal exibida |
| CT02 | Login com senha incorreta | Mensagem de erro e acesso negado |
| CT03 | Login com campos vazios | Mensagem de campo obrigatório |
| CT04 | Cadastro de livro válido | Livro salvo e exibido na lista |
| CT05 | Cadastro de livro com quantidade negativa | Cadastro recusado com mensagem |
| CT06 | Empréstimo com estoque | Empréstimo registrado e quantidade reduzida |
| CT07 | Empréstimo sem estoque | Operação bloqueada com mensagem |
| CT08 | Devolução de empréstimo ativo | Devolução registrada e quantidade aumentada |
| CT09 | Exclusão de livro com histórico | Exclusão bloqueada com mensagem |
| CT10 | Acesso a tela interna sem login | Redirecionamento para o login |

## Detalhamento

### CT01 Login válido

- **Pré-condição:** usuário cadastrado no banco.
- **Passos:** abrir a tela de login, informar e-mail e senha corretos, clicar em Entrar.
- **Resultado esperado:** o sistema abre a página principal com o menu e o dashboard.

### CT02 Login com senha incorreta

- **Pré-condição:** usuário cadastrado no banco.
- **Passos:** informar e-mail correto e senha errada, clicar em Entrar.
- **Resultado esperado:** permanece na tela de login com a mensagem "E-mail ou senha incorretos.".

### CT03 Login com campos vazios

- **Pré-condição:** nenhuma.
- **Passos:** deixar e-mail e senha em branco e clicar em Entrar.
- **Resultado esperado:** o sistema indica que os campos são obrigatórios e não tenta autenticar.

### CT04 Cadastro de livro válido

- **Pré-condição:** usuário autenticado.
- **Passos:** na tela de livros, preencher título, autor, categoria e quantidade 3, clicar em Cadastrar.
- **Resultado esperado:** mensagem de sucesso e o livro aparece na listagem com quantidade 3.

### CT05 Cadastro de livro com quantidade negativa

- **Pré-condição:** usuário autenticado.
- **Passos:** preencher todos os campos com quantidade -1 e clicar em Cadastrar.
- **Resultado esperado:** o livro não é salvo e uma mensagem informa que a quantidade deve ser maior ou igual a zero.

### CT06 Empréstimo com estoque

- **Pré-condição:** livro com quantidade maior que zero.
- **Passos:** na tela de empréstimos, escolher usuário e livro, informar as datas e clicar em Registrar empréstimo.
- **Resultado esperado:** empréstimo aparece no histórico como ativo e a quantidade do livro diminui em 1.

### CT07 Empréstimo sem estoque

- **Pré-condição:** livro com quantidade igual a zero.
- **Passos:** tentar registrar empréstimo desse livro.
- **Resultado esperado:** operação bloqueada com a mensagem "Sem estoque disponível para este livro." e nenhum registro criado.

### CT08 Devolução de empréstimo ativo

- **Pré-condição:** empréstimo ativo existente.
- **Passos:** no histórico, clicar em Registrar devolução no empréstimo ativo.
- **Resultado esperado:** a situação muda para devolvido, a data de devolução é preenchida e a quantidade do livro aumenta em 1.

### CT09 Exclusão de livro com histórico

- **Pré-condição:** livro com ao menos um empréstimo registrado.
- **Passos:** na tela de livros, excluir esse livro e confirmar.
- **Resultado esperado:** o livro permanece cadastrado e uma mensagem explica que há empréstimos vinculados.

### CT10 Acesso a tela interna sem login

- **Pré-condição:** sessão encerrada.
- **Passos:** acessar diretamente o endereço da tela de livros.
- **Resultado esperado:** o sistema redireciona para a tela de login.
