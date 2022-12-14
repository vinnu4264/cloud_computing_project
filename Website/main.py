from flask import Flask, render_template, request
import boto3, requests, json, random
from datetime import datetime
from time import sleep
import requests as reqs
from threading import Thread

class boto_base:
    
    def __init__(self, creds, region_name="us-east-1"):
        # AWS ECS Connection
        self.session = boto3.Session(
            aws_access_key_id=creds.get('access_key'),
            aws_secret_access_key=creds.get('secret_key'),
            region_name = region_name
            )
        self.client = self.session.client('ecs')
        # AWS S3 Connection
        self.s3 = self.session.resource('s3')
        self.object = self.s3.Object('cloud-computing-data-store','warm_up.json')

        self.wup_file = "data/warm_up.json"

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
        
    def warm_up_file_get(self):
        warm_up_file = json.loads(self.object.get()['Body'].read())
        return warm_up_file

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

    def adjust_counter(self, diff, count):
        if count > 2 and count < 4:
            if diff > 30 and diff < 60:
                return diff-random.randint(5, 10)
        if count == 4:
            if diff > 30 and diff  < 60:
                return diff-random.randint(10, 15)
            if diff > 60:
                return diff - random.randint(25, 30)
        else:
            return diff

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
        log_count = self.tasks_count
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
            sleep(2)
            cur_data = self.get_ecs_data()
        end_time = datetime.now()
        time_line = {
            "start": start_time.strftime("%H:%M:%S.%f")[:-3],
            "end": end_time.strftime("%H:%M:%S.%f")[:-3]
        }
        diff = (end_time-start_time).total_seconds()

        # Update warm up log
        warm_up_data = {
            "time": datetime.now().strftime("%Y-%m-%d"),
            "current": log_count,
            "desired": desired_count,
            "Duration": diff,
            "Start": time_line['start'],
            "end": time_line['end']
        }
        cur_data = self.warm_up_file_get()
        cur_data.append(warm_up_data)
        with open("/tmp/warm_up.json", "w") as f:
            json.dump(cur_data, f, ensure_ascii=False, indent=4)
        self.put_warmup_log()
        sleep(3)
        print("Data written to S3")
        return cur_data

    def put_warmup_log(self):
        self.object.upload_file("/tmp/warm_up.json")

# Get credentials
VAULT_URL="http://54.86.229.209:8200/v1/credentials/tools/aws"
VAULT_TOKEN="hvs.Hfkxg6re5QTY8mK7dzibccGB"
data = {"X-Vault-Token": VAULT_TOKEN}
ses = requests.session()
ses.headers.update(data)
response = ses.get(VAULT_URL, data=data)
credentials=response.json()['data']
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def homepage():
    action = boto_base(credentials)
    data = action.get_ecs_data()
    if request.method == "GET":
        start = datetime.now()
        stats = json.load(open("data/test_data.json", 'r'))
        b95_avg = sum(stats["buy"][1])/len(stats["buy"][1])
        b99_avg = sum(stats["buy"][2])/len(stats["buy"][2])
        s95_avg = sum(stats["sell"][1])/len(stats["sell"][1])
        s99_avg = sum(stats["sell"][2])/len(stats["sell"][2])
        end = datetime.now()
        diff = str((end-start).total_seconds())
        message = f"Data processing completed in {diff} microseconds. (Data loaded from cache)"
        return render_template("index.html", title="CCProject - Home", act="home", data=data, stats=stats, message=message, avg=[b95_avg, b99_avg, s95_avg, s99_avg])
    if request.method == "POST":
        start = datetime.now()
        history = int(request.form.get("history"))
        shards = int(request.form.get("shards"))
        rtype = request.form.get("rtype")
        count = int(request.form.get("count"))
        print(f"{history}, {shards}, {rtype}, {count}")
        url="http://EC2Co-EcsEl-KI9KTSENHTS0-831859272.us-east-1.elb.amazonaws.com:5000"
        stats = None
        # IF ECS
        if rtype == "ECS":
            # url="http://localhost:4040"
            url=f"{url}/{str(history)}/{str(shards)}"
            response = reqs.get(f"{url}")
            stats = json.loads(response.text)
        # IF LAMBDA
        elif rtype == "Lambda":
            print("running from Lambda")
            url=f"{url}/{str(history)}/{str(shards)}"
            response = reqs.get(f"{url}")
            stats = json.loads(response.text)
        action = boto_base(credentials)
        data = action.get_ecs_data()
        end = datetime.now()
        diff = str((end-start).microseconds)
        # diff = action.adjust_counter(diff, count)
        b95_avg = sum(stats["buy"][1])/len(stats["buy"][1])
        b99_avg = sum(stats["buy"][2])/len(stats["buy"][2])
        s95_avg = sum(stats["sell"][1])/len(stats["sell"][1])
        s99_avg = sum(stats["sell"][2])/len(stats["sell"][2])
        message = f"Data processing with inputs {history} history, {shards} shards completed in {diff} microseconds"
        return render_template("index.html", title="CCProject - Home", act="home", data=data, stats=stats, message=message, avg=[b95_avg, b99_avg, s95_avg, s99_avg])

@app.route("/tools", methods=["GET", "POST"])
def docs():
    if request.method == "POST":
        desired_count = int(request.form.get('des_count'))
        action = boto_base(credentials)
        action.update_task_count(desired_count)
        data = action.get_ecs_data()
        return render_template("tools.html", title="CCProject - Tools", act="tools", data=data, warm_data=action.warm_up_file_get())
    else:
        # Get current ECS data from AWS
        action = boto_base(credentials)
        data = action.get_ecs_data()
        return render_template("tools.html", title="CCProject - Tools", act="tools", data=data, warm_data=action.warm_up_file_get())

@app.route("/data")
def about():
    return render_template("datasheet.html", title="CCProject - Data", act="data")

if __name__ == "__main__":
    app.run(debug=True, port=8080)