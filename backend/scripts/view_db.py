"""
Database viewer - Simple tool to view AiKO database contents
"""

import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import get_db_context, User, ChatSession, Message
from sqlalchemy import func, desc

def print_header(title):
    """Print section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def view_users():
    """View all users"""
    print_header("👥 USERS")
    
    with get_db_context() as db:
        users = db.query(User).all()
        
        if not users:
            print("No users found.")
            return
        
        for user in users:
            print(f"\nID: {user.id}")
            print(f"Username: {user.username}")
            print(f"Created: {user.created_at}")
            print(f"Sessions: {len(user.sessions)}")

def view_sessions():
    """View active sessions"""
    print_header("📅 ACTIVE SESSIONS")
    
    with get_db_context() as db:
        sessions = db.query(ChatSession).filter(
            ChatSession.is_active == True
        ).order_by(desc(ChatSession.started_at)).all()
        
        if not sessions:
            print("No active sessions.")
            return
        
        for session in sessions:
            now = datetime.now()
            time_left = (session.expires_at - now).total_seconds() / 3600
            
            print(f"\nSession ID: {session.id}")
            print(f"User: {session.user.username}")
            print(f"Date: {session.session_date}")
            print(f"Started: {session.started_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Expires: {session.expires_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Time remaining: {time_left:.1f} hours")
            print(f"Messages: {session.message_count}")
            print(f"Active: {'✅' if session.is_active else '❌'}")

def view_recent_messages(limit=20):
    """View recent messages"""
    print_header(f"💬 RECENT MESSAGES (Last {limit})")
    
    with get_db_context() as db:
        messages = db.query(Message).order_by(
            desc(Message.timestamp)
        ).limit(limit).all()
        
        if not messages:
            print("No messages found.")
            return
        
        # Reverse to show chronological order
        messages = list(reversed(messages))
        
        for msg in messages:
            timestamp = msg.timestamp.strftime('%H:%M:%S')
            role_emoji = "👤" if msg.role == "user" else "🤖"
            
            # Truncate long messages
            content = msg.content
            if len(content) > 80:
                content = content[:77] + "..."
            
            print(f"\n[{timestamp}] {role_emoji} {msg.role.upper()}")
            print(f"  {content}")

def view_statistics():
    """View database statistics"""
    print_header("📊 STATISTICS")
    
    with get_db_context() as db:
        # Count users
        user_count = db.query(User).count()
        
        # Count sessions
        total_sessions = db.query(ChatSession).count()
        active_sessions = db.query(ChatSession).filter(
            ChatSession.is_active == True
        ).count()
        
        # Count messages
        total_messages = db.query(Message).count()
        
        # Messages today
        from datetime import date
        today_sessions = db.query(ChatSession).filter(
            ChatSession.session_date == date.today()
        ).all()
        
        messages_today = sum(s.message_count for s in today_sessions)
        
        # Average messages per session
        if total_sessions > 0:
            avg_messages = total_messages / total_sessions
        else:
            avg_messages = 0
        
        print(f"\n{'Metric':<30} {'Value':>10}")
        print("-"*42)
        print(f"{'Total Users':<30} {user_count:>10}")
        print(f"{'Total Sessions':<30} {total_sessions:>10}")
        print(f"{'Active Sessions':<30} {active_sessions:>10}")
        print(f"{'Total Messages':<30} {total_messages:>10}")
        print(f"{'Messages Today':<30} {messages_today:>10}")
        print(f"{'Avg Messages/Session':<30} {avg_messages:>10.1f}")

def view_session_details(session_id=None, username=None):
    """View detailed session information"""
    print_header("🔍 SESSION DETAILS")
    
    with get_db_context() as db:
        if session_id:
            session = db.query(ChatSession).filter(
                ChatSession.id == session_id
            ).first()
        elif username:
            user = db.query(User).filter(User.username == username).first()
            if not user:
                print(f"User '{username}' not found.")
                return
            session = db.query(ChatSession).filter(
                ChatSession.user_id == user.id,
                ChatSession.is_active == True
            ).first()
        else:
            print("Provide session_id or username")
            return
        
        if not session:
            print("Session not found.")
            return
        
        print(f"\nSession ID: {session.id}")
        print(f"User: {session.user.username}")
        print(f"Date: {session.session_date}")
        print(f"Started: {session.started_at}")
        print(f"Expires: {session.expires_at}")
        print(f"Message Count: {session.message_count}")
        print(f"Active: {session.is_active}")
        
        print("\n" + "-"*60)
        print("MESSAGES:")
        print("-"*60)
        
        messages = db.query(Message).filter(
            Message.session_id == session.id
        ).order_by(Message.timestamp).all()
        
        for msg in messages:
            timestamp = msg.timestamp.strftime('%H:%M:%S')
            role_emoji = "👤" if msg.role == "user" else "🤖"
            print(f"\n[{timestamp}] {role_emoji} {msg.role.upper()}")
            print(f"  {msg.content}")

def interactive_menu():
    """Interactive menu"""
    while True:
        print("\n" + "="*60)
        print("  🗄️  AiKO Database Viewer")
        print("="*60)
        print("\n1. View Users")
        print("2. View Active Sessions")
        print("3. View Recent Messages")
        print("4. View Statistics")
        print("5. View Session Details (by username)")
        print("6. View All")
        print("0. Exit")
        
        choice = input("\nSelect option (0-6): ").strip()
        
        if choice == "1":
            view_users()
        elif choice == "2":
            view_sessions()
        elif choice == "3":
            limit = input("How many messages? (default 20): ").strip()
            limit = int(limit) if limit.isdigit() else 20
            view_recent_messages(limit)
        elif choice == "4":
            view_statistics()
        elif choice == "5":
            username = input("Enter username (default: default_user): ").strip()
            username = username if username else "default_user"
            view_session_details(username=username)
        elif choice == "6":
            view_statistics()
            view_users()
            view_sessions()
            view_recent_messages(20)
        elif choice == "0":
            print("\n👋 Bye!")
            break
        else:
            print("❌ Invalid option!")
        
        input("\nPress Enter to continue...")

def main():
    """Main function"""
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "users":
            view_users()
        elif command == "sessions":
            view_sessions()
        elif command == "messages":
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 20
            view_recent_messages(limit)
        elif command == "stats":
            view_statistics()
        elif command == "session":
            if len(sys.argv) > 2:
                view_session_details(username=sys.argv[2])
            else:
                print("Usage: python view_db.py session <username>")
        elif command == "all":
            view_statistics()
            view_users()
            view_sessions()
            view_recent_messages(20)
        else:
            print("Unknown command!")
            print("\nUsage:")
            print("  python view_db.py              # Interactive menu")
            print("  python view_db.py users        # View users")
            print("  python view_db.py sessions     # View sessions")
            print("  python view_db.py messages [n] # View n recent messages")
            print("  python view_db.py stats        # View statistics")
            print("  python view_db.py session <username>  # View session details")
            print("  python view_db.py all          # View everything")
    else:
        # Interactive mode
        interactive_menu()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Bye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
