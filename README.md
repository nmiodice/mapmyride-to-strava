# Getting Started
 * Log into Strava
 * Create a [Strava Application](https://www.strava.com/settings/api)
 * Create an access token with permissions to the `activity:write` scope by executing the following:
```bash
./gen_strava_token.sh
```
 * You may need to re-generate the Strava SDK by executing the following:
```bash
./gen_strava_client.sh
```
 * Configure a `.env` file. Be sure to use the access token created by running `./gen_strava_token.sh` and not the default read-only token that is created by default. 
```bash
cp .env.template .env
vim .env
```
 * Run application
```bash
python3 main.py
```