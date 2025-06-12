# Projeto Final: Sistema de Gerenciamento de Convites

## Descrição do Projeto

Este projeto foi desenvolvido como trabalho final para uma disciplina de Design de Software. Ele implementa um sistema para gerenciar e enviar convites personalizados, demonstrando conceitos de design de software e boas práticas de programação.

## Estrutura do Projeto

```
projeto-final/
├── .streamlit/ (Configurações do Streamlit)
├── data/ (Dados utilizados pelo projeto)
├── db/ (Scripts de banco de dados ou arquivos de configuração)
├── frontend/
│   ├── anac/ (Módulos relacionados à análise de dados)
│   └── sono/ (Módulos relacionados à análise de dados)
├── utils/ (Utilitários e funções auxiliares)
├── .gitignore
├── app.py (Aplicação principal em Python)
└── style.css (Estilos CSS para a aplicação)
```

## Instalação e Uso

Para configurar e executar o projeto localmente, siga os passos abaixo:

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/Lucas-Sambati/projeto-final.git
    cd projeto-final
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

    *Nota: Se o arquivo `requirements.txt` não existir, você pode precisar criar um com as dependências do projeto (por exemplo, `streamlit`, `pandas`, `sqlalchemy`, etc.).*

4.  **Execute a aplicação:**

    ```bash
    streamlit run app.py
    ```

    A aplicação será aberta no seu navegador padrão.

## Tecnologias Utilizadas

*   **Python**: Linguagem de programação principal.
*   **Streamlit**: Framework para criação de aplicações web interativas.
*   **CSS**: Para estilização da interface do usuário.
*   **SQL**: Para gerenciamento de dados (presumido, com base na estrutura `db/`).

## Diretrizes de Contribuição

Contribuições são bem-vindas! Para contribuir com este projeto, por favor, siga estas diretrizes:

1.  Faça um fork do repositório.
2.  Crie uma nova branch para sua feature (`git checkout -b feature/sua-feature`).
3.  Faça suas alterações e commit-as (`git commit -m 'feat: Adiciona nova funcionalidade'`).
4.  Envie para a branch original (`git push origin feature/sua-feature`).
5.  Abra um Pull Request detalhando suas alterações.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
