'''
   This module was created to remove the octave dependency for reading data.
'''
def read_data(filename = 'data/sensor_data.dat'):
    odometry = []
    sensor_data = []
    sensor = []
    odom = {}
    first = 1;
    with open(filename) as f:
        line = f.readline()
        while(line):
            arr = line.split(' ')
            if(arr[0] == 'ODOMETRY'):
                if(first == 0):
                    odometry.append(odom)
                    sensor_data.append(sensor)
                    odom = {}
                    sensor = []
                first = 0
                odom['r1'] = float(arr[1])
                odom['t'] = float(arr[2])
                odom['r2'] = float(arr[3])
            elif(arr[0] == 'SENSOR'):
                reading = {}
                reading['id'] = float(arr[1])
                reading['range'] = float(arr[2])
                reading['bearing'] = float(arr[3])
                sensor.append(reading)
        
            line = f.readline()
            
    data = {}
    data['odometry'] = odometry
    data['sensor'] = sensor_data
    return data

def read_landmarks(filename='data/world.dat'):
    land_id = []
    x = []
    y = []

    with open(filename) as f:
        line = f.readline()
        while(line):
            arr = line.split(' ')
            land_id.append(int(arr[0]))
            x.append(float(arr[1]))
            y.append(float(arr[2]))
            line = f.readline()

    landmarks = {}
    landmarks['id'] = land_id
    landmarks['x'] = x
    landmarks['y'] = y

    return landmarks
            
