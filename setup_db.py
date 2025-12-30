"""
Database setup script for PostgreSQL.
"""
import subprocess
import sys
import os


def run_command(command: str, description: str) -> bool:
    """
    Run a shell command and handle errors.
    
    Args:
        command: Command to run
        description: Description of what the command does
        
    Returns:
        bool: True if successful, False otherwise
    """
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"   Error: {e.stderr.strip()}")
        return False


def main():
    """Main function to set up the PostgreSQL database."""
    print("🚀 Setting up PostgreSQL database for Cadot User Management API")
    print("=" * 60)
    
    # Check if PostgreSQL is running
    if not run_command("pg_isready -h localhost", "Checking PostgreSQL connection"):
        print("\n❌ PostgreSQL is not running or not accessible.")
        print("   Please start PostgreSQL and try again.")
        sys.exit(1)
    
    # Create database
    if not run_command("createdb cadot_user", "Creating database 'cadot_user'"):
        print("\n⚠️  Database 'cadot_user' might already exist or there was an error.")
        print("   Continuing with schema creation...")
    
    # Create schema
    if not run_command(
        'psql -d cadot_user -c "CREATE SCHEMA IF NOT EXISTS cadot;"',
        "Creating schema 'cadot'"
    ):
        print("\n❌ Failed to create schema 'cadot'.")
        sys.exit(1)
    
    # Grant permissions (optional, adjust as needed)
    if not run_command(
        'psql -d cadot_user -c "GRANT ALL ON SCHEMA cadot TO PUBLIC;"',
        "Setting schema permissions"
    ):
        print("\n⚠️  Failed to set schema permissions. This might not be critical.")
    
    print("\n" + "=" * 60)
    print("✅ Database setup completed successfully!")
    print("\n📋 Next steps:")
    print("   1. Install dependencies: pip install -r requirements.txt")
    print("   2. Initialize the application: python start.py")
    print("   3. Run the application: uvicorn main:app --reload")
    print("\n🌐 The application will be available at: http://localhost:8000")
    print("📚 API documentation will be at: http://localhost:8000/docs")


if __name__ == "__main__":
    main()
