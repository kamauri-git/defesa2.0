import psycopg2

try:
    conexao = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="654321",
        host="db.eczjxbeqpcpazuygpheh.supabase.co",
        port="5432"
    )
    print("✅ Conexão bem-sucedida com o banco de dados!")
    conexao.close()

except Exception as e:
    print("❌ Erro ao conectar:")
    print(e)
