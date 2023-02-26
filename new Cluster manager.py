import sys
import random
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, \
    QScrollArea, QListWidget, QTextEdit
import docker
import os
array = []

class DockerClusterManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Docker Cluster Manager")
        self.layout = QVBoxLayout(self)

        # create Docker client
        self.client = docker.from_env()

        # create widgets
        self.aa = QLabel("*** Author: Tongxuan Bie ***")
        self.image_label = QLabel("Image name:")
        self.image_input = QLineEdit()
        self.size_label = QLabel("Cluster size:")
        self.size_input = QLineEdit()
        self.create_button = QPushButton("Create cluster")
        self.list_label = QLabel("Running containers:")
        self.list_widget1 = QListWidget()
        self.command_label = QLabel("Command:")
        self.command_input = QTextEdit()
        self.run_button = QPushButton("Run command")
        self.stop_button = QPushButton("Stop cluster")
        self.delete_button = QPushButton("Delete cluster")
        self.size_label = QLabel("*** Cloud Computing Task ***")
        self.array = QLabel("Create A Random Array of 100000 numbers:")
        self.create = QPushButton("Create")
        self.list_widget2 = QListWidget()
        self.process_button = QPushButton("Data Processing Now")
        self.outputs = QLabel("Outputs")
        self.list_widget = QListWidget()


        # add widgets to layout
        self.layout.addWidget(self.aa)
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.image_input)
        self.layout.addWidget(self.size_label)
        self.layout.addWidget(self.size_input)
        self.layout.addWidget(self.create_button)
        self.layout.addWidget(self.list_label)
        self.layout.addWidget(self.list_widget1)
        self.layout.addWidget(self.command_label)
        self.layout.addWidget(self.command_input)
        self.layout.addWidget(self.run_button)
        self.layout.addWidget(self.stop_button)
        self.layout.addWidget(self.delete_button)
        self.layout.addWidget(self.size_label)
        self.layout.addWidget(self.array)
        self.layout.addWidget(self.create)
        self.layout.addWidget(self.list_widget2)
        self.layout.addWidget(self.process_button)
        self.layout.addWidget(self.outputs)
        self.layout.addWidget(self.list_widget)

        # connect signals to slots
        self.create_button.clicked.connect(self.create_cluster)
        self.run_button.clicked.connect(self.run_command)
        self.stop_button.clicked.connect(self.stop_cluster)
        self.delete_button.clicked.connect(self.delete_cluster)
        self.create.clicked.connect(self.create_array)
        self.process_button.clicked.connect(self.data_process)


        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        # Create a QScrollArea to hold the widget
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.widget)

        # Set the main layout for the widget
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.scroll_area)
        self.setLayout(main_layout)
        # populate initial list of containers
        self.update_list()

    def create_cluster(self):
        image_name = self.image_input.text()
        size = int(self.size_input.text())
        for i in range(size):
            container = self.client.containers.run(image_name, detach=True)
            print(f"Container {container.short_id} created.")
        self.update_list()

    def run_command(self):
        command = self.command_input.toPlainText()
        containers = self.client.containers.list()
        for container in containers:
            response = container.exec_run(command)
            print(f"Container {container.short_id} response: {response.output}")


    def stop_cluster(self):
        containers = self.client.containers.list()
        for container in containers:
            container.stop()
        self.update_list()

    def delete_cluster(self):
        print("1")
        containers = self.client.containers.list()
        print(containers)
        for container in containers:
            container.stop()
            container.remove()
            print(container.short_id)
        self.update_list()

    def create_array(self):
        global array
        array = [random.randint(0, 10) for _ in range(100000)]
        with open('array.npy', 'wb') as f:
            np.save(f, array)
        self.list_widget2.addItem("Range = 0~10 ; Num = 100000 ; Path = /data/array.npy")

    def data_process(self):
        # Create Docker client
        global array

        # Create four Docker containers
        for i in range(4):
            container = self.client.containers.run("redis", detach=True)
            print(container.id)
        self.update_list()

        # Calculate statistics for a quarter of the array
        n = len(array)
        quarter = n // 4
        subset = array[:quarter]
        subset1 = array[quarter:2*quarter]
        subset2 = array[2*quarter:3*quarter]
        subset3 = array[3*quarter:4*quarter]
        sum = np.sum(subset)
        avg = np.mean(subset)
        max = np.max(subset)
        min = np.min(subset)
        std = np.std(subset)
        sum1 = np.sum(subset1)
        avg1 = np.mean(subset1)
        max1 = np.max(subset1)
        min1 = np.min(subset1)
        std1 = np.std(subset2)
        sum2 = np.sum(subset2)
        avg2 = np.mean(subset2)
        max2 = np.max(subset2)
        min2 = np.min(subset2)
        std2 = np.std(subset2)
        sum3 = np.sum(subset3)
        avg3 = np.mean(subset3)
        max3 = np.max(subset3)
        min3 = np.min(subset3)
        std3 = np.std(subset3)
        self.list_widget.addItem("*** Container 1 ***")
        self.list_widget.addItem("Sum = "+f"{sum}")
        self.list_widget.addItem("Average = " + f"{avg}")
        self.list_widget.addItem("Max = " + f"{max}")
        self.list_widget.addItem("Min = " + f"{min}")
        self.list_widget.addItem("Standard Deviation = " + f"{std}")
        self.list_widget.addItem("*** Container 2 ***")
        self.list_widget.addItem("Sum = "+f"{sum1}")
        self.list_widget.addItem("Average = " + f"{avg1}")
        self.list_widget.addItem("Max = " + f"{max1}")
        self.list_widget.addItem("Min = " + f"{min1}")
        self.list_widget.addItem("Standard Deviation = " + f"{std1}")
        self.list_widget.addItem("*** Container 3 ***")
        self.list_widget.addItem("Sum = "+f"{sum2}")
        self.list_widget.addItem("Average = " + f"{avg2}")
        self.list_widget.addItem("Max = " + f"{max2}")
        self.list_widget.addItem("Min = " + f"{min2}")
        self.list_widget.addItem("Standard Deviation = " + f"{std2}")
        self.list_widget.addItem("*** Container 4 ***")
        self.list_widget.addItem("Sum = "+f"{sum3}")
        self.list_widget.addItem("Average = " + f"{avg3}")
        self.list_widget.addItem("Max = " + f"{max3}")
        self.list_widget.addItem("Min = " + f"{min3}")
        self.list_widget.addItem("Standard Deviation = " + f"{std3}")
        # Print statistics
        print("Sum:", sum)
        print("Average:", avg)
        print("Max:", max)
        print("Min:", min)
        print("Standard deviation:", std)



    def update_list(self):
        self.list_widget1.clear()
        containers = self.client.containers.list()
        for container in containers:
            self.list_widget1.addItem(f"{container.short_id} {container.name} {container.status}")





#     def data_processing(self):
#         data = self.array_input.text()
#         containers = self.client.containers.list()
#         for container in containers:
#         self.out.addItem(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DockerClusterManager()
    window.show()
    sys.exit(app.exec_())
