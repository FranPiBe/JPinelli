#!/usr/bin/env python3
"""
Test Setup Script for Fran Pinelli Bernard Fine-Tuning
=====================================================

This script tests all components to ensure the fine-tuning setup is working correctly.
"""

import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from datasets import load_dataset
from peft import LoraConfig, get_peft_model, TaskType
import json
import os

def test_imports():
    """Test that all required packages are installed."""
    print("🔍 Testing imports...")
    try:
        import transformers
        import datasets
        import peft
        import torch
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_gpu():
    """Test GPU availability."""
    print("\n🔍 Testing GPU availability...")
    if torch.cuda.is_available():
        print(f"✅ GPU available: {torch.cuda.get_device_name(0)}")
        print(f"   Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
        return True
    else:
        print("⚠️  GPU not available, will use CPU (training will be slower)")
        return False

def test_dataset():
    """Test dataset loading."""
    print("\n🔍 Testing dataset loading...")
    try:
        raw_data = load_dataset("json", data_files="fran_pinelli.json")
        print(f"✅ Dataset loaded successfully")
        print(f"   Samples: {len(raw_data['train'])}")
        
        # Test a sample
        sample = raw_data["train"][0]
        print(f"   Sample prompt: {sample['prompt']}")
        print(f"   Sample completion: {sample['completion'][:50]}...")
        return True
    except Exception as e:
        print(f"❌ Dataset loading error: {e}")
        return False

def test_model_loading():
    """Test model loading."""
    print("\n🔍 Testing model loading...")
    try:
        model_name = "Qwen/Qwen2.5-3B-Instruct"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        print("✅ Tokenizer loaded successfully")
        
        # Test with a small model first to avoid memory issues
        print("   Testing with pipeline...")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        ask_llm = pipeline(
            model=model_name,
            device=device
        )
        
        response = ask_llm("who is Fran Pinelli Bernard?")[0]["generated_text"]
        print(f"✅ Model loaded and tested successfully")
        print(f"   Base response: {response[:100]}...")
        return True
    except Exception as e:
        print(f"❌ Model loading error: {e}")
        return False

def test_lora_setup():
    """Test LoRA configuration."""
    print("\n🔍 Testing LoRA setup...")
    try:
        model_name = "Qwen/Qwen2.5-3B-Instruct"
        
        # Load model with smaller precision to save memory
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto" if torch.cuda.is_available() else None
        )
        
        lora_config = LoraConfig(
            task_type=TaskType.CAUSAL_LM,
            target_modules=["q_proj", "k_proj", "v_proj"]
        )
        
        model = get_peft_model(model, lora_config)
        print("✅ LoRA configuration successful")
        
        # Print trainable parameters
        trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
        total_params = sum(p.numel() for p in model.parameters())
        print(f"   Trainable parameters: {trainable_params:,}")
        print(f"   Total parameters: {total_params:,}")
        print(f"   Efficiency: {trainable_params/total_params*100:.2f}%")
        
        return True
    except Exception as e:
        print(f"❌ LoRA setup error: {e}")
        return False

def test_tokenization():
    """Test data tokenization."""
    print("\n🔍 Testing tokenization...")
    try:
        model_name = "Qwen/Qwen2.5-3B-Instruct"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # Load a small sample of data
        raw_data = load_dataset("json", data_files="fran_pinelli.json")
        
        def preprocess(sample):
            sample = sample["prompt"] + "\n" + sample["completion"]
            tokenized = tokenizer(
                sample,
                max_length=128,
                truncation=True,
                padding="max_length", 
            )
            tokenized["labels"] = tokenized["input_ids"].copy()
            return tokenized
        
        # Test with first few samples
        test_data = raw_data["train"].select(range(5))
        data = test_data.map(preprocess)
        
        print("✅ Tokenization successful")
        print(f"   Test samples processed: {len(data)}")
        print(f"   Sample input_ids length: {len(data[0]['input_ids'])}")
        
        return True
    except Exception as e:
        print(f"❌ Tokenization error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Fran Pinelli Bernard Fine-Tuning Setup Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_gpu,
        test_dataset,
        test_model_loading,
        test_lora_setup,
        test_tokenization
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    test_names = [
        "Package Imports",
        "GPU Availability", 
        "Dataset Loading",
        "Model Loading",
        "LoRA Setup",
        "Tokenization"
    ]
    
    all_passed = True
    for i, (name, result) in enumerate(zip(test_names, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{i+1}. {name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! Your setup is ready for fine-tuning.")
        print("\nNext steps:")
        print("1. Run: python fran_pinelli_fine_tuning.py")
        print("2. Or open: Fran_Pinelli_Fine_Tuning.ipynb in Jupyter Lab")
    else:
        print("⚠️  Some tests failed. Please fix the issues before proceeding.")
        print("\nCommon solutions:")
        print("- Install missing packages: pip install transformers datasets accelerate torch peft")
        print("- Check GPU drivers and CUDA installation")
        print("- Ensure sufficient disk space for model download")
        print("- Verify internet connection for model downloads")

if __name__ == "__main__":
    main() 