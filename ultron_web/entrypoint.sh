#!bin/sh

### WAIT FOR MYSQL ###
# RETRIES=7
# while [ "$RETRIES" -gt 0 ]
# do
#     echo "Waiting for MySQL Server, $RETRIES remaining atempts..."
#     RETRIES=$((RETRIES-1))
#     MYSQL_STATUS="$(nc -z database 3306)"
#     MYSQL_EXIT=$(echo $?)
#     echo "MySQL Status: $MYSQL_EXIT - $MYSQL_STATUS"
#     if [ "$MYSQL_EXIT" = "0" ]; then
#         RETRIES=0
#     else
#         sleep 5
#     fi
# done

if [ ${MULTISTAGE} = "LOCAL" ]; then
     while :
     do
        clear &&
        echo "MULTISTAGE: LOCAL. Access container with docker exec -it ultron_web zsh"
        echo "For outher stage change MULTISTAGE enviroment variable:"
        echo "- For LOCAL stage, use LOCAL"
        echo "- For DEVELPMENT stage, use STAG"
        echo "- For STAGE stage, use STAG"
        echo "- For PRODUCTION stage, use PROD"
        echo "Ctr+C for exit"
        sleep 30
    done
else
    # DJANGO MIGRATE AND COLLECT STATIC FILES ###
    poetry run ./manage.py migrate &&
    poetry run ./manage.py collectstatic --noinput &&

    # START WEBSERVER ###
    if [ ${MULTISTAGE} = "DEV" ] || [ ${MULTISTAGE} = "STAG" ]; then
        gunicorn -D -b 0.0.0.0:80 -w 2 -p /tmp/gunicorn_ultron.pid selectrh.wsgi:application &&
        poetry run ./manage.py runserver 0:8000
    elif [ ${MULTISTAGE} = "PROD" ]; then
        gunicorn -b 0.0.0.0:80 -w ${GUNICORN_WORKERS} -p /tmp/gunicorn_ultron.pid selectrh.wsgi:application
    else
        echo "Not server started for multstage: ${MULTISTAGE}"
    fi
fi
