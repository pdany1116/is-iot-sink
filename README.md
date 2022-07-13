# is-iot-sink

This repository represents the sink module of an IoT Irrigation System that:
1. Communicates with collectors via MQTT and uploads collected data into a MongoDB database.
2. Communicates with a web application via MQTT accepting configurations and manual control of water valves.

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
```
`Note: Replace the environment variables with your values. All variables need to have values!!!`
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
