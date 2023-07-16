from consumer import RobotConsumer

# Create a new RobotConsumer instance
robot = RobotConsumer('robots_file_directory', 'robot_file.json')

# Start consuming process
robot.start()
