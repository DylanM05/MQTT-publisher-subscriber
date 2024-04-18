import paho.mqtt.client as mqtt
import json
from tkinter import Tk, Text, END, Scrollbar, VERTICAL, Frame, Button, N, E, S, W

class SubscriberGUI(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.initUI()
        self.initMQTT()

    def initUI(self):
        self.master.title("MQTT Subscriber")
        self.grid(sticky=N+E+S+W)

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.text_output = Text(self, height=30, width=80)
        self.text_output.grid(row=0, column=0, padx=(10, 0), pady=10, sticky=N+E+S+W) 

        scrollbar = Scrollbar(self, command=self.text_output.yview, orient=VERTICAL)
        scrollbar.grid(row=0, column=1, padx=(0, 10), pady=10, sticky=N+S) 

        self.text_output['yscrollcommand'] = scrollbar.set

        self.close_button = Button(self, text="Close Connection", command=self.close_connection)
        self.close_button.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky=E)


    def initMQTT(self):
        self.broker_address = "localhost" 
        self.port = 1883
        self.topic = "weather/data"        
        self.client = mqtt.Client(protocol=mqtt.MQTTv311)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        try:
            self.client.connect(self.broker_address, self.port, 60)
            self.client.loop_start()
        except Exception as e:
            self.text_output.insert(END, f"Failed to connect to MQTT broker: {e}\n")

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.text_output.insert(END, "Connected successfully to MQTT broker.\n")
            client.subscribe(self.topic)
        else:
            self.text_output.insert(END, f"Failed to connect with error code {rc}\n")

    def on_message(self, client, userdata, msg):
        message = f"Received message on topic '{msg.topic}':\n{msg.payload.decode()}\n"
        self.text_output.insert(END, message)
        try:
            data_dict = json.loads(msg.payload.decode('utf-8'))
            if self.validate_data(data_dict):
                self.display_data(data_dict)
            else:
                self.text_output.insert(END, "Error: Received data with invalid values.\n")
        except json.JSONDecodeError:
            self.text_output.insert(END, "Error: Received corrupted data or non-JSON data.\n")
        self.text_output.see(END)

    def validate_data(self, data):
        if data['temperature'] < -50 or data['temperature'] > 50:
            return False
        if data['humidity'] < 0 or data['humidity'] > 100:
            return False
        return True


    def display_data(self, data):
        self.text_output.insert(END, "Formatted Received Data:\n")
        for key, value in data.items():
            self.text_output.insert(END, f"  {key}: {value}\n")
        self.text_output.insert(END, "-----\n")
        self.text_output.see(END) 

    def close_connection(self):
        self.client.loop_stop()
        self.client.disconnect()
        self.text_output.insert(END, "MQTT connection closed.\n")

if __name__ == "__main__":
    root = Tk()
    root.geometry("800x600")
    app = SubscriberGUI(master=root)
    app.mainloop()
