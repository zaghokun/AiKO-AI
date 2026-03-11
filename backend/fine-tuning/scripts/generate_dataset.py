"""
Combine all dataset files into a single JSONL for Gemini fine-tuning

This script merges all category datasets into combined_dataset.jsonl
"""

import json
from pathlib import Path
import random

def combine_datasets(shuffle=True, output_name="combined_dataset.jsonl"):
    """
    Combine all JSONL files into one
    
    Args:
        shuffle: Whether to shuffle the examples
        output_name: Output file name
    """
    datasets_dir = Path(__file__).parent.parent / "datasets"
    
    # Find all JSONL files except combined
    jsonl_files = [f for f in datasets_dir.glob("*.jsonl") 
                   if not f.name.startswith("combined")]
    
    if not jsonl_files:
        print("❌ No dataset files found!")
        return False
    
    print("📚 Combining datasets...\n")
    
    all_examples = []
    category_counts = {}
    
    # Read all files
    for file_path in sorted(jsonl_files):
        examples = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    examples.append(line)
        
        category = file_path.stem  # filename without extension
        category_counts[category] = len(examples)
        all_examples.extend(examples)
        
        print(f"✅ {file_path.name}: {len(examples)} examples")
    
    # Shuffle if requested
    if shuffle:
        random.shuffle(all_examples)
        print(f"\n🔀 Shuffled {len(all_examples)} examples")
    
    # Write combined file
    output_path = datasets_dir / output_name
    with open(output_path, 'w', encoding='utf-8') as f:
        for example in all_examples:
            f.write(example + '\n')
    
    print(f"\n✅ Combined dataset saved to: {output_path.name}")
    print(f"\n{'='*50}")
    print("📊 Dataset Summary:")
    print(f"{'='*50}")
    
    for category, count in sorted(category_counts.items()):
        percentage = (count / len(all_examples)) * 100
        print(f"  {category}: {count} ({percentage:.1f}%)")
    
    print(f"{'='*50}")
    print(f"  Total: {len(all_examples)} examples")
    print(f"{'='*50}\n")
    
    print("🚀 Ready for upload to Google AI Studio!")
    print(f"   File: {output_path}\n")
    
    return True

if __name__ == "__main__":
    # Combine with shuffling
    combine_datasets(shuffle=True)
    
    # You can also create non-shuffled version
    # combine_datasets(shuffle=False, output_name="combined_dataset_ordered.jsonl")
