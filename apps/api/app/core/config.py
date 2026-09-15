from pydantic_settings import BaseSettings, SettingsConfigDict

# Herdamos de BaseSettings. O Pydantic fará o trabalho de validar se os tipos de dados estão corretos.
class Settings(BaseSettings):
    # Valores padrão: Se não passarmos nada no .env, ele usará "FitCore API"
    PROJECT_NAME: str = "FitCore API"
    VERSION: str = "0.1.0"
    
    # Como não tem valor padrão, o Pydantic vai OBRIGAR que o arquivo .env contenha a variável DATABASE_URL.
    # Se ela não existir, o aplicativo se recusa a iniciar. Isso previne erros silenciosos.
    DATABASE_URL: str
    
    # Esta linha diz ao Pydantic onde buscar as variáveis de ambiente secretas.
    # env_file=".env" diz que ele deve ler o arquivo .env localizado na raiz do projeto.
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")

# Instanciamos as configurações para importar e usar no resto do projeto.
# Daqui em diante, quando precisarmos da URL do banco, basta importar a variável `settings`.
settings = Settings()

