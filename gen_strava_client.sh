TMP="./dep"

mkdir -p "$TMP"

wget -nc http://central.maven.org/maven2/io/swagger/swagger-codegen-cli/2.4.9/swagger-codegen-cli-2.4.9.jar \
	-O "$TMP/swagger-codegen-cli.jar"

java -jar $(echo "$TMP/swagger-codegen-cli.jar") generate \
    -i https://developers.strava.com/swagger/swagger.json                \
    -l python \
    -o ./swagger

