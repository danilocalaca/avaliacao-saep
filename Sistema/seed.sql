INSERT INTO Usuario (id_usuario, nome, email, senha) VALUES
(1, 'Ana Souza', 'ana@escola.br', 'pbkdf2:sha256:1000000$bFw5WYoU6QhXMDAU$235168d99cab17f28328b1e6b5ae46d77935a3473b6ffc3793a81a0e491e4881'),
(2, 'Bruno Lima', 'bruno@escola.br', 'pbkdf2:sha256:1000000$xHKJS1G61LYtZQ06$02b171afbb191e4059f0506126a0c9ad075f5948515dc4263576696f384340b5'),
(3, 'Carla Mendes', 'carla@escola.br', 'pbkdf2:sha256:1000000$3Y7rhCB8jv28P5tW$39e0d897de7f98f45f3b7e919e37a83894f438e5c4d80a4a0cfa0c5d3eaa6c41');

INSERT INTO Livro (id_livro, titulo, autor, categoria, quantidade) VALUES
(1, 'Dom Casmurro', 'Machado de Assis', 'Literatura brasileira', 2),
(2, 'Vidas Secas', 'Graciliano Ramos', 'Literatura brasileira', 1),
(3, 'O Cortiço', 'Aluísio Azevedo', 'Literatura brasileira', 1),
(4, 'O Meu Pé de Laranja Lima', 'José Mauro de Vasconcelos', 'Literatura juvenil', 4),
(5, 'A Bolsa Amarela', 'Lygia Bojunga', 'Literatura juvenil', 3);

INSERT INTO Emprestimo (id_emprestimo, data_emprestimo, data_prevista_devolucao, data_devolucao, id_usuario, id_livro) VALUES
(1, '2026-09-01', '2026-09-15', '2026-09-12', 1, 1),
(2, '2026-09-10', '2026-09-24', '2026-09-23', 2, 2),
(3, '2026-10-05', '2026-10-25', NULL, 1, 1),
(4, '2026-10-08', '2026-10-28', NULL, 2, 2),
(5, '2026-10-12', '2026-11-01', NULL, 3, 3);