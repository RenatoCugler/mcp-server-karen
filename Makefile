.PHONY: help build test run clean install

# Default target - show help
help:
	@echo "🎓 Karen MCP Server - Makefile Commands"
	@echo "========================================"
	@echo ""
	@echo "🐳 Docker-First Workflow (Recommended):"
	@echo "  make build    - Build the Docker image"
	@echo "  make test     - Run tests in Docker (auto-loads .env if present)"
	@echo "  make run      - Run server in Docker (auto-loads .env if present)"
	@echo "  make validate - Validate Python syntax in Docker"
	@echo "  make all      - Build, validate, and test"
	@echo "  make clean    - Remove Docker image"
	@echo ""
	@echo "🐍 Local Development (Requires Python 3.11+):"
	@echo "  make install  - Install Python dependencies locally"
	@echo ""
	@echo "💡 Quick Start:"
	@echo "  make build    # Build the Docker image"
	@echo "  make test     # Run tests to verify everything works"
	@echo ""
	@echo "🔑 API Key Testing:"
	@echo "  1. Copy .env.example to .env"
	@echo "  2. Add your API keys to .env"
	@echo "  3. Run 'make test' - it will auto-load your .env file"
	@echo ""
	@echo "📦 All operations use Docker - no local Python 3.11+ needed!"
	@echo ""

# Install Python dependencies
install:
	@echo "📦 Installing Python dependencies..."
	pip3 install -r requirements.txt
	@echo "✅ Dependencies installed!"

# Build the Docker image
build:
	@echo "🏗️  Building Karen MCP Server Docker image..."
	docker build -t karen-mcp-server:latest .
	@echo "✅ Build complete!"

# Run tests in Docker
test:
	@echo "🧪 Running tests in Docker..."
	@if [ -f .env ]; then \
		echo "📝 Found .env file - mounting for API key testing"; \
		docker run --rm --env-file .env karen-mcp-server:latest python test_karen_server.py; \
	else \
		echo "💡 No .env file found - tests will use fallback responses"; \
		echo "   Create .env from .env.example to test with real APIs"; \
		docker run --rm karen-mcp-server:latest python test_karen_server.py; \
	fi
	@echo "✅ Tests complete!"

# Run the server locally in Docker (useful for debugging)
run:
	@echo "🚀 Running Karen MCP Server in stdio mode (Docker)..."
	@echo "💡 Send JSON-RPC messages to test the server"
	@echo "   Press Ctrl+C to stop"
	@if [ -f .env ]; then \
		echo "📝 Loading API keys from .env file"; \
		docker run --rm -i --env-file .env karen-mcp-server:latest; \
	else \
		docker run --rm -i karen-mcp-server:latest; \
	fi

# Validate Python syntax in Docker
validate:
	@echo "🔍 Validating Python syntax in Docker..."
	docker run --rm karen-mcp-server:latest python -m py_compile karen_server.py
	docker run --rm karen-mcp-server:latest python -m py_compile test_karen_server.py
	@echo "✅ Syntax validation passed!"

# Clean up Docker image
clean:
	@echo "🧹 Cleaning up..."
	docker rmi karen-mcp-server:latest || true
	@echo "✅ Cleanup complete!"

# Run all checks (Docker-based workflow)
all: build validate test
	@echo "✨ All checks passed!"
