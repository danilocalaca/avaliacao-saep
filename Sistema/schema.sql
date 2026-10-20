PRAGMA foreign_keys = ON;

CREATE TABLE Usuario (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL
);

CREATE TABLE Livro (
    id_livro INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    categoria TEXT NOT NULL,
    quantidade INTEGER NOT NULL CHECK (quantidade >= 0)
);

CREATE TABLE Emprestimo (
    id_emprestimo INTEGER PRIMARY KEY AUTOINCREMENT,
    data_emprestimo TEXT NOT NULL,
    data_prevista_devolucao TEXT NOT NULL,
    data_devolucao TEXT,
    id_usuario INTEGER NOT NULL,
    id_livro INTEGER NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuario (id_usuario),
    FOREIGN KEY (id_livro) REFERENCES Livro (id_livro)
);