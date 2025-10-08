-- AssetManager - Database Setup Script v5 (Password Reset)
-- Este script cria o banco de dados e as tabelas com suporte a MFA e recuperação de senha.

-- --------------------------------------------------------
--
-- Criação do Banco de Dados
--
DROP DATABASE IF EXISTS `asset_manager`;
CREATE DATABASE `asset_manager` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `asset_manager`;

-- --------------------------------------------------------

--
-- Estrutura da tabela `users` (com suporte a MFA e Recuperação de Senha)
--
CREATE TABLE `users` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password_hash` VARCHAR(255) NOT NULL,
  `mfa_secret` VARCHAR(255) DEFAULT NULL,
  `mfa_code` VARCHAR(6) DEFAULT NULL,
  `mfa_code_expires_at` DATETIME DEFAULT NULL,
  `password_reset_token` VARCHAR(255) DEFAULT NULL,
  `password_reset_expires_at` DATETIME DEFAULT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura da tabela `machines`
--
CREATE TABLE `machines` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_id` INT(11) NOT NULL,
  `localidade` VARCHAR(255) DEFAULT NULL,
  `nome_dispositivo` VARCHAR(255) DEFAULT NULL,
  `numero_serie` VARCHAR(255) DEFAULT NULL,
  `nota_fiscal` VARCHAR(255) DEFAULT NULL,
  `responsavel` VARCHAR(255) DEFAULT NULL,
  `email_responsavel` VARCHAR(255) DEFAULT NULL,
  `setor` VARCHAR(255) DEFAULT NULL,
  `windows_update_ativo` VARCHAR(3) DEFAULT NULL, -- 'Sim' ou 'Não'
  `sistema_operacional` VARCHAR(255) DEFAULT NULL,
  `observacao` TEXT DEFAULT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `machines_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Fim do Script
--