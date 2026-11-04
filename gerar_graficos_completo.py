

# ==============================================================================
# GRÁFICOS INICIAIS
# ==============================================================================

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ENTRADA = Path("base_churn_nova_tratada.xlsx")
SAIDA = Path("graficos")
SAIDA.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", palette="deep")
CORES_CHURN = {0: "#4C78A8", 1: "#E45756"}
ROTULOS_CHURN = {0: "Permaneceu", 1: "Cancelou"}

base = pd.read_excel(ENTRADA, sheet_name="clientes_modelagem")
base["status_churn"] = base["churn"].map(ROTULOS_CHURN)

# 1. Distribuição do alvo.
contagem = base["status_churn"].value_counts().reindex(["Permaneceu", "Cancelou"])
fig, ax = plt.subplots(figsize=(8, 5))
barras = ax.bar(contagem.index, contagem.values, color=[CORES_CHURN[0], CORES_CHURN[1]])
ax.set_title("Distribuição do churn", fontsize=16, weight="bold")
ax.set_xlabel("Situação do cliente")
ax.set_ylabel("Quantidade de clientes")
for barra, valor in zip(barras, contagem.values):
    ax.text(barra.get_x() + barra.get_width()/2, valor + 35, f"{valor:,}".replace(",", "."), ha="center", weight="bold")
fig.tight_layout()
fig.savefig(SAIDA / "01_distribuicao_churn.png", dpi=160)
plt.close(fig)

# 2. Taxa de churn por tipo de contrato.
taxa_contrato = base.groupby("tipo_contrato", dropna=False)["churn"].agg(["mean", "count"]).reset_index()
taxa_contrato["taxa"] = taxa_contrato["mean"] * 100
taxa_contrato = taxa_contrato.sort_values("taxa", ascending=False)
fig, ax = plt.subplots(figsize=(8, 5))
barras = ax.bar(taxa_contrato["tipo_contrato"], taxa_contrato["taxa"], color="#F58518")
ax.set_title("Taxa de churn por tipo de contrato", fontsize=16, weight="bold")
ax.set_xlabel("Tipo de contrato")
ax.set_ylabel("Taxa de churn (%)")
ax.set_ylim(0, max(taxa_contrato["taxa"].max() * 1.2, 10))
for barra, taxa in zip(barras, taxa_contrato["taxa"]):
    ax.text(barra.get_x() + barra.get_width()/2, taxa + 0.7, f"{taxa:.1f}%", ha="center", weight="bold")
fig.tight_layout()
fig.savefig(SAIDA / "02_churn_por_contrato.png", dpi=160)
plt.close(fig)

# 3. Taxa de churn por forma de pagamento.
taxa_pagamento = base.groupby("forma_pagamento", dropna=False)["churn"].agg(["mean", "count"]).reset_index()
taxa_pagamento["taxa"] = taxa_pagamento["mean"] * 100
taxa_pagamento = taxa_pagamento.sort_values("taxa", ascending=False)
fig, ax = plt.subplots(figsize=(8, 5))
barras = ax.bar(taxa_pagamento["forma_pagamento"], taxa_pagamento["taxa"], color="#72B7B2")
ax.set_title("Taxa de churn por forma de pagamento", fontsize=16, weight="bold")
ax.set_xlabel("Forma de pagamento")
ax.set_ylabel("Taxa de churn (%)")
ax.set_ylim(0, max(taxa_pagamento["taxa"].max() * 1.2, 10))
for barra, taxa in zip(barras, taxa_pagamento["taxa"]):
    ax.text(barra.get_x() + barra.get_width()/2, taxa + 0.7, f"{taxa:.1f}%", ha="center", weight="bold")
fig.tight_layout()
fig.savefig(SAIDA / "03_churn_por_pagamento.png", dpi=160)
plt.close(fig)

# 4. Distribuição da mensalidade por classe de churn.
fig, ax = plt.subplots(figsize=(9, 5))
sns.boxplot(data=base, x="status_churn", y="mensalidade_rs", order=["Permaneceu", "Cancelou"], palette=[CORES_CHURN[0], CORES_CHURN[1]], ax=ax)
ax.set_title("Distribuição da mensalidade por situação", fontsize=16, weight="bold")
ax.set_xlabel("Situação do cliente")
ax.set_ylabel("Mensalidade (R$)")
fig.tight_layout()
fig.savefig(SAIDA / "04_mensalidade_por_churn.png", dpi=160)
plt.close(fig)

# 5. Taxa de churn por quantidade de chamados.
chamados = base.groupby("chamados_suporte")["churn"].agg(["mean", "count"]).reset_index()
chamados["taxa"] = chamados["mean"] * 100
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(chamados["chamados_suporte"], chamados["taxa"], marker="o", color="#E45756", linewidth=2.5)
ax.set_title("Taxa de churn por chamados de suporte", fontsize=16, weight="bold")
ax.set_xlabel("Chamados nos 90 dias anteriores")
ax.set_ylabel("Taxa de churn (%)")
ax.set_xticks(sorted(chamados["chamados_suporte"].unique()))
fig.tight_layout()
fig.savefig(SAIDA / "05_churn_por_chamados.png", dpi=160)
plt.close(fig)

# 6. Taxa de churn por quantidade de atrasos.
atrasos = base.groupby("atrasos_6m")["churn"].agg(["mean", "count"]).reset_index()
atrasos["taxa"] = atrasos["mean"] * 100
fig, ax = plt.subplots(figsize=(8, 5))
barras = ax.bar(atrasos["atrasos_6m"].astype(str), atrasos["taxa"], color="#B279A2")
ax.set_title("Taxa de churn por atrasos nos últimos 6 meses", fontsize=16, weight="bold")
ax.set_xlabel("Quantidade de atrasos")
ax.set_ylabel("Taxa de churn (%)")
ax.set_ylim(0, max(atrasos["taxa"].max() * 1.2, 10))
for barra, taxa in zip(barras, atrasos["taxa"]):
    ax.text(barra.get_x() + barra.get_width()/2, taxa + 0.7, f"{taxa:.1f}%", ha="center", weight="bold")
fig.tight_layout()
fig.savefig(SAIDA / "06_churn_por_atrasos.png", dpi=160)
plt.close(fig)

# 7. Perfil dos clientes por tempo de relacionamento.
base["faixa_tempo"] = pd.cut(
    base["tempo_cliente_meses"],
    bins=[-1, 12, 24, 36, 60, 120],
    labels=["Até 1 ano", "1–2 anos", "2–3 anos", "3–5 anos", "Mais de 5 anos"],
)
tempo = base.groupby("faixa_tempo", observed=False)["churn"].agg(["mean", "count"]).reset_index()
tempo["taxa"] = tempo["mean"] * 100
fig, ax = plt.subplots(figsize=(9, 5))
barras = ax.bar(tempo["faixa_tempo"].astype(str), tempo["taxa"], color="#54A24B")
ax.set_title("Taxa de churn por tempo de relacionamento", fontsize=16, weight="bold")
ax.set_xlabel("Tempo como cliente")
ax.set_ylabel("Taxa de churn (%)")
ax.tick_params(axis="x", rotation=15)
ax.set_ylim(0, max(tempo["taxa"].max() * 1.2, 10))
for barra, taxa in zip(barras, tempo["taxa"]):
    ax.text(barra.get_x() + barra.get_width()/2, taxa + 0.7, f"{taxa:.1f}%", ha="center", weight="bold")
fig.tight_layout()
fig.savefig(SAIDA / "07_churn_por_tempo_cliente.png", dpi=160)
plt.close(fig)

print(f"Gráficos salvos em: {SAIDA.resolve()}")
for arquivo in sorted(SAIDA.glob("*.png")):
    print(arquivo.name)

# ==============================================================================
# GRÁFICOS ADICIONAIS
# ==============================================================================

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

# 4. Taxa de churn por combinação de contrato x pagamento.
ordem_linhas = [x for x in ["Mensal", "Anual", "Bienal"] if x in base["tipo_contrato"].unique()]
ordem_colunas = [x for x in ["Boleto", "Cartão", "Pix"] if x in base["forma_pagamento"].unique()]
taxa_churn = (
    base[base["tipo_contrato"].isin(ordem_linhas) & base["forma_pagamento"].isin(ordem_colunas)]
    .pivot_table(index="tipo_contrato", columns="forma_pagamento", values="churn", aggfunc="mean")
    .mul(100)
    .reindex(index=ordem_linhas, columns=ordem_colunas)
)
fig, ax = plt.subplots(figsize=(9, 6))
sns.heatmap(
    taxa_churn, annot=True, fmt=".1f", cmap="YlOrRd", linewidths=0.5,
    vmin=0, vmax=max(50, float(taxa_churn.max().max()) * 1.05),
    cbar_kws={"label": "Taxa de churn (%)"}, ax=ax,
)
for texto in ax.texts:
    texto.set_text(f"{float(texto.get_text()):.1f}%")
ax.set_title("Taxa de churn: tipo de contrato × forma de pagamento", fontsize=16, weight="bold", pad=15)
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

# ==============================================================================
# DISTRIBUIÇÃO, KDE, VIOLINOS E ESCALAS
# ==============================================================================

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ENTRADA = Path("base_churn_nova_tratada.xlsx")
SAIDA = Path("graficos_distribuicao")
SAIDA.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", font_scale=1.0)
base = pd.read_excel(ENTRADA, sheet_name="clientes_modelagem")
base["status_churn"] = base["churn"].map({0: "Permaneceu", 1: "Cancelou"})

# Variáveis numéricas contínuas ou de contagem usadas na análise.
variaveis = [
    "tempo_cliente_meses",
    "mensalidade_rs",
    "chamados_suporte",
    "atrasos_6m",
]
rotulos = {
    "tempo_cliente_meses": "Tempo de cliente (meses)",
    "mensalidade_rs": "Mensalidade (R$)",
    "chamados_suporte": "Chamados de suporte",
    "atrasos_6m": "Atrasos nos últimos 6 meses",
}
ordem_classes = ["Permaneceu", "Cancelou"]
cores = {"Permaneceu": "#4C78A8", "Cancelou": "#E45756"}

# 1. Box plots das variáveis numéricas por classe.
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
for ax, coluna in zip(axes.flatten(), variaveis):
    sns.boxplot(
        data=base,
        x="status_churn",
        y=coluna,
        order=ordem_classes,
        hue="status_churn",
        hue_order=ordem_classes,
        palette=cores,
        legend=False,
        ax=ax,
    )
    ax.set_title(rotulos[coluna], weight="bold")
    ax.set_xlabel("Status do cliente")
    ax.set_ylabel("")
fig.suptitle("Box plots das variáveis numéricas por classe de churn", fontsize=17, weight="bold")
fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig(SAIDA / "13_boxplots_numericas_por_classe.png", dpi=160, bbox_inches="tight")
plt.close(fig)

# 2. Gráficos de densidade de probabilidade (KDE) por classe.
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
for ax, coluna in zip(axes.flatten(), variaveis):
    for classe in ordem_classes:
        valores = base.loc[base["status_churn"] == classe, coluna].dropna()
        # KDE não é estável para um grupo com apenas um valor distinto.
        if valores.nunique() > 1:
            sns.kdeplot(
                valores,
                fill=True,
                alpha=0.25,
                linewidth=2,
                color=cores[classe],
                label=classe,
                ax=ax,
            )
    ax.set_title(rotulos[coluna], weight="bold")
    ax.set_xlabel("")
    ax.set_ylabel("Densidade")
    ax.legend(title="Classe")
fig.suptitle("Densidade de probabilidade (KDE) por classe de churn", fontsize=17, weight="bold")
fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig(SAIDA / "14_kde_numericas_por_classe.png", dpi=160, bbox_inches="tight")
plt.close(fig)

# 3. Violin plots por classe.
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
for ax, coluna in zip(axes.flatten(), variaveis):
    sns.violinplot(
        data=base,
        x="status_churn",
        y=coluna,
        order=ordem_classes,
        hue="status_churn",
        hue_order=ordem_classes,
        palette=cores,
        inner="quartile",
        cut=0,
        legend=False,
        ax=ax,
    )
    ax.set_title(rotulos[coluna], weight="bold")
    ax.set_xlabel("Status do cliente")
    ax.set_ylabel("")
fig.suptitle("Violin plots das variáveis numéricas por classe de churn", fontsize=17, weight="bold")
fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig(SAIDA / "15_violinplots_numericas_por_classe.png", dpi=160, bbox_inches="tight")
plt.close(fig)

# 4. Transformações Min-Max e StandardScaler.
# A transformação é feita apenas para visualização comparativa das escalas.
X = base[variaveis].copy()
# Fórmulas equivalentes às transformações do scikit-learn, implementadas
# diretamente para que o script funcione apenas com Pandas.
amplitudes = X.max() - X.min()
amplitudes = amplitudes.replace(0, 1)
minmax = (X - X.min()) / amplitudes
desvios = X.std(ddof=0).replace(0, 1)
zscore = (X - X.mean()) / desvios

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
for ax, coluna in zip(axes.flatten(), variaveis):
    comparacao = pd.DataFrame({
        "Original": X[coluna],
        "Min-Max [0, 1]": minmax[coluna],
        "StandardScaler (Z-Score)": zscore[coluna],
    })
    comparacao_melt = comparacao.melt(var_name="escala", value_name="valor")
    sns.boxplot(
        data=comparacao_melt,
        x="escala",
        y="valor",
        color="#72B7B2",
        ax=ax,
    )
    ax.set_title(rotulos[coluna], weight="bold")
    ax.set_xlabel("")
    ax.set_ylabel("Valor transformado")
    ax.tick_params(axis="x", rotation=20)
fig.suptitle("Transformação de escala: original vs. Min-Max vs. StandardScaler", fontsize=17, weight="bold")
fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig(SAIDA / "16_comparacao_escalas.png", dpi=160, bbox_inches="tight")
plt.close(fig)

# Exporta uma tabela de apoio com os valores transformados.
base_escalada = base[["id_cliente", "churn"]].copy()
for coluna in variaveis:
    base_escalada[f"{coluna}_minmax"] = minmax[coluna]
    base_escalada[f"{coluna}_zscore"] = zscore[coluna]
base_escalada.to_csv(SAIDA / "dados_transformados.csv", index=False, encoding="utf-8-sig")

# 5. Gráfico mensalidade original, Min-Max e Z-Score.
variavel_aula = "mensalidade_rs"
valor_original = X[variavel_aula].dropna()
valor_minmax = minmax[variavel_aula].dropna()
valor_zscore = zscore[variavel_aula].dropna()

fig = plt.figure(figsize=(13, 7), facecolor="#F7F7F7")
grade = fig.add_gridspec(
    nrows=1,
    ncols=3,
    width_ratios=[1.0, 1.0, 1.0],
    wspace=0.28,
    left=0.055,
    right=0.97,
    top=0.84,
    bottom=0.18,
)

ax_original = fig.add_subplot(grade[0, 0])
ax_minmax = fig.add_subplot(grade[0, 1])
ax_zscore = fig.add_subplot(grade[0, 2])

fig.suptitle(
    "Transformação de Escala: Min-Max [0,1] vs. StandardScaler (Z-Score)",
    fontsize=18,
    weight="bold",
    color="#242A4A",
    x=0.50,
    y=0.95,
)

def histograma(ax, valores, bins, cor, titulo, xlabel):
    ax.hist(valores, bins=bins, color=cor, edgecolor="#263238", linewidth=0.65)
    ax.set_title(titulo, fontsize=10, weight="bold", color="#263238", pad=10)
    ax.set_xlabel(xlabel, fontsize=8)
    ax.set_ylabel("Frequência", fontsize=8)
    ax.tick_params(axis="both", labelsize=7)
    ax.grid(axis="y", alpha=0.25)
    ax.set_axisbelow(True)

histograma(
    ax_original,
    valor_original,
    bins=24,
    cor="#37474F",
    titulo="1. Escala Original (R$)",
    xlabel=f"[{valor_original.min():.2f}, {valor_original.max():.2f}]",
)
histograma(
    ax_minmax,
    valor_minmax,
    bins=24,
    cor="#28A887",
    titulo="2. Normalização Min-Max",
    xlabel="Escala [0, 1]",
)
histograma(
    ax_zscore,
    valor_zscore,
    bins=24,
    cor="#E8872D",
    titulo="3. Padronização StandardScaler",
    xlabel="Z-Score (Desvios Padrão)",
)

fig.text(
    0.055,
    0.075,
    "ANÁLISE EXPLORATÓRIA • BASE DE CHURN • VARIÁVEL: MENSALIDADE",
    fontsize=8,
    color="#6B7280",
)
fig.savefig(
    SAIDA / "16b_transformacao_escalas.png",
    dpi=160,
    bbox_inches="tight",
    facecolor=fig.get_facecolor(),
)
plt.close(fig)

print(f"Gráficos salvos em: {SAIDA.resolve()}")
for arquivo in sorted(SAIDA.glob("*.png")):
    print(arquivo.name)
print("dados_transformados.csv")

# ==============================================================================
# ANÁLISES BIVARIADAS
# ==============================================================================

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ENTRADA = Path("base_churn_nova_tratada.xlsx")
SAIDA = Path("graficos_bivariados")
SAIDA.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", font_scale=1.0)
base = pd.read_excel(ENTRADA, sheet_name="clientes_modelagem")
base["status_churn"] = base["churn"].map({0: "Permaneceu", 1: "Cancelou"})
base_sem_desconhecido = base[base["tipo_contrato"] != "Desconhecido"].copy()
ordem_classes = ["Permaneceu", "Cancelou"]
cores = {"Permaneceu": "#4C78A8", "Cancelou": "#E45756"}
ordem_contratos = ["Mensal", "Anual", "Bienal"]

# 1. Análise bivariada: tempo de cliente x chamados de suporte.
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(
    data=base,
    x="tempo_cliente_meses",
    y="chamados_suporte",
    hue="status_churn",
    hue_order=ordem_classes,
    palette=cores,
    alpha=0.55,
    s=55,
    ax=ax,
)
ax.set_title("Análise bivariada: tempo de cliente × chamados de suporte", fontsize=16, weight="bold")
ax.set_xlabel("Tempo de cliente (meses)")
ax.set_ylabel("Chamados de suporte nos 90 dias anteriores")
ax.legend(title="Status do cliente")
fig.tight_layout()
fig.savefig(SAIDA / "17_bivariada_tempo_chamados.png", dpi=160, bbox_inches="tight")
plt.close(fig)

# 2. Countplot: frequência de contratos por status de churn.
fig, ax = plt.subplots(figsize=(10, 6))
sns.countplot(
    data=base_sem_desconhecido,
    x="tipo_contrato",
    hue="status_churn",
    order=ordem_contratos,
    hue_order=ordem_classes,
    palette=cores,
    ax=ax,
)
ax.set_title("Frequência de contratos por status de churn", fontsize=16, weight="bold")
ax.set_xlabel("Tipo de contrato")
ax.set_ylabel("Quantidade de clientes")
ax.legend(title="Status do cliente")
fig.tight_layout()
fig.savefig(SAIDA / "18_countplot_contratos_status_churn.png", dpi=160, bbox_inches="tight")
plt.close(fig)

# 3. Scatterplot com FacetGrid: tempo vs. mensalidade, separado por contrato.
grid = sns.lmplot(
    data=base_sem_desconhecido,
    x="tempo_cliente_meses",
    y="mensalidade_rs",
    col="tipo_contrato",
    col_order=ordem_contratos,
    hue="status_churn",
    hue_order=ordem_classes,
    palette=cores,
    height=4.8,
    aspect=0.95,
    scatter_kws={"alpha": 0.45, "s": 35},
    fit_reg=False,
)
grid.set_axis_labels("Tempo de cliente (meses)", "Mensalidade (R$)")
grid.set_titles("Contrato: {col_name}")
grid.figure.suptitle("Tempo vs. mensalidade por tipo de contrato", y=1.05, fontsize=16, weight="bold")
grid.figure.savefig(SAIDA / "19_facetgrid_tempo_mensalidade_contrato.png", dpi=160, bbox_inches="tight")
plt.close(grid.figure)

# 4. Regression plot: tendência linear entre tempo e chamados por status de churn.
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(
    data=base,
    x="tempo_cliente_meses",
    y="chamados_suporte",
    hue="status_churn",
    hue_order=ordem_classes,
    palette=cores,
    alpha=0.35,
    s=35,
    ax=ax,
    legend=True,
)
for status in ordem_classes:
    dados_status = base[base["status_churn"] == status]
    sns.regplot(
        data=dados_status,
        x="tempo_cliente_meses",
        y="chamados_suporte",
        scatter=False,
        color=cores[status],
        line_kws={"linewidth": 2.5},
        ax=ax,
    )
ax.set_title("Tendência linear: tempo de cliente × chamados de suporte", fontsize=16, weight="bold")
ax.set_xlabel("Tempo de cliente (meses)")
ax.set_ylabel("Chamados de suporte")
ax.legend(title="Status do cliente")
fig.tight_layout()
fig.savefig(SAIDA / "20_regression_tempo_chamados.png", dpi=160, bbox_inches="tight")
plt.close(fig)

# 5. Strip plot: mensalidade por número de chamados e status de churn.
fig, ax = plt.subplots(figsize=(11, 6))
sns.stripplot(
    data=base,
    x="chamados_suporte",
    y="mensalidade_rs",
    hue="status_churn",
    hue_order=ordem_classes,
    palette=cores,
    dodge=True,
    jitter=0.22,
    alpha=0.5,
    size=4,
    ax=ax,
)
ax.set_title("Mensalidade por número de chamados e status de churn", fontsize=16, weight="bold")
ax.set_xlabel("Chamados de suporte")
ax.set_ylabel("Mensalidade (R$)")
ax.legend(title="Status do cliente")
fig.tight_layout()
fig.savefig(SAIDA / "21_strip_mensalidade_chamados_churn.png", dpi=160, bbox_inches="tight")
plt.close(fig)

# 6. Letter-value plot (boxen plot): tempo de contrato por status de churn.
fig, ax = plt.subplots(figsize=(9, 6))
sns.boxenplot(
    data=base,
    x="status_churn",
    y="tempo_cliente_meses",
    order=ordem_classes,
    hue="status_churn",
    hue_order=ordem_classes,
    palette=cores,
    legend=False,
    ax=ax,
)
ax.set_title("Letter-value plot: tempo de contrato por status de churn", fontsize=16, weight="bold")
ax.set_xlabel("Status do cliente")
ax.set_ylabel("Tempo de contrato (meses)")
fig.tight_layout()
fig.savefig(SAIDA / "22_boxen_tempo_contrato_churn.png", dpi=160, bbox_inches="tight")
plt.close(fig)

print(f"Gráficos salvos em: {SAIDA.resolve()}")
for arquivo in sorted(SAIDA.glob("*.png")):
    print(arquivo.name)
