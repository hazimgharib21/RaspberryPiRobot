import irSensor

lineSensor = irSensor.irSensor(11,9,10,22,27)
lineSensor.setSampleTime(0.01)

while True:

    lineSensor.update()
    sensors = lineSensor.output
    strSensors = "";
    

 
    s1 = sensors[0]
    s2 = sensors[1]
    s3 = sensors[2]
    s4 = sensors[3]
    s5 = sensors[4]
    sampleTime = sensors[5]

    strSensors = strSensors + str(s1) + "\t"
    strSensors = strSensors + str(s2) + "\t"
    strSensors = strSensors + str(s3) + "\t"
    strSensors = strSensors + str(s4) + "\t"
    strSensors = strSensors + str(s5) + "\t"
    strSensors = strSensors + str(sampleTime)

    print strSensors
