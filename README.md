# is-iot-sink

This repository represents the sink module of an IoT Irrigation System that:
1. Communicates with collectors via MQTT and uploads collected data into a MongoDB database.
2. Communicates with a web application via MQTT accepting configurations and manual control of water valves.

### System requirements
The application was developed on Raspberry Pi 4B+ 8Gb RAM with Raspbian Buster as operating system, written in Python3.7.

### Electric connections
![sink-electric](https://user-images.githubusercontent.com/51260103/178804914-d656d58f-85b0-4758-9ed9-78cdeef43d41.png)
  1. 1x 8 Relay Module board -> [source](https://www.amazon.com/SainSmart-101-70-102-8-Channel-Relay-Module/dp/B0057OC5WK)
  2. 1x 230VAC to 24VAC Transformer -> [source](https://www.tme.eu/ro/en/details/stm50_24v/transformers-with-fastening/breve-tufvassons/stm50-230-24v/)
  3. 6x 24VAC Solenoid Valves -> [source](https://www.amazon.com/Hunter-Industries-RTL0502PGV101G-Irrigation-Valve/dp/B000678LWQ/ref=pd_lpo_2?pd_rd_i=B000678LWQ&th=1)

### Install prerequisites
```
sudo apt-get update
sudo apt-get install git python3-pip python3-venv
```

### Clone repository
```
cd ~/ && git clone https://github.com/pdany1116/is-iot-sink.git
cd is-iot-sink
```

### Create virtual environment and activate
```
python3 -m venv env
source env/bin/activate
```

### Install requirements packages
```
pip install -r requirements.txt
```

### Configure enviroment variables
#### Change default values
```
cp .env.example .env
nano .env
```
`Note: Replace the environment variables with your values. All variables need to be defined!!!`
#### Export environment variables
```
set -o allexport; source .env; set +o allexport
```

### Configure system setup
```
nano setup.xml
```

### Configure python path
```
export PYTHONPATH=$(pwd):${PYTHONPATH}
```

### Run main
```
python3 is_iot_sink/main.py
```
