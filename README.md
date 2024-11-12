## Simple Word Count on AWS EC2/LightSail using PySpark with Data from S3

### Goal
The purpose of this project is to set up an environment on an AWS EC2 or LightSail instance to run a simple word count Python script using PySpark. The dataset will be stored on Amazon S3, and we'll access it directly from our PySpark script. This guide will walk you through setting up your environment, installing necessary tools, and running the word count script.

---

## Prerequisites
Before starting, make sure you have:
- An AWS account with access to EC2 or LightSail.
- An S3 bucket with a text file that will be used for the word count.
- SSH access to your EC2 or LightSail instance.

---

## Step 1: Setting Up Your EC2/LightSail Instance
1. **Log in to your AWS Console** and launch an EC2 or LightSail instance (preferably with Amazon Linux 2).
2. **Connect to your instance** via SSH:
   ```bash
   ssh -i "your-key.pem" ec2-user@your-instance-ip
   ```

---

## Step 2: Installing Java
PySpark requires Java to run. We'll install Java 11:
```bash
sudo yum install java-11 -y
```

Set the `JAVA_HOME` environment variable:
```bash
export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which java))))
```

Verify the Java installation:
```bash
java --version
```

---

## Step 3: Preparing `/tmp` Directory for Spark
Increase the `/tmp` directory size to avoid "No space left on device" errors:
```bash
sudo mount -o remount,size=2G /tmp
```

---

## Step 4: Installing Python and PySpark
Install `pip`, the Python package manager:
```bash
sudo yum install python3-pip -y
```

Install PySpark using `pip`:
```bash
pip install pyspark
```

Verify the Spark installation:
```bash
spark-submit --version
```

---

## Step 5: Setting Up GitHub SSH Access (Optional)
If you plan to pull code from a GitHub repository:
1. Generate an SSH key:
   ```bash
   ssh-keygen -t rsa -b 4096 -C "your-email@example.com"
   ```
2. Add the SSH key to your GitHub account:
   ```bash
   cat ~/.ssh/id_rsa.pub
   ```
3. Test the SSH connection:
   ```bash
   ssh -T git@github.com
   ```

---

## Step 6: Installing and Configuring Jupyter Notebook (Optional)
If you prefer using Jupyter Notebook for development, follow these steps:

1. Install Jupyter:
   ```bash
   pip install jupyter
   ```

2. Generate a Jupyter configuration file:
   ```bash
   jupyter notebook --generate-config
   ```

3. Set a password for Jupyter Notebook:
   ```bash
   jupyter notebook password
   ```

4. Edit the configuration file to allow remote access:
   ```bash
   vi ~/.jupyter/jupyter_notebook_config.py
   ```

   Add the following lines:
   ```python
   c.ServerApp.ip = '0.0.0.0'
   c.ServerApp.port = 8888
   ```

5. Start the Jupyter Notebook server:
   ```bash
   jupyter notebook --no-browser --port=8888 &
   ```

Access the Jupyter Notebook using your browser:
```
http://your-instance-ip:8888
```

---

## Step 7: Running the Word Count PySpark Script

1. **Create a Python script** (e.g., `word_count.py`) with the following content:

   ```python
   from pyspark.sql import SparkSession

   AWS_ACCESS_KEY_ID = 'YOUR_AWS_ACCESS_KEY'
   AWS_SECRET_ACCESS_KEY = 'YOUR_AWS_SECRET_KEY'
   S3_INPUT_PATH = 's3a://your-bucket-name/path/to/your/input_file.txt'
   S3_OUTPUT_PATH = 's3a://your-bucket-name/path/to/your/output_folder/'

   spark = SparkSession.builder \
       .appName("WordCount") \
       .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.1,com.amazonaws:aws-java-sdk-bundle:1.11.901") \
       .getOrCreate()

   hadoop_conf = spark.sparkContext._jsc.hadoopConfiguration()
   hadoop_conf.set("fs.s3a.access.key", AWS_ACCESS_KEY_ID)
   hadoop_conf.set("fs.s3a.secret.key", AWS_SECRET_ACCESS_KEY)

   text_file = spark.sparkContext.textFile(S3_INPUT_PATH)
   counts = text_file.flatMap(lambda line: line.split()) \
                     .map(lambda word: (word, 1)) \
                     .reduceByKey(lambda a, b: a + b)
   counts.saveAsTextFile(S3_OUTPUT_PATH)
   spark.stop()
   ```

2. **Run the script** using the following command:
   ```bash
   spark-submit word_count.py
   ```

3. Verify that the output is saved to your specified S3 output path.

---

## Troubleshooting
- If you encounter issues with S3 access, ensure your AWS credentials are correctly set.
- If Spark runs out of space, increase the size of your `/tmp` directory.

---
