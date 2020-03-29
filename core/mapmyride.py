import os
import requests
from . import ratelimiter
from pathlib import Path
from collections import namedtuple
from http.cookies import SimpleCookie

MapMyRideExport = namedtuple(
	'MapMyRideExport',
	['Name', 'Filepath', 'Type']
)

class MapMyRide:
	def __init__(
		self,
		cookie=os.environ['MAP_MY_RIDE_COOKIE'],
		rate_limiter=ratelimiter.RateLimiter(4, 1)):

		cookies = SimpleCookie()
		cookies.load(cookie)
		self.cookies = {}
		for key, morsel in cookies.items():
		    self.cookies[key] = morsel.value

		self.rate_limiter = rate_limiter

	def get_workout_export_urls(self, export_type):
		self.rate_limiter.limit()

		r = requests.get('https://www.mapmyride.com/workout/export/csv', cookies=self.cookies)
		export_urls = []

		is_first = True
		for line in r.text.split('\n'):
			if is_first:
				is_first = False
				continue

			parts = line.split(',')
			if len(parts) > 1:
				export_urls.append(self._workout_url_to_export_url(parts[-1], export_type))

		return export_urls

	def _workout_url_to_export_url(self, url, export_type):
		parts = url.strip().split('/')
		parts.insert(-1, 'export')
		parts.append(export_type)
		return '/'.join(parts)

	def download_export(self, export_url, output_dir, export_type):
		export = self._get_from_local(export_url, output_dir, export_type)
		if export is not None:
			return export
		return self._download_export(export_url, output_dir, export_type)

	def _get_from_local(self, export_url, output_dir, export_type):
		self.rate_limiter.limit()
		r = requests.head(export_url, cookies=self.cookies)
		r.raise_for_status()
		workout_name = self._request_to_workout_name(r)
		filepath = Path(output_dir) / workout_name.replace('/', '-')

		if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
			return MapMyRideExport(workout_name, filepath, export_type)
		return None

	def _download_export(self, export_url, output_dir, export_type):
		self.rate_limiter.limit()
		r = requests.get(export_url, cookies=self.cookies)
		r.raise_for_status()
		workout_name = self._request_to_workout_name(r)
		filepath = Path(output_dir) / workout_name.replace('/', '-')

		file = open(filepath, "w")
		file.write(r.text)
		file.close()

		return MapMyRideExport(
			'.'.join(workout_name.split('.')[:-1]),
			filepath,
			export_type)

	def _request_to_workout_name(self, r):
		content_disposition = r.headers['content-disposition']
		return content_disposition.split('=')[-1].strip('"')

	
