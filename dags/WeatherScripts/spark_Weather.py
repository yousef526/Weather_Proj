
# way to define spark context
from datetime import datetime 
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col, to_timestamp,from_json
from pyspark.sql.types import TimestampNTZType, StructField, StructType, LongType, DoubleType, StringType, ArrayType

def processData():
    spark = SparkSession.builder\
        .appName("WeathProj") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1,com.datastax.spark:spark-cassandra-connector_2.12:3.5.0") \
        .config("spark.cassandra.connection.port", "9042") \
        .config("spark.cassandra.connection.host", "cassandra")\
        .getOrCreate()


    schema = ArrayType(StructType([
        StructField("base",StringType(),True),
        StructField("clouds",StructType([
            StructField("all",LongType(),True)]
        ),True),
        StructField("cod",LongType(),True),
        StructField("coord",
            StructType(
            [StructField("lat",DoubleType(),True),
            StructField("lon",DoubleType(),True)]
            ),True),
        StructField("dt",LongType(),True),
        StructField("id",LongType(),True),
        StructField("main",
            StructType([
                StructField("feels_like",DoubleType(),True),
                StructField("grnd_level",LongType(),True),
                StructField("humidity",LongType(),True),
                StructField("pressure",LongType(),True),
                StructField("sea_level",LongType(),True),
                StructField("temp",DoubleType(),True),
                StructField("temp_max",DoubleType(),True),
                StructField("temp_min",DoubleType(),True),
            ]),True),
        StructField("name",StringType(),True),
        StructField("sys",
            StructType([
                StructField("country",StringType(),True),
                StructField("id",LongType(),True),
                StructField("sunrise",LongType(),True),
                StructField("sunset",LongType(),True),
                StructField("type",LongType(),True),
        ]),True),
        StructField("timezone",LongType(),True),
        StructField("visibility",LongType(),True),
        StructField("weather",ArrayType(
            StructType([
                StructField("description",StringType(),True),
                StructField("icon",StringType(),True),
                StructField("id",LongType(),True),
                StructField("main",StringType(),True),
            ]))
        ,True),
        StructField("wind",
            StructType([
                StructField("deg",LongType(),True),
                StructField("gust",DoubleType(),True),
                StructField("speed",DoubleType(),True),
            ]),True)
    ]))


    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("subscribe", "Topic_1") \
        .option("startingOffsets", "earliest") \
        .option("failOnDataLoss", "false")\
        .load()
        
        

    df_parsed = df.selectExpr("CAST(value AS STRING) as json_str")
    

    parsed_df = df_parsed.select(from_json(col("json_str"), schema).alias("data"))


    parsed_df = parsed_df.withColumn("data", explode("data"))
    
    parsed_df.printSchema()

    

    df_exploded = parsed_df.select(
            col("data.name").alias("city_name"),
            col("data.timezone").alias("city_timezone"),
            col("data.dt").alias("time_utc"),
            col("data.sys.country").alias("city_country"),
            col("data.sys.sunrise").alias("sunrise_time_utc"),
            col("data.sys.sunset").alias("sunset_time_utc"),
            explode(col("data.weather")).alias("weather"),
            col("data.main.sea_level").alias("sea_level_meter"),
            col("data.main.temp").alias("temp_celisus"),
            col("data.main.temp_min").alias("temp_min_celisus"),
            col("data.main.temp_max").alias("temp_max_celisus"),
            col("data.main.humidity").alias("humidity_gram_m3"),
            col("data.main.pressure").alias("pressure_pascal"),
            col("data.coord.lon").alias("latitude"),
            col("data.coord.lat").alias("longtiude"),
        ).select(
            "*",
            col("weather.description").alias("weather_description")
        ).drop("weather")



    df_exploded.printSchema()

    

    query = df_exploded.writeStream \
        .foreachBatch(write_to_cassandra)\
        .outputMode("append") \
        .option("checkpointLocation", "/opt/airflow/dags/WeatherScripts/Spark_chkP/topic_1")\
        .start()
        

    
    
    query.awaitTermination(60)
    #query.stop()

def write_to_cassandra(batch_df,batch_id):
    print(f"Stuck here2 with batch id{batch_id}",)
    batch_df.show(n=3, truncate=False)
    if batch_df.isEmpty():
        print(f"⚠️ No data in batch {str(datetime.now())}")
        return
    else:
        print(f"✅ Batch {str(datetime.now())} has data: {batch_df.count()} rows")

    json_output_path = f"/opt/airflow/dags/WeatherScripts/GeneratedData/{str(datetime.now())}.json"
    batch_df.write \
        .mode("overwrite") \
        .json(json_output_path)
    

    #batch_df.printSchema()
    batch_df.write \
        .format("org.apache.spark.sql.cassandra") \
        .mode("append") \
        .options(table="weather", keyspace="weatherks") \
        .save()
    
