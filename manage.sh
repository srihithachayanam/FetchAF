#!/bin/bash
# Management script for FetchAF Docker environment

# Function to start Docker containers
start() {
    echo "Starting FetchAF containers..."
    docker-compose up -d
    echo "Containers started! Access the application at http://localhost:8501"
}

# Function to stop Docker containers
stop() {
    echo "Stopping FetchAF containers..."
    docker-compose down
    echo "Containers stopped!"
}

# Function to restart Docker containers
restart() {
    echo "Restarting FetchAF containers..."
    docker-compose down
    docker-compose up -d
    echo "Containers restarted! Access the application at http://localhost:8501"
}

# Function to show container logs
logs() {
    if [ "$1" == "app" ]; then
        docker-compose logs -f app
    elif [ "$1" == "db" ]; then
        docker-compose logs -f db
    else
        docker-compose logs -f
    fi
}

# Function to build/rebuild containers
build() {
    echo "Building FetchAF containers..."
    docker-compose build
    echo "Build complete! Run './manage.sh start' to start the containers."
}

# Function to display container status
status() {
    echo "FetchAF Container Status:"
    docker-compose ps
}

# Function to display help
show_help() {
    echo "FetchAF Management Script"
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  start              Start all containers"
    echo "  stop               Stop all containers"
    echo "  restart            Restart all containers"
    echo "  logs [app|db]      Show logs (optionally for specific service)"
    echo "  build              (Re)build containers"
    echo "  status             Show container status"
    echo "  help               Show this help message"
}

# Main command dispatcher
case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    logs)
        logs "$2"
        ;;
    build)
        build
        ;;
    status)
        status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        show_help
        exit 1
        ;;
esac

exit 0 