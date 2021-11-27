import utils
import weather

def main():
    w = weather.Weather(utils.getSetting('latitude'), utils.getSetting('longitude'))

if __name__ == "__main__":
    main()