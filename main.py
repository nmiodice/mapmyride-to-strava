import sys
import os
sys.path.append(os.path.abspath('swagger'))

import concurrent.futures
import queue
import settings
import core.strava
import core.mapmyride

SKIP_TO=180

def main():
	export_type = 'tcx'
	q = queue.Queue()

	with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
		mmy_export_future = executor.submit(get_mmy_exports, q, export_type)
		strava_upload_future = executor.submit(strava_upload, q)

		# block until future is done
		print(mmy_export_future.result())
		print(strava_upload_future.result())


def strava_upload(queue):
	s = core.strava.Strava()
	i = 0
	while True:
		i = i + 1
		if i < SKIP_TO:
			continue
		export = queue.get()

		try:
			s.upload_activity(export, export.Name + ' (Imported from MapMyRide)')
		except Exception as e:
			if 'duplicate' in str(e).lower():
				print('...upload {0} skipped because it was a duplicate'.format(i))
				continue
			elif 'file is empty' in str(e).lower():
				print('...upload {0} skipped because it was a empty'.format(i))
				continue
			else:
				raise
		print('uploaded export ' + str(i))

def get_mmy_exports(queue, export_type):
	m = core.mapmyride.MapMyRide()
	urls = m.get_workout_export_urls(export_type)
	i = 0
	for url in urls:
		i = i + 1
		if i < SKIP_TO:
			continue
		log_prefix = '{0}/{1}: '.format(i, len(urls))
		export = m.download_export(url, 'data', export_type)
		print(log_prefix + 'got ' + str(export), flush=True)
		queue.put(export, False)


if __name__ == '__main__':
	main()