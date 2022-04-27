from simpful import *
from is_iot_sink.irrigation.automated.flc_constants import *
from is_iot_sink.logger import LOG

ZERO_THRESHOLD = 2

class FLC:
    def __init__(self):
        self.fs1 = FuzzySystem(show_banner = False)
        self.fs2 = FuzzySystem(show_banner = False)
        self.fs3 = FuzzySystem(show_banner = False)
        self.__add_fs_variables(self.fs1, FLC1_SETS)
        self.__add_fs_variables(self.fs2, FLC2_SETS)
        self.__add_fs_variables(self.fs3, FLC3_SETS)
        self.fs1.add_rules(FLC1_RULES)
        self.fs2.add_rules(FLC2_RULES)
        self.fs3.add_rules(FLC3_RULES)
        LOG.info("Fuzzy logic controller initialized!")

    def solve(self,
            soil_moisture,
            air_temperature,
            air_humidity,
            light_intensity):
        self.__fuzzify_fs1(
            soil_moisture,
            air_temperature,
        )
        irrigation_time = self.fs1.Mamdani_inference(["irrigation_time"])["irrigation_time"]

        self.__fuzzify_fs2(
            irrigation_time,
            air_humidity,
        )
        irrigation_time = self.fs2.Mamdani_inference(["irrigation_time"])["irrigation_time"]

        self.__fuzzify_fs3(
            irrigation_time,
            light_intensity,
        )
        irrigation_time = self.fs3.Mamdani_inference(["irrigation_time"])["irrigation_time"]

        if irrigation_time <= ZERO_THRESHOLD:
            irrigation_time = 0

        return irrigation_time

    def __fuzzify_fs1(self,
            soil_moisture,
            air_temperature
            ):
        self.fs1.set_variable("soil_moisture", soil_moisture)
        self.fs1.set_variable("air_temperature", air_temperature)

    def __fuzzify_fs2(self,
            irrigation_time_input,
            air_humidity
            ):
        self.fs2.set_variable("irrigation_time_input", irrigation_time_input)
        self.fs2.set_variable("air_humidity", air_humidity)

    def __fuzzify_fs3(self,
            irrigation_time_input,
            light_intensity
            ):
        self.fs3.set_variable("irrigation_time_input", irrigation_time_input)
        self.fs3.set_variable("light_intensity", light_intensity)

    def __add_fs_variables(self, fs, data_sets):
        for variable in data_sets:
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
                    LOG.error("Invalid key in flc config!")
                    return
                fuzzy_sets.append(f)
            fs.add_linguistic_variable(
                set_name,
                LinguisticVariable(
                    fuzzy_sets,
                    universe_of_discourse = uod
                )
            )

flc = FLC()