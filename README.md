To run the project run the below command,
   uvicorn app.main:app --reload --host 127.0.0.1 --port 9000
Docker-compose build,
   docker-compose up --build


   
1. FastAPI App Container Running
llmops-app | Application startup complete.
llmops-app | Uvicorn running on http://0.0.0.0:8000


 API is accessible on:

http://localhost:9000

2. Prometheus Running
prometheus | Start listening on 0.0.0.0:9090

Metrics at:

http://localhost:9090

3. Grafana Running
HTTP Server Listen address=[::]:3000


 Grafana:

 http://localhost:3000


Login: admin / admin

4. Jaeger Tracing Running
Query server started on :16686


Open Jaeger UI:

 http://localhost:16686
   
   
   
