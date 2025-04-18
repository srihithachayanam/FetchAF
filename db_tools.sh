#!/bin/bash
# Database backup and restore utilities for FetchAF

# Load environment variables
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo "Error: .env file not found!"
    exit 1
fi

# Function to backup the database
backup_db() {
    echo "Backing up database ${DB_NAME}..."
    timestamp=$(date +"%Y%m%d_%H%M%S")
    docker exec -t fetchaf-postgres pg_dump -U ${DB_USER} -d ${DB_NAME} > backup_${timestamp}.sql
    if [ $? -eq 0 ]; then
        echo "Backup created: backup_${timestamp}.sql"
    else
        echo "Error: Database backup failed!"
    fi
}

# Function to restore the database
restore_db() {
    if [ -z "$1" ]; then
        echo "Error: No backup file specified!"
        echo "Usage: $0 restore <backup_file.sql>"
        exit 1
    fi

    if [ ! -f "$1" ]; then
        echo "Error: Backup file '$1' not found!"
        exit 1
    fi

    echo "Restoring database ${DB_NAME} from $1..."
    cat "$1" | docker exec -i fetchaf-postgres psql -U ${DB_USER} -d ${DB_NAME}
    if [ $? -eq 0 ]; then
        echo "Database restored successfully!"
    else
        echo "Error: Database restore failed!"
    fi
}

# Function to display help
show_help() {
    echo "FetchAF Database Tools"
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  backup                Create a database backup"
    echo "  restore <file.sql>    Restore database from backup file"
    echo "  help                  Show this help message"
}

# Main command dispatcher
case "$1" in
    backup)
        backup_db
        ;;
    restore)
        restore_db "$2"
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