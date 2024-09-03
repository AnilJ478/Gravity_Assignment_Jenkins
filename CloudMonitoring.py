import boto3
import sys
import logging
import logging.config

### Setting up log formatting
logging.config.fileConfig("log.ini")
logger = logging.getLogger('sLogger')

### Using SDK 'boto3' : ec2 instance CPU, Disk monitoring and CloudWatch Functions
ec = boto3.client('ec2')
cloudwatch = boto3.client('cloudwatch')

def main():
    
    alert_setup()

Tag = { "Ubuntu, AmazonAMI"}
read_tags=dict['Tag']
tag1 = read_tags.split(",") 
read_sns = "SNS Topic URL" 

def alert_setup():
    for i in tag1:
                response=ec.describe_instances(
                Filters=[
                    {
                    'Name': 'tag:Tag',
                    'Values': [
                        i,
                        ]
                    }])
		
                for reservation in response["Reservations"]:
                    for instance in reservation["Instances"]:
                        id = instance['InstanceId']
                        print(id)
                        hostname = instance['PrivateDnsName']
                        for t in instance['Tags']:
                            if t['Key'] == 'Name':
                                iname = t['Value']
                                logger.info("Generating the CPU Alarm")
                                cpu_alarm = cloudwatch.put_metric_alarm(
                                    AlarmName= 'CPUAlarm' + iname,
                                    AlarmDescription= hostname,
                                    MetricName='CPUUtilization',
                                    Namespace='AWS/EC2',
                                    Statistic='Average'
                                    ComparisonOperator='GreaterThanOrEqualToThreshold',
                                    Threshold=70,
                                    Period=5,
                                    EvaluationPeriods=5,
                                    ActionsEnabled=True,
                                    AlarmActions=[
                                        read_sns
                                        ],
                                    Dimensions=[
                                        {
                                            'Name': 'InstanceId',
                                            'Value': id
                                        },
                                    ],
                                    Unit='Percent'
                                )
                                print("CPU Alarm Status for InstanceName" + iname)
                                print(cpu_alarm)
                                
                                
                                cpu_alarm_reset = cloudwatch.set_alarm_state(
                                    AlarmName='CPUAlarm' + iname,
                                    StateValue='OK',
                                    StateReason='Reset'
                                )
                                                                
                                diskreadops_alarm = cloudwatch.put_metric_alarm(
                                    AlarmName= 'DiskReadOpsAlarm' + iname,
                                    AlarmDescription= hostname,
                                    #InstanceName= iname,
                                    MetricName='DiskReadOps',
                                    Namespace='AWS/EC2',
                                    Statistic='Avarage',
                                    ComparisonOperator='GreaterThanOrEqualToThreshold',
                                    Threshold=70,
                                    Period=5,
                                    EvaluationPeriods=5,
                                    ActionsEnabled=True,
                                    AlarmActions=[
                                        read_sns
                                        ],
                                    Dimensions=[
                                        {
                                            'Name': 'InstanceId',
                                            'Value': id
                                        },
                                    ],
                                    Unit='Count'
                                )
                                print("DiskReadOps Alarm Status for InstanceName" + iname)
                                print(diskreadops_alarm)
                                
                                diskreadops_alarm_reset = cloudwatch.set_alarm_state(
                                    AlarmName='DiskReadOpsAlarm' + iname,
                                    StateValue='OK',
                                    StateReason='Reset'
                                )
                                
                                diskwriteops_alarm = cloudwatch.put_metric_alarm(
                                    AlarmName= 'DiskWriteOpsAlarm' + iname,
                                    AlarmDescription= hostname,
                                    #InstanceName= iname,
                                    MetricName='DiskWriteOps',
                                    Namespace='AWS/EC2',
                                    Statistic='Avarage',
                                    ComparisonOperator='GreaterThanOrEqualToThreshold',
                                    Threshold=80,
                                    Period=5,
                                    EvaluationPeriods=5,
                                    ActionsEnabled=True,
                                    AlarmActions=[
                                        read_sns
                                        ],
                                    Dimensions=[
                                        {
                                            'Name': 'InstanceId',
                                            'Value': id
                                        },
                                    ],
                                    Unit='Count'
                                )
                                print("DiskWriteOpsOps Alarm Status for InstanceName" + iname)
                                print(diskwriteops_alarm)
                                
                                diskwriteops_alarm_reset = cloudwatch.set_alarm_state(
                                    AlarmName='DiskWriteOpsAlarm' + iname,
                                    StateValue='OK',
                                    StateReason='Reset'
                                )

if __name__ == '__main__': main()