import boto3
import sys
import logging
import logging.config
import json

### Setting up log formatting
logging.config.fileConfig("log.ini")
logger = logging.getLogger('sLogger')

### Using SDK 'boto3' : Elastic Load Balancer and CloudWatch Functions
ec = boto3.client('ec2')
cloudwatch = boto3.client('cloudwatch')


def main():
    
    inputValidationGeneratingAlarm()


#### Validation - need to pass 'alert_configuration.json' while running the script

def inputValidationGeneratingAlarm():

    ## Checking if we are passing configuration file as parameter to the script
    logger.info("Passing parameters to the python script for generation of CloudWatch Alarms based on Thresholds")
    args = sys.argv[1:]

    if args:
        logger.info("We can proceed with the script execution")
    else:
        print("Please pass parameter while setting up the alarms\nFormat - python alert_elbsetup.py alert_configuration.json")
        logger.info("Exiting without execution need parameters while running the script")
        exit()
    
    inputFileFormatCheck()


### Reading configuration file
Tag = { "Ubuntu, AmazonAMI"}
read_tags=dict['Tag']
tag1 = read_tags.split(",") 
read_sns = "SNS Topic URL" 
def inputFileFormatCheck():
    try:
        with open(sys.argv[1],'r') as f:
            contents=f.read()
        dict = json.loads(contents)
    except:
        print("Could not open file contents due to improper inputs in configuration file,exiting the script")
        logger.info("Could not open file contents, exiting the script")
        exit()
		

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

if __name__ == '__main__': main(alert_setup)