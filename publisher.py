import serial
import statistics
import json
import time
from rabbitmq import RabbitMQ

# Configuración del puerto serie (serial)
port = "/dev/ttyACM0"  # Cambia esto al puerto correcto donde está conectado tu Arduino
baudrate = 9600

# Configuración de RabbitMQ
rabbitmq_host = "44.215.6.149"
rabbitmq_user = "IntelliFish"
rabbitmq_password = "piloto123"
rabbitmq_queue_phSensor = "phSensor"
rabbitmq_queue_waterFlowSensor = "waterFlowSensor"
rabbitmq_queue_waterTemperatureSensor = "waterTemperatureSensor"
rabbitmq_exchange = "intelliFishName"

rabbit = RabbitMQ(rabbitmq_host, rabbitmq_user, rabbitmq_password)
rabbit.create_exchange("intelliFishName", "topic")
rabbit.create_queue(rabbitmq_queue_phSensor)
rabbit.bind_queue(rabbitmq_exchange, rabbitmq_queue_phSensor, "ph")
rabbit.create_queue(rabbitmq_queue_waterFlowSensor)
rabbit.bind_queue(rabbitmq_exchange, rabbitmq_queue_waterFlowSensor, "flow")
rabbit.create_queue(rabbitmq_queue_waterTemperatureSensor)
rabbit.bind_queue(rabbitmq_exchange, rabbitmq_queue_waterTemperatureSensor, "temperature")


# Conexión al puerto serie (serial)
ser = serial.Serial(port, baudrate)

# Listas para almacenar los datos de los sensores
data = []  # Lista para almacenar los datos de la tasa de flujo de agua
ph_data = []
temperature_data = []
flow_data = []# Lista para almacenar los datos del valor de pH
temp_data = []  # Lista para almacenar los datos de la temperatura del agua

# Bucle principal
while True:
    # Lectura de datos desde el puerto serie (serial)
    line = ser.readline().decode().strip()
    print(line)

    if line.startswith("waterFlow:"):
        value = line[10:]
        data.append(float(value))
    elif line.startswith("ph:"):
        value = line[3:]
        ph_data.append(float(value))
    elif line.startswith("temperature:"):
        value = line[12:]
        temp_data.append(float(value))

    # Realizar operaciones con los datos de tasa de flujo de agua
    if len(data) > 1:
        # Cálculo de la media, desviación estándar, desviación media y varianza de la tasa de flujo de agua
        flow_mean = statistics.mean(data)
        flow_stdev = statistics.stdev(data)
        flow_mean_dev = statistics.mean([abs(x - flow_mean) for x in data])
        flow_variance = statistics.variance(data)

        # print("Tasa de flujo de agua (media):", flow_mean)
        # print("Tasa de flujo de agua (desviación estándar):", flow_stdev)
        # print("Tasa de flujo de agua (desviación media):", flow_mean_dev)
        # print("Tasa de flujo de agua (varianza):", flow_variance)
        # print(
            # "Dato bruto de la tasa de flujo de agua:", data[-1]
        # )  # Último dato almacenado

        # Creación del diccionario con los datos de la tasa de flujo de agua
        flow_data_dict = {
            "mesuare": data[-1],
            "average": flow_mean,
            "variance": flow_variance,
            "standardDeviation": flow_stdev,
            "meanDeviation": flow_mean_dev,
        }

        # Convertir el diccionario a JSON
        flow_json_data = json.dumps(flow_data_dict)

        # Envío de los datos de la tasa de flujo de agua a RabbitMQ
        rabbit.send(rabbitmq_exchange, "flow", flow_json_data)
        # print("flow")
        # print(flow_json_data)
        # print("Datos de tasa de flujo de agua enviados correctamente a RabbitMQ.")

    # Realizar operaciones con los datos de pH
    if len(ph_data) > 1:
        # Cálculo de la media, desviación estándar, desviación media y varianza del 
        ph_mean = statistics.mean(ph_data)
        ph_stdev = statistics.stdev(ph_data)
        ph_mean_dev = statistics.mean([abs(x - ph_mean) for x in ph_data])
        ph_variance = statistics.variance(ph_data)

        # print("Valor de pH (media):", ph_mean)
        # print("Valor de pH (desviación estándar):", ph_stdev)
        # print("Valor de pH (desviación media):", ph_mean_dev)
        # print("Valor de pH (varianza):", ph_variance)
        # print("Dato bruto de pH:", ph_data[-1])  # Último dato almacenado

        # Creación del diccionario con los datos del pH
        ph_data_dict = {
            "measure": ph_data[-1],
            "average": ph_mean,
            "variance": ph_variance,
            "standardDeviation": ph_stdev,
            "meanDeviation": ph_mean_dev
        }

        # Convertir el diccionario a JSON
        ph_json_data = json.dumps(ph_data_dict)

        # Envío de los datos del pH a RabbitMQ
        rabbit.send(rabbitmq_exchange, "ph", ph_json_data)
        # print("ph")
        # print("Datos de pH enviados correctamente a RabbitMQ.")

    # Realizar operaciones con los datos de temperatura del agua
    if len(temp_data) > 1:
        # Cálculo de la media, desviación estándar, desviación media y varianza de la temperatura del agua
        temp_mean = statistics.mean(temp_data)
        temp_stdev = statistics.stdev(temp_data)
        temp_mean_dev = statistics.mean([abs(x - temp_mean) for x in temp_data])
        temp_variance = statistics.variance(temp_data)

        # print("Temperatura del agua (media):", temp_mean)
        # print("Temperatura del agua (desviación estándar):", temp_stdev)
        # print("Temperatura del agua (desviación media):", temp_mean_dev)
        # print("Temperatura del agua (varianza):", temp_variance)
        # print(
            # "Dato bruto de la temperatura del agua:", temp_data[-1]
        # )  # Último dato almacenado

        # Creación del diccionario con los datos de la temperatura del agua
        temp_data_dict = {
            "measure": temp_data[-1],
            "average": temp_mean,
            "variance": temp_variance,
            "standardDeviation": temp_stdev,
            "meanDeviation": temp_mean_dev,
            
        }

        # Convertir el diccionario a JSON
        temp_json_data = json.dumps(temp_data_dict)

        # Envío de los datos de la temperatura del agua a RabbitMQ
        rabbit.send(rabbitmq_exchange, "temperature", temp_json_data)
        # print(f"temperature")
        # print(temp_json_data)
        # print("Datos de temperatura del agua enviados correctamente a RabbitMQ.")
        # print("aadioooos")
        
    
# Cierre de conexiones
ser.close()