#!/bin/env bash
set -e

# Set up the create tables migration before starting server
echo "Run apply migration"
alembic upgrade head
echo "Migration applied"

# Running CMD command
exec "$@"
