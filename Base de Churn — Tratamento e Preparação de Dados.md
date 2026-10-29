# Base de Churn — Tratamento e Preparação de Dados

Projeto de preparação de uma base de clientes para análise e previsão de **churn** — cancelamento de clientes nos próximos 60 dias.

O projeto foi desenvolvido com base nas regras de negócio e de qualidade de dados apresentadas nas aulas de Sistemas Inteligentes.

## Objetivo

Transformar uma planilha bruta de clientes em uma base tratada e organizada para análise exploratória e treinamento de modelos de aprendizagem de máquina.

O processo realiza:

- validação dos dados;
- padronização de categorias;
- tratamento de valores ausentes;
- correção de valores fora do domínio;
- remoção de duplicidades;
- normalização dos chamados de suporte;
- cálculo do tempo de relacionamento do cliente;
- criação do alvo `churn`;
- geração de relatório de auditoria;
- exportação de uma nova planilha Excel organizada.

## Estrutura do projeto

```text
.
├── tratamento_base_churn.py          # Script principal de tratamento
├── base_churn_nova_tratada.xlsx      # Base final gerada pelo script
└── README.md                         # Documentação do projeto
```

> A base original não é alterada pelo script. O resultado é salvo em um novo arquivo.

## Tecnologias utilizadas

- Python 3.10 ou superior;
- Pandas;
- OpenPyXL;
- Excel/XLSX.

## Instalação

Clone o repositório:

```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
```

Instale as dependências:

```bash
pip install pandas openpyxl
```

Ou, se preferir criar um ambiente virtual:

```bash
python -m venv .venv
```

No Linux/macOS:

```bash
source .venv/bin/activate
```

No Windows:

```powershell
.venv\Scripts\activate
```

Depois instale as dependências:

```bash
pip install pandas openpyxl
```

## Como executar

Coloque o arquivo original na mesma pasta do script, com o nome:

```text
base_churn_5000_VF2_aluno.xlsx
```

Execute:

```bash
python tratamento_base_churn.py
```

O script irá gerar:

```text
base_churn_nova_tratada.xlsx
```

## Regras utilizadas

### Data de corte

A data de corte utilizada é:

```text
21/09/2026
```

O horizonte de previsão é de 60 dias, até:

```text
20/11/2026
```

O cliente recebe `churn = 1` quando a data de cancelamento está dentro dessa janela.

Clientes que já haviam cancelado antes ou na data de corte são excluídos da fotografia de previsão, pois não estão mais ativos para uma ação preventiva.

### Padronização de categorias

Os valores categóricos são convertidos para um padrão único:

| Campo | Valores padronizados |
|---|---|
| `tipo_contrato` | `Mensal`, `Anual`, `Bienal`, `Desconhecido` |
| `forma_pagamento` | `Boleto`, `Cartão`, `Pix`, `Desconhecido` |

Exemplos de correções:

```text
mensal  -> Mensal
bienal  -> Bienal
cartao  -> Cartão
PIX     -> Pix
```

### Mensalidade

A mensalidade válida deve estar entre R$ 10,00 e R$ 500,00.

Valores ausentes, negativos ou fora desse intervalo são tratados como inválidos e substituídos pela mediana da mensalidade dentro do tipo de contrato. O campo `mensalidade_ausente` indica quais registros precisaram desse tratamento.

### Atrasos

O campo `atrasos_6m` deve estar entre 0 e 6.

Valores ausentes ou fora desse intervalo são substituídos pela mediana do tipo de contrato. O campo `atrasos_ausente` indica quais registros foram tratados.

### Duplicidades

O identificador do cliente deve ser único dentro da fotografia da base. Quando o mesmo cliente aparece mais de uma vez, o script mantém uma ocorrência e registra a duplicidade na aba `auditoria`.

### Chamados de suporte

Na planilha original, os chamados aparecem juntos em uma única célula, separados por vírgulas. O script transforma esses dados em uma tabela normalizada, com um chamado por linha.

Além disso, a coluna `chamados_suporte` conta os chamados ocorridos nos 90 dias anteriores à data de corte.

## Abas do arquivo final

### `clientes_modelagem`

Base final para análise e treinamento do modelo. Contém:

- identificação do cliente;
- data de aquisição;
- data de corte;
- tempo de relacionamento em meses;
- mensalidade tratada;
- quantidade de chamados;
- quantidade de atrasos;
- contrato e forma de pagamento padronizados;
- indicadores de ausência;
- variáveis binárias;
- alvo `churn`.

### `chamados_suporte`

Tabela normalizada com um registro por chamado:

- `id_cliente`;
- `data_chamado`.

### `auditoria`

Registra os problemas identificados e as ações aplicadas:

- dados ausentes;
- valores fora do domínio;
- categorias não padronizadas;
- clientes duplicados.

### `dominios`

Lista os valores permitidos para os campos categóricos.

### `resumo`

Apresenta as principais métricas do processo, como quantidade de linhas, clientes distintos, duplicidades removidas e distribuição do alvo.

## Resultado atual

Com a base fornecida, o tratamento produz:

- 5.020 linhas originais;
- 5.000 clientes distintos;
- 20 duplicidades removidas;
- 4.990 clientes na base final;
- 1.772 clientes com `churn = 1`;
- 3.218 clientes com `churn = 0`.

## Observação sobre as datas

A planilha possui datas em mais de um formato, incluindo:

```text
DD/MM/AAAA
AAAA-MM-DD
```

O script trata os dois formatos para evitar que datas válidas sejam descartadas durante a leitura.

## Limitações

- A base é didática e não representa necessariamente clientes reais;
- o preenchimento por mediana é uma estratégia simples de imputação;
- para um projeto de produção, recomenda-se avaliar KNNImputer, modelos de imputação e validação temporal;
- o ajuste de qualquer imputador de machine learning deve ocorrer somente no conjunto de treinamento para evitar data leakage;
- o limiar de decisão do modelo deve considerar o custo de intervenção e a capacidade da equipe de relacionamento.

