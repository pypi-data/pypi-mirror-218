import json
import os
import sys
import logging
import pulsar
import random
import string
import mysql.connector
import pandas as pd



def source_config(dict_pulsar):

    hostname = dict_pulsar["hostname"]
    port= dict_pulsar["port"]
    topic = dict_pulsar["topic"]

    conection = f'pulsar://{hostname}:{port}'
    logging.info("Connecting Pulsar:"+ conection)
    client = pulsar.Client(conection)
    '''
    CONSUME the right data, known the schema
    '''
    logging.info("Pulsar connected")       
    subcription = ''.join(random.choice(string.ascii_lowercase)
                            for i in range(10))
    consumer = client.subscribe(topic, subcription)
    
    sys.modules["datapeach.consumer"] = consumer



def sink_config(dict_cnn, sql):
    sys.modules["datapeach.sinkconfig"] = dict_cnn  
    sys.modules["datapeach.sql"] = sql
    cfg = sys.modules["datapeach.sinkconfig"]





def dp_function(original_func):
    def wrapper(*args, **kwargs):
        # Additional functionality before calling the decorated function
        #source
        
        # print("source init")

        # source_config()
        # Call the decorated function
        consumer = sys.modules["datapeach.consumer"]
        while True:
            msg = consumer.receive()
            try:
                msg_data = msg.data().decode('utf-8')
                print('Received message: {}'.format(msg_data))
                data_dict = json.loads(msg_data)
                result = original_func(**data_dict)
                print(result)
                if(result is not None):
                    sink_init(result)
                consumer.acknowledge(msg)
            except Exception as e:
                print('Error processing message: {}'.format(e))
                consumer.negative_acknowledge(msg)

        
       
        
        return result
    
    def sink_init(sqlvalue):
        cfg = sys.modules["datapeach.sinkconfig"] 
        sql =  sys.modules["datapeach.sql"]
        conn = mysql.connector.connect(**cfg)
        # Create a cursor object to execute SQL statements
        cursor = conn.cursor()
        cursor.execute(sql, sqlvalue)
        conn.commit()

        # Close the cursor and the database connection
        cursor.close()
        conn.close()


    return wrapper






