#!/bin/bash

echo remove any old version
rm ~/.local/share/gedit/plugins/mdshortcuts.*

echo copy plugin files
cp mdshortcuts.plugin ~/.local/share/gedit/plugins/
cp mdshortcuts.py ~/.local/share/gedit/plugins/
