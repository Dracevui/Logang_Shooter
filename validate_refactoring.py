#!/usr/bin/env python3
"""
Validation script to check the refactored main.py code structure.
This script validates that all necessary classes and functions exist.
"""

import os
import sys

# Disable display for validation
os.environ['SDL_VIDEODRIVER'] = 'dummy'

def validate_game_objects():
    """Validate that game_objects.py has the expected classes."""
    print("Validating game_objects.py...")
    
    from game_objects import Player, Asteroid, Bullet
    
    # Check Player class
    assert hasattr(Player, '__init__'), "Player missing __init__"
    assert hasattr(Player, 'move'), "Player missing move method"
    assert hasattr(Player, 'shoot'), "Player missing shoot method"
    assert hasattr(Player, 'update_bullets'), "Player missing update_bullets method"
    assert hasattr(Player, 'draw'), "Player missing draw method"
    
    # Check Asteroid class
    assert hasattr(Asteroid, '__init__'), "Asteroid missing __init__"
    assert hasattr(Asteroid, 'move'), "Asteroid missing move method"
    assert hasattr(Asteroid, 'rotate'), "Asteroid missing rotate method"
    assert hasattr(Asteroid, 'draw'), "Asteroid missing draw method"
    assert hasattr(Asteroid, 'is_off_screen'), "Asteroid missing is_off_screen method"
    
    # Check Bullet class
    assert hasattr(Bullet, '__init__'), "Bullet missing __init__"
    assert hasattr(Bullet, 'move'), "Bullet missing move method"
    assert hasattr(Bullet, 'draw'), "Bullet missing draw method"
    
    print("✓ game_objects.py validation passed")
    return True

def validate_main_functions():
    """Validate that main.py still has expected functions."""
    print("\nValidating main.py functions...")
    
    # Import specific functions to check they exist
    import importlib.util
    spec = importlib.util.spec_from_file_location("main_module", "main.py")
    
    # We can't actually import main.py in headless mode due to mixer,
    # but we can check the file contents
    with open("main.py", "r") as f:
        content = f.read()
    
    required_functions = [
        'create_asteroid',
        'move_asteroids',
        'draw_asteroids',
        'check_asteroid_collision',
        'red_handle_movement',
        'handle_bullets',
        'draw_stuff',
        'start_screen',
        'main',
        'game_clear',
        'running_loop'
    ]
    
    for func_name in required_functions:
        assert f"def {func_name}(" in content, f"Function {func_name} not found"
    
    print("✓ main.py functions validation passed")
    return True

def validate_class_usage():
    """Validate that Player, Asteroid, and Bullet are imported and used."""
    print("\nValidating class usage in main.py...")
    
    with open("main.py", "r") as f:
        content = f.read()
    
    # Check imports
    assert "from game_objects import Player, Asteroid, Bullet" in content, \
        "Missing imports from game_objects"
    
    # Check Player instantiation
    assert "player = Player(" in content, "Player class not instantiated"
    
    # Check Asteroid instantiation
    assert "Asteroid(" in content, "Asteroid class not used"
    
    # Check that player object is used
    assert "player.shoot(" in content, "player.shoot method not called"
    assert "player.bullets" in content, "player.bullets not accessed"
    
    print("✓ Class usage validation passed")
    return True

def main():
    """Run all validations."""
    print("="*60)
    print("Starting validation of OOP refactoring...")
    print("="*60)
    
    try:
        validate_game_objects()
        validate_main_functions()
        validate_class_usage()
        
        print("\n" + "="*60)
        print("✓ ALL VALIDATIONS PASSED!")
        print("="*60)
        print("\nThe refactoring appears to be successful.")
        print("The code now uses object-oriented programming with:")
        print("  - Player class for managing the spaceship")
        print("  - Asteroid class for managing asteroids")
        print("  - Bullet class for managing bullets")
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Validation failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
