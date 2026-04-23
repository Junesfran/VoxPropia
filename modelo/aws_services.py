import boto3
import pymysql
import os

# Hereda permisos del rol EC2 automáticamente
cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')

def send_metric_to_cloudwatch(metric_name, value=1):
    try:
        cloudwatch.put_metric_data(
            Namespace='VoxPropia/Chatbot',
            MetricData=[{
                'MetricName': metric_name,
                'Value': value,
                'Unit': 'Count'
            }]
        )
    except Exception as e:
        # Falla silenciosamente para no romper el chatbot
        print(f"[AWSError - CloudWatch] No se pudo enviar métrica: {e}")

def save_query_to_rds(query_text, response_text=""):
    try:
        connection = pymysql.connect(
            host=os.environ.get("RDS_HOST", "voxpropia-db.cxgeswuswcvs.us-east-1.rds.amazonaws.com"),
            user=os.environ.get("RDS_USER", "admin"),
            password=os.environ.get("RDS_PASSWORD", "12345678"), 
            database=os.environ.get("RDS_DB", "voxpropia_db")
        )
        with connection.cursor() as cursor:
            sql = "INSERT INTO chat_history (query_text, chat_id) VALUES (%s, %s)"
            cursor.execute(sql, (query_text, chat_id))
        connection.commit()
        connection.close()
    except Exception as e:
        # Falla silenciosamente para no romper el chatbot
        print(f"[AWSError - RDS] No se pudo guardar historial: {e}")
