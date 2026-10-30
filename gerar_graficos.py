"""Gráficos adicionais para análise exploratória da base de churn."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ENTRADA = Path("base_churn_nova_tratada.xlsx")
SAIDA = Path("graficos_adicionais")
SAIDA.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", font_scale=1.0)
base = pd.read_excel(ENTRADA, sheet_name="clientes_modelagem")
base["status_churn"] = base["churn"].map({0: "Permaneceu", 1: "Cancelou"})

# 1. Matriz de correlação das variáveis numéricas.
colunas_numericas = [
    "tempo_cliente_meses",
    "mensalidade_rs",
    "chamados_suporte",
    "atrasos_6m",
    "fibra_optica",
    "debito_automatico",
    "churn",
]
correlacao = base[colunas_numericas].corr(numeric_only=True)
fig, ax = plt.subplots(figsize=(11, 9))
sns.heatmap(
    correlacao,
    annot=True,
    fmt=".2f",
    cmap="RdBu_r",
    center=0,
    vmin=-1,
    vmax=1,
    square=True,
    linewidths=0.5,
    ax=ax,
)
ax.set_title("Matriz de correlação das variáveis numéricas", fontsize=16, weight="bold", pad=15)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
fig.tight_layout()
fig.savefig(SAIDA / "08_matriz_correlacao.png", dpi=160, bbox_inches="tight")
plt.close(fig)

# 2. Proporção de churn por categoria e meio de pagamento.
fig, axes = plt.subplots(1, 2, figsize=(15, 6))
for ax, coluna, titulo, cor in [
    (axes[0], "tipo_contrato", "Proporção de churn por tipo de contrato", "#F58518"),
    (axes[1], "forma_pagamento", "Proporção de churn por meio de pagamento", "#72B7B2"),
]:
    base_grafico = base[base[coluna] != "Desconhecido"]
    proporcao = base_grafico.groupby(coluna, dropna=False)["churn"].mean().mul(100).sort_values(ascending=False)
    barras = ax.bar(proporcao.index.astype(str), proporcao.values, color=cor)
    ax.set_title(titulo, fontsize=13, weight="bold")
    ax.set_xlabel(coluna.replace("_", " ").title())
    ax.set_ylabel("Clientes com churn (%)")
    ax.set_ylim(0, max(proporcao.max() * 1.2, 10))
    ax.tick_params(axis="x", rotation=20)
    for barra, valor in zip(barras, proporcao.values):
        ax.text(barra.get_x() + barra.get_width() / 2, valor + 0.8, f"{valor:.1f}%", ha="center", weight="bold")
fig.suptitle("Proporção de churn por categoria e meio de pagamento", fontsize=17, weight="bold")
fig.tight_layout()
fig.savefig(SAIDA / "09_proporcao_churn_categoria_pagamento.png", dpi=160, bbox_inches="tight")
plt.close(fig)

# 3. Countplot — frequência de contratos por status de churn.
fig, ax = plt.subplots(figsize=(10, 6))
ordem_contratos = ["Mensal", "Anual", "Bienal"]
base_countplot = base[base["tipo_contrato"] != "Desconhecido"]
sns.countplot(
    data=base_countplot,
    x="tipo_contrato",
    hue="status_churn",
    order=[x for x in ordem_contratos if x in base["tipo_contrato"].unique()],
    hue_order=["Permaneceu", "Cancelou"],
    palette={"Permaneceu": "#4C78A8", "Cancelou": "#E45756"},
    ax=ax,
)
ax.set_title("Frequência de contratos por status de churn", fontsize=16, weight="bold")
ax.set_xlabel("Tipo de contrato")
ax.set_ylabel("Quantidade de clientes")
ax.legend(title="Status do cliente")
fig.tight_layout()
fig.savefig(SAIDA / "10_countplot_contratos_status_churn.png", dpi=160, bbox_inches="tight")
plt.close(fig)

# 4. Crosstab heatmap — cruzamento real contrato x pagamento.
crosstab = pd.crosstab(base["tipo_contrato"], base["forma_pagamento"])
ordem_linhas = [x for x in ["Mensal", "Anual", "Bienal"] if x in crosstab.index]
ordem_colunas = [x for x in ["Boleto", "Cartão", "Pix"] if x in crosstab.columns]
crosstab = crosstab.reindex(index=ordem_linhas, columns=ordem_colunas, fill_value=0)
fig, ax = plt.subplots(figsize=(9, 6))
sns.heatmap(crosstab, annot=True, fmt="d", cmap="YlOrRd", linewidths=0.5, cbar_kws={"label": "Quantidade de clientes"}, ax=ax)
ax.set_title("Cruzamento real: tipo de contrato × forma de pagamento", fontsize=16, weight="bold", pad=15)
ax.set_xlabel("Forma de pagamento")
ax.set_ylabel("Tipo de contrato")
fig.tight_layout()
fig.savefig(SAIDA / "11_heatmap_contrato_pagamento.png", dpi=160, bbox_inches="tight")
plt.close(fig)

# 5. Histogramas e distribuição global das variáveis numéricas.
variaveis_hist = [
    ("tempo_cliente_meses", "Tempo de cliente (meses)"),
    ("mensalidade_rs", "Mensalidade (R$)"),
    ("chamados_suporte", "Chamados de suporte"),
    ("atrasos_6m", "Atrasos nos últimos 6 meses"),
]
fig, axes = plt.subplots(2, 2, figsize=(12, 9))
axes = axes.flatten()
for ax, (coluna, titulo) in zip(axes, variaveis_hist):
    sns.histplot(base[coluna].dropna(), bins=20, kde=True, color="#4C78A8", ax=ax)
    ax.set_title(titulo, weight="bold")
    ax.set_xlabel("")
    ax.set_ylabel("Frequência")
for ax in axes[len(variaveis_hist):]:
    ax.axis("off")
fig.suptitle("Histograma e distribuição global das variáveis numéricas", fontsize=17, weight="bold")
fig.tight_layout(rect=[0, 0, 1, 0.97])
fig.savefig(SAIDA / "12_histogramas_variaveis_numericas.png", dpi=160, bbox_inches="tight")
plt.close(fig)

print(f"Gráficos salvos em: {SAIDA.resolve()}")
for arquivo in sorted(SAIDA.glob("*.png")):
    print(arquivo.name)
