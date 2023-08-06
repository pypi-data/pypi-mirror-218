from datetime import datetime
from datetime import datetime
from typing import Any
from typing import List
from uuid import UUID

from ..authenticate import AuthenticationResult
from ..consts import ENDPOINT
from ..helpers import from_str, from_datetime, from_none, from_int, from_list, from_float, from_bool


# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = welcome3_from_dict(json.loads(json_string))


class House:
    house_id: UUID
    electricity_local_id: str
    name: str
    address: str
    postal_code: str
    city: str
    district: str
    country: str
    timezone: str
    creation_date: datetime
    client_id: UUID
    house_profile: str
    service_provider: str
    gas_local_id: None
    classification: str
    status: str
    is_settlement_active: int
    settlement_valid_from: datetime
    billing_date: datetime
    billing_period: str
    readings_date: datetime
    product_type: str
    latitude: float
    longitude: float
    id_meteo: int
    plan: str
    permission_role: str

    def __init__(self, house_id: UUID, electricity_local_id: str, name: str, address: str, postal_code: str, city: str,
                 district: str, country: str, timezone: str, creation_date: datetime, client_id: UUID,
                 house_profile: str, service_provider: str, gas_local_id: None, classification: str, status: str,
                 is_settlement_active: int, settlement_valid_from: datetime, billing_date: datetime,
                 billing_period: str, readings_date: datetime, product_type: str, latitude: float, longitude: float,
                 id_meteo: int, plan: str, permission_role: str) -> None:
        self.house_id = house_id
        self.electricity_local_id = electricity_local_id
        self.name = name
        self.address = address
        self.postal_code = postal_code
        self.city = city
        self.district = district
        self.country = country
        self.timezone = timezone
        self.creation_date = creation_date
        self.client_id = client_id
        self.house_profile = house_profile
        self.service_provider = service_provider
        self.gas_local_id = gas_local_id
        self.classification = classification
        self.status = status
        self.is_settlement_active = is_settlement_active
        self.settlement_valid_from = settlement_valid_from
        self.billing_date = billing_date
        self.billing_period = billing_period
        self.readings_date = readings_date
        self.product_type = product_type
        self.latitude = latitude
        self.longitude = longitude
        self.id_meteo = id_meteo
        self.plan = plan
        self.permission_role = permission_role

    @staticmethod
    def from_dict(obj: Any) -> 'House':
        assert isinstance(obj, dict)
        house_id = UUID(obj.get("houseId"))
        electricity_local_id = from_str(obj.get("electricityLocalId"))
        name = from_str(obj.get("name"))
        address = from_str(obj.get("address"))
        postal_code = from_str(obj.get("postalCode"))
        city = from_str(obj.get("city"))
        district = from_str(obj.get("district"))
        country = from_str(obj.get("country"))
        timezone = from_str(obj.get("timezone"))
        creation_date = from_datetime(obj.get("creationDate"))
        client_id = UUID(obj.get("clientId"))
        house_profile = from_str(obj.get("houseProfile"))
        service_provider = from_str(obj.get("serviceProvider"))
        gas_local_id = from_none(obj.get("gasLocalId"))
        classification = from_str(obj.get("classification"))
        status = from_str(obj.get("status"))
        is_settlement_active = from_int(obj.get("isSettlementActive"))
        settlement_valid_from = from_datetime(obj.get("settlementValidFrom"))
        billing_date = from_datetime(obj.get("billingDate"))
        billing_period = from_str(obj.get("billingPeriod"))
        readings_date = from_datetime(obj.get("readingsDate"))
        product_type = from_str(obj.get("productType"))
        latitude = from_float(obj.get("latitude"))
        longitude = from_float(obj.get("longitude"))
        id_meteo = from_int(obj.get("idMeteo"))
        plan = from_str(obj.get("plan"))
        permission_role = from_str(obj.get("permissionRole"))
        return House(house_id, electricity_local_id, name, address, postal_code, city, district, country, timezone,
                     creation_date, client_id, house_profile, service_provider, gas_local_id, classification, status,
                     is_settlement_active, settlement_valid_from, billing_date, billing_period, readings_date,
                     product_type, latitude, longitude, id_meteo, plan, permission_role)


class Device:
    connection_state: bool
    creation_date: datetime
    device_id: UUID
    device_local_id: str
    firmware_version: str
    house_id: UUID
    last_communication: datetime
    model: str
    type: str

    def __init__(self, connection_state: bool, creation_date: datetime, device_id: UUID, device_local_id: str,
                 firmware_version: str, house_id: UUID, last_communication: datetime, model: str, type: str) -> None:
        self.connection_state = connection_state
        self.creation_date = creation_date
        self.device_id = device_id
        self.device_local_id = device_local_id
        self.firmware_version = firmware_version
        self.house_id = house_id
        self.last_communication = last_communication
        self.model = model
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> 'Device':
        assert isinstance(obj, dict)
        connection_state = from_bool(obj.get("connectionState"))
        creation_date = from_datetime(obj.get("creationDate"))
        device_id = UUID(obj.get("deviceId"))
        device_local_id = from_str(obj.get("deviceLocalId"))
        firmware_version = from_str(obj.get("firmwareVersion"))
        house_id = UUID(obj.get("houseId"))
        last_communication = from_datetime(obj.get("lastCommunication"))
        model = from_str(obj.get("model"))
        type = from_str(obj.get("type"))
        return Device(connection_state, creation_date, device_id, device_local_id, firmware_version, house_id,
                      last_communication, model, type)


class HousesResponse:
    houses: List[House]

    def __init__(self, houses: List[House]) -> None:
        self.houses = houses

    @staticmethod
    def from_dict(obj: Any) -> 'HousesResponse':
        assert isinstance(obj, dict)
        houses = from_list(House.from_dict, obj.get("houses"))
        return HousesResponse(houses)


class HardwareAttributes:
    supported: List[Any]

    def __init__(self, supported: List[Any]) -> None:
        self.supported = supported

    @staticmethod
    def from_dict(obj: Any) -> 'HardwareAttributes':
        assert isinstance(obj, dict)
        supported = from_list(lambda x: x, obj.get("supported"))
        return HardwareAttributes(supported)


class ActiveEnergyProduced:
    period: int
    unit: str

    def __init__(self, period: int, unit: str) -> None:
        self.period = period
        self.unit = unit

    @staticmethod
    def from_dict(obj: Any) -> 'ActiveEnergyProduced':
        assert isinstance(obj, dict)
        period = from_int(obj.get("period"))
        unit = from_str(obj.get("unit"))
        return ActiveEnergyProduced(period, unit)


class HistoricVars:
    average_voltage: ActiveEnergyProduced
    active_energy_produced: ActiveEnergyProduced
    supported: List[str]

    def __init__(self, average_voltage: ActiveEnergyProduced, active_energy_produced: ActiveEnergyProduced, supported: List[str]) -> None:
        self.average_voltage = average_voltage
        self.active_energy_produced = active_energy_produced
        self.supported = supported

    @staticmethod
    def from_dict(obj: Any) -> 'HistoricVars':
        assert isinstance(obj, dict)
        average_voltage = ActiveEnergyProduced.from_dict(obj.get("AverageVoltage"))
        active_energy_produced = None
        if obj.get("ActiveEnergyProduced") is not None:
            active_energy_produced = ActiveEnergyProduced.from_dict(obj.get("ActiveEnergyProduced"))
        supported = from_list(from_str, obj.get("supported"))
        return HistoricVars(average_voltage, active_energy_produced, supported)


class ActivePowerAminus:
    unit: str

    def __init__(self, unit: str) -> None:
        self.unit = unit

    @staticmethod
    def from_dict(obj: Any) -> 'ActivePowerAminus':
        assert isinstance(obj, dict)
        unit = from_str(obj.get("unit"))
        return ActivePowerAminus(unit)


class TotalActiveEnergyAminus:
    value: float
    unit: str

    def __init__(self, value: float, unit: str) -> None:
        self.value = value
        self.unit = unit

    @staticmethod
    def from_dict(obj: Any) -> 'TotalActiveEnergyAminus':
        assert isinstance(obj, dict)
        value = from_float(obj.get("value"))
        unit = from_str(obj.get("unit"))
        return TotalActiveEnergyAminus(value, unit)


class StateVars:
    active_power_aminus: ActivePowerAminus
    total_active_energy_aminus: TotalActiveEnergyAminus
    supported: List[str]
    voltage: TotalActiveEnergyAminus

    def __init__(self, active_power_aminus: ActivePowerAminus, total_active_energy_aminus: TotalActiveEnergyAminus, supported: List[str], voltage: TotalActiveEnergyAminus) -> None:
        self.active_power_aminus = active_power_aminus
        self.total_active_energy_aminus = total_active_energy_aminus
        self.supported = supported
        self.voltage = voltage

    @staticmethod
    def from_dict(obj: Any) -> 'StateVars':
        assert isinstance(obj, dict)
        active_power_aminus = ActivePowerAminus.from_dict(obj.get("activePowerAminus"))
        total_active_energy_aminus = TotalActiveEnergyAminus.from_dict(obj.get("totalActiveEnergyAminus"))
        supported = from_list(from_str, obj.get("supported"))
        voltage = TotalActiveEnergyAminus.from_dict(obj.get("voltage"))
        return StateVars(active_power_aminus, total_active_energy_aminus, supported, voltage)

class UserAttributes:
    pass

    def __init__(self, ) -> None:
        pass

    @staticmethod
    def from_dict(obj: Any) -> 'UserAttributes':
        assert isinstance(obj, dict)
        return UserAttributes()


class Module:
    historic_vars: HistoricVars
    model: int
    user_attributes: UserAttributes
    house_id: UUID
    last_communication: int
    module_id: UUID
    hardware_attributes: HardwareAttributes
    creation_date: datetime
    state_vars: StateVars
    name: str
    vendor: str
    connectivity_state: str
    firmware_version: str
    groups: List[str]
    device_id: UUID
    module_local_id: str
    favorite: bool
    legacy_module_local_id: str
    serial_number: str

    def __init__(self, historic_vars: HistoricVars, model: int, user_attributes: UserAttributes, house_id: UUID, last_communication: int, module_id: UUID, hardware_attributes: HardwareAttributes, creation_date: datetime, state_vars: StateVars, name: str, vendor: str, connectivity_state: str, firmware_version: str, groups: List[str], device_id: UUID, module_local_id: str, favorite: bool, legacy_module_local_id: str, serial_number: str) -> None:
        self.historic_vars = historic_vars
        self.model = model
        self.user_attributes = user_attributes
        self.house_id = house_id
        self.last_communication = last_communication
        self.module_id = module_id
        self.hardware_attributes = hardware_attributes
        self.creation_date = creation_date
        self.state_vars = state_vars
        self.name = name
        self.vendor = vendor
        self.connectivity_state = connectivity_state
        self.firmware_version = firmware_version
        self.groups = groups
        self.device_id = device_id
        self.module_local_id = module_local_id
        self.favorite = favorite
        self.legacy_module_local_id = legacy_module_local_id
        self.serial_number = serial_number

    @staticmethod
    def from_dict(obj: Any) -> 'Module':
        assert isinstance(obj, dict)
        historic_vars = HistoricVars.from_dict(obj.get("historicVars"))
        model = int(from_str(obj.get("model")))
        user_attributes = UserAttributes.from_dict(obj.get("userAttributes"))
        house_id = UUID(obj.get("houseId"))
        last_communication = from_int(obj.get("lastCommunication"))
        module_id = UUID(obj.get("moduleId"))
        hardware_attributes = HardwareAttributes.from_dict(obj.get("hardwareAttributes"))
        creation_date = from_datetime(obj.get("creationDate"))
        state_vars = StateVars.from_dict(obj.get("stateVars"))
        name = from_str(obj.get("name"))
        vendor = from_str(obj.get("vendor"))
        connectivity_state = from_str(obj.get("connectivityState"))
        firmware_version = from_str(obj.get("firmwareVersion"))
        groups = from_list(from_str, obj.get("groups"))
        device_id = UUID(obj.get("deviceId"))
        module_local_id = from_str(obj.get("moduleLocalId"))
        favorite = from_bool(obj.get("favorite"))
        legacy_module_local_id = from_str(obj.get("legacyModuleLocalId"))
        serial_number = from_str(obj.get("serialNumber"))
        return Module(historic_vars, model, user_attributes, house_id, last_communication, module_id, hardware_attributes, creation_date, state_vars, name, vendor, connectivity_state, firmware_version, groups, device_id, module_local_id, favorite, legacy_module_local_id, serial_number)


class ModulesResponse:
    modules: List[Module]

    def __init__(self, modules: List[Module]) -> None:
        self.modules = modules

    @staticmethod
    def from_dict(obj: Any) -> 'ModulesResponse':
        assert isinstance(obj, dict)
        modules = from_list(Module.from_dict, obj.get("Modules"))
        return ModulesResponse(modules)

class Equipment:
    authentication: AuthenticationResult = None
    endpoint = ENDPOINT + "/equipment"

    def __init__(self, authentication: AuthenticationResult):
        self.authentication = authentication

    def houses(self) -> List[House]:
        response = self.authentication.get(f"{self.endpoint}/houses")
        houses_response = HousesResponse.from_dict(response.json())
        return houses_response.houses

    def device(self, house_id: UUID) -> List[Device]:
        response = self.authentication.get(f"{self.endpoint}/houses/{house_id}/device")
        devices = from_list(Device.from_dict, response.json())
        return devices

    def modules(self, house_id: UUID) -> List[Module]:
        response = self.authentication.get(f"{self.endpoint}/houses/{house_id}/modules")
        modules = ModulesResponse.from_dict(response.json())
        return modules.modules

