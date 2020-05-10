import requests
import re
from pathlib import Path
import json
import sys

BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
END = '\033[0m'
BOLD = '\033[1m'
FAIL=RED+BOLD
UNDERLINE = '\033[4m'

SUCCESS=GREEN+BOLD

class CheckException(Exception):
	def __init__(self, url, msg):
		self.url = url
		super().__init__(msg)

class Configuration:
	def __init__(self, url, title=None):
		self.url = url
		self.title = title

	def check(self):
		r = requests.get(self.url)
		if r.status_code != 200:
			raise CheckException(self.url, f"Not OK: {r.status_code}")
		if self.title is not None:
			title = re.search(r'<title>(.+)</title>', r.text, flags=re.MULTILINE|re.DOTALL)
			if not title:
				raise CheckException(self.url, f"No title found")
			title = title.group(1).strip()
			if not re.match(self.title, title):
				raise CheckException(self.url, f"Invalid title: {title}")

def fail(url, error):
	print(f"[{FAIL}FAIL{END}] {url}\n  {error}")

def ok(url):
	print(f"[{SUCCESS} OK {END}] {url}")

def checking(url):
	print(f"[ .. ] {url}\r", end="")


def load_config(config_path):
	with config_path.open() as configfile:
		config_json = json.load(configfile)
	for config_entry in config_json["services"]:
		yield Configuration(config_entry["url"], title=config_entry.get("title"))

def run():
	failed = False
	config_path = Path.home() / '.config/lauft/config.json'
	for config in load_config(config_path):
		checking(config.url)
		try:
			config.check()
		except CheckException as e:
			fail(config.url, str(e))
			failed = True
		except Exception as e:
			fail(config.url, str(e))
			failed = True
		else:
			ok(config.url)

	if failed:
		sys.exit(1)

if __name__ == "__main__":
	run()