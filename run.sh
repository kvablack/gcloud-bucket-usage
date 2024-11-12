trap 'kill 0' INT TERM

while true
do
    if test -d data_live; then
        echo "Killing..."
        kill $serverPID
        echo "Starting server..."
        gunicorn "app:app" -w 4 --preload -b 0.0.0.0 &
        serverPID=$!
        sleep 1d
    fi

    echo "Collecting data..."
    rm -rf data
    bash collect_usage.sh
    rm -rf data_live
    mv data data_live
done
