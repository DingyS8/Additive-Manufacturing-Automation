

***Como Iniciar***

```bash
pip install dash dash-bootstrap-components pandas plotly trimesh
```


```python
import pandas as pd
import numpy as np
from datetime import date
from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
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
# 2) APP E TEMA
# -----------------------------
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "Mini Dashboard de Vendas"

# -----------------------------
# 3) COMPONENTES REUTILIZÁVEIS
# -----------------------------
def kpi_card(titulo, valor, id_badge=None):
    return dbc.Card(
        [
            dbc.CardHeader(titulo, className="fw-semibold"),
            dbc.CardBody(
                [
                    html.H3(id=id_badge) if id_badge else html.H3(valor),
                ],
                className="py-3",
            ),
        ],
        className="shadow-sm h-100",
    )

# -----------------------------
# 4) LAYOUT
# -----------------------------
app.layout = dbc.Container(
    [
        # Título
        dbc.Row(
            [
                dbc.Col(
                    html.H2("📊 Dashboard de Vendas — Exemplo Dash", className="my-3"),
                    width=12
                )
            ]
        ),

        # Filtros
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Categoria:", className="fw-semibold"),
                        dcc.Dropdown(
                            id="filtro-categoria",
                            options=[{"label": c, "value": c} for c in categorias],
                            value=categorias[0],
                            clearable=False,
                        ),
                    ],
                    md=4,
                ),
                dbc.Col(
                    [
                        html.Label("Região:", className="fw-semibold"),
                        dcc.Dropdown(
                            id="filtro-regiao",
                            options=[{"label": r, "value": r} for r in regioes] + [{"label": "Todas", "value": "Todas"}],
                            value="Todas",
                            clearable=False,
                        ),
                    ],
                    md=4,
                ),
                dbc.Col(
                    [
                        html.Label("Ano:", className="fw-semibold"),
                        dcc.Slider(
                            id="filtro-ano",
                            min=min(anos),
                            max=max(anos),
                            step=1,
                            value=max(anos),
                            marks={a: str(a) for a in anos},
                            tooltip={"placement": "bottom", "always_visible": True},
                        ),
                    ],
                    md=4,
                ),
            ],
            className="gy-3",
        ),

        html.Hr(className="my-3"),

        # KPIs
        dbc.Row(
            [
                dbc.Col(kpi_card("Receita (R$)", "—", id_badge="kpi-receita"), md=4),
                dbc.Col(kpi_card("Vendas (unid.)", "—", id_badge="kpi-vendas"), md=4),
                dbc.Col(kpi_card("Satisfação Média", "—", id_badge="kpi-satisfacao"), md=4),
            ],
            className="gy-3",
        ),

        html.Hr(className="my-3"),

        # Gráfico
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Receita por Categoria (ano selecionado)"),
                            dbc.CardBody(
                                dcc.Graph(id="grafico-receita", figure={}, style={"height": "420px"})
                            ),
                        ],
                        className="shadow-sm",
                    ),
                    md=8,
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Top 5 (Categoria/Região) por Receita"),
                            dbc.CardBody(
                                dcc.Loading(
                                    dcc.Graph(id="grafico-top5", figure={}, style={"height": "420px"}),
                                    type="default",
                                )
                            ),
                        ],
                        className="shadow-sm",
                    ),
                    md=4,
                ),
            ],
            className="gy-3 mb-4",
        ),

        dbc.Row(
            [
                dbc.Col(html.Small(f"Atualizado em {date.today().strftime('%d/%m/%Y')} — Exemplo didático."), width=12)
            ],
            className="pb-4"
        ),
    ],
    fluid=True,
)

# -----------------------------
# 5) CALLBACKS
# -----------------------------
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
    # Filtra por ano e categoria
    dff = df[(df["ano"] == ano)]
    if cat:
        dff = dff[dff["categoria"] == cat]
    if reg and reg != "Todas":
        dff = dff[dff["regiao"] == reg]

    # Evitar DataFrame vazio
    if dff.empty:
        # KPIs zerados
        k_receita = "R$ 0"
        k_vendas = "0"
        k_satisf = "—"

        # Gráficos vazios
        fig1 = px.bar(title="Sem dados para o filtro selecionado")
        fig2 = px.bar(title="Sem dados para o filtro selecionado")
        fig1.update_layout(margin=dict(l=20, r=20, t=60, b=20))
        fig2.update_layout(margin=dict(l=20, r=20, t=60, b=20))
        return k_receita, k_vendas, k_satisf, fig1, fig2

    # KPIs
    k_receita = f"R$ {dff['receita'].sum():,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    k_vendas = f"{int(dff['vendas'].sum()):,}".replace(",", ".")
    k_satisf = f"{dff['satisfacao'].mean():.2f} ⭐"

    # Gráfico 1: Receita por Categoria no ano (considerando filtro de região)
    g1 = df[(df["ano"] == ano)]
    if reg and reg != "Todas":
        g1 = g1[g1["regiao"] == reg]

    fig1 = px.bar(
        g1.groupby("categoria", as_index=False)["receita"].sum(),
        x="categoria",
        y="receita",
        labels={"categoria": "Categoria", "receita": "Receita (R$)"},
        text_auto=".2s",
    )
    fig1.update_traces(textposition="outside")
    fig1.update_layout(margin=dict(l=20, r=20, t=40, b=20), xaxis_title=None)

    # Gráfico 2: Top 5 (Categoria/Região) por Receita (no ano)
    g2 = df[df["ano"] == ano].copy()
    g2["cat_reg"] = g2["categoria"] + " — " + g2["regiao"]
    g2 = g2.groupby("cat_reg", as_index=False)["receita"].sum().nlargest(5, "receita")

    fig2 = px.bar(
        g2,
        x="receita",
        y="cat_reg",
        orientation="h",
        labels={"cat_reg": "Categoria — Região", "receita": "Receita (R$)"},
        text_auto=".2s",
    )
    fig2.update_layout(margin=dict(l=20, r=20, t=40, b=20), yaxis_title=None)

    return k_receita, k_vendas, k_satisf, fig1, fig2

# -----------------------------
# 6) MAIN
# -----------------------------
if __name__ == "__main__":
    app.run_server(debug=True)

```

**Salve o Conteúdo e execute: **
```bash
python app.py
```