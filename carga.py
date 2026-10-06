import pandas as pd
from sqlalchemy import create_engine, text

# Conexão com o banco SQLite local (arquivo iot_database.db)
engine = create_engine('sqlite:///iot_database.db')

print("1. Lendo o arquivo CSV...")
df = pd.read_csv('temperature_readings.csv')

print("2. Inserindo os dados na tabela do SQLite...")
df.to_sql('temperature_readings', engine, if_exists='replace', index=False)

print("3. Criando as Views SQL...")
with engine.connect() as conn:
    # Apaga as views se já existirem
    conn.execute(text("DROP VIEW IF EXISTS avg_temp_por_dispositivo;"))
    conn.execute(text("DROP VIEW IF EXISTS leituras_por_hora;"))
    conn.execute(text("DROP VIEW IF EXISTS temp_max_min_por_dia;"))
    
    # View 1: Média de temperatura por dispositivo
    conn.execute(text("""
        CREATE VIEW avg_temp_por_dispositivo AS
        SELECT device_id, AVG(temperature) as avg_temp
        FROM temperature_readings
        GROUP BY device_id;
    """))
    
    # View 2: Contagem de leituras por hora do dia (ajustado para SQLite)
    conn.execute(text("""
        CREATE VIEW leituras_por_hora AS
        SELECT strftime('%H', timestamp_coluna) as hora, COUNT(*) as contagem
        FROM temperature_readings
        GROUP BY hora
        ORDER BY hora;
    """))
    
    # View 3: Temperaturas máximas e mínimas por dia (ajustado para SQLite)
    conn.execute(text("""
        CREATE VIEW temp_max_min_por_dia AS
        SELECT date(timestamp_coluna) as data, MAX(temperature) as temp_max, MIN(temperature) as temp_min
        FROM temperature_readings
        GROUP BY data
        ORDER BY data;
    """))
    conn.commit()

print("Tudo pronto! Dados inseridos e views criadas no SQLite com sucesso!")
