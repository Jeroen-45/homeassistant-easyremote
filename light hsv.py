"""Platform for light integration."""
from __future__ import annotations

import logging

from pyeasyremote import EasyRemote
import voluptuous as vol

# Import the device class from the component that you want to support
import homeassistant.helpers.config_validation as cv
from homeassistant.components.light import (
    ATTR_HS_COLOR,
    ATTR_BRIGHTNESS,
    COLOR_MODE_HS,
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

    _attr_color_mode = COLOR_MODE_HS
    _attr_supported_color_modes = (COLOR_MODE_HS)

    def __init__(self, light) -> None:
        """Initialize an Easy Remote colorwheel."""
        self._light = light
        self._name = light.name
        self._brightness = None
        self._hs = None

    @property
    def name(self) -> str:
        """Return the display name of this light."""
        return self._name

    @property
    def is_on(self) -> bool | None:
        """Return true if light is on."""
        if self._brightness is None:
            return None
        return self._brightness != 0

    @property
    def brightness(self) -> int | None:
        """Return the current brightness."""
        return self._brightness

    @property
    def hs_color(self) -> tuple | None:
        """Return the current rgb color value."""
        return self._hs

    def turn_on(self, **kwargs: Any) -> None:
        """Instruct the light to turn on.
        Use the given RGB values if present, otherwise use white.
        """
        h, s = kwargs.get(ATTR_HS_COLOR, (255.0, 255.0))
        v = kwargs.get(ATTR_BRIGHTNESS, 255)

        self._hs = (h, s)
        self._brightness = v

        # h /= 255.0
        # s /= 255.0
        v /= 255.0

        self._light.set_hsv(h, s, v)

    def turn_off(self, **kwargs: Any) -> None:
        """Instruct the light to turn off."""
        h, s = self._hs

        self._brightness = 0

        # h /= 255.0
        # s /= 255.0

        self._light.set_hsv(h, s, 0.0)
