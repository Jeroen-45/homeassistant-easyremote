"""Platform for light integration."""
from __future__ import annotations

import logging

from pyeasyremote import EasyRemote
import voluptuous as vol

# Import the device class from the component that you want to support
import homeassistant.helpers.config_validation as cv
from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_RGB_COLOR,
    COLOR_MODE_RGB,
    SUPPORT_COLOR,
    PLATFORM_SCHEMA,
    LightEntity
)
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string
})


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the Easy Remote connection."""
    # Assign configuration variables.
    host = config[CONF_HOST]

    # Setup connection with lighting software
    er = EasyRemote(host)

    # Add devices
    add_entities(HAEasyRemoteColorwheel(light) for light in er.objects.values())


class HAEasyRemoteColorwheel(LightEntity):
    """Representation of an Easy Remote colorwheel."""

    _attr_color_mode = COLOR_MODE_RGB
    _attr_supported_color_modes = {COLOR_MODE_RGB}
    _attr_supported_features = SUPPORT_COLOR

    def __init__(self, light) -> None:
        """Initialize an Easy Remote colorwheel."""
        self._light = light
        self._id = "easyremote.%i.%i" % (light.page, light.id)
        self._name = light.name
        self._state = None
        self._brightness = 255
        self._rgb = (255, 255, 255)

    @property
    def unique_id(self):
        """Return the ID of this Hue light."""
        return self._id

    @property
    def name(self) -> str:
        """Return the display name of this light."""
        return self._name

    @property
    def is_on(self) -> bool | None:
        """Return true if light is on."""
        return self._state

    @property
    def brightness(self) -> int | None:
        """Return the current brightness."""
        return self._brightness

    @property
    def rgb_color(self) -> tuple | None:
        """Return the current rgb color value."""
        return self._rgb

    def turn_on(self, **kwargs: Any) -> None:
        """Instruct the light to turn on.
        Use the given brightness if present, otherwise use last known value.
        Use the given RGB values if present, otherwise use last known color.
        """
        brightness = kwargs.get(ATTR_BRIGHTNESS, self._brightness)
        r, g, b = kwargs.get(ATTR_RGB_COLOR, self._rgb)

        self._state = True
        self._brightness = brightness
        self._rgb = (r, g, b)

        bm = brightness / 255.0

        self._light.set_rgb(int(r * bm), int(g * bm), int(b * bm))

    def turn_off(self, **kwargs: Any) -> None:
        """Instruct the light to turn off."""
        self._state = False
        self._light.set_rgb(0, 0, 0)
