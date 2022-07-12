IRRIGATION_TIME_MF = [
    {
        "none": [0, 0, 2]
    }, {
        "short": [0, 2, 4]
    }, {
        "medium": [2, 4, 6]
    }, {
        "long": [4, 6, 8]
    }, {
        "very_long": [6, 8, 10, 10]
    }
]

IRRIGATION_TIME_SET = {
    "irrigation_time": IRRIGATION_TIME_MF,
    "uod": [0, 10]
}

IRRIGATION_TIME_INPUT_SET = {
    "irrigation_time_input": IRRIGATION_TIME_MF,
    "uod": [0, 10]
}

FLC1_SETS = [
    {
        "soil_moisture": [{
            "dry": [0, 0, 30, 40]
        }, {
            "moderate": [20, 50, 80]
        }, {
            "wet": [60, 70, 100, 100]
        }],
        "uod": [0, 100]
    },
    {
        "air_temperature": [{
            "cold": [-30, -30, 10, 13]
        }, {
            "moderate": [10, 16.5, 23]
        }, {
            "hot": [20, 23, 50, 50]
        }],
        "uod": [-30, 50]
    }, 
    IRRIGATION_TIME_SET
]

FLC2_SETS = [  IRRIGATION_TIME_INPUT_SET,
    {
        "air_humidity": [{
            "low": [0, 0, 30, 40]
        }, {
            "moderate": [30, 50, 70]
        }, {
            "high": [70, 80, 100, 100]
        }],
        "uod": [0, 100]
    }, 
    IRRIGATION_TIME_SET
]

FLC3_SETS = [
    IRRIGATION_TIME_INPUT_SET,
    {
        "light_intensity": [{
            "dark": [0, 0, 30, 40]
        }, {
            "moderate": [30, 50, 70]
        }, {
            "bright": [60, 70, 100, 100]
        }],
        "uod": [0, 100]
    },
    IRRIGATION_TIME_SET
]

FLC1_RULES = [
    "IF (soil_moisture IS dry) AND (air_temperature IS cold) THEN (irrigation_time IS long)",
    "IF (soil_moisture IS dry) AND (air_temperature IS moderate) THEN (irrigation_time IS very_long)",
    "IF (soil_moisture IS dry) AND (air_temperature IS hot) THEN (irrigation_time IS very_long)",
    "IF (soil_moisture IS moderate) AND (air_temperature IS cold) THEN (irrigation_time IS short)",
    "IF (soil_moisture IS moderate) AND (air_temperature IS moderate) THEN (irrigation_time IS medium)",
    "IF (soil_moisture IS moderate) AND (air_temperature IS hot) THEN (irrigation_time IS medium)",
    "IF (soil_moisture IS wet) THEN (irrigation_time IS none)"
]

FLC2_RULES = [
    "IF (irrigation_time_input IS none) THEN (irrigation_time IS none)",
    "IF (irrigation_time_input IS short) AND (air_humidity IS low) THEN (irrigation_time IS medium)",
    "IF (irrigation_time_input IS short) AND (air_humidity IS moderate) THEN (irrigation_time IS short)",
    "IF (irrigation_time_input IS short) AND (air_humidity IS high) THEN (irrigation_time IS none)",
    "IF (irrigation_time_input IS medium) AND (air_humidity IS low) THEN (irrigation_time IS long)",
    "IF (irrigation_time_input IS medium) AND (air_humidity IS moderate) THEN (irrigation_time IS medium)",
    "IF (irrigation_time_input IS medium) AND (air_humidity IS high) THEN (irrigation_time IS medium)",
    "IF (irrigation_time_input IS long) AND (air_humidity IS low) THEN (irrigation_time IS very_long)",
    "IF (irrigation_time_input IS long) AND (air_humidity IS moderate) THEN (irrigation_time IS long)",
    "IF (irrigation_time_input IS long) AND (air_humidity IS high) THEN (irrigation_time IS long)",
    "IF (irrigation_time_input IS very_long) AND (air_humidity IS low) THEN (irrigation_time IS very_long)",
    "IF (irrigation_time_input IS very_long) AND (air_humidity IS moderate) THEN (irrigation_time IS very_long)",
    "IF (irrigation_time_input IS very_long) AND (air_humidity IS high) THEN (irrigation_time IS long)"
]

FLC3_RULES = [
    "IF (irrigation_time_input IS none) THEN (irrigation_time IS none)",
    "IF (irrigation_time_input IS short) AND (light_intensity IS dark) THEN (irrigation_time IS medium)",
    "IF (irrigation_time_input IS short) AND (light_intensity IS moderate) THEN (irrigation_time IS short)",
    "IF (irrigation_time_input IS short) AND (light_intensity IS bright) THEN (irrigation_time IS short)",
    "IF (irrigation_time_input IS medium) AND (light_intensity IS dark) THEN (irrigation_time IS long)",
    "IF (irrigation_time_input IS medium) AND (light_intensity IS moderate) THEN (irrigation_time IS medium)",
    "IF (irrigation_time_input IS medium) AND (light_intensity IS bright) THEN (irrigation_time IS medium)",
    "IF (irrigation_time_input IS long) AND (light_intensity IS dark) THEN (irrigation_time IS long)",
    "IF (irrigation_time_input IS long) AND (light_intensity IS moderate) THEN (irrigation_time IS long)",
    "IF (irrigation_time_input IS long) AND (light_intensity IS bright) THEN (irrigation_time IS long)",
    "IF (irrigation_time_input IS very_long) AND (light_intensity IS dark) THEN (irrigation_time IS very_long)",
    "IF (irrigation_time_input IS very_long) AND (light_intensity IS moderate) THEN (irrigation_time IS very_long)",
    "IF (irrigation_time_input IS very_long) AND (light_intensity IS bright) THEN (irrigation_time IS very_long)"
]
