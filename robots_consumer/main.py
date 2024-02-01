from consumer import RobotConsumer

dirname = input("Nombre de la carpeta a buscar: ")
filename = input("Nombre del JSON en el cuál están los robots: ")

# Create a new RobotConsumer instance
robot = RobotConsumer(dirname=dirname, filename=f'{filename}.json')

# Start consuming process
robot.start()
