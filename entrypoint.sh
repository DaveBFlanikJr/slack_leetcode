# TODO: Improve and validate
if [ "$1" == "db:drop" ]; then
    python manage_db.py drop
elif [ "$1" == "db:init" ]; then
    python manage_db.py init
elif [ "$1" == "db:reset" ]; then
    python manage_db.py reset
else
    echo "Invalid command. Available commands are db:drop, db:init, and db:reset."
fi