# ETL vs ELT Comparison

## ETL

In ETL, data is extracted from the source, transformed before loading,
and then loaded into the target system.

Example:

CSV → Python Transformation → PostgreSQL

## ELT

In ELT, data is extracted and loaded into the target system first.
Transformation is performed after loading.

Example:

CSV → Raw PostgreSQL Table → SQL Transformation → Target Table

## Comparison

| Feature | ETL | ELT |
|---|---|---|
| Transformation | Before loading | After loading |
| Processing | External engine | Target warehouse |
| Raw data retention | Usually limited | Easy |
| Scalability | Depends on ETL engine | Strong in cloud warehouses |
| Flexibility | Moderate | High |

## Architecture Decision

For this project, ELT is preferred when using a modern cloud
data warehouse because raw data can be retained and transformations
can be performed using warehouse compute.

For smaller local processing workloads, Python-based ETL is simpler.

Therefore, the project demonstrates both approaches.