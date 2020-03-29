. .env

STRAVA_AUTH_URL="http://www.strava.com/oauth/authorize?client_id=$STRAVA_CLIENT_ID&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=activity:write"

echo "Visit the following URL and login. After you login, your will be redirected to a page that will not load. This is expected"
echo "$STRAVA_AUTH_URL"
read -ep "Provide \`code\` from URL you were redirected to: " STRAVA_CODE


STRAVA_ACCESS_TOKEN=$(curl -s -X POST https://www.strava.com/oauth/token \
	-F client_id="$STRAVA_CLIENT_ID" \
	-F client_secret="$STRAVA_CLIENT_SECRET" \
	-F code="$STRAVA_CODE" \
	-F grant_type=authorization_code | jq -r '.access_token')

echo "Strava Token: $STRAVA_ACCESS_TOKEN"
