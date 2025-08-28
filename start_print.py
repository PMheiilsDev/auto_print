import paramiko

import sys
from PyQt6.QtWidgets import QApplication, QFileDialog

def send_file(local_path, remote_filename, password):
    host = "192.168.178.105"
    port = 22
    username = "pi"
    remote_path = f"/home/pi/3d_print/gcode/{remote_filename}"

    transport = paramiko.Transport((host, port))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(local_path, remote_path)
    sftp.close()
    transport.close()
    print(f"File sent to {remote_path}")

def execute_remote_command(password):

    host = "192.168.178.105"
    port = 22
    username = "pi"
    command = "nohup python -u print_new.py > out.log 2>&1 &"
    workdir = "/home/pi/3d_print"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port=port, username=username, password=password)

    ssh.exec_command(f"cd {workdir} && {command}")
    ssh.close()
    print("Remote script started in background.")

def select_file():
    app = QApplication.instance() or QApplication(sys.argv)

    # Show native file dialog
    file_path, _ = QFileDialog.getOpenFileName(
        None,
        "Select a G-code file",
        "",  # start directory ("" = current dir)
        "G-code Files (*.gcode);;All Files (*)"
    )

    return file_path


if __name__ == "__main__":
    # Example usage
    local_file = select_file()  
    remote_file = "temp.gcode" # Change to desired remote filename
    with open("pw.txt", "r") as f:
        pi_password = f.read().strip()

    send_file(local_file, remote_file, pi_password)
    execute_remote_command(pi_password)


