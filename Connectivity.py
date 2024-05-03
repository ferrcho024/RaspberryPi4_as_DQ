# Connectivity

import time
import paho.mqtt.client as mqtt
import multiprocessing


## MQTT Parameters
hostname = "Rpi"
broker_port = 1883
topic = "80"
broker_address = "192.168.1.104"


def MQTTConection(get_queue):

    def on_connect(client, userdata, flags, rc, properties=None):
        if rc==0:
            print("Connected OK Returned code=",rc)
        else:
            print("Bad connection Returned code=",rc)
        client.subscribe(topic)
    
    def on_message(client, userdata, msg):
        userdata.append(msg.payload.decode())
        if len(userdata) == 60:
            get_queue.put(userdata)
            print("*********************************************************")
            userdata.clear()
        
        #print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        
        

    
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=hostname)
    client.on_connect = on_connect
    client.on_message = on_message
    
    client.user_data_set([])

    client.connect(broker_address, broker_port)
    client.loop_forever()

    #return client

def MQTTDisconnection(client):
    client.loop_stop()
    client.disconnect()





def publish(client):
     msg_count = 1
     while True:
         time.sleep(1)
         msg = f"messages: {msg_count}"
         result = client.publish(topic, msg)
         # result: [0, 1]
         status = result[0]
         if status == 0:
             print(f"Send `{msg}` to topic `{topic}`")
         else:
             print(f"Failed to send message to topic {topic}")
         msg_count += 1
         if msg_count > 5:
             break

def subscribe(client: MQTTConection):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message


'''
def on_message(client, userdata, msg, porperties=None):
        #print("Message received: " + msg.payload.decode())
        received = msg.payload.decode()

def on_subscribe(client, userdata, mid, qos, properties=None):
    print("Subscribed")





client.on_message = on_message
client.on_subscribe = on_subscribe

properties = mqtt.Properties(mqtt.PacketTypes.CONNECT)
#properties.SessionExpiryInterval=30*60 # in seconds
client.connect(broker_address,
                port=broker_port,
                clean_start=mqtt.MQTT_CLEAN_START_FIRST_ONLY,
                properties=properties,
                keepalive=60)   

client.loop_start()  
 


## MQTT callback functions
def MQTTConection(send_queue, get_queue):

    def on_connect(client, userdata, flags, rc, properties):
        if rc==0:
            print("Connected OK Returned code=",rc)
        else:
            print("Bad connection Returned code=",rc)
        client.subscribe(topic)
    
    

        
        df, nova, siata = msg.payload.decode().split(",")
        
        try:
            count += 1
            print("Sumando...")
            
                
        except:
            print("no existe")
            count = 1
            df_queue = []
            nova_queue = []
        
        print(count)
        print(f"Valor DF: {df}\n"
                f"Valor NOVA: {nova}\n"
                f"Valor SIATA: {siata}\n")
        
        df_queue.append(df)
        nova_queue.append(nova)
        
            
        if count > 59:
            print("********** VAN 60 ********")
            count = 0
            Q.put(df_queue, nova_queue, siata)
            df_queue.clear()
            nova_queue.clear()
        

    
    
    

    ## MQTT Connection
    client.connect(broker_address, broker_port, 60)
    client.loop_start()

    #return client

def on_disconnect(client, userdata, flags, rc, properties):

    if rc == 0:
        print("Client disconnected ok")
    else:
        print("Abnormal disconnection")
    
    client.loop_stop()

def message_handle(get_queue):
    while True:
        received = get_queue.get()
        if received == "disconnection":
            # Si se recibe un mensaje para desconectar, salir del bucle
            break
        # Procesar el mensaje recibido aquí
        print("Procesando mensaje: " + received)

def MQTTDisconnection(client):
    client.on_disconnect = on_disconnect
    client.loop_stop()
    client.disconnect()
    #print("unsubscribe succeeded")
'''
