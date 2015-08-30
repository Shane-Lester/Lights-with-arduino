** Raspberry Pi based lights control system

- uses serial protocol to control Arduino via USB

- Arduino runs rcswitch library to control lights

- Lights are 433mHz switches from Maplin with the control hacked

- IR control of lights monitored by Arduino

- Pi runs webiopi server to provide web interface

- Able to control lights via time (heavily base on Eric Ptak's example)

- Pyephem calculates sun rise and sunset to allow year round automation

- option to have lights on early in morning (until sunrise)

- option to have randomness to lights to make it look like someone is in the house when you are away

- GUI updates even if the lights are controlled by the IR

- code is messy as this was only my second hardware/ software project
