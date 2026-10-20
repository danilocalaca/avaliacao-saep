# Requisitos de Infraestrutura

Sistema: Biblioteca Escolar

## Hardware

### Servidor

| Item | Mínimo |
| --- | --- |
| Processador | Dual core ou superior |
| Memória RAM | 4 GB |
| Armazenamento | 20 GB livres |

### Estações de uso (computadores da biblioteca e da secretaria)

| Item | Mínimo |
| --- | --- |
| Processador | Dual core ou superior |
| Memória RAM | 4 GB |
| Monitor | Resolução de 1366 x 768 ou superior |

## Software

### Servidor

| Item | Requisito |
| --- | --- |
| Sistema operacional | Windows 10 ou superior, ou Linux (Ubuntu 22.04 ou superior) |
| Linguagem e framework | Python 3.10 ou superior com Flask |
| Banco de dados | SQLite no ambiente de desenvolvimento e de demonstração; MySQL ou PostgreSQL em produção |
| Servidor web | Servidor embutido do Flask em desenvolvimento; Gunicorn com Nginx em produção |

### Estações de uso

| Item | Requisito |
| --- | --- |
| Navegador web | Versão atual do Chrome, Edge ou Firefox, com JavaScript habilitado |

## Rede

| Item | Requisito |
| --- | --- |
| Rede local | Rede da escola conectando as estações ao servidor, com o endereço do servidor fixo ou nome interno definido |
| Internet | Necessária para instalar dependências, aplicar atualizações e carregar as fontes da interface |
| Porta | Porta do servidor web liberada no firewall da rede local (80 ou 443 em produção, 5000 em desenvolvimento) |

## Segurança e manutenção

- Senhas armazenadas somente como hash.
- Cópia de segurança do banco de dados em rotina semanal, guardada fora do servidor.
- Acesso ao servidor restrito à equipe de TI da escola.
- Atualização periódica do Python, das dependências e do sistema operacional.
