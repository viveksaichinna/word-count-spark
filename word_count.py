from pyspark.sql import SparkSession

# AWS Credentials
AWS_ACCESS_KEY_ID = 'AKIA5FTZACIWX5VOYY6D'

AWS_SECRET_ACCESS_KEY = '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'

# S3 paths
S3_INPUT = 's3a://vivek0987wc/hello.txt'
S3_OUTPUT = 's3a://vivek0987wc/output_folder/'

# Spark Session
spark = SparkSession.builder \
    .appName("WordCount") \
    .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.1,com.amazonaws:aws-java-sdk-bundle:1.11.901") \
    .getOrCreate()

# Hadoop S3 Configuration
hadoop_conf = spark.sparkContext._jsc.hadoopConfiguration()
hadoop_conf.set("fs.s3a.access.key", AWS_ACCESS_KEY_ID)
hadoop_conf.set("fs.s3a.secret.key", AWS_SECRET_ACCESS_KEY)

# Word Count Logic
text_file = spark.sparkContext.textFile(S3_INPUT)
counts = text_file.flatMap(lambda line: line.split()) \
                  .map(lambda word: (word, 1)) \
                  .reduceByKey(lambda a, b: a + b)
counts.saveAsTextFile(S3_OUTPUT)
spark.stop()