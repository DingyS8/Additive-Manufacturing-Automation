# Sistema de Automação de Manufatura Aditiva

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Desenvolvimento](https://img.shields.io/badge/Status-Desenvolvimento-orange.svg)]()
[![Version: 1.0](https://img.shields.io/badge/Version-1.0-blue.svg)]()

Sistema web automatizado para facilitar o processo de venda e gestão de serviços de impressão 3D, voltado para pequenos empreendedores, designers e usuários com pouca familiaridade técnica.

## 🎯 Objetivo

Democratizar o acesso à manufatura aditiva através de uma solução completa que automatiza desde o preparo até o controle da produção, eliminando a dependência de conhecimento técnico avançado ou serviços de terceiros.

## 🚀 Funcionalidades Principais

### Para Usuários
- **Upload Inteligente**: Suporte a arquivos STL, imagens e descrição textual
- **Conversão Automática**: 
  - Texto → Imagem (TXT2IMG)
  - Imagem → Modelo 3D (IMG2STL)
- **Orçamento Automático**: Cálculo baseado em peso, tempo de impressão e quantidade
- **Sistema de Pedidos**: Fluxo completo desde orçamento até entrega
- **Pagamento Integrado**: PIX e cartão de crédito
- **Acompanhamento**: Status em tempo real da produção
- **Avaliação**: Sistema de feedback pós-entrega

### Para Administradores
- **Painel de Controle**: Gestão completa de pedidos e usuários
- **Aprovação de Envios**: Controle de qualidade antes da expedição
- **Relatórios**: Histórico e análise de pedidos
- **Gerenciamento de Usuários**: Administração de contas e permissões

## 👥 Público-Alvo

- 🏪 **Pequenos empreendedores e artesãos**: Produtos personalizados sem conhecimento técnico
- 🎨 **Designers e criadores independentes**: Protótipos e peças utilitárias com agilidade
- 🎓 **Instituições de ensino e estudantes**: Ferramenta educacional simplificada
- 🔧 **Hobbystas e entusiastas**: Exploração prática com curva de aprendizado reduzida

## 🛠️ Arquitetura Técnica

### Stack Tecnológico
- **Backend**: Python (Flask/Django)
- **Frontend**: Web responsivo
- **Banco de Dados**: PostgreSQL/MySQL
- **Integração Hardware**: OctoPrint API
- **Arquitetura**: MVC em ambiente cloud

### Componentes do Sistema
- **Interface Web**: Navegação intuitiva e responsiva
- **API de Conversão**: Processamento de arquivos 3D
- **Motor de Orçamento**: Cálculo automático de custos
- **Gateway de Pagamento**: Integração PIX/Cartão
- **Sistema de Filas**: Gerenciamento de produção
- **Controle de Impressoras**: Interface com hardware via OctoPrint

## 📋 Requisitos do Sistema

### Funcionais
- Sistema completo de cadastro e autenticação de usuários
- Upload e validação de arquivos STL
- Conversão automática de formatos (texto/imagem → 3D)
- Cálculo automático de orçamentos
- Processamento de pedidos e pagamentos
- Emissão automática de notas fiscais
- Sistema de acompanhamento e suporte

### Não-Funcionais
- **Performance**: Tempo de resposta < 2 segundos
- **Disponibilidade**: 99,5% de uptime
- **Segurança**: Comunicação HTTPS/TLS
- **Escalabilidade**: Suporte a 100+ usuários simultâneos
- **Compatibilidade**: Chrome, Firefox, Edge (3 versões mais recentes)

## 🏗️ Status do Projeto

Este é um **projeto acadêmico** desenvolvido para a disciplina de Modelagem de Sistemas Computacionais. O escopo atual inclui:

### ✅ Entregáveis Concluídos
- Análise completa de requisitos funcionais e não-funcionais
- Diagramas UML completos:
  - Diagrama de Casos de Uso
  - Diagrama de Classes (Domínio e Projeto)
  - Diagrama de Sequência
  - Diagrama de Estados (Máquina de Estados)
  - Diagrama de Implantação
- Especificação de arquitetura do software
- Análise de riscos e planos de contingência
- Cronograma de desenvolvimento

### 🚧 Não Incluído Nesta Fase
- Implementação em código
- Protótipo funcional ou MVP
- Integrações reais com pagamento e logística

## 👨‍💻 Equipe de Desenvolvimento

- **Eugênio Polistchuk Berendsen**
- **Gabriel Almeida Fontes**
- **Isabella Barbosa de Brito**
- **Vinícius Baldan Herrera**

## 📄 Documentação

A documentação completa do projeto está disponível no diretório `/docs` e inclui:
- Especificação de Requisitos
- Diagramas UML
- Modelo de Dados
- Arquitetura do Sistema
- Análise de Riscos

## 🔄 Roadmap Futuro

- [ ] Implementação do backend em Python
- [ ] Desenvolvimento da interface web
- [ ] Integração com APIs de pagamento
- [ ] Conexão com impressoras 3D
- [ ] Testes de integração
- [ ] Deploy em ambiente de produção

## 📞 Contato

Para mais informações sobre o projeto ou colaborações, entre em contato com a equipe de desenvolvimento.

---

*Projeto desenvolvido como parte do curso de Modelagem de Sistemas Computacionais*
