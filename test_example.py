from urllib import response

import cooltest

import time, pexpect, wexpect


def test_math():
	print("  testing the ground...")
	if 2 + 2 != 4:
		cooltest.fail("Non-standard math domain!")
	print("  all good!")


def test_weather(sky, rain):
	if time.localtime().tm_hour < 8:
		cooltest.skip("Too early, where's my coffee?")
	if rain != "no" and sky == "blue":
		cooltest.fail("The sky is blue, but it is raining!")
	print(f"The sky is {sky}, raining: {rain}")


def api_activate(addr, path, value):
	"""simple code to call StreamSDK via HTTP/Thrift API"""
	...


"""def test_ping(dut_ip):
	cooltest.skipif(not dut_ip, "No device to test on!")
	ping = wexpect.spawn(f"ping -c 3 {dut_ip}")
	found = ping.expect(["3 received", pexpect.TIMEOUT, pexpect.exceptions.EOF], timeout=5)
	cooltest.failif(found != 0, f"No ping to the device '{dut_ip}'") """


"""def test_play(dut_ip):
	cooltest.skipif(not dut_ip, "No device to test on!")
	#response = api_activate(dut_ip, < a StreamSDK request to play >)
	cooltest.failif(not response or int(response) < 0, "Failed to play")
	print("  playing...")
	time.sleep(5)
	api_activate(dut_ip, 'player:player/control', {"control": "stop"})
	print("  stopped.")"""