import base64, io
import numpy as np
import plotly.graph_objects as go
import trimesh as tm
from dash import Dash, html, dcc, Input, Output, callback

from pathlib import Path
ASSETS = Path(__file__).parent / "assets"

app = Dash(
    __name__,
    assets_folder=str(ASSETS),     # <— força o Dash a usar ./assets ao lado do script
    assets_url_path="/assets"      # opcional (rota padrão)
)

app = Dash(__name__)
app.title = "Visualizador 3D — Tema Escuro"

# Cor de destaque (mantenha igual à --accent no CSS)
ACCENT = "#00C4FF"

def empty_fig(msg="📄 Faça upload de um STL/OBJ/PLY."):
    fig = go.Figure()
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False), yaxis=dict(visible=False),
        annotations=[dict(text=msg, x=0.5, y=0.5, showarrow=False, xref="paper", yref="paper",
                          font=dict(color="#A8A8A8", size=14))]
    )
    return fig

def mesh_to_figure(mesh: tm.Trimesh) -> go.Figure:
    V = mesh.vertices
    F = mesh.faces
    fig = go.Figure(
        data=[
            go.Mesh3d(
                x=V[:, 0], y=V[:, 1], z=V[:, 2],
                i=F[:, 0], j=F[:, 1], k=F[:, 2],
                color=ACCENT, opacity=1.0, flatshading=True,
                lighting=dict(ambient=0.45, diffuse=0.8, specular=0.7, roughness=0.45),
                lightposition=dict(x=1200, y=1200, z=1200),
                hoverinfo="skip",
            )
        ]
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        scene=dict(
            xaxis=dict(visible=False, showgrid=False, zeroline=False),
            yaxis=dict(visible=False, showgrid=False, zeroline=False),
            zaxis=dict(visible=False, showgrid=False, zeroline=False),
            aspectmode="data",
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        uirevision=True,  # preserva a câmera ao atualizar
    )
    fig.update_layout(scene_camera=dict(eye=dict(x=1.8, y=1.8, z=1.2)))
    return fig

app.layout = html.Div(
    className="page",
    children=[
        html.Div(
            className="container",
            children=[
                html.H2("👁️ Visualizador 3D no Dash", className="title"),
                html.P(
                    "Arraste um arquivo STL, OBJ ou PLY para visualizar em 3D (rotacione com o mouse).",
                    className="subtitle"
                ),

                # Área de upload (com ícone 📄)
                html.Div(
                    className="card",
                    children=[
                        dcc.Upload(
                            id="upload-model",
                            children=html.Div(
                                className="upload-area",
                                children=["📄  Solte o arquivo aqui ou ", html.B("clique para selecionar")]
                            ),
                            multiple=False,
                        ),
                    ],
                ),

                # Checklist para wireframe
                html.Div(
                    className="controls",
                    children=dcc.Checklist(
                        id="chk-wire",
                        options=[{"label": " Mostrar wireframe", "value": "wire"}],
                        value=[],
                        className="checklist"
                    ),
                ),

                # Gráfico 3D
                html.Div(
                    className="card graph-card",
                    children=dcc.Graph(id="graph3d", figure=empty_fig(), style={"height": "70vh"}),
                ),

                html.Small(
                    "Dica: Scroll = zoom · Botão direito = pan · Botão esquerdo = rotacionar.",
                    className="hint"
                ),
            ],
        )
    ]
)

@callback(
    Output("graph3d", "figure"),
    Input("upload-model", "contents"),
    Input("upload-model", "filename"),
    Input("chk-wire", "value"),
)
def render_model(contents, filename, flags):
    if not contents or not filename:
        return empty_fig()

    # Decodifica o arquivo base64
    header, b64 = contents.split(",")
    data = base64.b64decode(b64)
    buf = io.BytesIO(data)

    # Detecta tipo pelo sufixo
    ext = filename.split(".")[-1].lower()
    obj = tm.load(buf, file_type=ext) if ext in {"stl", "obj", "ply"} else tm.load(buf)

    # Scene -> unir geometrias
    if isinstance(obj, tm.Trimesh):
        mesh = obj
    else:
        geoms = list(getattr(obj, "geometry", {}).values())
        if not geoms:
            return empty_fig("Não foi possível ler a malha.")
        mesh = tm.util.concatenate(geoms)

    fig = mesh_to_figure(mesh)

    # Wireframe opcional
    if "wire" in (flags or []):
        edges = mesh.edges_unique
        seg = go.Scatter3d(
            x=np.r_[mesh.vertices[edges][:, :, 0].T, [None]*edges.shape[0]].ravel(),
            y=np.r_[mesh.vertices[edges][:, :, 1].T, [None]*edges.shape[0]].ravel(),
            z=np.r_[mesh.vertices[edges][:, :, 2].T, [None]*edges.shape[0]].ravel(),
            mode="lines",
            line=dict(width=1, color="rgba(0,196,255,0.6)"),  # ACCENT com alpha
            hoverinfo="skip", showlegend=False
        )
        fig.add_trace(seg)

    return fig

if __name__ == "__main__":
    # Ajuste host/porta conforme sua rede
    app.run(debug=True, host="192.168.100.63", port=8050)
