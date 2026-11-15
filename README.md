# FreshCart Pipelines

**Assignment: From Git to Gold – Data Engineering Pipeline Orchestration**

This repository contains the full implementation of the Data Engineering assignment, covering:

- **Part A**: Git & CI/CD (GitHub Actions)
- **Part B**: FreshCart ELT pipeline on Snowflake (bronze → silver → quarantine → gold)
- **Part C**: Iris ML pipeline with Mage AI
- **Part D**: Food-order stream with RabbitMQ (topic exchange, ACK/NACK)
- **Bonus**: Stream into the lakehouse

## Repository Structure

```
freshcart-pipelines/
├── README.md
├── .gitignore
├── requirements.txt
├── elt/                    ← FreshCart ELT notebook (Part B)
├── iris_project/           ← Mage ML project (Part C)
│   ├── data_loaders/
│   ├── transformers/
│   ├── data_exporters/
│   └── metadata.yaml
├── stream/                 ← Dispatcher and driver scripts (Part D)
│   ├── dispatcher.py
│   └── driver.py
├── tests/
│   └── test_prepare_data.py
├── screenshots/            ← Evidence screenshots organised by part
│   ├── A_github_ci/
│   ├── B_freshcart_elt/
│   ├── C_mage_pipeline/
│   └── D_rabbitmq_stream/
└── .github/
    └── workflows/
        └── ci.yml
```

## Platform

- **Google Colab** (notebook execution)
- **Snowflake** (trial account – bronze/silver/gold ELT)
- **GitHub** (version control + CI/CD via GitHub Actions)
- **Mage AI** (ML pipeline orchestration)
- **RabbitMQ / CloudAMQP** (event streaming)
