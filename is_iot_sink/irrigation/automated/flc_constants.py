FUZZY_SETS = [{
    "soil_moisture": [{
        "dry": [0, 0, 30, 40]
    }, {
        "moderate": [20, 50, 80]
    }, {
        "wet": [60, 70, 100, 100]
    }],
    "uod": [0, 100]
}, {
    "air_temperature": [{
        "cold": [-10, -10, 10, 12]
    }, {
        "moderate": [10, 15, 20]
    }, {
        "hot": [18, 20, 40, 40]
    }],
    "uod": [-10, 40]
}, {
    "air_humidity": [{
        "low": [0, 0, 30, 40]
    }, {
        "moderate": [30, 50, 70]
    }, {
        "high": [70, 80, 100, 100]
    }],
    "uod": [0, 100]
}, {
    "light_intensity": [{
        "dark": [0, 0, 30, 40]
    }, {
        "moderate": [30, 50, 70]
    }, {
        "bright": [60, 70, 100, 100]
    }],
    "uod": [0, 100]
}, {
    "irrigation_time": [{
        "non": [0, 0, 2]
    }, {
        "short": [0, 2, 4]
    }, {
        "medium": [2, 4, 6]
    }, {
        "long": [4, 6, 8]
    }, {
        "very_long": [6, 8, 10, 10]
    }],
    "uod": [0, 10]
}]

RULES = ["IF (soil_moisture IS dry) THEN (irrigation_time IS very_long)"]
