import numpy as np
from PIL import ImageGrab
import requests
from time import sleep

step = 10 # how many pixels to skip in both x and y direction when sampling colors
bounds = (0, 0, 1920, 1080) # bounds of the screenshot (tlx, tly, brx, bry)
serverAddress = "http://192.168.123.165"
colorScale = 0.8

oldAverage = (0, 0, 0)

while True:
	grab = ImageGrab.grab(bbox=bounds)

	img = np.frombuffer(grab.tobytes(), dtype=np.uint8)
	img = img.reshape((-1, 3))

	average = [colorScale * val for val in img.mean(axis=0)]

	diffR = average[0] - oldAverage[0]
	diffG = average[1] - oldAverage[1]
	diffB = average[2] - oldAverage[2]
	if diffR < -1 or diffR > 1 or diffG < -1 or diffG > 1 or diffB < -1 or diffB > 1:
		oldAverage = average

		# jank don't flashbang
		# todo: convert to hsv and adjust v
		average = [min(val, 130) for val in average]

		# todo: send over serial?
		requests.get(f"{serverAddress}/cm?cmnd=color {average[0]},{average[1]},{average[2]}")

	# sleep(0.1)