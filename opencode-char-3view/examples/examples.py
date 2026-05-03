#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example usage for opencode-char-3view
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from char_3view import generate_three_view, STYLE_PRESETS

def example_1_han_warrior():
    """Example 1: Han Dynasty warrior (realistic style)"""
    print("\n" + "="*60)
    print("Example 1: Han Dynasty Warrior (Realistic)")
    print("="*60)

    result = generate_three_view(
        description="汉朝战士，身穿盔甲，手持长枪",
        style="realistic",
        is_chinese=True,
        dry_run=True  # Set to False to actually generate
    )

    print("\nGenerated prompts:")
    print(f"Positive: {result['prompts']['positive'][:200]}...")
    print(f"Negative: {result['prompts']['negative'][:100]}...")

def example_2_cartoon_soldier():
    """Example 2: Sci-fi soldier (cartoon style)"""
    print("\n" + "="*60)
    print("Example 2: Sci-fi Soldier (Cartoon)")
    print("="*60)

    result = generate_three_view(
        description="futuristic soldier with plasma rifle and energy shield",
        style="cartoon",
        dry_run=True
    )

def example_3_anime_mage():
    """Example 3: Fantasy mage (anime style)"""
    print("\n" + "="*60)
    print("Example 3: Fantasy Mage (Anime)")
    print("="*60)

    result = generate_three_view(
        description="年轻女法师，穿着蓝色长袍，手持魔法杖",
        style="anime",
        is_chinese=True,
        dry_run=True
    )

def example_4_chinese_assassin():
    """Example 4: Ancient assassin (chinese style)"""
    print("\n" + "="*60)
    print("Example 4: Ancient Assassin (Chinese Style)")
    print("="*60)

    result = generate_three_view(
        description="古代刺客，黑衣蒙面，手持双匕首",
        style="chinese",
        is_chinese=True,
        dry_run=True
    )

def example_5_fantasy_knight():
    """Example 5: Fantasy knight (fantasy style)"""
    print("\n" + "="*60)
    print("Example 5: Fantasy Knight")
    print("="*60)

    result = generate_three_view(
        description="medieval knight in full plate armor with sword and shield",
        style="fantasy",
        dry_run=True
    )

def example_6_scifi_mech():
    """Example 6: Sci-fi mech pilot (scifi style)"""
    print("\n" + "="*60)
    print("Example 6: Sci-fi Mech Pilot")
    print("="*60)

    result = generate_three_view(
        description="机甲驾驶员，穿紧身作战服，带头盔",
        style="scifi",
        is_chinese=True,
        dry_run=True
    )

def example_7_chibi_character():
    """Example 7: Cute character (chibi style)"""
    print("\n" + "="*60)
    print("Example 7: Cute Chibi Character")
    print("="*60)

    result = generate_three_view(
        description="小精灵魔法师，穿紫色斗篷，戴尖帽子",
        style="chibi",
        is_chinese=True,
        dry_run=True
    )

def show_available_styles():
    """Display all available style presets"""
    print("\n" + "="*60)
    print("Available Style Presets")
    print("="*60)

    for key, preset in STYLE_PRESETS.items():
        print(f"\n{key}: {preset['name']}")
        print(f"  Positive tags: {', '.join(preset['positive'][:3])}...")
        print(f"  Negative tags: {', '.join(preset['negative'][:3])}...")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("opencode-char-3view Examples")
    print("="*60)

    # Show available styles
    show_available_styles()

    # Run examples (dry run mode)
    example_1_han_warrior()
    example_2_cartoon_soldier()
    example_3_anime_mage()
    example_4_chinese_assassin()
    example_5_fantasy_knight()
    example_6_scifi_mech()
    example_7_chibi_character()

    print("\n" + "="*60)
    print("To generate actual images, set dry_run=False")
    print("="*60 + "\n")
