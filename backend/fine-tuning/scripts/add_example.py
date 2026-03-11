"""
Helper script to add new conversation examples to dataset

Makes it easy to expand dataset without manual JSONL editing
"""

import json
from pathlib import Path

CATEGORIES = {
    "1": ("01_caring_support.jsonl", "Caring/Support"),
    "2": ("02_daily_conversation.jsonl", "Daily Conversation"),
    "3": ("03_playful_teasing.jsonl", "Playful Teasing"),
    "4": ("04_assistant_commands.jsonl", "Assistant Commands"),
    "5": ("05_mood_transitions.jsonl", "Mood Transitions"),
}

def format_example(user_msg, model_msg):
    """Format conversation into JSONL format"""
    return json.dumps({
        "messages": [
            {"role": "user", "content": user_msg},
            {"role": "model", "content": model_msg}
        ]
    }, ensure_ascii=False)

def add_example():
    """Interactive prompt to add new example"""
    print("="*60)
    print("🎯 Add New Training Example for Aiko")
    print("="*60)
    
    # Select category
    print("\nSelect category:")
    for key, (filename, name) in CATEGORIES.items():
        print(f"  {key}. {name}")
    
    while True:
        choice = input("\nEnter category number (1-5): ").strip()
        if choice in CATEGORIES:
            break
        print("Invalid choice! Please enter 1-5.")
    
    filename, category_name = CATEGORIES[choice]
    print(f"\n✅ Category: {category_name}")
    
    # Get user message
    print("\n" + "-"*60)
    print("Enter USER message:")
    user_msg = input("User: ").strip()
    
    if not user_msg:
        print("❌ User message cannot be empty!")
        return
    
    # Get Aiko's response
    print("\n" + "-"*60)
    print("Enter AIKO's response:")
    print("(Tips: Be caring, energetic, use emojis, mix ID/EN)")
    model_msg = input("Aiko: ").strip()
    
    if not model_msg:
        print("❌ Aiko's response cannot be empty!")
        return
    
    # Preview
    print("\n" + "="*60)
    print("📝 Preview:")
    print("="*60)
    print(f"User: {user_msg}")
    print(f"Aiko: {model_msg}")
    print("="*60)
    
    # Confirm
    confirm = input("\nAdd this example? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("❌ Cancelled.")
        return
    
    # Save to file
    datasets_dir = Path(__file__).parent.parent / "datasets"
    file_path = datasets_dir / filename
    
    example_line = format_example(user_msg, model_msg)
    
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(example_line + '\n')
    
    print(f"\n✅ Example added to {filename}!")
    print(f"\n💡 Tip: Run 'python validate_dataset.py' to validate")
    print(f"💡 Tip: Run 'python generate_dataset.py' to regenerate combined dataset")

def batch_add():
    """Add multiple examples in one session"""
    print("="*60)
    print("🎯 Batch Add Training Examples")
    print("="*60)
    
    count = 0
    while True:
        add_example()
        count += 1
        
        print("\n" + "-"*60)
        another = input("Add another example? (y/n): ").strip().lower()
        if another != 'y':
            break
        print("\n")
    
    print(f"\n🎉 Added {count} example(s) total!")
    print("\n📊 Next steps:")
    print("  1. Validate: python validate_dataset.py")
    print("  2. Combine: python generate_dataset.py")
    print("  3. Upload to Google AI Studio for retraining\n")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--batch":
        batch_add()
    else:
        add_example()
