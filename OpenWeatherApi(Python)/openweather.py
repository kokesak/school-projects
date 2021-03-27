import socket
import sys
import json

#print(len(sys.argv))
#print(sys.argv)
if len(sys.argv) != 3:
    sys.stderr.write("Invalid Number Of Arguments\n")
    sys.exit(1)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = "api.openweathermap.org"
port = 80

# appid = 0a32faeaef688ed39f87ae9e28f3c026
city = sys.argv[2]
appid = sys.argv[1]

#city.lower()
data_path = "/data/2.5/weather?q="+city.lower()+"&APPID="+appid+"&units=metric"


request = "GET "+data_path+" HTTP/1.1\r\n" "Host: "+server+"\r\n" "Connecton: close\r\n\r\n"

s.connect((server,port))
s.send(request.encode())
try:
        result = s.recv(4096)
except socket.timeout as e:
        err = e.args[0]
        if err == 'timed out':
                print ('Recieved timed out, retry later\n')
                sys.exit(1)
        else:
                print (e)
                sys.exit(1)
except socket.error as e:
        print (e)
        sys.exit(1)
else:
        if len(result) == 0:
                print("Message error\n")
                sys.exit(0)
        result = result.decode()
        
        # data pro json zacinaji prvim znakem {
        result = result[result.find("{"):]

        try:
                data = json.loads(result)
        except ValueError as e:
                print("Bad request or some other error\n")
                sys.exit(1)

        else:
                if data['cod'] != 200:
                        sys.stderr.write("Message: {}\n".format(data['message']))
                        sys.stderr.write("Error code: {}\n".format(data['cod']))
                        sys.exit(1)



                weather = data['weather'][0]['description']
                temp = data['main']['temp']
                humidity = data['main']['humidity']
                pressure = data['main']['pressure']
                wind_speed = data['wind']['speed']
                
                # deg nemusi byt zahrnut ve wind
                if 'deg' in data['wind']:
                        wind_deg = data['wind']['deg']
                else:
                        wind_deg = "-"

                print(city)
                print(weather)
                print("temp: {}\u2103".format(temp))
                print("humidity: {}%".format(humidity))
                print("pressure: {} hPa".format(pressure))
                print("wind-speed: {} m/s".format(wind_speed)) # nebo vynasobit 3.6 abych dostal km/h
                print("wind-deg: {}".format(wind_deg))
                sys.exit(0)
finally:
        s.close()

