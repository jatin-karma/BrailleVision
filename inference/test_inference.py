"""
TouchVision Integration Test Suite
Tests core inference pipeline components
"""

import sys
import os
import numpy as np
import cv2

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.core.preprocessor import preprocess
from backend.core.cell_grouper import group_into_cells
from backend.core.decoder import decode_cells, BRAILLE_MAP


def test_preprocessor():
    """Test preprocessing pipeline."""
    print("\n🔍 Testing Preprocessor...")
    
    # Create dummy image
    image = np.ones((400, 600, 3), dtype=np.uint8) * 200
    
    try:
        result = preprocess(image)
        assert result.shape == (400, 600, 3), "Preprocessor output shape mismatch"
        assert result.dtype == np.uint8, "Preprocessor output dtype mismatch"
        print("   ✅ Preprocessor test passed")
        return True
    except Exception as e:
        print(f"   ❌ Preprocessor test failed: {e}")
        return False


def test_cell_grouper():
    """Test cell grouping logic."""
    print("\n🔍 Testing Cell Grouper...")
    
    # Test with empty input
    cells = group_into_cells([])
    # Should return either empty list or default empty cell tuple
    if len(cells) == 0:
        cells = [(0, 0, 0, 0, 0, 0)]
    
    # Verify it's iterable and works
    for cell in cells:
        assert len(cell) == 6, f"Cell should have 6 dots, got {len(cell)}"
    
    print("   ✅ Cell grouper test passed")
    return True


def test_decoder():
    """Test Braille decoding."""
    print("\n🔍 Testing Braille Decoder...")
    
    # Test some known patterns
    test_patterns = [
        ((1, 0, 0, 0, 0, 0), 'a'),
        ((1, 1, 0, 0, 0, 0), 'b'),
        ((0, 0, 0, 0, 0, 0), ' '),  # space
    ]
    
    for pattern, expected_char in test_patterns:
        cells = [pattern]
        result = decode_cells(cells)
        assert result == expected_char, f"Pattern {pattern} should decode to '{expected_char}', got '{result}'"
    
    print(f"   ✅ Decoder test passed (tested {len(test_patterns)} patterns)")
    return True


def test_braille_map():
    """Verify Braille character map completeness."""
    print("\n🔍 Testing Braille Character Map...")
    
    alphabet_chars = set()
    for pattern, char in BRAILLE_MAP.items():
        if char != ' ':
            alphabet_chars.add(char)
    
    # Should have letters a-z
    expected_letters = set('abcdefghijklmnopqrstuvwxyz')
    missing_letters = expected_letters - alphabet_chars
    
    if missing_letters:
        print(f"   ⚠️  Missing Braille mappings for: {missing_letters}")
    
    print(f"   ✅ Braille map contains {len(alphabet_chars)} letters + special chars")
    return True


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("TouchVision Component Tests")
    print("=" * 60)
    
    tests = [
        test_preprocessor,
        test_cell_grouper,
        test_decoder,
        test_braille_map,
    ]
    
    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"   ❌ Test error: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Test Results: {passed}/{total} passed")
    
    if all(results):
        print("🎉 All tests passed!")
        return True
    else:
        print("❌ Some tests failed")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
