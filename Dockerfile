FROM python:3.8-slim
RUN pip install mlflow[extras]==1.9.1 && \
    pip install psycopg2-binary==2.8.5 && \
    pip install boto3==1.15.16
EXPOSE 5000
ENTRYPOINT ["mlflow", "server"]
