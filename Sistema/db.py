import sqlite3
from contextlib import contextmanager
from pathlib import Path


PASTA_PROJETO = Path(__file__).resolve().parent
ARQUIVO_BANCO = PASTA_PROJETO / 'biblioteca.db'


def conectar():
    conexao = sqlite3.connect(ARQUIVO_BANCO, timeout=10)
    conexao.row_factory = sqlite3.Row
    conexao.execute('PRAGMA foreign_keys = ON')
    return conexao


@contextmanager
def abrir_banco():
    conexao = conectar()
    try:
        yield conexao
        conexao.commit()
    except Exception:
        conexao.rollback()
        raise
    finally:
        conexao.close()


def inicializar_banco():
    if ARQUIVO_BANCO.exists():
        return

    conexao = conectar()
    try:
        conexao.executescript((PASTA_PROJETO / 'schema.sql').read_text(encoding='utf-8'))
        conexao.executescript((PASTA_PROJETO / 'seed.sql').read_text(encoding='utf-8'))
        conexao.commit()
    except Exception:
        conexao.rollback()
        if ARQUIVO_BANCO.exists():
            ARQUIVO_BANCO.unlink()
        raise
    finally:
        conexao.close()