import pandas as pd
from sqlalchemy import create_engine, text

# Conexão oficial PostgreSQL conforme o manual da UniFECAF
# Altere 'sua_senha' caso tenha definido outra senha no docker run
DB_URL = 'postgresql://postgres:sua_senha@localhost:5432/postgres'
engine = create_engine(DB_URL)

print("1. Lendo o arquivo CSV...")
df = pd.read_csv('temperature_readings.csv')

print("2. Inserindo os dados na tabela do PostgreSQL...")
df.to_sql('temperature_readings', engine, if_exists='replace', index=False)

print("3. Criando as Views SQL exigidas...")
with engine.connect() as conn:
    # View 1: Média de temperatura por dispositivo
    conn.execute(text("DROP VIEW IF EXISTS avg_temp_por_dispositivo CASCADE;"))
    conn.execute(text("""
        CREATE VIEW avg_temp_por_dispositivo AS
        SELECT device_id, AVG(temperature) as avg_temp
        FROM temperature_readings
        GROUP BY device_id;
    """))
    
    # View 2: Contagem de leituras por hora do dia
    conn.execute(text("DROP VIEW IF EXISTS leituras_por_hora CASCADE;"))
    conn.execute(text("""
        CREATE VIEW leituras_por_hora AS
        SELECT TO_CHAR(CAST(timestamp_coluna AS TIMESTAMP), 'HH24') as hora, COUNT(*) as contagem
        FROM temperature_readings
        GROUP BY hora
        ORDER BY hora;
    """))
    
    # View 3: Temperaturas máximas e mínimas por dia
    conn.execute(text("DROP VIEW IF EXISTS temp_max_min_por_dia CASCADE;"))
    conn.execute(text("""
        CREATE VIEW temp_max_min_por_dia AS
        SELECT DATE(CAST(timestamp_coluna AS TIMESTAMP)) as data, MAX(temperature) as temp_max, MIN(temperature) as temp_min
        FROM temperature_readings
        GROUP BY data
        ORDER BY data;
    """))
    conn.commit()

print("Pipeline executado com sucesso no PostgreSQL!")