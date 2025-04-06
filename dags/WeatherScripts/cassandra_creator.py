from cassandra.cluster import Cluster

def create_schema():
    cluster = Cluster(["cassandra"])  # Use container name or ip address but make sure they are all in same docker network
    session = cluster.connect()
    keyspaces = session.execute("SELECT keyspace_name FROM system_schema.keyspaces")
    keyspace_names = [ks.keyspace_name for ks in keyspaces]

    
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS weatherks
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
    """)


    
    session.execute("""
        CREATE TABLE IF NOT EXISTS weatherks.weather (
            city_name text PRIMARY KEY,
            city_timezone int,
            time_UTC bigint,
            city_country text,
            sunrise_time_UTC bigint,
            sunset_time_UTC bigint,
            weather_description text,
            sea_level_Meter bigint,
            temp_celisus double,
            temp_min_celisus double,
            temp_max_celisus double,
            humidity_gram_m3 bigint,
            pressure_Pascal bigint,
            latitude double,
            longtiude double
        )
    """)

    session.shutdown()