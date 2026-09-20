-- Esse arquivo serve para refletir o mapa do banco atual, apenas exposição. Considere usar o alembic.

USE finance_core;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

CREATE TABLE contas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    saldo DECIMAL(10, 2) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE transacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    conta_id INT NOT NULL,
    tipo ENUM('entrada', 'saida') NOT NULL,
    valor DECIMAL(10, 2) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    data DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conta_id) REFERENCES contas(id)
);

CREATE TABLE transacoes_recorrentes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    conta_id INT NOT NULL,
    tipo ENUM('entrada', 'saida') NOT NULL,
    valor DECIMAL(10, 2) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    frequencia ENUM('semanal', 'quinzenal', 'mensal') NOT NULL,
    data_inicio DATE NOT NULL,
    proxima_data DATE NOT NULL,
    ativo BOOLEAN NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (conta_id) REFERENCES contas(id)
);

CREATE TABLE ocorrencias_recorrentes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transacao_recorrente_id INT NOT NULL,
    transacao_id INT,
    data_prevista DATE NOT NULL,
    data_processamento DATETIME,
    status ENUM('pendente', 'realizada', 'falhou') NOT NULL,
    motivo_falha VARCHAR(255),
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (transacao_recorrente_id) REFERENCES transacoes_recorrentes(id),
    FOREIGN KEY (transacao_id) REFERENCES transacoes(id)
);
