#!/usr/bin/env python3
"""Computer_Vision wiki 链接检查器。

按 llm-wiki-ingest 协议实现：
  - 别名优先、其次 basename、再其次 路径前缀 basename（subroutine #4）
  - 统计断链（unresolved）与孤儿页（no inbound）
  - 统计有歧义的 basename（多文件同名）

用法: python3 cv_lint.py [wiki_root]
"""
import pathlib, re, sys, collections
import yaml

# 默认 wiki 根 = 本脚本所在目录的同级 notes/wiki，这样从任何 cwd 调用都能跑
DEFAULT_WIKI = pathlib.Path(__file__).resolve().parent.parent / 'notes' / 'wiki'
WIKI = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_WIKI

# [[target]] / [[target|alias]] / [[target#heading]] / ![[embed]]
LINK = re.compile(r'!?\[\[([^\]\[]+?)\]\]')
# 围栏代码块（``` 或 ~~~）与行内代码：里面的 [[ ]] 是 Python 嵌套列表 / numpy 索引，不是 wikilink
FENCE = re.compile(r'^(?P<f>```+|~~~+).*?^(?P=f)\s*$', re.M | re.S)
INLINE = re.compile(r'`[^`\n]*`')


def strip_code(t):
    """把代码块/行内代码替换成等长空白，保持行号不变。"""
    t = FENCE.sub(lambda m: re.sub(r'[^\n]', ' ', m.group(0)), t)
    return INLINE.sub(lambda m: ' ' * len(m.group(0)), t)


def load(p):
    t = p.read_text(encoding='utf-8')
    fm = {}
    if t.startswith('---\n'):
        end = t.index('\n---\n', 3)
        fm = yaml.safe_load(t[4:end]) or {}
    return t, fm


def main():
    notes = sorted(WIKI.rglob('*.md'))
    # 资源按**带扩展名的全名**索引：Obsidian 的 ![[X.png]] 写的是文件名，不是 stem
    assets = {p.name for p in WIKI.rglob('*') if p.is_file() and p.suffix != '.md'}

    by_stem = collections.defaultdict(list)
    by_alias = {}
    meta = {}
    for p in notes:
        _, fm = load(p)
        meta[p] = fm
        by_stem[p.stem].append(p)
        for a in (fm.get('aliases') or []):
            by_alias.setdefault(str(a), []).append(p)
        title = fm.get('title')
        if title:
            by_alias.setdefault(str(title), []).append(p)

    ambiguous = {k: v for k, v in by_stem.items() if len(v) > 1}
    # alias 与真实文件名撞车：Obsidian 解析到真实文件，alias 静默失效
    shadow = {k: v for k, v in by_alias.items() if k in by_stem and by_stem[k] != v}

    def resolve(raw):
        """返回 (命中路径列表, 解析方式)

        优先级必须是 stem > alias：当某页的 alias 恰好等于另一页的真实文件名时，
        Obsidian 解析到**真实文件**，alias 让位。所以 stem 必须先查。
        """
        t = raw.split('|', 1)[0].split('#', 1)[0].strip()
        if not t:
            return [], 'empty'
        base = t.split('/')[-1].strip()
        if base in by_stem:
            return by_stem[base], 'basename'
        if t in by_alias:
            return by_alias[t], 'alias'
        if base in by_alias:
            return by_alias[base], 'alias(base)'
        # 路径前缀：Obsidian 合法，basename-only 扫描器会误报，同样应视为已解析
        for p in notes:
            if str(p.relative_to(WIKI)).replace('.md', '') == t:
                return [p], 'path'
        if base in assets:
            return [], 'asset'
        return [], 'MISS'

    unresolved, inbound = [], collections.defaultdict(set)
    for p in notes:
        t, _ = load(p)
        for m in LINK.finditer(strip_code(t)):
            raw = m.group(1)
            hits, how = resolve(raw)
            if not hits:
                if how == 'asset':
                    inbound[('ASSET', raw.split('|')[-1].split('#')[0].strip())].add(p)
                else:
                    unresolved.append((p, raw, t[:m.start()].count('\n') + 1))
            else:
                for h in hits:
                    inbound[('NOTE', h)].add(p)

    orphans = [p for p in notes if not inbound[('NOTE', p)]]
    # 排除 MOC / index —— 它们是入口，天然容易没入链或承担全部入链
    def is_hub(p):
        fm = meta[p]
        return fm.get('type') in ('知识地图', '索引', '复习') or p.stem == 'index'

    print(f'== {WIKI} ==')
    print(f'笔记总数        : {len(notes)}')
    print(f'断链 unresolved : {len(unresolved)}')
    print(f'孤儿页 no-inbound: {len(orphans)}  (其中 hub {sum(map(is_hub, orphans))})')
    print(f'歧义 basename   : {len(ambiguous)}')
    print(f'alias 遮蔽真实页 : {len(shadow)}')
    print(f'被链接到的笔记  : {len([k for k in inbound if k[0]=="NOTE"])}')

    if ambiguous:
        print('\n-- 歧义 basename（同名多文件）--')
        for k, v in sorted(ambiguous.items()):
            print(f'   {k!r} -> {[str(x.relative_to(WIKI)) for x in v]}')

    if shadow:
        print('\n-- alias 遮蔽真实页（alias 与某页文件名相同，alias 永不生效）--')
        for k, v in sorted(shadow.items()):
            real = [str(x.relative_to(WIKI)) for x in by_stem[k]]
            print(f'   {k!r} 被声明为 {[str(x.relative_to(WIKI)) for x in v]} 的 alias，'
                  f'但它同时是真实页 {real} 的文件名')

    if unresolved:
        print('\n-- 断链 --')
        for p, raw, line in unresolved:
            print(f'   {p.relative_to(WIKI)}:{line}  [[{raw}]]')

    if orphans:
        print('\n-- 孤儿页（无入链）--')
        for p in orphans:
            tag = '  [hub]' if is_hub(p) else ''
            print(f'   {p.relative_to(WIKI)}{tag}')

    if not unresolved and not ambiguous:
        print('\n✓ 无断链、无歧义 basename')


if __name__ == '__main__':
    main()
