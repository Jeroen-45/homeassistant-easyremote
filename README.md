# Easy Remote integration for Home Assistant
This integration makes controls for various DMX lighting softwares that are
available through the use of the Easy Remote app available as lights in
Home Assistant. This library was only tested using the Daslight DVC4 software,
but should work for other software too.
Please let me know if you have tested the library with other software.

For now, only color wheels are supported. If you need support for other
Easy Remote controls, please open an issue.

**NOTE: I am not affiliated with LIGHTINGSOFT, Daslight, Nicolaudie Group or
any other related companies. This is an unofficial piece of software just for
tinkering with Easy Remote in combination with Home Assistant.**

## Installation
Copy the contents of this repository to
`<config_dir>/custom_components/example_light/`.

Add the following entry in your `configuration.yaml`:
```
light:
  - platform: easyremote
    host: HOST_HERE
```