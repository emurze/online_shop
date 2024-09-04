up:
	docker compose up --build

down:
	docker compose down

test:
	docker exec api pytest

# up               = "$DC up --build"
# down             = "$DC down -v"
# reup             = { shell = "poe down && poe up" }
# test             = "$EXEC $APP_CONTAINER pytest"
# shell            = "$EXEC $APP_CONTAINER /bin/bash"
# db_shell         = "$EXEC $DB_CONTAINER /bin/bash"