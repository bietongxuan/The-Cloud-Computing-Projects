import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QListWidget, QTextEdit
import docker
import os
class DockerClusterManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Docker Cluster Manager")
        self.layout = QVBoxLayout(self)

        # create Docker client
        self.client = docker.from_env()

        # create widgets
        self.image_label = QLabel("Image name:")
        self.image_input = QLineEdit()
        self.size_label = QLabel("Cluster size:")
        self.size_input = QLineEdit()
        self.create_button = QPushButton("Create cluster")
        self.list_label = QLabel("Running containers:")
        self.list_widget = QListWidget()
        self.command_label = QLabel("Command:")
        self.command_input = QTextEdit()
        self.run_button = QPushButton("Run command")
        self.stop_button = QPushButton("Stop cluster")
        self.delete_button = QPushButton("Delete cluster")

        # add widgets to layout
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.image_input)
        self.layout.addWidget(self.size_label)
        self.layout.addWidget(self.size_input)
        self.layout.addWidget(self.create_button)
        self.layout.addWidget(self.list_label)
        self.layout.addWidget(self.list_widget)
        self.layout.addWidget(self.command_label)
        self.layout.addWidget(self.command_input)
        self.layout.addWidget(self.run_button)
        self.layout.addWidget(self.stop_button)
        self.layout.addWidget(self.delete_button)

        # connect signals to slots
        self.create_button.clicked.connect(self.create_cluster)
        self.run_button.clicked.connect(self.run_command)
        self.stop_button.clicked.connect(self.stop_cluster)
        self.delete_button.clicked.connect(self.delete_cluster)

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
        self.update_list()

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

    def update_list(self):
        self.list_widget.clear()
        containers = self.client.containers.list()
        for container in containers:
            self.list_widget.addItem(f"{container.short_id} {container.name} {container.status}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DockerClusterManager()
    window.show()
    sys.exit(app.exec_())