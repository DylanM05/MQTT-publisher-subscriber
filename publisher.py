import paho.mqtt.client as mqtt
import json
import time
import threading
from tkinter import Tk, Canvas, Frame, BOTH, Button, Entry, Label, Text, ttk, StringVar, messagebox, END
from group_3_Wk12a_util import create_data
import random

class Publisher(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title('MQTT Data Publisher')
        self.pack(fill=BOTH, expand=True)

        self.canvas_input = Canvas(self, width=600, height=200)
        self.canvas_input.pack(side="top", padx=20, pady=20)

        self.params_label = Label(self.canvas_input, text="Publisher Parameters", font=("Helvetica", 16, "bold"))
        self.params_label.grid(row=0, column=0, columnspan=2, pady=(5, 20))

        self.num_publishers_label = Label(self.canvas_input, text="Number of Publishes per group:", font=("Helvetica", 12))
        self.num_publishers_label.grid(row=1, column=0, padx=(10, 10), sticky='w')
        self.num_publishers_entry = ttk.Entry(self.canvas_input, width=20)
        self.num_publishers_entry.grid(row=1, column=1, sticky='w', padx=(0, 10))
        self.num_publishers_entry.insert(0, "1")

        self.sleep_time_label = Label(self.canvas_input, text="Sleep time between groups of messages (sec):", font=("Helvetica", 12))
        self.sleep_time_label.grid(row=2, column=0, padx=(10, 10), sticky='w')
        self.sleep_time_entry = ttk.Entry(self.canvas_input, width=20)
        self.sleep_time_entry.grid(row=2, column=1, sticky='w')
        self.sleep_time_entry.insert(0, "1")

        self.start_button = ttk.Button(self.canvas_input, text="Start Publishing", command=self.start_publishing)
        self.start_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.console_output = Text(self, width=70, height=10)
        self.console_output.pack(padx=10, pady=10, fill=BOTH, expand=True)

        self.status_var = StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(self, textvariable=self.status_var, relief='sunken', anchor='w')
        self.status_bar.pack(side='bottom', fill='x')

    def start_publishing(self):
        try:
            num_publishers = int(self.num_publishers_entry.get())
            sleep_time = int(self.sleep_time_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values.")
            return

        self.status_var.set("Publishing...")
        self.console_output.delete(1.0, END)

        start_id = 111
        publisher_threads = []

        for i in range(num_publishers):
            thread = threading.Thread(target=self.publisher_thread, args=(start_id, sleep_time))
            thread.daemon = True
            publisher_threads.append(thread)
            start_id += 100
            thread.start()

    def publisher_thread(self, start_id, sleep_time):
        broker_address = "localhost"
        port = 1883
        topic = "weather/data"
        client = mqtt.Client()
        client.connect(broker_address, port, 60)

        for _ in range(10):
            if random.randint(1, 100) == 1:
                corrupted_data = '{"This is a corrupted message.'
                client.publish(topic, corrupted_data)
                self.console_output.insert(END, "Sent corrupted data.\n")
            else:
                data = create_data(start_id)
                data_json = json.dumps(data)
                client.publish(topic, data_json)
                self.console_output.insert(END, f"Sent data: {data['id']}\n")
        
            self.console_output.see(END)
            start_id += 1
            time.sleep(sleep_time)

        client.disconnect()
        self.status_var.set("Ready")

if __name__ == "__main__":
    root = Tk()
    app = Publisher(root)
    root.geometry('800x600+300+200') 
    root.mainloop()
