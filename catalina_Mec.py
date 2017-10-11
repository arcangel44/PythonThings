import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import serial

ser = serial.Serial('COM3', 115200)

results = []
calibrationList = []
dataList = []

try:
    print("Inicio de calibracion del sensor mioelectrico")
    print("Por favor espere")
    calibrate = False
    while not calibrate:
        calibrationVerification = input("Escriba 's' y luego presione entrar cuando esté preparado el sensor \n")
        if calibrationVerification == "s":
            while len(calibrationList) <= 350:
                dataCalibration = ser.readline()[:-2]
                if dataCalibration != "":
                    try:
                        calibVal = float(dataCalibration)
                        calibrationList.append(calibVal)
                        calibrate = True
                    except (ValueError, IndexError):
                        print("Dato ignorado. Formato incorrecto")
        calibrationVector = np.asarray(calibrationList)
        mediaCalibration = float(sum(calibrationVector))/float(len(calibrationVector))
    print("Lectura de datos...")
    while True:
        dataMio = ser.readline()[:-2]
        print(dataMio)
        if dataMio != "":
            try:
                readVal = float(dataMio)-mediaCalibration
                dataList.append(readVal)
            except:
                print("Dato ignorado. Formato incorrecto")
except KeyboardInterrupt:
    selected = False
    dataVecMio = np.asarray(dataList)
    while not selected:
        response = input("Desea guardar el vector de datos. s/n \n")
        if response == "s":
            print("Recibido si")
            np.savetxt('data.txt', dataVecMio)
        selected = True
    plt.plot(dataVecMio, 'r')
    plt.show()
