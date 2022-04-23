# (Work In Progress) is-iot-sink

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
python3 is-iot-collector/main.py
```