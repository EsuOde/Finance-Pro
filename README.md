# 💰 Finance Pro - Gestão Financeira Pessoal

O **Finance Pro** é um sistema desktop completo para controle de finanças pessoais, desenvolvido em **Python** com foco em uma interface moderna, intuitiva e, acima de tudo, na **segurança rigorosa** dos dados de acesso.

## 🚀 Funcionalidades Principais
* **Autenticação Segura**: Sistema de login e cadastro com validação de credenciais.
* **Gestão de Transações**: Registro completo de receitas e despesas com definição de categorias e valores.
* **Recuperação de Acesso**: Fluxo dedicado para redefinição de senha diretamente na interface.
* **Persistência Local**: Armazenamento em banco de dados SQLite, garantindo que os dados fiquem sob controle do usuário.

## 🛡️ Segurança e Diferenciais Técnicos
Diferente de sistemas amadores, este projeto implementa padrões de segurança de nível profissional:
* **Criptografia com Bcrypt**: As senhas dos usuários nunca são armazenadas em texto simples. Elas passam por um processo de *hashing* com *salt*, o que impossibilita a leitura da senha original mesmo que o banco de dados seja acessado.
* **Interface CustomTkinter**: Uso de widgets modernos e estilizados para uma experiência de usuário (UX) superior ao Tkinter padrão.
* **Arquitetura Modular**: Divisão clara entre lógica de interface (`app/`), persistência de dados (`database/`) e execução (`main.py`).

## 🛠️ Tecnologias Utilizadas
* **Linguagem**: Python 3.13
* **Interface Gráfica**: [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
* **Banco de Dados**: SQLite3
* **Segurança/Criptografia**: Bcrypt

## 📂 Como Instalar e Executar o Projeto
1. **Clone o repositório**:
   ```bash
   Desenvolvido por Gabriel como parte de um portfólio focado em desenvolvimento seguro e interfaces modernas.
   git clone [https://github.com/EsuOde/Finance-Pro.git](https://github.com/EsuOde/Finance-Pro.git)
