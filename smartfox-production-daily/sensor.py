"""Platform for sensor integration."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfEnergy
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
import requests
from xml.etree import ElementTree as ET


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the sensor platform."""
    add_entities([ProductionDailySolarSensor()])


class ProductionDailySolarSensor(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Production Solar Sensor Daily"
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        # Fetch the XML content
        response = requests.get('http://192.168.2.220/values.xml')
        if response.status_code == 200:
            # Parse the XML content
            root = ET.fromstring(response.content)

            # Find the 'value' element with id 'wr1PowerValue'
            # toGridValue = root.find('.//value[@id="toGridValue"]')
            wr1PowerValueElement = root.find('.//value[@id="hidWr1EnergyDay"]')

            if wr1PowerValueElement is not None:
                # Extract the text content of the element, remove ' kW', and convert to float
                powerValueText = wr1PowerValueElement.text
                self._attr_native_value = float(powerValueText) / 1000

            else:
                print("element not found.")
        else:
            print("Failed to fetch XML content.")
