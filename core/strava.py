import os
import time
import swagger_client
from . import ratelimiter

_STRAVA_DEFAULT_PERIOD_SEC = 15 * 60
_STRAVA_DEFAULT_MAX_CALLS = 600


class Strava:
	def __init__(
		self,
		access_token=os.environ['STRAVA_ACCESS_TOKEN'],
		rate_limiter=ratelimiter.RateLimiter(_STRAVA_DEFAULT_MAX_CALLS, _STRAVA_DEFAULT_PERIOD_SEC)):

		configuration = swagger_client.Configuration()
		configuration.access_token = access_token
		self.uploads_api = swagger_client.UploadsApi(swagger_client.ApiClient(configuration))
		self.rate_limiter = rate_limiter

	def upload_activity(self, export, description):
		self.rate_limiter.limit()
		response = self.uploads_api.create_upload_with_http_info(
			file=export.Filepath,
			name=export.Name,
			description=description,
			data_type=export.Type)

