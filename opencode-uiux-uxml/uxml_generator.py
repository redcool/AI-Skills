#!/usr/bin/env python3
"""
UXML Generator with Design Token Support
==========================================
从设计 Token + 自然语言描述 → UXML + USS + C# ViewModel + Model

用法：
  python uxml_generator.py --tokens dark_glassmorphism --name Login --desc "用户名输入框、密码输入框、登录按钮"
  python uxml_generator.py --tokens my_theme.json --name Inventory --yaml spec.yaml

与 opencode-unity-uixml 的区别：
  - 接受设计 Token（色板/字体/间距/圆角/阴影）
  - USS 输出由 Token 驱动，不再是硬编码 4 种预设
  - 组件尺寸/间距来自 Token 中的 components 规范
  - 支持 MVVM 和 MVP 两种模式
"""

import json
import os
import re
import sys
import argparse
import copy
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple

# 导入设计 Token 系统
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from design_tokens import DesignTokenManager, PRESETS, COLOR_PALETTES


# ============================================================
# 中文组件映射
# ============================================================

COMPONENT_MAP = {
    # 容器
    "容器": "VisualElement", "面板": "VisualElement", "卡片": "VisualElement",
    "区域": "VisualElement", "分组": "VisualElement", "布局": "VisualElement",
    "滚动区域": "ScrollView", "滚动容器": "ScrollView", "列表容器": "ScrollView",
    "行": "VisualElement", "列": "VisualElement",
    "模态框": "VisualElement", "弹窗": "VisualElement", "对话框": "VisualElement",
    "标签页容器": "VisualElement",

    # 输入
    "输入框": "TextField", "文本框": "TextField", "文本输入": "TextField",
    "密码框": "TextField", "密码输入": "TextField",
    "搜索框": "TextField", "搜索输入": "TextField",
    "多行输入": "TextField", "多行文本框": "TextField",
    "数字输入": "IntegerField", "数字框": "IntegerField",
    "浮点输入": "FloatField", "滑块": "Slider", "滑动条": "Slider",
    "下拉框": "DropdownField", "选择器": "DropdownField", "下拉选择": "DropdownField",
    "开关": "Toggle", "复选框": "Toggle", "勾选框": "Toggle",
    "颜色选择": "ColorField", "曲线编辑": "CurveField",
    "整数滑块": "SliderInt",

    # 按钮
    "按钮": "Button", "登录按钮": "Button", "提交按钮": "Button",
    "取消按钮": "Button", "确认按钮": "Button", "返回按钮": "Button",
    "保存按钮": "Button", "删除按钮": "Button", "搜索按钮": "Button",
    "关闭按钮": "Button", "刷新按钮": "Button", "下载按钮": "Button",
    "上传按钮": "Button", "播放按钮": "Button", "暂停按钮": "Button",
    "图标按钮": "Button",

    # 显示
    "标题": "Label", "文字": "Label", "文本": "Label", "标签": "Label",
    "副标题": "Label", "说明文字": "Label", "提示文字": "Label",
    "图标": "Image", "图片": "Image", "头像": "Image",
    "分隔线": "VisualElement", "分割线": "VisualElement",
    "进度条": "ProgressBar", "加载指示": "ProgressBar",
    "状态栏": "VisualElement", "通知": "Label",
    "徽章": "Label", "计数器": "Label",

    # 复合
    "列表": "ListView", "列表项": "VisualElement",
    "树形视图": "TreeView", "折叠面板": "Foldout",
    "折叠": "Foldout", "展开收起": "Foldout",
    "标签页": "TabView", "选项卡": "TabView",
    "工具栏": "Toolbar", "导航栏": "VisualElement",
    "侧边栏": "VisualElement", "侧栏": "VisualElement",
    "菜单栏": "ToolbarMenu", "菜单项": "ToolbarMenuItem",
    "表格": "MultiColumnListView",

    # 游戏
    "血条": "ProgressBar", "生命条": "ProgressBar", "蓝条": "ProgressBar",
    "魔法条": "ProgressBar", "经验条": "ProgressBar", "体力条": "ProgressBar",
    "能量条": "ProgressBar", "技能栏": "VisualElement", "快捷栏": "VisualElement",
    "背包格子": "VisualElement", "物品格子": "VisualElement",
    "小地图": "Image", "准星": "Image", "瞄准镜": "Image",
    "伤害数字": "Label", "战斗日志": "ListView",
    "任务追踪": "VisualElement", "技能图标": "Image",
    "属性面板": "VisualElement", "角色面板": "VisualElement",
}

# 英文映射
COMPONENT_MAP_EN = {
    "container": "VisualElement", "panel": "VisualElement", "card": "VisualElement",
    "section": "VisualElement", "group": "VisualElement", "row": "VisualElement",
    "column": "VisualElement", "modal": "VisualElement", "dialog": "VisualElement",
    "scroll": "ScrollView", "scrollview": "ScrollView",
    "input": "TextField", "textfield": "TextField", "text_field": "TextField",
    "password": "TextField", "search": "TextField",
    "textarea": "TextField", "number": "IntegerField", "float": "FloatField",
    "slider": "Slider", "dropdown": "DropdownField", "select": "DropdownField",
    "toggle": "Toggle", "checkbox": "Toggle", "switch": "Toggle",
    "button": "Button", "icon_button": "Button",
    "label": "Label", "text": "Label", "heading": "Label", "title": "Label",
    "subtitle": "Label", "icon": "Image", "image": "Image", "avatar": "Image",
    "divider": "VisualElement", "separator": "VisualElement",
    "progress": "ProgressBar", "progress_bar": "ProgressBar",
    "hp_bar": "ProgressBar", "mp_bar": "ProgressBar", "xp_bar": "ProgressBar",
    "list": "ListView", "tree": "TreeView", "foldout": "Foldout",
    "tab": "VisualElement", "toolbar": "Toolbar",
    "sidebar": "VisualElement", "navbar": "VisualElement",
    "table": "MultiColumnListView",
    "inventory_slot": "VisualElement", "skill_bar": "VisualElement",
    "minimap": "Image", "crosshair": "Image",
    "notification": "Label", "badge": "Label",
}


# ============================================================
# UI 解析器
# ============================================================

class UIParser:
    """将自然语言 UI 描述解析为结构化组件列表。"""

    def __init__(self, tokens: Dict):
        self.tokens = tokens

    def parse(self, desc: str) -> List[Dict]:
        """解析中文/英文描述为组件列表。"""
        components = []
        items = re.split(r'[，,、；;\n]+', desc)
        for item in items:
            item = item.strip()
            if not item:
                continue
            comp = self._match_component(item)
            components.append(comp)
        return components

    def _match_component(self, item: str) -> Dict:
        """匹配单个组件。"""
        # 先精确匹配
        if item in COMPONENT_MAP:
            return self._build_component(item, COMPONENT_MAP[item])
        if item.lower() in COMPONENT_MAP_EN:
            return self._build_component(item, COMPONENT_MAP_EN[item.lower()])

        # 模糊匹配
        for key, uxtype in COMPONENT_MAP.items():
            if key in item:
                return self._build_component(item, uxtype)

        for key, uxtype in COMPONENT_MAP_EN.items():
            if key in item.lower():
                return self._build_component(item, uxtype)

        # 默认为标签
        return self._build_component(item, "Label")

    def _build_component(self, name: str, uxtype: str) -> Dict:
        """构建组件定义。"""
        # 生成变量名
        var_name = self._to_var_name(name)
        return {
            "name": name,
            "var_name": var_name,
            "uxtype": uxtype,
            "binding": self._default_binding(uxtype, var_name),
            "class_name": f"uxml-{var_name}",
        }

    def _to_var_name(self, name: str) -> str:
        """将中文名转为合法变量名。"""
        # 移除常见修饰词
        name = re.sub(r'^(我的|自定义|大|小|中)', '', name)
        # 中文 → 拼音映射（常见词）
        cn_map = {
            "用户名": "username", "密码": "password", "登录": "login",
            "注册": "register", "提交": "submit", "取消": "cancel",
            "确认": "confirm", "返回": "back", "保存": "save",
            "删除": "delete", "搜索": "search", "关闭": "close",
            "刷新": "refresh", "标题": "title", "副标题": "subtitle",
            "说明": "description", "提示": "hint", "图标": "icon",
            "头像": "avatar", "图片": "image", "进度": "progress",
            "血条": "hpBar", "蓝条": "mpBar", "经验条": "xpBar",
            "体力条": "staminaBar", "技能": "skill", "背包": "inventory",
            "物品": "item", "装备": "equipment", "属性": "attribute",
            "设置": "settings", "音量": "volume", "画质": "quality",
            "语言": "language", "通知": "notification", "消息": "message",
            "邮箱": "email", "昵称": "nickname", "等级": "level",
            "金币": "gold", "钻石": "diamond", "积分": "points",
        }
        for cn, en in cn_map.items():
            if cn in name:
                return en

        # 纯英文
        if re.match(r'^[a-zA-Z_]', name):
            return re.sub(r'[^a-zA-Z0-9_]', '_', name).lower()

        # fallback
        return f"comp_{abs(hash(name)) % 10000}"

    def _default_binding(self, uxtype: str, var_name: str) -> Optional[Dict]:
        """根据组件类型返回默认绑定配置。"""
        bindings = {
            "TextField": {"property": "value", "type": "string"},
            "IntegerField": {"property": "value", "type": "int"},
            "FloatField": {"property": "value", "type": "float"},
            "Slider": {"property": "value", "type": "float"},
            "SliderInt": {"property": "value", "type": "int"},
            "Toggle": {"property": "value", "type": "bool"},
            "DropdownField": {"property": "index", "type": "int"},
            "ProgressBar": {"property": "value", "type": "float"},
            "Button": {"event": "clicked", "type": "event"},
            "Label": {"property": "text", "type": "string"},
            "Image": {"property": "image", "type": "Texture2D"},
        }
        return bindings.get(uxtype)


# ============================================================
# UXML 生成器
# ============================================================

class UXMLGenerator:
    """从 Token + 组件列表生成 UXML/USS/C#。"""

    def __init__(self, tokens: Dict, pattern: str = "mvvm"):
        self.tokens = tokens
        self.pattern = pattern  # mvvm or mvp
        self.colors = tokens.get("colors", {})
        self.typo = tokens.get("typography", {})
        self.spacing = tokens.get("spacing", {})
        self.radius = tokens.get("radius", {})
        self.shadow = tokens.get("shadow", {})
        self.animation = tokens.get("animation", {})
        self.components_spec = tokens.get("components", {})
        self.meta = tokens.get("meta", {})

    def generate(self, name: str, components: List[Dict], layout: str = "vertical") -> Dict[str, str]:
        """生成完整文件集合。"""
        return {
            f"{name}.uxml": self._gen_uxml(name, components, layout),
            f"{name}.uss": self._gen_uss(name, components),
            f"{name}ViewModel.cs": self._gen_viewmodel(name, components),
            f"{name}Model.cs": self._gen_model(name, components) if self.pattern == "mvvm" else "",
        }

    # ----------------------------------------------------------
    # UXML
    # ----------------------------------------------------------

    def _gen_uxml(self, name: str, components: List[Dict], layout: str) -> str:
        """生成 UXML 文件。"""
        direction = "column" if layout == "vertical" else "row"
        lines = [
            '<ui:UXML xmlns:ui="UnityEngine.UIElements" xmlns:uie="UnityEditor.UIElements">',
            f'  <Style src="{name}.uss" />',
            f'  <ui:VisualElement class="{self._css_class(name)}-root" style="flex-direction: {direction};">',
        ]

        for comp in components:
            lines.append(self._gen_uxml_component(comp, indent=4))

        lines.append("  </ui:VisualElement>")
        lines.append("</ui:UXML>")
        return "\n".join(lines)

    def _gen_uxml_component(self, comp: Dict, indent: int = 4) -> str:
        """生成单个组件的 UXML。"""
        pad = " " * indent
        uxtype = comp["uxtype"]
        cls = comp["class_name"]
        var = comp["var_name"]
        binding = comp.get("binding")

        # 组件特化属性
        attrs = {}
        if uxtype == "TextField" and "密码" in comp["name"]:
            attrs["is-password"] = "true"
        if uxtype == "TextField":
            attrs["placeholder-text"] = f'"{comp["name"]}"'
        if uxtype == "Label":
            attrs["text"] = f'"{comp["name"]}"'
        if uxtype == "ProgressBar":
            attrs["title"] = f'"{comp["name"]}"'
            attrs["low-value"] = "0"
            attrs["high-value"] = "100"

        # 数据绑定属性
        binding_attr = ""
        if binding and self.pattern == "mvvm" and "property" in binding:
            binding_attr = f' binding-{binding["property"]}="{{{var}}}"'

        attr_str = ""
        for k, v in attrs.items():
            attr_str += f" {k}={v}"

        # 自闭合 vs 子元素
        void_elements = {"Button", "Label", "Image", "ProgressBar", "Toggle", "Slider",
                         "SliderInt", "IntegerField", "FloatField", "DropdownField", "ColorField", "CurveField"}
        if uxtype in void_elements:
            return f'{pad}<ui:{uxtype} name="{var}" class="{cls}"{attr_str}{binding_attr} />'
        else:
            return f'{pad}<ui:{uxtype} name="{var}" class="{cls}"{attr_str}{binding_attr}></ui:{uxtype}>'

    # ----------------------------------------------------------
    # USS
    # ----------------------------------------------------------

    def _gen_uss(self, name: str, components: List[Dict]) -> str:
        """生成 USS 文件，完全由 Token 驱动。"""
        c = self.colors
        t = self.typo
        s = self.spacing
        r = self.radius
        sh = self.shadow
        anim = self.animation
        cs = self.components_spec

        lines = []
        lines.append(f"/* ============================================")
        lines.append(f"   {name} — {self.meta.get('name', 'Custom')} Theme")
        lines.append(f"   Preset: {self.meta.get('preset', 'custom')}")
        lines.append(f"   ============================================ */")
        lines.append("")

        # 根容器
        root_cls = self._css_class(name)
        lines.append(f".{root_cls}-root {{")
        lines.append(f"  background-color: {c.get('background', '#1A1A2E')};")
        lines.append(f"  color: {c.get('on_background', '#E0E0E0')};")
        lines.append(f"  font-family: \"{t.get('body', {}).get('family', 'Noto Sans SC')}\";")
        lines.append(f"  font-size: {t.get('body', {}).get('sizes', {}).get('md', 14)}px;")
        lines.append(f"  padding: {s.get('lg', 16)}px;")
        lines.append(f"  flex-grow: 1;")
        lines.append("}")
        lines.append("")

        # 通用卡片/容器
        lines.append(f".{root_cls}-card {{")
        lines.append(f"  background-color: {c.get('card', c.get('surface', '#252540'))};")
        lines.append(f"  border-color: {c.get('border', '#3A3A5C')};")
        lines.append(f"  border-width: 1px;")
        lines.append(f"  border-radius: {r.get('md', 6)}px;")
        lines.append(f"  padding: {cs.get('card', {}).get('padding', 16)}px;")
        if sh.get("md") and sh["md"] != "none":
            lines.append(f"  /* box-shadow: {sh['md']}; */  /* USS limited shadow support */")
        lines.append("}")
        lines.append("")

        # 各组件样式
        for comp in components:
            lines.extend(self._gen_uss_component(comp, root_cls))
            lines.append("")

        # 按钮交互状态
        lines.extend(self._gen_button_states(root_cls))
        lines.append("")

        # 输入框焦点状态
        lines.extend(self._gen_input_focus(root_cls))
        lines.append("")

        # 动画
        if anim.get("duration_ms", 0) > 0:
            lines.append(f"/* Transitions */")
            lines.append(f".{root_cls}-root * {{")
            lines.append(f"  transition-duration: {anim['duration_ms']}ms;")
            lines.append(f"}}")
            lines.append("")

        return "\n".join(lines)

    def _gen_uss_component(self, comp: Dict, root_cls: str) -> List[str]:
        """生成单个组件的 USS。"""
        c = self.colors
        t = self.typo
        s = self.spacing
        r = self.radius
        cs = self.components_spec
        cls = comp["class_name"]
        uxtype = comp["uxtype"]

        lines = [f".{cls} {{"]

        if uxtype == "TextField":
            inp = cs.get("input", {})
            lines.append(f"  height: {inp.get('height', 36)}px;")
            lines.append(f"  padding-left: {inp.get('padding_h', 12)}px;")
            lines.append(f"  padding-right: {inp.get('padding_h', 12)}px;")
            lines.append(f"  background-color: {c.get('surface_variant', c.get('surface', '#1E1E36'))};")
            lines.append(f"  border-color: {c.get('border', '#3A3A5C')};")
            lines.append(f"  border-width: 1px;")
            lines.append(f"  border-radius: {r.get('sm', 4)}px;")
            lines.append(f"  color: {c.get('on_surface', '#E0E0E0')};")
            lines.append(f"  font-size: {t.get('body', {}).get('sizes', {}).get('md', 14)}px;")
            lines.append(f"  margin-bottom: {s.get('sm', 8)}px;")

        elif uxtype == "Button":
            btn = cs.get("button", {})
            lines.append(f"  height: {btn.get('height', 36)}px;")
            lines.append(f"  padding-left: {btn.get('padding_h', 16)}px;")
            lines.append(f"  padding-right: {btn.get('padding_h', 16)}px;")
            lines.append(f"  background-color: {c.get('primary', '#6366F1')};")
            lines.append(f"  border-radius: {r.get('md', 6)}px;")
            lines.append(f"  color: {c.get('on_primary', '#FFFFFF')};")
            lines.append(f"  font-size: {t.get('body', {}).get('sizes', {}).get('md', 14)}px;")
            lines.append(f"  font-weight: bold;")
            lines.append(f"  margin-top: {s.get('sm', 8)}px;")
            lines.append(f"  align-self: flex-start;")
            # 删除/危险按钮
            if "删除" in comp["name"] or "danger" in comp["var_name"].lower():
                lines.append(f"  background-color: {c.get('error', '#EF4444')};")

        elif uxtype == "Label":
            lines.append(f"  color: {c.get('on_surface', '#E0E0E0')};")
            if "标题" in comp["name"] or "title" in comp["var_name"].lower():
                lines.append(f"  font-size: {t.get('heading', {}).get('sizes', {}).get('h2', 24)}px;")
                lines.append(f"  font-weight: bold;")
                lines.append(f"  margin-bottom: {s.get('md', 12)}px;")
            elif "副标题" in comp["name"]:
                lines.append(f"  font-size: {t.get('heading', {}).get('sizes', {}).get('h4', 18)}px;")
                lines.append(f"  margin-bottom: {s.get('sm', 8)}px;")
            else:
                lines.append(f"  font-size: {t.get('body', {}).get('sizes', {}).get('md', 14)}px;")

        elif uxtype == "ProgressBar":
            lines.append(f"  height: {cs.get('hud', {}).get('bar_height', 8)}px;")
            lines.append(f"  background-color: {c.get('surface_variant', '#1E1E36')};")
            lines.append(f"  border-radius: {r.get('xs', 2)}px;")
            # 根据类型选色
            var = comp["var_name"]
            if "hp" in var or "血" in comp["name"] or "生命" in comp["name"]:
                lines.append(f"  --unity-progress-bar-color: {c.get('error', '#EF4444')};")
            elif "mp" in var or "蓝" in comp["name"] or "魔法" in comp["name"]:
                lines.append(f"  --unity-progress-bar-color: {c.get('info', '#3B82F6')};")
            elif "xp" in var or "经验" in comp["name"]:
                lines.append(f"  --unity-progress-bar-color: {c.get('success', '#10B981')};")
            else:
                lines.append(f"  --unity-progress-bar-color: {c.get('primary', '#6366F1')};")

        elif uxtype == "Toggle":
            lines.append(f"  margin-bottom: {s.get('xs', 4)}px;")
            lines.append(f"  color: {c.get('on_surface', '#E0E0E0')};")

        elif uxtype == "Slider":
            lines.append(f"  height: 24px;")
            lines.append(f"  margin-bottom: {s.get('sm', 8)}px;")

        elif uxtype == "DropdownField":
            inp = cs.get("input", {})
            lines.append(f"  height: {inp.get('height', 36)}px;")
            lines.append(f"  background-color: {c.get('surface_variant', '#1E1E36')};")
            lines.append(f"  border-color: {c.get('border', '#3A3A5C')};")
            lines.append(f"  border-width: 1px;")
            lines.append(f"  border-radius: {r.get('sm', 4)}px;")
            lines.append(f"  margin-bottom: {s.get('sm', 8)}px;")

        elif uxtype == "Foldout":
            lines.append(f"  background-color: {c.get('surface', '#252540')};")
            lines.append(f"  border-radius: {r.get('sm', 4)}px;")
            lines.append(f"  margin-bottom: {s.get('xs', 4)}px;")
            lines.append(f"  padding: {s.get('sm', 8)}px;")

        elif uxtype == "ScrollView":
            lines.append(f"  flex-grow: 1;")
            lines.append(f"  background-color: {c.get('surface', '#252540')};")
            lines.append(f"  border-radius: {r.get('sm', 4)}px;")

        elif uxtype == "ListView":
            lines.append(f"  flex-grow: 1;")
            lines.append(f"  background-color: {c.get('surface', '#252540')};")

        elif uxtype == "VisualElement":
            lines.append(f"  padding: {s.get('sm', 8)}px;")

        elif uxtype == "Image":
            lines.append(f"  width: 32px;")
            lines.append(f"  height: 32px;")

        lines.append("}")
        return lines

    def _gen_button_states(self, root_cls: str) -> List[str]:
        """按钮交互状态。"""
        c = self.colors
        lines = [
            f".{root_cls}-root Button:hover {{",
            f"  background-color: {c.get('primary_variant', c.get('primary', '#4F46E5'))};",
            f"}}",
            f".{root_cls}-root Button:active {{",
            f"  background-color: {c.get('primary_variant', c.get('primary', '#4F46E5'))};",
            f"  opacity: 0.85;",
            f"}}",
            f".{root_cls}-root Button:disabled {{",
            f"  background-color: {c.get('disabled_bg', '#1E293B')};",
            f"  color: {c.get('disabled', '#475569')};",
            f"}}",
        ]
        return lines

    def _gen_input_focus(self, root_cls: str) -> List[str]:
        """输入框焦点状态。"""
        c = self.colors
        lines = [
            f".{root_cls}-root TextField:focus {{",
            f"  border-color: {c.get('border_focus', c.get('primary', '#6366F1'))};",
            f"  border-width: 2px;",
            f"}}",
        ]
        return lines

    # ----------------------------------------------------------
    # C# ViewModel / Presenter
    # ----------------------------------------------------------

    def _gen_viewmodel(self, name: str, components: List[Dict]) -> str:
        """生成 C# ViewModel（MVVM）或 Presenter（MVP）。"""
        if self.pattern == "mvvm":
            return self._gen_viewmodel_mvvm(name, components)
        else:
            return self._gen_presenter_mvp(name, components)

    def _gen_viewmodel_mvvm(self, name: str, components: List[Dict]) -> str:
        """MVVM 模式 ViewModel。"""
        lines = [
            "using UnityEngine;",
            "using UnityEngine.UIElements;",
            "using Unity.Properties;",
            "",
            f"public class {name}ViewModel : MonoBehaviour",
            "{",
            "    [SerializeField] private UIDocument _document;",
            f"    private {name}Model _model = new {name}Model();",
            "",
            "    private void OnEnable()",
            "    {",
            "        var root = _document.rootVisualElement;",
        ]

        # 绑定代码
        for comp in components:
            binding = comp.get("binding")
            var = comp["var_name"]
            uxtype = comp["uxtype"]

            if not binding:
                continue

            if binding.get("type") == "event" and uxtype == "Button":
                lines.append(f'        root.Q<Button>("{var}").clicked += On{self._pascal(var)}Clicked;')
            elif "property" in binding:
                lines.append(f'        root.Q<{uxtype}>("{var}").{self._binding_property(binding["property"])} = _model.{self._pascal(var)};')

        lines.append("    }")
        lines.append("")

        # 事件处理
        for comp in components:
            binding = comp.get("binding")
            if binding and binding.get("type") == "event" and comp["uxtype"] == "Button":
                var = comp["var_name"]
                lines.append(f"    private void On{self._pascal(var)}Clicked()")
                lines.append("    {")
                lines.append(f"        Debug.Log(\"{comp['name']} clicked\");")
                lines.append("    }")
                lines.append("")

        lines.append("}")
        return "\n".join(lines)

    def _gen_presenter_mvp(self, name: str, components: List[Dict]) -> str:
        """MVP 模式 Presenter。"""
        lines = [
            "using UnityEngine;",
            "using UnityEngine.UIElements;",
            "",
            f"public class {name}Presenter : MonoBehaviour",
            "{",
            "    [SerializeField] private UIDocument _document;",
            "",
            "    private void OnEnable()",
            "    {",
            "        var root = _document.rootVisualElement;",
        ]

        for comp in components:
            binding = comp.get("binding")
            var = comp["var_name"]
            uxtype = comp["uxtype"]

            if not binding:
                continue

            if binding.get("type") == "event" and uxtype == "Button":
                lines.append(f'        root.Q<Button>("{var}").clicked += On{self._pascal(var)}Clicked;')
            elif "property" in binding:
                lines.append(f'        var _{var} = root.Q<{uxtype}>("{var}");')

        lines.append("    }")
        lines.append("")

        for comp in components:
            binding = comp.get("binding")
            if binding and binding.get("type") == "event" and comp["uxtype"] == "Button":
                var = comp["var_name"]
                lines.append(f"    private void On{self._pascal(var)}Clicked()")
                lines.append("    {")
                lines.append(f"        Debug.Log(\"{comp['name']} clicked\");")
                lines.append("    }")
                lines.append("")

        lines.append("}")
        return "\n".join(lines)

    # ----------------------------------------------------------
    # C# Model
    # ----------------------------------------------------------

    def _gen_model(self, name: str, components: List[Dict]) -> str:
        """MVVM 模式 Model。"""
        lines = [
            "using UnityEngine;",
            "using Unity.Properties;",
            "",
            f"public class {name}Model",
            "{",
        ]

        for comp in components:
            binding = comp.get("binding")
            if not binding or "property" not in binding:
                continue
            var = self._pascal(comp["var_name"])
            dtype = self._binding_cs_type(binding["type"])
            lines.append(f"    [CreateProperty]")
            lines.append(f"    public {dtype} {var} {{ get; set; }}")
            # 默认值
            defaults = {"string": '""', "int": "0", "float": "0f", "bool": "false"}
            default = defaults.get(dtype, "default")
            lines[-1] = lines[-1].rstrip() + f" = {default};"
            lines.append("")

        lines.append("}")
        return "\n".join(lines)

    # ----------------------------------------------------------
    # 辅助
    # ----------------------------------------------------------

    def _css_class(self, name: str) -> str:
        return re.sub(r'[^a-zA-Z0-9-]', '-', name.lower())

    def _pascal(self, s: str) -> str:
        return ''.join(w.capitalize() for w in re.split(r'[_\-\s]+', s))

    def _binding_property(self, prop: str) -> str:
        """UXML binding 属性 → C# 属性映射。"""
        mapping = {"value": "value", "text": "text", "index": "index", "image": "image"}
        return mapping.get(prop, prop)

    def _binding_cs_type(self, dtype: str) -> str:
        mapping = {"string": "string", "int": "int", "float": "float", "bool": "bool"}
        return mapping.get(dtype, "object")


# ============================================================
# YAML 规格解析（可选）
# ============================================================

def parse_yaml_spec(yaml_path: str) -> Tuple[str, List[Dict], str]:
    """解析 YAML 规格文件，返回 (name, components, layout)。"""
    try:
        import yaml
    except ImportError:
        print("Error: PyYAML not installed. Run: pip install pyyaml")
        sys.exit(1)

    with open(yaml_path, "r", encoding="utf-8") as f:
        spec = yaml.safe_load(f)

    name = spec.get("name", "Unnamed")
    layout = spec.get("layout", "vertical")
    components = []

    for item in spec.get("components", []):
        comp = {
            "name": item.get("name", ""),
            "var_name": item.get("var_name", item.get("name", "").lower()),
            "uxtype": item.get("type", "Label"),
            "binding": item.get("binding"),
            "class_name": item.get("class_name", f"uxml-{item.get('var_name', 'comp')}"),
        }
        if not comp["binding"]:
            parser = UIParser({})
            comp["binding"] = parser._default_binding(comp["uxtype"], comp["var_name"])
        components.append(comp)

    return name, components, layout


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="UXML Generator with Design Token Support",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # 使用预设
  python uxml_generator.py --tokens dark_glassmorphism --name Login --desc "用户名输入框、密码输入框、登录按钮"

  # 使用自定义 Token JSON
  python uxml_generator.py --tokens my_theme.json --name Inventory --desc "64格背包、详情面板、使用按钮"

  # MVP 模式
  python uxml_generator.py --tokens game_fantasy --name Settings --desc "音量滑块、画质下拉框" --pattern mvp

  # YAML 规格
  python uxml_generator.py --tokens cyber_neon --yaml spec.yaml --out ./Output
        """,
    )

    parser.add_argument("--tokens", required=True, help="预设名称或 Token JSON 文件路径")
    parser.add_argument("--name", help="界面名称（--desc 模式必填）")
    parser.add_argument("--desc", help="自然语言 UI 描述")
    parser.add_argument("--yaml", help="YAML 规格文件路径")
    parser.add_argument("--pattern", choices=["mvvm", "mvp"], default="mvvm", help="架构模式")
    parser.add_argument("--layout", choices=["vertical", "horizontal"], default="vertical", help="布局方向")
    parser.add_argument("--out", "-o", default="./Output", help="输出目录")
    parser.add_argument("--override", action="append", default=[], help="覆盖 Token，格式 key.subkey=value")

    args = parser.parse_args()

    # 加载 Token
    mgr = DesignTokenManager()
    if os.path.isfile(args.tokens):
        tokens = mgr.load(args.tokens)
    elif args.tokens in mgr.presets:
        tokens = mgr.load_preset(args.tokens)
    else:
        print(f"Error: '{args.tokens}' is neither a file nor a known preset.")
        print(f"Available presets: {', '.join(mgr.presets.keys())}")
        sys.exit(1)

    # 应用覆盖
    for override in args.override:
        key, value = override.split("=", 1)
        parts = key.split(".")
        obj = tokens
        for part in parts[:-1]:
            obj = obj.setdefault(part, {})
        obj[parts[-1]] = value

    # 解析组件
    if args.yaml:
        name, components, layout = parse_yaml_spec(args.yaml)
    elif args.desc and args.name:
        ui_parser = UIParser(tokens)
        components = ui_parser.parse(args.desc)
        name = args.name
        layout = args.layout
    else:
        parser.error("Must provide --name + --desc, or --yaml")

    # 生成
    gen = UXMLGenerator(tokens, pattern=args.pattern)
    files = gen.generate(name, components, layout)

    # 输出
    out_dir = os.path.join(args.out, name)
    os.makedirs(out_dir, exist_ok=True)

    # 同时保存 Token
    mgr.save(tokens, os.path.join(out_dir, "design_tokens.json"))

    for filename, content in files.items():
        if not content:
            continue
        path = os.path.join(out_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✓ {path}")

    print(f"\nDone! {len([c for c in files.values() if c])} files + design_tokens.json → {out_dir}")


if __name__ == "__main__":
    main()
