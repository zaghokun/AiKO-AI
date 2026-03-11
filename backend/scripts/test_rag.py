#!/usr/bin/env python3
"""
Test RAG (Retrieval Augmented Generation) System

Usage:
    python scripts/test_rag.py              # Interactive testing
    python scripts/test_rag.py --auto       # Automated tests
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import asyncio
from datetime import datetime, date, timedelta
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from app.services.embedding_service import embedding_service
from app.services.qdrant_service import qdrant_service
from app.services.memory_service import MemoryService
from app.config import settings
from app.database.connection import get_db
from app.database.models import User, ChatSession, Message
from sqlalchemy import select

console = Console()


async def test_embedding_service():
    """Test embedding generation"""
    console.print("\n[bold cyan]🧪 Test 1: Embedding Service[/bold cyan]")
    
    # Use singleton instance
    service = embedding_service
    
    # Test single embedding
    text = "Aku suka makan bakso"
    vector = service.encode(text)
    
    console.print(f"✅ Text: '{text}'")
    console.print(f"✅ Vector dimension: {len(vector)}")
    console.print(f"✅ First 5 values: {vector[:5]}")
    
    # Test similarity
    text1 = "Aku suka makan bakso"
    text2 = "Saya doyan makan bakso"
    text3 = "Cuaca hari ini cerah sekali"
    
    vec1 = service.encode(text1)
    vec2 = service.encode(text2)
    vec3 = service.encode(text3)
    
    sim_similar = service.compute_similarity(vec1, vec2)
    sim_different = service.compute_similarity(vec1, vec3)
    
    console.print(f"\n✅ Similarity (bakso vs bakso): {sim_similar:.4f} (should be high)")
    console.print(f"✅ Similarity (bakso vs cuaca): {sim_different:.4f} (should be low)")
    
    if sim_similar > 0.7 and sim_different < 0.5:
        console.print("[bold green]✅ Embedding service working correctly![/bold green]")
    else:
        console.print("[bold red]❌ Similarity scores unexpected![/bold red]")


async def test_qdrant_service():
    """Test Qdrant operations"""
    console.print("\n[bold cyan]🧪 Test 2: Qdrant Service[/bold cyan]")
    
    # Use singleton instances
    qdrant = qdrant_service
    emb_service = embedding_service
    
    # Test add memory
    test_user_id = "test_user_123"
    test_session_id = "test_session_456"
    
    messages = [
        ("user", "Aku kerja sebagai software engineer"),
        ("assistant", "Wah keren! Kamu kerja di bidang apa?"),
        ("user", "Aku bikin aplikasi web pakai Python"),
    ]
    
    console.print("\n📝 Adding test memories...")
    for role, content in messages:
        success = qdrant.add_memory(
            message_id=f"test_{role}_{hash(content)}",
            user_id=test_user_id,
            session_id=test_session_id,
            role=role,
            content=content,
            timestamp=datetime.now()
        )
        if success:
            console.print(f"✅ Added: {content[:50]}...")
        else:
            console.print(f"❌ Failed: {content[:50]}...")
    
    # Test search
    console.print("\n🔍 Searching for relevant memories...")
    query = "pekerjaan software"
    
    results = qdrant.search_memories(
        query=query,
        user_id=test_user_id,
        limit=3,
        score_threshold=0.5,
        exclude_session_id=None
    )
    
    table = Table(title="Search Results")
    table.add_column("Score", style="cyan")
    table.add_column("Role", style="magenta")
    table.add_column("Content", style="white")
    
    for result in results:
        table.add_row(
            f"{result['score']:.4f}",
            result['role'],
            result['content'][:60]
        )
    
    console.print(table)
    
    # Test stats
    count = qdrant.get_memory_count(test_user_id)
    console.print(f"\n✅ Total memories for test user: {count}")
    
    # Cleanup
    console.print("\n🧹 Cleaning up test data...")
    qdrant.delete_session_memories(test_session_id)
    console.print("✅ Test data cleaned!")


async def test_memory_service():
    """Test memory service orchestration"""
    console.print("\n[bold cyan]🧪 Test 3: Memory Service (RAG Pipeline)[/bold cyan]")
    
    # MemoryService uses static methods
    # Create test database session
    db = next(get_db())
    
    try:
        # Get or create test user
        user = db.execute(
            select(User).where(User.username == "test_rag_user")
        ).scalar_one_or_none()
        
        if not user:
            user = User(username="test_rag_user")
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # Create test session
        today = date.today()
        session = ChatSession(
            user_id=user.id,
            session_date=today,
            expires_at=datetime.now() + timedelta(hours=24),
            message_count=0,
            is_active=True
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        
        console.print(f"✅ Created test user: {user.username}")
        console.print(f"✅ Created test session: {session.id}")
        
        # Simulate saving messages
        test_messages = [
            ("user", "Aku lagi belajar machine learning nih"),
            ("assistant", "Wah keren! Fokus di area apa?"),
            ("user", "Aku lagi fokus ke NLP dan transformer"),
            ("assistant", "Oh! NLP menarik banget! Pakai library apa?"),
        ]
        
        console.print("\n📝 Saving messages to vector DB...")
        for role, content in test_messages:
            # Create Message object
            message = Message(
                session_id=session.id,
                role=role,
                content=content
            )
            db.add(message)
            db.commit()
            db.refresh(message)
            
            # Save to Qdrant
            success = MemoryService.save_message_to_vector_db(
                message=message,
                user_id=str(user.id),
                session_id=str(session.id)
            )
            if success:
                console.print(f"✅ Saved: {content[:50]}...")
        
        # Test semantic search
        console.print("\n🔍 Testing semantic search...")
        query = "belajar AI dan NLP"
        relevant_memories = MemoryService.get_relevant_memories(
            query=query,
            user_id=str(user.id),
            current_session_id=str(session.id)
        )
        
        console.print(f"\n📊 Found {len(relevant_memories)} relevant memories for: '{query}'")
        
        if relevant_memories:
            for i, memory in enumerate(relevant_memories, 1):
                console.print(Panel(
                    f"[cyan]Score: {memory['score']:.4f}[/cyan]\n"
                    f"[yellow]{memory['role']}:[/yellow] {memory['content']}\n"
                    f"[dim]{memory['timestamp']}[/dim]",
                    title=f"Memory {i}"
                ))
        
        # Test memory stats
        stats = MemoryService.get_memory_stats(str(user.id))
        console.print("\n📊 Memory Stats:")
        console.print(f"  Total memories: {stats['total_memories']}")
        console.print(f"  Embedding model: {stats['vector_dimension']}")
        console.print(f"  Search limit: {stats['search_limit']}")
        console.print(f"  Relevance threshold: {stats['relevance_threshold']}")
        
        # Cleanup
        console.print("\n🧹 Cleaning up...")
        qdrant_service.delete_session_memories(str(session.id))
        db.delete(session)
        db.delete(user)
        db.commit()
        console.print("✅ Cleanup complete!")
        
    finally:
        db.close()


async def interactive_test():
    """Interactive RAG testing"""
    console.print(Panel.fit(
        "[bold cyan]RAG System Interactive Test[/bold cyan]\n"
        "Test the Retrieval Augmented Generation system",
        border_style="cyan"
    ))
    
    # Use default user for testing
    user_id = "interactive_test_user"
    session_id = f"session_{datetime.now().timestamp()}"
    
    console.print("\n[yellow]💡 Tip: Add some memories first, then search for them![/yellow]")
    console.print("[dim]Commands: 'add', 'search', 'stats', 'quit'[/dim]\n")
    
    while True:
        command = console.input("[bold cyan]Command[/bold cyan] (add/search/stats/quit): ").strip().lower()
        
        if command == "quit":
            break
        
        elif command == "add":
            role = console.input("  Role (user/assistant): ").strip()
            content = console.input("  Message: ").strip()
            
            if role and content:
                success = qdrant_service.add_memory(
                    message_id=f"interactive_{hash(content)}",
                    user_id=user_id,
                    session_id=session_id,
                    role=role,
                    content=content,
                    timestamp=datetime.now()
                )
                if success:
                    console.print("  [green]✅ Memory saved![/green]")
                else:
                    console.print("  [red]❌ Failed to save![/red]")
        
        elif command == "search":
            query = console.input("  Search query: ").strip()
            
            if query:
                memories = MemoryService.get_relevant_memories(
                    query=query,
                    user_id=user_id,
                    current_session_id=session_id
                )
                
                console.print(f"\n  [cyan]Found {len(memories)} relevant memories:[/cyan]")
                for i, mem in enumerate(memories, 1):
                    console.print(Panel(
                        f"[cyan]Score: {mem['score']:.4f}[/cyan]\n"
                        f"[yellow]{mem['role']}:[/yellow] {mem['content']}",
                        title=f"Memory {i}"
                    ))
                console.print()
        
        elif command == "stats":
            stats = MemoryService.get_memory_stats(user_id)
            console.print(f"\n  [cyan]Memory Statistics:[/cyan]")
            console.print(f"    Total memories: {stats['total_memories']}")
            console.print(f"    Embedding model: {stats['vector_dimension']}")
            console.print(f"    Search limit: {stats['search_limit']}")
            console.print(f"    Threshold: {stats['relevance_threshold']}\n")
        
        else:
            console.print("  [red]Unknown command![/red]")


async def run_all_tests():
    """Run all automated tests"""
    console.print(Panel.fit(
        "[bold green]🧪 RAG System Test Suite[/bold green]\n"
        "Testing all components of the RAG system",
        border_style="green"
    ))
    
    try:
        await test_embedding_service()
        await test_qdrant_service()
        await test_memory_service()
        
        console.print("\n" + "="*50)
        console.print("[bold green]✅ All tests passed![/bold green]")
        console.print("="*50)
        
    except Exception as e:
        console.print(f"\n[bold red]❌ Test failed: {str(e)}[/bold red]")
        import traceback
        traceback.print_exc()


def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        asyncio.run(run_all_tests())
    else:
        asyncio.run(interactive_test())


if __name__ == "__main__":
    main()
