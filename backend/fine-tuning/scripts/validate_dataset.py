"""
Dataset validation script for Gemini fine-tuning

Validates JSONL format and checks for common issues
"""

import json
import sys
from pathlib import Path

def validate_jsonl_file(file_path):
    """Validate a single JSONL file"""
    errors = []
    warnings = []
    line_count = 0
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                    
                line_count += 1
                
                try:
                    data = json.loads(line)
                    
                    # Check structure
                    if "messages" not in data:
                        errors.append(f"Line {line_num}: Missing 'messages' key")
                        continue
                    
                    messages = data["messages"]
                    
                    # Check messages is array
                    if not isinstance(messages, list):
                        errors.append(f"Line {line_num}: 'messages' must be an array")
                        continue
                    
                    # Check message count
                    if len(messages) != 2:
                        warnings.append(f"Line {line_num}: Expected 2 messages (user + model), got {len(messages)}")
                    
                    # Check each message
                    for msg_idx, msg in enumerate(messages):
                        if "role" not in msg:
                            errors.append(f"Line {line_num}, Message {msg_idx}: Missing 'role'")
                        elif msg["role"] not in ["user", "model"]:
                            errors.append(f"Line {line_num}, Message {msg_idx}: Invalid role '{msg['role']}' (must be 'user' or 'model')")
                        
                        if "content" not in msg:
                            errors.append(f"Line {line_num}, Message {msg_idx}: Missing 'content'")
                        elif not msg["content"].strip():
                            errors.append(f"Line {line_num}, Message {msg_idx}: Empty content")
                        
                        # Check content length
                        if "content" in msg and len(msg["content"]) > 2000:
                            warnings.append(f"Line {line_num}, Message {msg_idx}: Very long content ({len(msg['content'])} chars)")
                    
                except json.JSONDecodeError as e:
                    errors.append(f"Line {line_num}: Invalid JSON - {str(e)}")
                    
    except FileNotFoundError:
        errors.append(f"File not found: {file_path}")
    except Exception as e:
        errors.append(f"Error reading file: {str(e)}")
    
    return {
        "file": file_path.name,
        "line_count": line_count,
        "errors": errors,
        "warnings": warnings,
        "valid": len(errors) == 0
    }

def validate_all_datasets():
    """Validate all dataset files"""
    datasets_dir = Path(__file__).parent.parent / "datasets"
    
    if not datasets_dir.exists():
        print(f"❌ Datasets directory not found: {datasets_dir}")
        return False
    
    jsonl_files = list(datasets_dir.glob("*.jsonl"))
    
    if not jsonl_files:
        print(f"❌ No JSONL files found in {datasets_dir}")
        return False
    
    print("🔍 Validating dataset files...\n")
    
    all_valid = True
    total_examples = 0
    
    for file_path in sorted(jsonl_files):
        result = validate_jsonl_file(file_path)
        total_examples += result["line_count"]
        
        status = "✅" if result["valid"] else "❌"
        print(f"{status} {result['file']}: {result['line_count']} examples")
        
        if result["errors"]:
            all_valid = False
            print(f"   Errors:")
            for error in result["errors"]:
                print(f"     • {error}")
        
        if result["warnings"]:
            print(f"   Warnings:")
            for warning in result["warnings"]:
                print(f"     ⚠️  {warning}")
        
        print()
    
    print(f"{'='*50}")
    print(f"Total examples: {total_examples}")
    print(f"Status: {'✅ All valid!' if all_valid else '❌ Some files have errors'}")
    print(f"{'='*50}\n")
    
    return all_valid

if __name__ == "__main__":
    is_valid = validate_all_datasets()
    sys.exit(0 if is_valid else 1)
