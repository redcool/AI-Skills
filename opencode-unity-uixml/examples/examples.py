#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unity UI Toolkit 示例 - 一键生成常见界面
"""

import os
import sys

# 添加脚本目录到路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(SCRIPT_DIR))

from unity_uixml_generator import generate_ui


def example_login():
    """示例1：登录界面"""
    print("=== 生成登录界面 ===")
    files = generate_ui(
        ui_name="Login",
        description="用户名输入框、密码输入框、登录按钮、注册链接、忘记密码链接",
        output_dir="./Output/Login",
        pattern="mvvm",
        style="dark",
        namespace="Game.UI"
    )
    for ftype, fpath in files.items():
        print(f"  [{ftype}] {fpath}")
    print()


def example_inventory():
    """示例2：背包界面（奇幻风格）"""
    print("=== 生成背包界面 ===")
    files = generate_ui(
        ui_name="Inventory",
        description="标题栏、64格物品网格、物品详情面板、物品图标、物品名称、物品描述、使用按钮、丢弃按钮",
        output_dir="./Output/Inventory",
        pattern="mvp",
        style="game_fantasy",
        namespace="Game.UI"
    )
    for ftype, fpath in files.items():
        print(f"  [{ftype}] {fpath}")
    print()


def example_settings():
    """示例3：设置界面"""
    print("=== 生成设置界面 ===")
    files = generate_ui(
        ui_name="Settings",
        description="主音量滑块、音乐滑块、音效滑块、画质下拉框、全屏开关、垂直同步开关、保存按钮、取消按钮",
        output_dir="./Output/Settings",
        pattern="mvvm",
        style="dark",
        namespace="Game.UI"
    )
    for ftype, fpath in files.items():
        print(f"  [{ftype}] {fpath}")
    print()


def example_player_hud():
    """示例4：玩家HUD"""
    print("=== 生成玩家HUD ===")
    files = generate_ui(
        ui_name="PlayerHUD",
        description="头像图标、血条、蓝条、经验条、等级文本、金币文本",
        output_dir="./Output/PlayerHUD",
        pattern="mvp",
        style="game_fantasy",
        namespace="Game.UI"
    )
    for ftype, fpath in files.items():
        print(f"  [{ftype}] {fpath}")
    print()


def example_dialog():
    """示例5：对话框"""
    print("=== 生成对话框 ===")
    files = generate_ui(
        ui_name="ConfirmDialog",
        description="标题文本、消息内容文本、确认按钮、取消按钮",
        output_dir="./Output/ConfirmDialog",
        pattern="mvp",
        style="dark",
        namespace="Game.UI"
    )
    for ftype, fpath in files.items():
        print(f"  [{ftype}] {fpath}")
    print()


def example_shop():
    """示例6：商店界面（科幻风格）"""
    print("=== 生成商店界面 ===")
    files = generate_ui(
        ui_name="Shop",
        description="商店标题、商品列表、商品图标、商品名称、商品价格、购买按钮、关闭按钮",
        output_dir="./Output/Shop",
        pattern="mvvm",
        style="game_sci-fi",
        namespace="Game.UI"
    )
    for ftype, fpath in files.items():
        print(f"  [{ftype}] {fpath}")
    print()


def main():
    """运行所有示例"""
    print("\n" + "="*50)
    print("Unity UI Toolkit Generator - 示例生成")
    print("="*50 + "\n")
    
    example_login()
    example_inventory()
    example_settings()
    example_player_hud()
    example_dialog()
    example_shop()
    
    print("="*50)
    print("✅ 所有示例生成完成！")
    print("="*50)


if __name__ == "__main__":
    main()
