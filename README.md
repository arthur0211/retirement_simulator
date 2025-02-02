# 🎯 Simulador Avançado de Aposentadoria

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Um simulador interativo e visual para planejamento financeiro de aposentadoria, desenvolvido com Streamlit e Python.

![Preview do Simulador](docs/images/preview.png)

## ✨ Funcionalidades

- 📊 **Simulação Visual**: Gráficos interativos mostrando a evolução do seu patrimônio
- 💰 **Múltiplas Fontes de Renda**: Adicione e gerencie diferentes fontes de renda na aposentadoria
- 📈 **Estratégias de Retirada**: Escolha entre retirada personalizada ou baseada em estratégia
- 💾 **Exportação de Dados**: Baixe os resultados em CSV ou Excel
- ⚙️ **Configurações Salváveis**: Exporte e importe suas configurações em JSON
- 📱 **Interface Responsiva**: Funciona em desktop e dispositivos móveis

## 🚀 Como Usar

### Instalação Local

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/retirement-simulator.git
cd retirement-simulator
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute o aplicativo:
```bash
streamlit run retirement_simulator.py
```

### Uso Online

Acesse a versão online em: [Link para sua aplicação Streamlit]

## 📋 Guia de Uso

1. **Dados Pessoais**
   - Insira sua data de nascimento
   - Informe seus investimentos atuais

2. **Fase de Acumulação**
   - Configure o investimento mensal
   - Defina a taxa real de retorno esperada

3. **Fase de Aposentadoria**
   - Escolha a idade alvo de aposentadoria
   - Defina sua expectativa de vida
   - Configure a taxa real de retorno na aposentadoria

4. **Estratégia de Retirada**
   - Escolha entre retirada personalizada ou baseada em estratégia
   - Configure os parâmetros de acordo com sua escolha

5. **Rendas Adicionais**
   - Adicione outras fontes de renda (aposentadoria, aluguéis, etc.)
   - Configure início, duração e taxa de crescimento de cada fonte

## 🔧 Configuração

O simulador permite personalizar diversos parâmetros:

- **Taxas de Retorno**: Diferentes taxas para fase de acumulação e aposentadoria
- **Estratégias de Retirada**: 
  - Personalizada: você define o valor mensal
  - Baseada em Estratégia: calculada automaticamente
    - Drawdown: zerando os ativos
    - Renda Perpétua: preservando o principal
- **Fontes de Renda**: Configure múltiplas fontes com diferentes características

## 💾 Salvando e Carregando Configurações

1. **Exportar**:
   - Clique em "Exportar Configurações"
   - Salve o arquivo JSON gerado

2. **Importar**:
   - Clique em "Importar Configurações"
   - Selecione um arquivo JSON previamente exportado

## 📊 Visualização de Dados

O simulador oferece duas visualizações principais:

1. **Evolução do Patrimônio**
   - Mostra o saldo do portfólio ao longo do tempo
   - Indica fases de acumulação e aposentadoria
   - Exibe retiradas mensais

2. **Evolução da Renda**
   - Composição detalhada das diferentes fontes de renda
   - Gráfico de área empilhada interativo
   - Seleção das fontes a serem exibidas

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, leia nosso [Guia de Contribuição](CONTRIBUTING.md) para mais detalhes.

1. Faça um Fork do projeto
2. Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👥 Autores

- **Seu Nome** - *Desenvolvimento Inicial* - [@seu-usuario](https://github.com/seu-usuario)

## 🙏 Agradecimentos

- Streamlit pela excelente framework
- Plotly pela biblioteca de visualização
- Todos os contribuidores e usuários

## 📞 Suporte

- Abra uma [Issue](https://github.com/seu-usuario/retirement-simulator/issues)
- Envie um email para [seu-email@exemplo.com]

---
⌨️ com ❤️ por [Seu Nome](https://github.com/seu-usuario) 