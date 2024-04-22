#!/bin/bash

DIR="/Volumes/RPI-RP2"
if [ -d "$DIR" ]; then
  echo "Installing firmwire to pico in ${DIR}..."
  cd /tmp
  wget https://downloads.circuitpython.org/bin/raspberry_pi_pico/en_US/adafruit-circuitpython-raspberry_pi_pico-en_US-8.0.4.uf2
  cp adafruit-circuitpython-raspberry_pi_pico-en_US-8.0.4.uf2 /Volumes/RPI-RP2
  echo "Sleeping 40 seconds for firmware to install"
  cd -
  sleep 40
fi

DIR="/Volumes/CIRCUITPY"
if [ -d "$DIR" ]; then
  echo "Install demo software in ${DIR}..."
  cd src
  cp -r lib /Volumes/CIRCUITPY
  cp *.py /Volumes/CIRCUITPY
  diskutil unmount /Volumes/CIRCUITPY
  echo "done"
fi

DIR="/Volumes/MICROPICO"
if [ -d "$DIR" ]; then
  echo "Updating demo software in ${DIR}..."
  cd src
  cp -r lib /Volumes/MICROPICO
  cp *.py /Volumes/MICROPICO
  echo "done"
fi
