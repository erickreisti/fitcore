from fastapi import FastAPI

# Inicializa o aplicativo FastAPI. O FastAPI é a classe principal que usamos para criar nossa API.
# Os parâmetros title, description e version servem para gerar a documentação automática da API (Swagger).
app = FastAPI(
    title="FitCore API",
    description="API do sistema de gestão para redes de academias",
    version="0.1.0",
)

# O "decorador" @app.get("/") diz ao FastAPI que quando alguém acessar a URL raiz (o endereço base da API) 
# usando o método HTTP GET, esta função deve ser executada.
@app.get("/")
def read_root():
    # Retorna um dicionário Python que o FastAPI converte automaticamente para JSON (o formato padrão das APIs)
    return {"message": "Bem-vindo à API do FitCore!"}

