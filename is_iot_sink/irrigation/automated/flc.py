from simpful import *
from flc_constants import *
from pprint import *
#from is_iot_sink.logger import LOG

class FLC:
    def __init__(self):
        self.fs = FuzzySystem()
        for variable in FUZZY_SETS:
            set_name = next(iter(variable.keys()))
            values_iter = iter(variable.values())
            sets = next(values_iter)
            uod = next(values_iter)
            fuzzy_sets = []
            for set in sets:
                values = next(iter(set.values()))
                name = next(iter(set.keys()))
                size = len(values)
                if size == 3:    
                    f = FuzzySet(
                        function = Triangular_MF(
                            a = values[0],
                            b = values[1],
                            c = values[2]
                        ),
                        term = name
                    )
                elif size == 4:    
                    f = FuzzySet(
                        function=Trapezoidal_MF(
                            a = values[0],
                            b = values[1],
                            c = values[2],
                            d = values[3]
                        ),
                        term = name
                    )
                else:
                    #LOG.error("Invalid key in flc config!")
                    return
                fuzzy_sets.append(f)
            self.fs.add_linguistic_variable(
                set_name,
                LinguisticVariable(
                    fuzzy_sets,
                    universe_of_discourse = uod
                )
            )
        self.fs.add_rules(RULES)

    def solve(self,
            soil_moisture,
            air_temperature,
            air_humidity,
            light_intensity):
        self.fuzzify(
            soil_moisture,
            air_temperature,
            air_humidity,
            light_intensity
        )
        
        return self.inference()

    def fuzzify(self,
            soil_moisture,
            air_temperature,
            air_humidity,
            light_intensity):
        self.fs.set_variable("soil_moisture", soil_moisture)
        self.fs.set_variable("air_temperature", air_temperature)
        self.fs.set_variable("air_humidity", air_humidity)
        self.fs.set_variable("light_intensity", light_intensity)

    def inference(self):
        return (self.fs.Mamdani_inference(["irrigation_time"]))
