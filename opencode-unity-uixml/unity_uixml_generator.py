#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unity UI Toolkit Generator - AI驱动的UXML/USS/C#界面生成器
支持MVVM/MVP模式，自动生成完整界面组件

用法:
    python unity_uixml_generator.py --desc "登录界面：用户名输入框、密码输入框、登录按钮、注册链接"
    python unity_uixml_generator.py --desc "背包界面：网格布局64格、物品图标、数量标签、详情面板" --pattern mvvm
    python unity_uixml_generator.py --yaml ui_spec.yaml --out ./Output/Inventory
"""

import os
import json
import argparse
import textwrap
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# ============================================================
# 中英文组件映射词典
# ============================================================
UI_COMPONENT_DICT = {
    # 容器类
    "容器": "VisualElement",
    "面板": "VisualElement",
    "弹窗": "VisualElement",
    "滚动": "ScrollView",
    "滚动视图": "ScrollView",
    "滚动列表": "ScrollView",
    "列表": "ListView",
    "网格": "VisualElement",
    "水平布局": "VisualElement",
    "垂直布局": "VisualElement",
    
    # 输入类
    "输入框": "TextField",
    "文本框": "TextField",
    "输入": "TextField",
    "密码框": "TextField",
    "密码输入": "TextField",
    "数字输入": "IntegerField",
    "整数输入": "IntegerField",
    "浮点输入": "FloatField",
    "滑块": "Slider",
    "滑动条": "Slider",
    "复选框": "Toggle",
    "开关": "Toggle",
    "下拉框": "DropdownField",
    "下拉选择": "DropdownField",
    "选择框": "DropdownField",
    
    # 按钮类
    "按钮": "Button",
    "点击": "Button",
    "确认按钮": "Button",
    "取消按钮": "Button",
    "关闭按钮": "Button",
    
    # 显示类
    "文本": "Label",
    "标签": "Label",
    "标题": "Label",
    "图片": "Image",
    "图像": "Image",
    "图标": "Image",
    "头像": "Image",
    "进度条": "ProgressBar",
    "血条": "ProgressBar",
    "蓝条": "ProgressBar",
    "经验条": "ProgressBar",
    
    # 特殊类
    "分割线": "VisualElement",
    "间隔": "VisualElement",
    "占位": "VisualElement",
    "遮罩": "VisualElement",
    "拖拽区域": "VisualElement",
}

# USS样式预设
STYLE_PRESETS = {
    "dark": {
        "bg_color": "#1E1E1E",
        "panel_bg": "#2D2D2D",
        "text_color": "#FFFFFF",
        "text_secondary": "#B0B0B0",
        "accent": "#0078D4",
        "accent_hover": "#1A8CFF",
        "border": "#404040",
        "input_bg": "#3C3C3C",
        "button_hover": "#3E3E3E",
    },
    "light": {
        "bg_color": "#F5F5F5",
        "panel_bg": "#FFFFFF",
        "text_color": "#1E1E1E",
        "text_secondary": "#666666",
        "accent": "#0078D4",
        "accent_hover": "#1A8CFF",
        "border": "#E0E0E0",
        "input_bg": "#FFFFFF",
        "button_hover": "#F0F0F0",
    },
    "game_fantasy": {
        "bg_color": "#0A0A14",
        "panel_bg": "#1A1A2E",
        "text_color": "#E8D5B7",
        "text_secondary": "#9A8878",
        "accent": "#D4AF37",
        "accent_hover": "#F0D060",
        "border": "#3A3A5E",
        "input_bg": "#2A2A3E",
        "button_hover": "#3A3A4E",
    },
    "game_sci-fi": {
        "bg_color": "#0A1015",
        "panel_bg": "#0F1A25",
        "text_color": "#00FFFF",
        "text_secondary": "#4A8090",
        "accent": "#00FF88",
        "accent_hover": "#40FFAA",
        "border": "#1A3A4A",
        "input_bg": "#152535",
        "button_hover": "#1A3040",
    },
}

# ============================================================
# UXML模板生成器
# ============================================================
class UXMLGenerator:
    """生成UXML界面结构"""
    
    def __init__(self, ui_name: str, namespace: str = "Game.UI"):
        self.ui_name = ui_name
        self.namespace = namespace
        self.elements: List[Dict] = []
        self.bindings: List[Dict] = []
        self.event_handlers: List[Dict] = []
    
    def add_element(self, elem_type: str, name: str, 
                    parent: Optional[str] = None,
                    attributes: Optional[Dict] = None,
                    binding_path: Optional[str] = None,
                    text: Optional[str] = None):
        """添加UI元素"""
        elem = {
            "type": elem_type,
            "name": name,
            "parent": parent,
            "attributes": attributes or {},
            "binding_path": binding_path,
            "text": text,
        }
        self.elements.append(elem)
        
        if binding_path:
            self.bindings.append({
                "element": name,
                "path": binding_path,
                "type": elem_type
            })
        
        return elem
    
    def add_event(self, element_name: str, event_type: str, handler_name: str):
        """添加事件处理"""
        self.event_handlers.append({
            "element": element_name,
            "event": event_type,
            "handler": handler_name
        })
    
    def generate_uxml(self) -> str:
        """生成UXML文件内容"""
        lines = [
            '<UXML xmlns="UnityEngine.UIElements" xmlns:uie="UnityEditor.UIElements">',
            f'    <Style src="project://database/Assets/UI/Styles/{self.ui_name}.uss?fileID=7423427704685742052&amp;guid=STYLE_GUID&amp;type=3#Styles/{self.ui_name}.uss" />',
            f'    <Style src="project://database/Assets/UI/Styles/Common.uss?fileID=7423427704685742052&amp;guid=COMMON_STYLE_GUID&amp;type=3#Styles/Common.uss" />',
            '',
        ]
        
        # 生成元素树
        for elem in self.elements:
            indent = "    " if not elem["parent"] else "        "
            elem_xml = self._render_element(elem, indent)
            lines.append(elem_xml)
        
        lines.append('</UXML>')
        return '\n'.join(lines)
    
    def _render_element(self, elem: Dict, indent: str) -> str:
        """渲染单个元素"""
        elem_type = elem["type"]
        name = elem["name"]
        attrs = elem["attributes"].copy()
        
        attrs["name"] = name
        attrs["class"] = f"{elem_type.lower()}-{name.replace('_', '-')}"
        
        if elem.get("binding_path"):
            attrs["binding-path"] = elem["binding_path"]
        
        if elem.get("text") and elem_type in ["Label", "Button", "TextField"]:
            if elem_type == "TextField":
                attrs["value"] = elem["text"]
            else:
                # Button和Label用子元素
                pass
        
        attr_str = " ".join([f'{k}="{v}"' for k, v in attrs.items()])
        
        if elem.get("text") and elem_type in ["Button", "Label"]:
            return f'{indent}<{elem_type} {attr_str}>{elem["text"]}</{elem_type}>'
        else:
            return f'{indent}<{elem_type} {attr_str} />'
    
    def generate_uss(self, style_preset: str = "dark") -> str:
        """生成USS样式文件"""
        preset = STYLE_PRESETS.get(style_preset, STYLE_PRESETS["dark"])
        
        lines = [
            f"/* {self.ui_name}.uss - Auto-generated UI Styles */",
            f"/* Style: {style_preset} */",
            f"/* Generated: {datetime.now().isoformat()} */",
            "",
            "/* ============================================",
            "   Root Container",
            "   ============================================ */",
            f".{self.ui_name.lower()}-container {{",
            f"    background-color: {preset['panel_bg']};",
            f"    border-color: {preset['border']};",
            f"    border-width: 1px;",
            f"    border-radius: 8px;",
            f"    padding: 16px;",
            "}",
            "",
        ]
        
        for elem in self.elements:
            elem_style = self._generate_element_style(elem, preset)
            lines.extend(elem_style)
        
        return '\n'.join(lines)
    
    def _generate_element_style(self, elem: Dict, preset: Dict) -> List[str]:
        """生成元素样式"""
        elem_type = elem["type"]
        name = elem["name"]
        class_name = f"{elem_type.lower()}-{name.replace('_', '-')}"
        
        lines = [f"/* {name} ({elem_type}) */"]
        
        if elem_type == "Button":
            lines.extend([
                f".{class_name} {{",
                f"    background-color: {preset['accent']};",
                f"    color: {preset['text_color']};",
                f"    border-radius: 4px;",
                f"    padding: 8px 16px;",
                f"    font-size: 14px;",
                f"    margin-top: 8px;",
                "}",
                "",
                f".{class_name}:hover {{",
                f"    background-color: {preset['accent_hover']};",
                "}",
            ])
        elif elem_type == "TextField":
            lines.extend([
                f".{class_name} {{",
                f"    background-color: {preset['input_bg']};",
                f"    color: {preset['text_color']};",
                f"    border-color: {preset['border']};",
                f"    border-width: 1px;",
                f"    border-radius: 4px;",
                f"    padding: 8px;",
                f"    font-size: 14px;",
                f"    margin-bottom: 8px;",
                "}",
            ])
        elif elem_type == "Label":
            lines.extend([
                f".{class_name} {{",
                f"    color: {preset['text_color']};",
                f"    font-size: 14px;",
                f"    margin-bottom: 4px;",
                "}",
            ])
        elif elem_type == "Image":
            lines.extend([
                f".{class_name} {{",
                f"    width: 64px;",
                f"    height: 64px;",
                f"    margin: 4px;",
                "}",
            ])
        elif elem_type == "ProgressBar":
            lines.extend([
                f".{class_name} {{",
                f"    height: 8px;",
                f"    background-color: {preset['border']};",
                f"    border-radius: 4px;",
                "}",
            ])
        
        lines.append("")
        return lines
    
    def generate_viewmodel(self, pattern: str = "mvvm") -> str:
        """生成C# ViewModel/Presenter代码"""
        class_name = f"{self.ui_name}ViewModel" if pattern == "mvvm" else f"{self.ui_name}Presenter"
        
        lines = [
            f"// {class_name}.cs - Auto-generated",
            f"// Pattern: {pattern.upper()}",
            f"// Generated: {datetime.now().isoformat()}",
            "",
            f"using UnityEngine;",
            f"using UnityEngine.UIElements;",
            f"using Unity.Properties;",
            "",
            f"namespace {self.namespace}",
            "{",
            f"    /// <summary>",
            f"    /// {self.ui_name}界面数据模型",
            f"    /// </summary>",
            f"    public class {class_name} : MonoBehaviour",
            f"    {{",
            f"        [Header(\"UI Reference\")]",
            f"        [SerializeField] private UIDocument _uiDocument;",
            "",
        ]
        
        # 生成UI元素引用
        lines.append("        // UI Elements")
        for elem in self.elements:
            lines.append(f"        private {elem['type']} _{elem['name']};")
        lines.append("")
        
        # 生成绑定属性
        if pattern == "mvvm":
            lines.append("        // Bindable Properties")
            for binding in self.bindings:
                prop_name = binding["path"]
                lines.extend([
                    f"        private string _{prop_name.lower()};",
                    f"        [CreateProperty]",
                    f"        public string {prop_name}",
                    f"        {{",
                    f"            get => _{prop_name.lower()};",
                    f"            set",
                    f"            {{",
                    f"                if (_{prop_name.lower()} != value)",
                    f"                {{",
                    f"                    _{prop_name.lower()} = value;",
                    f"                    NotifyPropertyChanged(nameof({prop_name}));",
                    f"                }}",
                    f"            }}",
                    f"        }}",
                    "",
                ])
        
        # 生成事件处理
        lines.append("        // Event Handlers")
        for handler in self.event_handlers:
            lines.extend([
                f"        private void {handler['handler']}()",
                f"        {{",
                f"            // TODO: Implement {handler['handler']}",
                f"            Debug.Log(\"{handler['handler']} triggered\");",
                f"        }}",
                "",
            ])
        
        # 生成初始化方法
        lines.extend([
            "        private void Awake()",
            "        {",
            "            InitializeElements();",
            "            BindEvents();",
            "            SetupDataBinding();",
            "        }",
            "",
        ])
        
        # 初始化元素
        lines.extend([
            "        private void InitializeElements()",
            "        {",
            "            if (_uiDocument == null) return;",
            "",
            "            var root = _uiDocument.rootVisualElement;",
            "",
        ])
        for elem in self.elements:
            lines.append(f"            _{elem['name']} = root.Q<{elem['type']}>(\"{elem['name']}\");")
        lines.extend([
            "        }",
            "",
        ])
        
        # 绑定事件
        lines.extend([
            "        private void BindEvents()",
            "        {",
        ])
        for handler in self.event_handlers:
            elem_type = next((e["type"] for e in self.elements if e["name"] == handler["element"]), "Button")
            if elem_type == "Button":
                lines.append(f"            _{handler['element']}.clicked += {handler['handler']};")
            else:
                lines.append(f"            _{handler['element']}.RegisterCallback<ClickEvent>(evt => {handler['handler']}());")
        lines.extend([
            "        }",
            "",
        ])
        
        # 数据绑定设置
        if pattern == "mvvm" and self.bindings:
            lines.extend([
                "        private void SetupDataBinding()",
                "        {",
                "            var root = _uiDocument.rootVisualElement;",
                "            root.dataSource = this;",
                "",
            ])
            for binding in self.bindings:
                lines.append(f"            _{binding['element']}.SetBinding(\"value\", \"{binding['path']}\");")
            lines.extend([
                "        }",
                "",
            ])
        
        # 销毁时清理
        lines.extend([
            "        private void OnDestroy()",
            "        {",
            "            // Unregister events",
        ])
        for handler in self.event_handlers:
            lines.append(f"            _{handler['element']}.clicked -= {handler['handler']};")
        lines.extend([
            "        }",
            "    }",
            "}",
        ])
        
        return '\n'.join(lines)
    
    def generate_model(self) -> str:
        """生成数据模型"""
        model_name = f"{self.ui_name}Model"
        
        lines = [
            f"// {model_name}.cs - Data Model",
            f"// Generated: {datetime.now().isoformat()}",
            "",
            f"namespace {self.namespace}",
            "{",
            f"    /// <summary>",
            f"    /// {self.ui_name}数据层",
            f"    /// </summary>",
            f"    public class {model_name}",
            f"    {{",
        ]
        
        # 根据绑定生成数据属性
        for binding in self.bindings:
            lines.append(f"        public string {binding['path']} {{ get; set; }}")
        
        lines.extend([
            "    }",
            "}",
        ])
        
        return '\n'.join(lines)


# ============================================================
# UI描述解析器
# ============================================================
class UIParser:
    """解析自然语言UI描述"""
    
    @staticmethod
    def parse_description(desc: str) -> List[Dict]:
        """解析中文UI描述，返回元素列表"""
        elements = []
        
        # 分割成组件描述
        parts = desc.replace("，", ",").replace("、", ",").replace("：", ":").replace("：", ":").split(",")
        
        for i, part in enumerate(parts):
            part = part.strip()
            if not part:
                continue
            
            elem = UIParser._parse_component(part, i)
            if elem:
                elements.append(elem)
        
        return elements
    
    @staticmethod
    def _parse_component(text: str, index: int) -> Optional[Dict]:
        """解析单个组件描述"""
        text = text.strip()
        
        # 检查是否包含已知的组件类型
        for cn_name, en_type in UI_COMPONENT_DICT.items():
            if cn_name in text:
                # 提取名称（如果有）
                name = text.replace(cn_name, "").strip()
                if not name:
                    name = f"{en_type}_{index}"
                else:
                    name = name.replace(" ", "_").replace("-", "_").lower()
                
                # 检查是否有默认文本
                default_text = None
                if ":" in text or "：" in text:
                    parts = text.replace("：", ":").split(":")
                    if len(parts) > 1:
                        default_text = parts[1].strip()
                
                return {
                    "type": en_type,
                    "name": name,
                    "text": default_text,
                    "description": text,
                }
        
        return None
    
    @staticmethod
    def parse_yaml(yaml_path: str) -> Dict:
        """解析YAML规格文件"""
        import yaml
        with open(yaml_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)


# ============================================================
# 主生成函数
# ============================================================
def generate_ui(ui_name: str, description: str, 
                output_dir: str, 
                pattern: str = "mvvm",
                style: str = "dark",
                namespace: str = "Game.UI") -> Dict[str, str]:
    """
    生成完整的UI组件
    
    Args:
        ui_name: UI名称（如"Login", "Inventory"）
        description: UI描述（中文或英文）
        output_dir: 输出目录
        pattern: 设计模式（mvvm/mvp）
        style: 样式预设（dark/light/game_fantasy/game_sci-fi）
        namespace: C#命名空间
    
    Returns:
        生成的文件路径字典
    """
    # 解析描述
    parser = UIParser()
    elements = parser.parse_description(description)
    
    # 创建生成器
    generator = UXMLGenerator(ui_name, namespace)
    
    # 添加元素
    root_container = generator.add_element("VisualElement", f"{ui_name}Container", 
                                           attributes={"class": f"{ui_name.lower()}-container"})
    
    for elem in elements:
        generator.add_element(
            elem["type"], 
            elem["name"],
            parent=root_container["name"],
            text=elem.get("text"),
            binding_path=elem.get("binding_path")
        )
        
        # 按钮自动添加点击事件
        if elem["type"] == "Button":
            handler_name = f"On{elem['name'].title().replace('_', '')}Clicked"
            generator.add_event(elem["name"], "Click", handler_name)
    
    # 生成文件
    os.makedirs(output_dir, exist_ok=True)
    
    files = {}
    
    # UXML
    uxml_content = generator.generate_uxml()
    uxml_path = os.path.join(output_dir, f"{ui_name}.uxml")
    with open(uxml_path, 'w', encoding='utf-8') as f:
        f.write(uxml_content)
    files["uxml"] = uxml_path
    
    # USS
    uss_content = generator.generate_uss(style)
    uss_path = os.path.join(output_dir, f"{ui_name}.uss")
    with open(uss_path, 'w', encoding='utf-8') as f:
        f.write(uss_content)
    files["uss"] = uss_path
    
    # C# ViewModel
    cs_content = generator.generate_viewmodel(pattern)
    cs_path = os.path.join(output_dir, f"{ui_name}ViewModel.cs" if pattern == "mvvm" else f"{ui_name}Presenter.cs")
    with open(cs_path, 'w', encoding='utf-8') as f:
        f.write(cs_content)
    files["viewmodel"] = cs_path
    
    # Model (如果MVVM)
    if pattern == "mvvm":
        model_content = generator.generate_model()
        model_path = os.path.join(output_dir, f"{ui_name}Model.cs")
        with open(model_path, 'w', encoding='utf-8') as f:
            f.write(model_content)
        files["model"] = model_path
    
    return files


# ============================================================
# CLI入口
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description="Unity UI Toolkit Generator - AI驱动的UXML/USS/C#生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
            示例:
              # 生成登录界面
              python unity_uixml_generator.py --name Login --desc "用户名输入框、密码输入框、登录按钮、注册链接" --out ./Output/Login
              
              # 生成背包界面（奇幻风格）
              python unity_uixml_generator.py --name Inventory --yaml inventory.yaml --style game_fantasy --out ./Output/Inventory
              
              # 使用MVP模式
              python unity_uixml_generator.py --name Settings --desc "音量滑块、画质下拉框、保存按钮" --pattern mvp
        """)
    )
    
    parser.add_argument("--name", required=True, help="UI名称（如Login, Inventory）")
    parser.add_argument("--desc", help="UI描述（中文或英文）")
    parser.add_argument("--yaml", help="YAML规格文件路径")
    parser.add_argument("--out", default="./Output", help="输出目录")
    parser.add_argument("--pattern", choices=["mvvm", "mvp"], default="mvvm", help="设计模式")
    parser.add_argument("--style", choices=list(STYLE_PRESETS.keys()), default="dark", help="样式预设")
    parser.add_argument("--namespace", default="Game.UI", help="C#命名空间")
    
    args = parser.parse_args()
    
    # 获取描述
    if args.yaml:
        spec = UIParser.parse_yaml(args.yaml)
        description = spec.get("description", "")
    else:
        description = args.desc or ""
    
    if not description:
        print("错误：请提供 --desc 或 --yaml 参数")
        return 1
    
    # 生成
    print(f"🚀 生成 {args.name} UI组件...")
    print(f"   模式: {args.pattern.upper()}")
    print(f"   样式: {args.style}")
    print()
    
    files = generate_ui(
        ui_name=args.name,
        description=description,
        output_dir=args.out,
        pattern=args.pattern,
        style=args.style,
        namespace=args.namespace
    )
    
    print("✅ 生成完成:")
    for file_type, file_path in files.items():
        print(f"   [{file_type}] {file_path}")
    
    return 0


if __name__ == "__main__":
    exit(main())
