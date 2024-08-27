broker_url = "amqp://guest:guest@rabbitmq"
# result_backend = "db+postgresql://myuser:mypassword@localhost:5432/mydatabase"
result_backend = "db+postgresql://myuser:mypassword@db:5432/mydatabase"
imports = ("app.mlflow",)
result_extended = True
