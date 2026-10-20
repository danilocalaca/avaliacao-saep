import os
import re
from datetime import date
from functools import wraps

from flask import Flask, abort, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from db import abrir_banco, inicializar_banco


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'chave-desenvolvimento-altere-antes-de-publicar')
app.config['TEMPLATES_AUTO_RELOAD'] = True

inicializar_banco()


def login_obrigatorio(funcao):
    @wraps(funcao)
    def verificar_login(*args, **kwargs):
        if 'id_usuario' not in session:
            return redirect(url_for('login'))
        return funcao(*args, **kwargs)

    return verificar_login


def obter_status(data_prevista, data_devolucao):
    if data_devolucao:
        return 'Devolvido'
    if data_prevista < date.today().isoformat():
        return 'Atrasado'
    return 'Ativo'


def validar_data(valor):
    try:
        return date.fromisoformat(valor)
    except (TypeError, ValueError):
        return None


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'id_usuario' in session:
        return redirect(url_for('inicio'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '')
        if not email or not senha:
            flash('Informe o e-mail e a senha.', 'erro')
        elif not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', email):
            flash('Informe um e-mail válido.', 'erro')
        else:
            with abrir_banco() as conexao:
                usuario = conexao.execute(
                    'SELECT id_usuario, nome, senha FROM Usuario WHERE email = ?', (email,)
                ).fetchone()
            if usuario and check_password_hash(usuario['senha'], senha):
                session.clear()
                session['id_usuario'] = usuario['id_usuario']
                session['nome_usuario'] = usuario['nome']
                return redirect(url_for('inicio'))
            flash('E-mail ou senha incorretos.', 'erro')

    return render_template('login.html')


@app.route('/sair', methods=['POST'])
@login_obrigatorio
def sair():
    session.clear()
    return redirect(url_for('login'))


@app.route('/')
@login_obrigatorio
def inicio():
    with abrir_banco() as conexao:
        total_livros = conexao.execute('SELECT COUNT(*) AS total FROM Livro').fetchone()['total']
        emprestimos_ativos = conexao.execute(
            'SELECT COUNT(*) AS total FROM Emprestimo WHERE data_devolucao IS NULL'
        ).fetchone()['total']
        total_usuarios = conexao.execute('SELECT COUNT(*) AS total FROM Usuario').fetchone()['total']
    return render_template(
        'inicio.html',
        ativo='inicio',
        total_livros=total_livros,
        emprestimos_ativos=emprestimos_ativos,
        total_usuarios=total_usuarios,
    )


@app.route('/livros', methods=['GET', 'POST'])
@login_obrigatorio
def livros():
    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        autor = request.form.get('autor', '').strip()
        categoria = request.form.get('categoria', '').strip()
        quantidade_texto = request.form.get('quantidade', '').strip()
        try:
            quantidade = int(quantidade_texto)
            if quantidade < 0:
                raise ValueError
        except ValueError:
            flash('A quantidade deve ser um número inteiro maior ou igual a zero.', 'erro')
        else:
            if not titulo or not autor or not categoria:
                flash('Preencha todos os campos do livro.', 'erro')
            else:
                with abrir_banco() as conexao:
                    conexao.execute(
                        'INSERT INTO Livro (titulo, autor, categoria, quantidade) VALUES (?, ?, ?, ?)',
                        (titulo, autor, categoria, quantidade),
                    )
                flash('Livro cadastrado.', 'sucesso')
                return redirect(url_for('livros'))

    busca = request.args.get('busca', '').strip()
    with abrir_banco() as conexao:
        if busca:
            termo = f'%{busca}%'
            lista_livros = conexao.execute(
                'SELECT * FROM Livro WHERE titulo LIKE ? OR autor LIKE ? OR categoria LIKE ? ORDER BY titulo',
                (termo, termo, termo),
            ).fetchall()
        else:
            lista_livros = conexao.execute('SELECT * FROM Livro ORDER BY titulo').fetchall()
    return render_template('livros.html', ativo='livros', livros=lista_livros, busca=busca)


@app.route('/livros/<int:id_livro>/editar', methods=['GET', 'POST'])
@login_obrigatorio
def editar_livro(id_livro):
    with abrir_banco() as conexao:
        livro = conexao.execute('SELECT * FROM Livro WHERE id_livro = ?', (id_livro,)).fetchone()
    if not livro:
        abort(404)

    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        autor = request.form.get('autor', '').strip()
        categoria = request.form.get('categoria', '').strip()
        quantidade_texto = request.form.get('quantidade', '').strip()
        try:
            quantidade = int(quantidade_texto)
            if quantidade < 0:
                raise ValueError
        except ValueError:
            flash('A quantidade deve ser um número inteiro maior ou igual a zero.', 'erro')
        else:
            if not titulo or not autor or not categoria:
                flash('Preencha todos os campos do livro.', 'erro')
            else:
                with abrir_banco() as conexao:
                    conexao.execute(
                        'UPDATE Livro SET titulo = ?, autor = ?, categoria = ?, quantidade = ? WHERE id_livro = ?',
                        (titulo, autor, categoria, quantidade, id_livro),
                    )
                flash('Livro alterado.', 'sucesso')
                return redirect(url_for('livros'))

    return render_template('livro_editar.html', ativo='livros', livro=livro)


@app.route('/livros/<int:id_livro>/excluir', methods=['POST'])
@login_obrigatorio
def excluir_livro(id_livro):
    with abrir_banco() as conexao:
        livro = conexao.execute('SELECT id_livro FROM Livro WHERE id_livro = ?', (id_livro,)).fetchone()
        if not livro:
            abort(404)
        total_emprestimos = conexao.execute(
            'SELECT COUNT(*) AS total FROM Emprestimo WHERE id_livro = ?', (id_livro,)
        ).fetchone()['total']
        if total_emprestimos:
            flash('Este livro possui empréstimos registrados e não pode ser excluído.', 'erro')
        else:
            conexao.execute('DELETE FROM Livro WHERE id_livro = ?', (id_livro,))
            flash('Livro excluído.', 'sucesso')
    return redirect(url_for('livros'))


@app.route('/emprestimos', methods=['GET', 'POST'])
@login_obrigatorio
def emprestimos():
    if request.method == 'POST':
        id_usuario = request.form.get('id_usuario', type=int)
        id_livro = request.form.get('id_livro', type=int)
        data_emprestimo = validar_data(request.form.get('data_emprestimo', ''))
        data_prevista = validar_data(request.form.get('data_prevista_devolucao', ''))
        if not id_usuario or not id_livro or not data_emprestimo or not data_prevista:
            flash('Preencha todos os campos com valores válidos.', 'erro')
        elif data_prevista < data_emprestimo:
            flash('A data prevista não pode ser anterior à data do empréstimo.', 'erro')
        else:
            try:
                with abrir_banco() as conexao:
                    conexao.execute('BEGIN IMMEDIATE')
                    usuario = conexao.execute(
                        'SELECT id_usuario FROM Usuario WHERE id_usuario = ?', (id_usuario,)
                    ).fetchone()
                    livro = conexao.execute(
                        'SELECT quantidade FROM Livro WHERE id_livro = ?', (id_livro,)
                    ).fetchone()
                    if not usuario or not livro:
                        abort(404)
                    if livro['quantidade'] < 1:
                        flash('Sem estoque disponível para este livro.', 'erro')
                    else:
                        conexao.execute(
                            'INSERT INTO Emprestimo (data_emprestimo, data_prevista_devolucao, id_usuario, id_livro) '
                            'VALUES (?, ?, ?, ?)',
                            (data_emprestimo.isoformat(), data_prevista.isoformat(), id_usuario, id_livro),
                        )
                        conexao.execute(
                            'UPDATE Livro SET quantidade = quantidade - 1 WHERE id_livro = ? AND quantidade > 0',
                            (id_livro,),
                        )
                        flash('Empréstimo registrado.', 'sucesso')
                if livro['quantidade'] > 0:
                    return redirect(url_for('emprestimos'))
            except Exception:
                raise

    situacao = request.args.get('situacao', '')
    condicoes = []
    parametros = []
    if situacao == 'Ativo':
        condicoes.append("e.data_devolucao IS NULL AND e.data_prevista_devolucao >= date('now', 'localtime')")
    elif situacao == 'Atrasado':
        condicoes.append("e.data_devolucao IS NULL AND e.data_prevista_devolucao < date('now', 'localtime')")
    elif situacao == 'Devolvido':
        condicoes.append('e.data_devolucao IS NOT NULL')
    consulta = (
        'SELECT e.*, u.nome AS nome_usuario, l.titulo AS titulo_livro '
        'FROM Emprestimo e JOIN Usuario u ON u.id_usuario = e.id_usuario '
        'JOIN Livro l ON l.id_livro = e.id_livro'
    )
    if condicoes:
        consulta += ' WHERE ' + ' AND '.join(condicoes)
    consulta += ' ORDER BY e.data_emprestimo DESC, e.id_emprestimo DESC'
    with abrir_banco() as conexao:
        usuarios = conexao.execute('SELECT id_usuario, nome FROM Usuario ORDER BY nome').fetchall()
        lista_livros = conexao.execute(
            'SELECT id_livro, titulo, quantidade FROM Livro WHERE quantidade > 0 ORDER BY titulo'
        ).fetchall()
        lista_emprestimos = conexao.execute(consulta, parametros).fetchall()
    return render_template(
        'emprestimos.html', ativo='emprestimos', usuarios=usuarios, livros=lista_livros,
        emprestimos=lista_emprestimos, situacao=situacao, hoje=date.today().isoformat(),
        obter_status=obter_status,
    )


@app.route('/emprestimos/<int:id_emprestimo>/devolver', methods=['POST'])
@login_obrigatorio
def devolver_emprestimo(id_emprestimo):
    with abrir_banco() as conexao:
        conexao.execute('BEGIN IMMEDIATE')
        emprestimo = conexao.execute(
            'SELECT id_livro, data_devolucao FROM Emprestimo WHERE id_emprestimo = ?',
            (id_emprestimo,),
        ).fetchone()
        if not emprestimo:
            abort(404)
        if emprestimo['data_devolucao']:
            flash('Este empréstimo já foi devolvido.', 'erro')
        else:
            conexao.execute(
                'UPDATE Emprestimo SET data_devolucao = ? WHERE id_emprestimo = ? AND data_devolucao IS NULL',
                (date.today().isoformat(), id_emprestimo),
            )
            conexao.execute(
                'UPDATE Livro SET quantidade = quantidade + 1 WHERE id_livro = ?',
                (emprestimo['id_livro'],),
            )
            flash('Devolução registrada.', 'sucesso')
    return redirect(url_for('emprestimos'))


@app.route('/relatorios')
@login_obrigatorio
def relatorios():
    data_inicio = request.args.get('data_inicio', '').strip()
    data_fim = request.args.get('data_fim', '').strip()
    situacao = request.args.get('situacao', '')
    condicoes = []
    parametros = []
    if data_inicio and validar_data(data_inicio):
        condicoes.append('e.data_emprestimo >= ?')
        parametros.append(data_inicio)
    if data_fim and validar_data(data_fim):
        condicoes.append('e.data_emprestimo <= ?')
        parametros.append(data_fim)
    if situacao == 'Ativo':
        condicoes.append("e.data_devolucao IS NULL AND e.data_prevista_devolucao >= date('now', 'localtime')")
    elif situacao == 'Atrasado':
        condicoes.append("e.data_devolucao IS NULL AND e.data_prevista_devolucao < date('now', 'localtime')")
    elif situacao == 'Devolvido':
        condicoes.append('e.data_devolucao IS NOT NULL')
    consulta = (
        'SELECT e.*, u.nome AS nome_usuario, l.titulo AS titulo_livro '
        'FROM Emprestimo e JOIN Usuario u ON u.id_usuario = e.id_usuario '
        'JOIN Livro l ON l.id_livro = e.id_livro'
    )
    if condicoes:
        consulta += ' WHERE ' + ' AND '.join(condicoes)
    consulta += ' ORDER BY e.data_emprestimo DESC, e.id_emprestimo DESC'
    with abrir_banco() as conexao:
        lista_emprestimos = conexao.execute(consulta, parametros).fetchall()
        mais_emprestados = conexao.execute(
            'SELECT l.titulo, l.autor, COUNT(e.id_emprestimo) AS total '
            'FROM Livro l LEFT JOIN Emprestimo e ON e.id_livro = l.id_livro '
            'GROUP BY l.id_livro, l.titulo, l.autor '
            'ORDER BY total DESC, l.titulo'
        ).fetchall()
    return render_template(
        'relatorios.html', ativo='relatorios', emprestimos=lista_emprestimos,
        mais_emprestados=mais_emprestados, data_inicio=data_inicio, data_fim=data_fim,
        situacao=situacao, obter_status=obter_status,
    )


@app.errorhandler(404)
def nao_encontrado(_erro):
    return 'Página não encontrada.', 404


if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG') == '1')