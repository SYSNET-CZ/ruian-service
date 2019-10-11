from service.query import _find_address, _get_nearby_localities, _validate_address, _find_coordinates, \
    _find_coordinates_by_address, _get_ruian_version_date, _set_ruian_version_data_today, _get_database_details, \
    _get_table_names, _get_addresses, _get_parcela, _get_rozvodnice

get_parcela = _get_parcela
get_rozvodnice = _get_rozvodnice
find_address = _find_address
get_nearby_localities = _get_nearby_localities
validateAddress = _validate_address
findCoordinates = _find_coordinates
findCoordinatesByAddress = _find_coordinates_by_address
getRUIANVersionDate = _get_ruian_version_date
saveRUIANVersionDateToday = _set_ruian_version_data_today
getDBDetails = _get_database_details
getTableNames = _get_table_names
getAddresses = _get_addresses

def build_validateDict(street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber):
    return {
        "street": street,
        "houseNumber": houseNumber,
        "recordNumber": recordNumber,
        "orientationNumber": orientationNumber,
        "orientationNumberCharacter": orientationNumberCharacter,
        "zipCode": str(zipCode).replace(" ", ""),
        "locality": locality,
        "localityPart": localityPart,
        "districtNumber": districtNumber
    }