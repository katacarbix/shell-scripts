#!/usr/bin/env python3

# Set colors of RGB devices in my room.
# by katacarbix
# do whatever you want

import sys, math, json, random
from colour import Color
import openrazer.client
import yeelight as yee

brightness = 20 # Default brightness of lightbulbs (1-100)

def hsl_to_hsv(h, s, l):
	v = (2*l + s*(1-math.fabs(2*l-1)))/2
	s = 2*(v-l)/v
	return h, s, v

# Yeelight RGB bulbs
def bulbs(colors):
	bulbs = yee.discover_bulbs()
	for b in bulbs:
		c = Color(random.choice(colors))

		c.saturation = 0.15
		c.luminance = 0.5

		c = hsl_to_hsv(c.hue, c.saturation, c.luminance)
		c = (c[0]*360, c[1]*100, c[2]*brightness)

		yee.Bulb(b['ip']).set_hsv(*c)

# Razer keyboards
def keeb(colors):
	c = Color(random.choice(colors))

	c.saturation = 1
	c.luminance = 0.65

	rgb = [int(x*255) for x in c.rgb]
	devices = openrazer.client.DeviceManager().devices
	for d in devices:
		d.fx.static(*rgb)

if __name__ == "__main__":
	colors = []
	if len(sys.argv) > 1:
		colors = sys.argv[1:]
	else:
		try:
			with open('/home/reese/.cache/wal/colors.json', 'r') as f:
				obj = json.loads(f.read())
				colors = list(obj['colors'].values())[1:7]
		except e:
			print("there was an error")
			print(e)

	keeb(colors)
	# bulbs(colors)
