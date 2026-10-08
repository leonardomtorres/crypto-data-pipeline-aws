# Crypto Market Risk Pipeline AWS

## Objetivo

Automatizar o acompanhamento diário de Bitcoin, Ethereum, Solana e Cardano, utilizando dados do CoinGecko e serviços AWS.

O projeto simula uma necessidade de uma equipe de risco: identificar quais ativos merecem investigação por mudanças de preço e volatilidade, verificando também se os dados estão completos e atualizados.

O painel apoia a priorização de análises. Não recomenda investimentos.

## O que será entregue

- Histórico de preços em reais.
- Atualização diária da base utilizada pelo dashboard.
- Retornos em 1, 7 e 30 dias.
- Volatilidade dos retornos diários em 30 dias.
- Queda em relação ao maior preço dos últimos 90 dias.
- Verificações de duplicidade, datas faltantes e atualização.

O horário de referência dos preços e a extensão do histórico serão definidos após verificar a API.

## Tecnologias propostas

- Python: coleta e validação das respostas da API.
- S3: armazenamento e reprocessamento dos dados coletados.
- Parquet: arquivos estruturados para consultas analíticas.
- Glue Data Catalog: registro do esquema e da localização das tabelas.
- Athena: consultas e transformações SQL sobre os dados no S3.
- IAM: controle das permissões de acesso.
- Airflow: agendamento e coordenação das tarefas.
- Docker: preparação do ambiente de execução.
- QuickSight: apresentação dos indicadores, após avaliar seu custo.

Começaremos com SQL em arquivos. A necessidade de dbt será avaliada durante a modelagem.

## Regras iniciais

Criptomoedas negociam continuamente. A frequência diária atende à rotina de análise proposta.

A carga histórica e a atualização diária devem alimentar a mesma base analítica.

Não preencheremos preços ausentes com zero. Métricas com histórico insuficiente serão identificadas.

## Estado atual

Primeira consulta local ao CoinGecko implementada e verificada. A infraestrutura AWS, a ingestão diária e o dashboard ainda não foram implementados.

## Como executar a inspeção

Com o ambiente virtual ativo, instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

Crie um `.env` com `COINGECKO_API_KEY`, usando `.env.example` como modelo. O `.env` não deve ser versionado.

```powershell
python ingestion\inspect_api.py
```

O script consulta Bitcoin em reais e mostra o preço atual, o horário de atualização da fonte e o horário da coleta em UTC. Ainda não grava dados no S3 nem estabelece o preço diário de referência para o histórico.
