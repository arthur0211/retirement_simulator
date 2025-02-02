import streamlit as st
import pandas as pd
import datetime
import math
import plotly.graph_objects as go
import io
import numpy as np
from PIL import ImageColor
import json

# Configuração da página
st.set_page_config(
    page_title="Simulador Avançado de Aposentadoria",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/seu-usuario/retirement-simulator',
        'Report a bug': "https://github.com/seu-usuario/retirement-simulator/issues",
        'About': "# Simulador Avançado de Aposentadoria\nDesenvolvido para ajudar no planejamento financeiro da sua aposentadoria."
    }
)

# CSS personalizado para melhorar a interface
st.markdown(
    """
    <style>
    /* Tema geral e cores */
    :root {
        --primary-color: #1f77b4;
        --secondary-color: #2ecc71;
        --background-color: #f8f9fa;
        --text-color: #2c3e50;
        --border-radius: 10px;
    }
    
    /* Estilo geral da página */
    .main {
        background-color: var(--background-color);
        color: var(--text-color);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Cabeçalhos */
    h1, h2, h3 {
        color: var(--primary-color);
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* Cards para conteúdo */
    .stCard {
        border-radius: var(--border-radius);
        padding: 1rem;
        background: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    
    /* Inputs e controles */
    .stNumberInput, .stTextInput, .stDateInput {
        border-radius: var(--border-radius);
    }
    
    /* Botões */
    .stButton>button {
        background-color: var(--secondary-color);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        border-radius: var(--border-radius);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: white;
        padding: 2rem 1rem;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        white-space: pre-wrap;
        background-color: white;
        border-radius: var(--border-radius);
        color: var(--text-color);
        border: 1px solid #e1e4e8;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--primary-color) !important;
        color: white !important;
    }
    
    /* Tooltips e informações */
    .stTooltipIcon {
        color: var(--primary-color);
    }
    
    /* Mensagens de erro e avisos */
    .stAlert {
        border-radius: var(--border-radius);
    }
    
    /* Gráficos */
    .js-plotly-plot {
        border-radius: var(--border-radius);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Animações */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .stMarkdown {
        animation: fadeIn 0.5s ease-in;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    # Container principal com logo ou ícone
    with st.container():
        col1, col2, col3 = st.columns([1,3,1])
        with col2:
            st.title("🎯 Simulador Avançado de Aposentadoria")
    
    # Card para importar/exportar configurações
    with st.container():
        st.markdown("""
        <div class='stCard'>
            <h3>⚙️ Configurações</h3>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Botão para exportar configurações
            if st.button("📤 Exportar Configurações", help="Salve suas configurações atuais em um arquivo JSON"):
                config = {
                    "birth_date": str(birth_date) if 'birth_date' in locals() else None,
                    "total_investments_today": total_investments_today if 'total_investments_today' in locals() else None,
                    "monthly_investment": monthly_investment if 'monthly_investment' in locals() else None,
                    "annual_rate_acc": annual_rate_acc if 'annual_rate_acc' in locals() else None,
                    "retirement_age": retirement_age if 'retirement_age' in locals() else None,
                    "life_expectancy": life_expectancy if 'life_expectancy' in locals() else None,
                    "annual_rate_ret": annual_rate_ret if 'annual_rate_ret' in locals() else None,
                    "strategy_mode": strategy_mode if 'strategy_mode' in locals() else None,
                    "monthly_expenses": monthly_expenses if 'monthly_expenses' in locals() and strategy_mode == "Retirada Personalizada" else None,
                    "strategy_type": strategy_type if 'strategy_type' in locals() and strategy_mode == "Retirada Baseada em Estratégia" else None,
                    "income_sources": income_sources if 'income_sources' in locals() else []
                }
                
                json_str = json.dumps(config, indent=2, ensure_ascii=False)
                st.download_button(
                    label="💾 Baixar Configurações",
                    data=json_str,
                    file_name="configuracoes_aposentadoria.json",
                    mime="application/json",
                    help="Clique para baixar suas configurações"
                )
        
        with col2:
            # Upload de configurações
            uploaded_file = st.file_uploader(
                "📥 Importar Configurações",
                type=['json'],
                help="Carregue um arquivo JSON com suas configurações salvas"
            )
            
            if uploaded_file is not None:
                try:
                    imported_config = json.loads(uploaded_file.getvalue())
                    st.success("✅ Configurações importadas com sucesso!")
                    
                    # Atualizar session state com as configurações importadas
                    if imported_config.get("birth_date"):
                        st.session_state['birth_date'] = datetime.datetime.strptime(imported_config["birth_date"], "%Y-%m-%d").date()
                    if imported_config.get("total_investments_today"):
                        st.session_state['total_investments_today'] = imported_config["total_investments_today"]
                    if imported_config.get("monthly_investment"):
                        st.session_state['monthly_investment'] = imported_config["monthly_investment"]
                    if imported_config.get("annual_rate_acc"):
                        st.session_state['annual_rate_acc'] = imported_config["annual_rate_acc"]
                    if imported_config.get("retirement_age"):
                        st.session_state['retirement_age'] = imported_config["retirement_age"]
                    if imported_config.get("life_expectancy"):
                        st.session_state['life_expectancy'] = imported_config["life_expectancy"]
                    if imported_config.get("annual_rate_ret"):
                        st.session_state['annual_rate_ret'] = imported_config["annual_rate_ret"]
                    if imported_config.get("strategy_mode"):
                        st.session_state['strategy_mode'] = imported_config["strategy_mode"]
                    if imported_config.get("monthly_expenses"):
                        st.session_state['monthly_expenses'] = imported_config["monthly_expenses"]
                    if imported_config.get("strategy_type"):
                        st.session_state['strategy_type'] = imported_config["strategy_type"]
                    
                    # Atualizar fontes de renda
                    if imported_config.get("income_sources"):
                        st.session_state['n_sources'] = len(imported_config["income_sources"])
                        for i, source in enumerate(imported_config["income_sources"]):
                            st.session_state[f"name_{i}"] = source["name"]
                            st.session_state[f"income_{i}"] = source["monthly_income"]
                            st.session_state[f"start_age_{i}"] = source["income_start_age"]
                            st.session_state[f"lifetime_{i}"] = source["lifetime"]
                            if not source["lifetime"] and source["duration_years"]:
                                st.session_state[f"duration_{i}"] = source["duration_years"]
                            st.session_state[f"rate_{i}"] = source["annual_rate"]
                    
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro ao importar configurações: {str(e)}")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Introdução em um card elegante
    with st.container():
        st.markdown("""
        <div class='stCard'>
            👋 Bem-vindo ao seu Planejador Financeiro!
            Planeje sua aposentadoria de forma inteligente e visual. Simule diferentes cenários e tome decisões informadas sobre seu futuro financeiro.
            
            ✨ Funcionalidades:
            
                🎯 Defina metas personalizadas de aposentadoria
                💰 Gerencie múltiplas fontes de renda
                📊 Visualize projeções detalhadas
                📈 Analise diferentes estratégias de retirada
                📥 Exporte seus dados para análise posterior
            
        
        """, unsafe_allow_html=True)

    # Organização da sidebar em seções com ícones
    with st.sidebar:
        st.sidebar.markdown("### 📊 Dados Pessoais")
        birth_date = st.date_input(
            "Data de Nascimento",
            value=st.session_state.get('birth_date', datetime.date(1990, 1, 1)),
            help="Insira sua data de nascimento no formato dd/mm/aaaa",
            key='birth_date'
        )
        
        st.sidebar.markdown("### 💰 Fase de Acumulação")
        total_investments_today = st.number_input(
            "Total de Investimentos Atual",
            value=st.session_state.get('total_investments_today', 10000),
            min_value=0,
            step=100,
            help="Valor total dos seus investimentos hoje",
            key='total_investments_today'
        )
        
        col1, col2 = st.columns(2)
        with col1:
            monthly_investment = st.number_input(
                "Investimento Mensal",
                value=st.session_state.get('monthly_investment', 500),
                min_value=0,
                step=50,
                key='monthly_investment'
            )
        with col2:
            annual_rate_acc = st.number_input(
                "Taxa Real Anual (%)",
                value=st.session_state.get('annual_rate_acc', 3.0),
                min_value=0.0,
                step=0.1,
                key='annual_rate_acc'
            )
        
        st.sidebar.markdown("### 🎯 Fase de Aposentadoria")
        col1, col2 = st.columns(2)
        with col1:
            retirement_age = st.number_input(
                "Idade Alvo",
                value=st.session_state.get('retirement_age', 65),
                min_value=1,
                step=1,
                key='retirement_age'
            )
        with col2:
            life_expectancy = st.number_input(
                "Expectativa de Vida",
                value=st.session_state.get('life_expectancy', 90),
                min_value=retirement_age+1,
                step=1,
                key='life_expectancy'
            )
        
        annual_rate_ret = st.number_input(
            "Taxa Real na Aposentadoria (%)",
            value=st.session_state.get('annual_rate_ret', 3.0),
            step=0.1,
            key='annual_rate_ret'
        )
        
        st.sidebar.markdown("### 📈 Estratégia de Retirada")
        strategy_mode = st.radio(
            "Modo de Retirada",
            ["Retirada Personalizada", "Retirada Baseada em Estratégia"],
            help="Escolha como deseja planejar seus gastos na aposentadoria",
            key='strategy_mode',
            index=0 if st.session_state.get('strategy_mode') == "Retirada Personalizada" else 1
        )
        
        if strategy_mode == "Retirada Personalizada":
            monthly_expenses = st.number_input(
                "Despesas Mensais Desejadas",
                value=st.session_state.get('monthly_expenses', 4000),
                min_value=0,
                step=100,
                help="Quanto você planeja gastar mensalmente na aposentadoria",
                key='monthly_expenses'
            )
        else:
            strategy_type = st.radio(
                "Tipo de Estratégia",
                ["Zerar os Ativos (Drawdown)", "Renda Perpétua (Preservar o Principal)"],
                help="Escolha entre gastar todo o patrimônio ou preservar o principal",
                key='strategy_type',
                index=0 if st.session_state.get('strategy_type') == "Zerar os Ativos (Drawdown)" else 1
            )
            st.info("💡 Seus gastos mensais serão calculados automaticamente com base na estratégia escolhida.")
        
        st.sidebar.markdown("### 💸 Rendas Adicionais")
        n_sources = st.number_input(
            "Número de Fontes de Renda Extra",
            value=st.session_state.get('n_sources', 0),
            min_value=0,
            step=1,
            help="Adicione outras fontes de renda como aposentadoria, aluguéis, etc.",
            key='n_sources'
        )
        
        income_sources = []
        for i in range(int(n_sources)):
            with st.expander(f"📋 Fonte de Renda {i+1}"):
                name = st.text_input(f"Nome", value=f"Fonte {i+1}", key=f"name_{i}")
                monthly_income = st.number_input(
                    "Valor Mensal Inicial",
                    value=1000,
                    min_value=0,
                    step=50,
                    key=f"income_{i}"
                )
                income_start_age = st.number_input(
                    "Idade de Início",
                    value=retirement_age,
                    min_value=retirement_age,
                    step=1,
                    key=f"start_age_{i}"
                )
                lifetime = st.checkbox("Renda Vitalícia", value=True, key=f"lifetime_{i}")
                
                duration_years = None
                if not lifetime:
                    duration_years = st.number_input(
                        "Duração (anos)",
                        value=10,
                        min_value=1,
                        step=1,
                        key=f"duration_{i}"
                    )
                
                annual_rate_source = st.number_input(
                    "Taxa Real Anual (%)",
                    value=0.0,
                    step=0.1,
                    key=f"rate_{i}"
                )
                monthly_rate_source = (1 + annual_rate_source/100)**(1/12) - 1
                
                income_sources.append({
                    "name": name,
                    "monthly_income": monthly_income,
                    "income_start_age": income_start_age,
                    "lifetime": lifetime,
                    "duration_years": duration_years,
                    "annual_rate": annual_rate_source,
                    "monthly_rate": monthly_rate_source
                })

    ##############################
    # Cálculos Básicos e Validações
    ##############################
    today = datetime.date.today()
    current_age = (today - birth_date).days / 365.25
    
    # Card com informações básicas
    with st.container():
        st.markdown("""
        <div class='stCard'>
            <h3>📊 Resumo Inicial</h3>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Sua Idade Atual",
                f"{current_age:.1f} anos",
                help="Calculada com base na sua data de nascimento"
            )
        with col2:
            st.metric(
                "Anos até Aposentadoria",
                f"{retirement_age - current_age:.1f}",
                help="Tempo restante até atingir a idade alvo de aposentadoria"
            )
        with col3:
            st.metric(
                "Anos de Aposentadoria",
                f"{life_expectancy - retirement_age:.1f}",
                help="Período estimado de aposentadoria"
            )
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Validações com mensagens de erro estilizadas
    if retirement_age <= current_age:
        st.error("⚠️ A idade de aposentadoria deve ser maior que sua idade atual.")
        return
    if life_expectancy <= retirement_age:
        st.error("⚠️ A expectativa de vida deve ser maior que a idade de aposentadoria.")
        return
    
    accumulation_years = retirement_age - current_age
    retirement_years = life_expectancy - retirement_age
    accumulation_months = math.ceil(accumulation_years * 12)
    retirement_months = math.ceil(retirement_years * 12)
    
    monthly_rate_acc = (1 + annual_rate_acc/100)**(1/12) - 1
    monthly_rate_ret = (1 + annual_rate_ret/100)**(1/12) - 1
    
    ##############################
    # Simulação da Fase de Acumulação
    ##############################
    ages = []
    portfolio_balances = []
    net_cash_flows = []           # (Usado somente no modo "Retirada Personalizada" na aposentadoria)
    additional_incomes_dynamic = []  # Renda adicional dinâmica (para modo personalizado)
    
    balance = total_investments_today
    for m in range(accumulation_months + 1):
        age = current_age + m/12
        ages.append(age)
        portfolio_balances.append(balance)
        net_cash_flows.append(None)
        additional_incomes_dynamic.append(None)
        if m < accumulation_months:
            balance = balance * (1 + monthly_rate_acc) + monthly_investment
    
    portfolio_at_retirement = balance
    
    ##############################
    # Simulação da Fase de Aposentadoria
    ##############################
    retire_ages = []
    retire_portfolio = []
    retire_net_withdrawals = []
    retire_additional_income = []
    
    if strategy_mode == "Retirada Personalizada":
        # Simula mês a mês com renda dinâmica de cada fonte.
        for m in range(1, retirement_months + 1):
            sim_age = retirement_age + m/12
            total_income = 0
            for source in income_sources:
                if sim_age < source["income_start_age"]:
                    income = 0
                else:
                    months_since_start = int(round((sim_age - source["income_start_age"]) * 12))
                    if not source["lifetime"]:
                        if sim_age > source["income_start_age"] + source["duration_years"]:
                            income = 0
                        else:
                            income = source["monthly_income"] * ((1 + source["monthly_rate"]) ** months_since_start)
                    else:
                        income = source["monthly_income"] * ((1 + source["monthly_rate"]) ** months_since_start)
                total_income += income
            
            retire_additional_income.append(total_income)
            net_withdrawal = monthly_expenses - total_income
            retire_net_withdrawals.append(net_withdrawal)
            balance = balance * (1 + monthly_rate_ret) - net_withdrawal
            retire_ages.append(sim_age)
            retire_portfolio.append(balance)
            if balance < 0:
                break
    else:
        # Modo "Retirada Baseada em Estratégia"
        A0 = 0
        for source in income_sources:
            if retirement_age >= source["income_start_age"]:
                if not source["lifetime"]:
                    if retirement_age <= source["income_start_age"] + source["duration_years"]:
                        A0 += source["monthly_income"]
                else:
                    A0 += source["monthly_income"]
        
        n = retirement_months
        r = monthly_rate_ret
        if strategy_type == "Zerar os Ativos (Drawdown)":
            if r == 0:
                computed_portfolio_withdrawal = portfolio_at_retirement / n
            else:
                computed_portfolio_withdrawal = portfolio_at_retirement * (r * (1 + r)**n) / ((1 + r)**n - 1)
        else:  # "Renda Perpétua (Preservar o Principal)"
            computed_portfolio_withdrawal = portfolio_at_retirement * r
        
        recommended_total_spending = computed_portfolio_withdrawal + A0
        
        st.subheader("Conselho de Gastos na Aposentadoria")
        st.write(f"Na aposentadoria (aos {retirement_age} anos), seu portfólio está estimado em **R$ {portfolio_at_retirement:,.2f}**.")
        st.write(f"Com base na renda adicional disponível na aposentadoria (**R$ {A0:,.2f} mensais**):")
        if strategy_type == "Zerar os Ativos (Drawdown)":
            st.write(
                f"Uma estratégia de **Drawdown** exige uma retirada mensal do portfólio de **R$ {computed_portfolio_withdrawal:,.2f}**. "
                f"Isso resulta em um gasto total mensal de **R$ {recommended_total_spending:,.2f}**, zerando seus ativos aos {life_expectancy} anos."
            )
        else:
            st.write(
                f"Uma estratégia de **Renda Perpétua** permite uma retirada mensal do portfólio de **R$ {computed_portfolio_withdrawal:,.2f}**. "
                f"Isso gera um gasto total mensal de **R$ {recommended_total_spending:,.2f}**, preservando seu principal."
            )
        
        retire_ages = []
        retire_portfolio = []
        retire_net_withdrawals = []
        retire_additional_income = []
        for m in range(1, retirement_months + 1):
            sim_age = retirement_age + m/12
            retire_additional_income.append(A0)
            retire_net_withdrawals.append(computed_portfolio_withdrawal)
            balance = balance * (1 + monthly_rate_ret) - computed_portfolio_withdrawal
            retire_ages.append(sim_age)
            retire_portfolio.append(balance)
            if strategy_type == "Zerar os Ativos (Drawdown)" and balance < 0:
                break
    
    # Combina os dados da fase de Acumulação e Aposentadoria.
    sim_ages = ages + retire_ages
    sim_portfolio = portfolio_balances + retire_portfolio
    sim_net_withdrawals = net_cash_flows + retire_net_withdrawals
    sim_add_income = additional_incomes_dynamic + retire_additional_income
    
    df = pd.DataFrame({
        "Idade": sim_ages,
        "Saldo do Portfólio (R$)": sim_portfolio,
        "Retirada do Portfólio (R$)": sim_net_withdrawals,
        "Renda Adicional (R$)": sim_add_income
    })
    
    ##############################
    # Visualização dos Resultados
    ##############################
    tab1, tab2, tab3 = st.tabs([
        "📈 Gráfico da Simulação",
        "📋 Resumo Detalhado",
        "💾 Download dos Dados"
    ])
    
    with tab1:
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        st.subheader("📈 Evolução do Patrimônio")
        
        # Gráfico do patrimônio (código existente)
        fig = go.Figure()
        
        # Área sombreada para fase de acumulação
        fig.add_vrect(
            x0=current_age,
            x1=retirement_age,
            fillcolor="rgba(46, 204, 113, 0.1)",
            layer="below",
            line_width=0,
            annotation_text="Fase de Acumulação",
            annotation_position="top left"
        )
        
        # Área sombreada para fase de aposentadoria
        fig.add_vrect(
            x0=retirement_age,
            x1=life_expectancy,
            fillcolor="rgba(52, 152, 219, 0.1)",
            layer="below",
            line_width=0,
            annotation_text="Fase de Aposentadoria",
            annotation_position="top left"
        )
        
        # Linha principal do portfólio
        fig.add_trace(go.Scatter(
            x=df["Idade"],
            y=df["Saldo do Portfólio (R$)"],
            mode='lines',
            name='Saldo do Portfólio',
            line=dict(color='#2ecc71', width=3),
            hovertemplate='Idade: %{x:.1f} anos<br>Saldo: R$ %{y:,.2f}<extra></extra>'
        ))
        
        if strategy_mode == "Retirada Personalizada" and n_sources > 0:
            fig.add_trace(go.Bar(
                x=df["Idade"],
                y=[val if val is not None else 0 for val in df["Retirada do Portfólio (R$)"]],
                name="Retirada Mensal",
                marker_color='rgba(231, 76, 60, 0.7)',
                hovertemplate='Idade: %{x:.1f} anos<br>Retirada: R$ %{y:,.2f}<extra></extra>',
                yaxis="y2"
            ))
        
        if strategy_mode == "Retirada Baseada em Estratégia":
            fig.add_trace(go.Scatter(
                x=retire_ages,
                y=[computed_portfolio_withdrawal]*len(retire_ages),
                mode='lines',
                name="Retirada Constante",
                line=dict(color='#e74c3c', dash='dash'),
                hovertemplate='Retirada: R$ %{y:,.2f}<extra></extra>'
            ))
        
        # Configuração do layout
        fig.update_layout(
            title={
                'text': "Evolução do seu Patrimônio",
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title="Idade (anos)",
            yaxis=dict(
                title="Saldo do Portfólio (R$)",
                gridcolor='rgba(0,0,0,0.1)',
                hoverformat="R$ ,.2f"
            ),
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bgcolor='rgba(255,255,255,0.8)'
            ),
            hovermode="x unified",
            template="plotly_white",
            margin=dict(l=60, r=30, t=80, b=60)
        )
        
        if strategy_mode == "Retirada Personalizada" and n_sources > 0:
            fig.update_layout(
                yaxis2=dict(
                    title="Retirada Mensal (R$)",
                    overlaying="y",
                    side="right",
                    showgrid=False,
                    hoverformat="R$ ,.2f"
                )
            )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Novo gráfico de evolução da renda
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        st.subheader("📊 Evolução da Renda")
        
        # Controles para seleção das fontes de renda
        st.write("Selecione as fontes de renda que deseja visualizar:")
        
        # Checkbox para incluir retirada do patrimônio
        include_portfolio_withdrawal = st.checkbox(
            "Incluir Retirada do Patrimônio",
            value=True,
            help="Soma a retirada do patrimônio com as outras rendas selecionadas"
        )
        
        # Checkboxes para cada fonte de renda adicional
        selected_sources = []
        if n_sources > 0:
            cols = st.columns(min(3, n_sources))
            for i, source in enumerate(income_sources):
                with cols[i % 3]:
                    if st.checkbox(
                        f"📌 {source['name']}",
                        value=True,
                        help=f"Renda mensal inicial: R$ {source['monthly_income']:,.2f}"
                    ):
                        selected_sources.append(source)
        
        # Criar DataFrame com evolução das rendas
        income_data = []
        ages_range = np.arange(current_age, life_expectancy + 1/12, 1/12)
        
        # Inicializar array de rendas totais
        total_income = np.zeros(len(ages_range))
        
        # Adicionar retirada do patrimônio se selecionada
        if include_portfolio_withdrawal:
            portfolio_withdrawals = []
            for age in ages_range:
                if age < retirement_age:
                    portfolio_withdrawals.append(0)
                else:
                    if strategy_mode == "Retirada Personalizada":
                        portfolio_withdrawals.append(monthly_expenses)
                    else:
                        portfolio_withdrawals.append(computed_portfolio_withdrawal)
            
            income_data.append({
                'name': 'Retirada do Patrimônio',
                'ages': ages_range,
                'values': portfolio_withdrawals,
                'color': '#e74c3c'
            })
            total_income += np.array(portfolio_withdrawals)
        
        # Adicionar cada fonte de renda selecionada
        colors = ['#3498db', '#2ecc71', '#f1c40f', '#9b59b6', '#1abc9c', '#34495e']
        for i, source in enumerate(selected_sources):
            source_income = []
            for age in ages_range:
                if age < source['income_start_age']:
                    source_income.append(0)
                else:
                    months_since_start = int(round((age - source['income_start_age']) * 12))
                    if not source['lifetime']:
                        if age > source['income_start_age'] + source['duration_years']:
                            source_income.append(0)
                        else:
                            income = source['monthly_income'] * ((1 + source['monthly_rate']) ** months_since_start)
                            source_income.append(income)
                    else:
                        income = source['monthly_income'] * ((1 + source['monthly_rate']) ** months_since_start)
                        source_income.append(income)
            
            income_data.append({
                'name': source['name'],
                'ages': ages_range,
                'values': source_income,
                'color': colors[i % len(colors)]
            })
            total_income += np.array(source_income)
        
        # Criar gráfico de área empilhada
        fig_income = go.Figure()
        
        # Área sombreada para fase de aposentadoria
        fig_income.add_vrect(
            x0=retirement_age,
            x1=life_expectancy,
            fillcolor="rgba(52, 152, 219, 0.1)",
            layer="below",
            line_width=0,
            annotation_text="Fase de Aposentadoria",
            annotation_position="top left"
        )
        
        # Adicionar cada fonte de renda como área
        for source in income_data:
            fig_income.add_trace(go.Scatter(
                x=source['ages'],
                y=source['values'],
                name=source['name'],
                mode='none',
                fill='tonexty',
                fillcolor=f"rgba{tuple(list(ImageColor.getrgb(source['color'])) + [0.6])}",
                line=dict(width=0),
                hovertemplate='Idade: %{x:.1f} anos<br>Renda: R$ %{y:,.2f}<extra></extra>'
            ))
        
        # Adicionar linha do total
        fig_income.add_trace(go.Scatter(
            x=ages_range,
            y=total_income,
            name='Renda Total',
            mode='lines',
            line=dict(color='#2c3e50', width=2, dash='dash'),
            hovertemplate='Idade: %{x:.1f} anos<br>Total: R$ %{y:,.2f}<extra></extra>'
        ))
        
        # Configuração do layout
        fig_income.update_layout(
            title={
                'text': "Composição da Renda ao Longo do Tempo",
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title="Idade (anos)",
            yaxis_title="Renda Mensal (R$)",
            hovermode="x unified",
            template="plotly_white",
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bgcolor='rgba(255,255,255,0.8)'
            ),
            margin=dict(l=60, r=30, t=80, b=60)
        )
        
        st.plotly_chart(fig_income, use_container_width=True)
        
        # Adicionar estatísticas da renda
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "Renda Total na Aposentadoria",
                f"R$ {total_income[np.where(ages_range >= retirement_age)[0][0]]:,.2f}",
                help="Soma de todas as fontes de renda no início da aposentadoria"
            )
        with col2:
            st.metric(
                "Renda Média na Aposentadoria",
                f"R$ {np.mean(total_income[np.where(ages_range >= retirement_age)[0]]):,.2f}",
                help="Média da renda total durante todo o período de aposentadoria"
            )
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        st.subheader("📊 Análise Detalhada")
        
        # Métricas principais
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "Patrimônio na Aposentadoria",
                f"R$ {portfolio_at_retirement:,.2f}",
                delta=f"{((portfolio_at_retirement/total_investments_today - 1) * 100):.1f}% do valor atual"
            )
        
        with col2:
            final_balance = sim_portfolio[-1]
            if final_balance < 0:
                st.metric(
                    "Idade de Esgotamento do Patrimônio",
                    f"{sim_ages[-1]:.1f} anos",
                    delta="Patrimônio insuficiente",
                    delta_color="inverse"
                )
            else:
                st.metric(
                    "Saldo Final Projetado",
                    f"R$ {final_balance:,.2f}",
                    delta=f"aos {life_expectancy} anos"
                )
        
        # Informações adicionais
        if strategy_mode == "Retirada Baseada em Estratégia":
            st.info(f"""
            💡 **Recomendação de Gastos Mensais**
            
            Com base na sua estratégia de {strategy_type}:
            - Retirada mensal sugerida do portfólio: **R$ {computed_portfolio_withdrawal:,.2f}**
            - Renda adicional disponível: **R$ {A0:,.2f}**
            - Gasto mensal total possível: **R$ {recommended_total_spending:,.2f}**
            """)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab3:
        st.markdown("<div class='stCard'>", unsafe_allow_html=True)
        st.subheader("💾 Download dos Dados")
        
        col1, col2 = st.columns(2)
        with col1:
            # Botão para CSV
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Baixar CSV",
                data=csv,
                file_name='simulacao_aposentadoria.csv',
                mime='text/csv',
                help="Baixe os dados da simulação em formato CSV"
            )
        
        with col2:
            # Botão para Excel
            output = io.BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            df.to_excel(writer, index=False, sheet_name='Simulacao')
            writer.close()
            processed_data = output.getvalue()
            st.download_button(
                label="📥 Baixar Excel",
                data=processed_data,
                file_name='simulacao_aposentadoria.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                help="Baixe os dados da simulação em formato Excel"
            )
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Mensagem final
    st.markdown("""
    <div class='stCard' style='text-align: center;'>
        <h3>🎯 Planejamento Concluído!</h3>
        <p>Use estas projeções como guia para suas decisões financeiras. Lembre-se de revisar e ajustar seu plano periodicamente.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()