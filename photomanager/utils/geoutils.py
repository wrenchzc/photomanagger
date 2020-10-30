from geopy.exc import GeopyError
import re
from geopy.geocoders import Nominatim
from geopy import units

_geo_locator = Nominatim(user_agent="photomanager")

def gps_info_to_degress(value):
    pattern = '(.*?)\|\[(\d+).*?(\d+).*?(\d+)\/(\d+)'
    match = re.match(pattern, value)
    if match:
        letter, radians, arcminutes, arcseconds_numerator, arcseconds_denominator = match.groups()
        arcseconds = int(arcseconds_numerator) / int(arcseconds_denominator)
        degress = int(radians) + float(arcminutes) / 60 + arcseconds / 3500
        return f"{letter}{degress}"

    # for format E|[111, 33, 36]
    pattern = '(.*?)\|\[(\d+).*?(\d+).*?(\d+)'
    match = re.match(pattern, value)
    if match:
        letter, radians, arcminutes, arcseconds= match.groups()
        degress = int(radians) + float(arcminutes) / 60 + float(arcseconds) / 3500
        return f"{letter}{degress}"


def get_address_by_lat_lng(latitude: str, longitude: str) -> str:
    """
    :param latitude:  should like N|[25, 44, 23236999/1000000]
    :param longitude: should like E|[113, 44, 7412567/250000]
    :return: address or None
    """
    try:
        latitude = gps_info_to_degress(latitude)
        longitude = gps_info_to_degress(longitude)

        location = _geo_locator.reverse(f"{latitude},{longitude}", exactly_one=True)
        return location.address

    except TypeError:
        return None
    except ValueError:
        return None
    except GeopyError:
        return None
    except Exception:
        return None


