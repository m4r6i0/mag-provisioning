# API de Provisionamento

## Descrição

Esta é uma API para provisionamento de recursos, permitindo a criação, gerenciamento e monitoramento de requisições de provisionamento. Ela utiliza uma arquitetura baseada em microsserviços, com componentes principais como FastAPI, SQLAlchemy e RabbitMQ.

## Pré-requisitos

Para executar esta API, você precisará ter os seguintes componentes instalados e configurados em seu ambiente:

*   **Python 3.11:** A linguagem de programação utilizada para a API.
*   **Pip:** O gerenciador de pacotes do Python.
*   **PostgreSQL:** O banco de dados relacional utilizado para persistir os dados.
*   **RabbitMQ:** O message broker utilizado para comunicação assíncrona.
*   **Docker:** Para construir e executar a API em um container.
*   **Helm:** Para gerenciar a implantação em Kubernetes.
*   **Minikube (Opcional):** Para executar um cluster Kubernetes localmente.
*   **Nix (Opcional):** Para executar a API localmente.

## Instalação

1.  **Clonar o Repositório:**

    
```sh
./devserver.sh
```