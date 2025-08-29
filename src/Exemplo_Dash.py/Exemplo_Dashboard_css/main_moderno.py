import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)  # opcional, só pra limpar o terminal

import pandas as pd
import numpy as np
from datetime import date
from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px

# -----------------------------
# 1) DADOS DE EXEMPLO (mock)
# -----------------------------
np.random.seed(42)
anos = list(range(2021, 2026))
categorias = ["Eletrônicos", "Casa & Decoração", "Moda", "Esportes"]
regioes = ["Sul", "Sudeste", "Centro-Oeste", "Nordeste", "Norte"]

dados = []
for ano in anos:
    for cat in categorias:
        for reg in regioes:
            vendas = np.random.randint(80, 400)
            receita = vendas * np.random.uniform(50, 350)
            satisfacao = np.random.uniform(3.2, 4.9)
            dados.append([ano, cat, reg, vendas, receita, satisfacao])

df = pd.DataFrame(dados, columns=["ano", "categoria", "regiao", "vendas", "receita", "satisfacao"])

# -----------------------------
# 2) APP
# -----------------------------
app = Dash(__name__)
app.title = "Dashboard de Vendas — UX Clean"

# -----------------------------
# 3) COMPONENTES REUTILIZÁVEIS
# -----------------------------
def kpi_card(titulo, valor, unidade=None, id_valor=None):
    return html.Div(
        className="card",
        children=[
            html.Div(titulo, className="kpi-title"),
            html.Div(
                className="kpi-value",
                children=[
                    html.Span(id=id_valor) if id_valor else html.Span(valor),
                    html.Span(unidade, className="kpi-badge") if unidade else None,
                ],
            ),
        ],
        style={"padding": "20px 22px"}
    )

# -----------------------------
# 4) LAYOUT
# -----------------------------
app.layout = html.Div(
    className="container",
    children=[

        # Título
        html.H2("📊 Dashboard de Vendas — Exemplo (UX Clean)", className="title"),
        html.P("Interface moderna, minimalista e responsiva — com paleta customizada e tipografia Inter.",
               className="subtitle"),

        # Filtros
        html.Div(
            className="grid row",
            children=[
                html.Div(
                    className="card col-4",
                    children=[
                        html.Label("Categoria", className="filter-label"),
                        dcc.Dropdown(
                            id="filtro-categoria",
                            options=[{"label": c, "value": c} for c in categorias],
                            value=categorias[0],
                            clearable=False,
                            className="custom-dropdown",
                        ),
                    ],
                    style={"padding": "18px"}
                ),
                html.Div(
                    className="card col-4",
                    children=[
                        html.Label("Região", className="filter-label"),
                        dcc.Dropdown(
                            id="filtro-regiao",
                            options=[{"label": r, "value": r} for r in regioes] + [{"label": "Todas", "value": "Todas"}],
                            value="Todas",
                            clearable=False,
                            className="custom-dropdown",
                        ),
                    ],
                    style={"padding": "18px"}
                ),
                html.Div(
                    className="card col-4",
                    children=[
                        html.Label("Ano", className="filter-label"),
                        dcc.Slider(
                            id="filtro-ano",
                            min=min(anos),
                            max=max(anos),
                            step=1,
                            value=max(anos),
                            marks={a: str(a) for a in anos},
                            tooltip={"placement": "bottom", "always_visible": True},
                            className="custom-slider",
                        ),
                    ],
                    style={"padding": "18px"}
                ),
            ]
        ),

        # KPIs
        html.Div(
            className="grid row",
            children=[
                html.Div(kpi_card("Receita Total", "—", "R$", id_valor="kpi-receita"), className="col-4"),
                html.Div(kpi_card("Vendas Totais", "—", "unid.", id_valor="kpi-vendas"), className="col-4"),
                html.Div(kpi_card("Satisfação Média", "—", "⭐", id_valor="kpi-satisfacao"), className="col-4"),
            ]
        ),

        # Gráficos
        html.Div(
            className="grid row",
            children=[
                html.Div(
                    className="card graph-card col-8",
                    children=[
                        html.Div("Receita por Categoria (ano selecionado)", className="card-header"),
                        html.Div(
                            className="card-body",
                            children=dcc.Graph(id="grafico-receita", figure={}, style={"height": "420px"})
                        ),
                    ],
                    style={"padding": "18px"}
                ),
                html.Div(
                    className="card graph-card col-4",
                    children=[
                        html.Div("Top 5 (Categoria/Região) por Receita", className="card-header"),
                        html.Div(
                            className="card-body",
                            children=dcc.Loading(
                                dcc.Graph(id="grafico-top5", figure={}, style={"height": "420px"}),
                                type="default",
                            ),
                        ),
                    ],
                    style={"padding": "18px"}
                ),
            ]
        ),

        # Rodapé
        html.Div(
            className="row",
            children=html.Small(
                f"Atualizado em {date.today().strftime('%d/%m/%Y')} — Exemplo didático.",
                style={"color": "var(--muted)"}
            ),
            style={"marginTop": "6px"}
        )
    ]
)

# -----------------------------
# 5) CALLBACKS (tema Plotly)
# -----------------------------
ACCENT = "#6C63FF"

def _apply_fig_theme(fig, showlegend=False):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#343A40"),
        margin=dict(l=12, r=12, t=8, b=12),
        showlegend=showlegend,
        xaxis=dict(gridcolor="rgba(0,0,0,0.06)", zeroline=False),
        yaxis=dict(gridcolor="rgba(0,0,0,0.06)", zeroline=False),
    )
    return fig

@callback(
    Output("kpi-receita", "children"),
    Output("kpi-vendas", "children"),
    Output("kpi-satisfacao", "children"),
    Output("grafico-receita", "figure"),
    Output("grafico-top5", "figure"),
    Input("filtro-categoria", "value"),
    Input("filtro-regiao", "value"),
    Input("filtro-ano", "value"),
)
def atualizar_dashboard(cat, reg, ano):
    dff = df[(df["ano"] == ano)]
    if cat:
        dff = dff[dff["categoria"] == cat]
    if reg and reg != "Todas":
        dff = dff[dff["regiao"] == reg]

    if dff.empty:
        k_receita = "0,00"
        k_vendas = "0"
        k_satisf = "—"

        fig1 = px.bar(title="Sem dados para o filtro selecionado")
        fig2 = px.bar(title="Sem dados para o filtro selecionado")
        fig1 = _apply_fig_theme(fig1)
        fig2 = _apply_fig_theme(fig2)
        return k_receita, k_vendas, k_satisf, fig1, fig2

    # KPIs
    k_receita = f"{dff['receita'].sum():,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    k_vendas = f"{int(dff['vendas'].sum()):,}".replace(",", ".")
    k_satisf = f"{dff['satisfacao'].mean():.2f}"

    # Gráfico 1
    g1 = df[(df["ano"] == ano)]
    if reg and reg != "Todas":
        g1 = g1[g1["regiao"] == reg]

    fig1 = px.bar(
        g1.groupby("categoria", as_index=False)["receita"].sum(),
        x="categoria",
        y="receita",
        labels={"categoria": "Categoria", "receita": "Receita (R$)"},
        text_auto=".2s",
        color_discrete_sequence=[ACCENT],
    )
    fig1.update_traces(textposition="outside", marker_line_width=0,
                       hovertemplate="<b>%{x}</b><br>R$ %{y:,.2f}<extra></extra>")
    fig1.update_layout(xaxis_title=None)
    fig1 = _apply_fig_theme(fig1)

    # Gráfico 2
    g2 = df[df["ano"] == ano].copy()
    g2["cat_reg"] = g2["categoria"] + " — " + g2["regiao"]
    g2 = g2.groupby("cat_reg", as_index=False)["receita"].sum().nlargest(5, "receita")

    fig2 = px.bar(
        g2, x="receita", y="cat_reg", orientation="h",
        labels={"cat_reg": "Categoria — Região", "receita": "Receita (R$)"},
        text_auto=".2s",
        color_discrete_sequence=[ACCENT],
    )
    fig2.update_traces(marker_line_width=0,
                       hovertemplate="<b>%{y}</b><br>R$ %{x:,.2f}<extra></extra>")
    fig2.update_layout(yaxis_title=None)
    fig2 = _apply_fig_theme(fig2)

    return k_receita, k_vendas, k_satisf, fig1, fig2

# -----------------------------
# 6) MAIN
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True, host="192.168.100.63", port=8050)
