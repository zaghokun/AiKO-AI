"""
Database initialization script

Run this script to create all database tables
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import init_db, drop_db
from app.config import settings

def main():
    """Initialize database"""
    print("="*60)
    print("🗄️  AiKO Database Initialization")
    print("="*60)
    print(f"\nDatabase URL: {settings.database_url}")
    print(f"Session Duration: {settings.session_duration_hours} hours")
    print(f"Max Messages per Session: {settings.max_messages_per_session}")
    
    print("\n" + "-"*60)
    choice = input("Initialize database? This will create all tables. (y/n): ").strip().lower()
    
    if choice != 'y':
        print("❌ Cancelled.")
        return
    
    try:
        init_db()
        print("\n✅ Database initialized successfully!")
        print("\n📊 Tables created:")
        print("  - users")
        print("  - chat_sessions")
        print("  - messages")
        print("\n🚀 You can now start the server!")
        
    except Exception as e:
        print(f"\n❌ Error initializing database: {e}")
        print("\n💡 Make sure:")
        print("  1. PostgreSQL is running (docker-compose up -d)")
        print("  2. .env file has correct DATABASE_URL")
        print("  3. Database credentials are correct")
        return 1
    
    return 0

def reset():
    """Reset database - DROP and recreate all tables"""
    print("="*60)
    print("⚠️  RESET DATABASE - WARNING!")
    print("="*60)
    print("\nThis will DELETE ALL DATA and recreate tables.")
    print(f"Database: {settings.database_url}")
    
    print("\n" + "-"*60)
    confirm = input("Are you SURE? Type 'DELETE ALL DATA' to confirm: ").strip()
    
    if confirm != "DELETE ALL DATA":
        print("❌ Cancelled.")
        return
    
    try:
        print("\n🗑️  Dropping all tables...")
        drop_db()
        
        print("📝 Creating fresh tables...")
        init_db()
        
        print("\n✅ Database reset complete!")
        
    except Exception as e:
        print(f"\n❌ Error resetting database: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        sys.exit(reset())
    else:
        sys.exit(main())
