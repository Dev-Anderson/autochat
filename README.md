# 🚀 AutoChat

AutoChat é uma aplicação para automatizar o atendimento de pequenas e médias empresas através de chat (inicialmente interno, evoluindo para WhatsApp).

## 💡 Objetivo

Reduzir atendimento manual e padronizar o fluxo de interação com clientes, permitindo que empresas configurem:

- Mensagens de saudação
- Menus de atendimento
- Produtos/serviços
- Fluxo de pedidos automatizado

---

## 🧠 Como funciona (MVP)

1. Cliente inicia conversa
2. Sistema responde com saudação
3. Exibe menu de opções
4. Cliente escolhe uma opção (ex: cardápio)
5. Sistema retorna produtos
6. Cliente seleciona item
7. Sistema pede confirmação (OK / CANCELAR)

---

## 🏗️ Arquitetura (MVP)

- Backend: FastAPI (Python)
- Banco: PostgreSQL
- Containerização: Docker

---

## 🚀 Como rodar o projeto

### Pré-requisitos

- Docker
- Docker Compose

---

### 🔧 Subir o ambiente

```bash
docker compose up --build