import boto3
import os
import requests
from time import sleep
from datetime import datetime

class boto_base:
    
    def __init__(self, creds, region_name="us-east-1"):
        self.session = boto3.Session(
            aws_access_key_id=creds.get('access_key'),
            aws_secret_access_key=creds.get('secret_key'),
            region_name = region_name
            )
        self.client = self.session.client('ecs')

        # Cluster Name
        self.cluster = self.client.list_clusters().get("clusterArns")[0]
        self.cluster_name = self.cluster.split("/")[-1]

        # Service information
        service = self.client.list_services(cluster=self.cluster_name).get('serviceArns')[0]
        self.service_name = service.split("/")[-1]            

        # Tasks information
        self.tasks = self.client.list_tasks(cluster=self.cluster_name, serviceName=self.service_name, desiredStatus='RUNNING').get("taskArns")
        self.tasks_count = len(self.tasks)

        print("[INFO] AWS Session creation completed")
        
    
    def get_ecs_data(self):
        # Tasks information
        running_count = 0
        tasks = self.client.list_tasks(cluster=self.cluster_name, serviceName=self.service_name, desiredStatus='RUNNING').get("taskArns")
        for task in tasks:
            _data_ = task_desc = self.client.describe_tasks(
                cluster=self.cluster_name,
                tasks=[task]
            )
            status = _data_.get('tasks')[0].get('lastStatus')
            if status == "RUNNING":
                running_count+=1
        resp_data = {
            "cluster_arn": self.cluster,
            "cluster_name": self.cluster_name,
            "running_count": running_count
        }
        return resp_data
        
    def update_task_count(self, desired_count):
        start_time = datetime.now()
        # Update desired count
        self.client.update_service(
            cluster=self.cluster_name, 
            service=self.service_name,
            desiredCount=desired_count
        )
        # Scale tasks
        current_count = self.tasks_count
        counter=0
        while desired_count<current_count:
            self.client.stop_task(
                cluster=self.cluster_name,
                task=self.tasks[counter],
                reason='string'
            )
            counter+=1
            current_count-=1
        # Post update validation
        cur_data = self.get_ecs_data()
        while cur_data["running_count"]<desired_count:
            sleep(5)
            cur_data = self.get_ecs_data()
        end_time = datetime.now()
        time_line = {
            "start": start_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:3],
            "end": end_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:3]
        }
        diff = (end_time-start_time).total_seconds()
        return {
            "status": f"{self.tasks_count}/{desired_count}",
            "duration": f"{diff}",
            "time_line": time_line
        }


def lambda_handler(event, context):
    
    # Get credentials
    VAULT_TOKEN = os.getenv('VAULT_TOKEN')
    VAULT_URL = os.getenv('VAULT_URL')
    data = {"X-Vault-Token": VAULT_TOKEN}
    ses = requests.session()
    ses.headers.update(data)
    response = ses.get(VAULT_URL, data=data)
    credentials=response.json()['data']

    action = boto_base(credentials)
   
    if event['action'] == "get_data":
        resp = action.get_ecs_data()
    elif event['action'] == "update":
        new_count=event["count"]
        resp = action.update_task_count(new_count)
    print(resp)


    return {
        'statusCode' : 200,
        'body': "result"
    }

# lambda_handler({"action":"get_data"}, "test")
# lambda_handler({"action":"update", "count": 1}, "test")