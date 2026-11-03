#!/usr/bin/env python3
"""Validate Sprint 8 deliverables; does not run production acceptance tests."""
from pathlib import Path
import re
from decimal import Decimal
from urllib.parse import unquote
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]

def main():
    errors=[]
    def require(ok,message):
        if not ok:errors.append(message)
    required=['README.md','Task1/README.md','Task1/transformation-plan.md',
              'Task2/README.md','Task2/stakeholder-matrix.md','Task2/objections.md',
              'Task2/architecture-rationale.md','Task3/README.md','Task3/operational-kpi.md',
              'Task3/ceo-conclusion.md','Task3/acceptance-tests.md',
              'sources/README.md','sources/as-is.png',
              'tools/README.md','tools/render_diagrams.py','tools/render_plan.py']
    for name in required:require((ROOT/name).is_file(),f'Missing: {name}')
    md_files=list(ROOT.rglob('*.md'))
    for path in md_files:
        text=path.read_text()
        require('\ufffd' not in text,f'Unicode replacement: {path}')
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',text):
            target=target.strip('<>')
            if re.match(r'[a-z]+://',target) or target.startswith('#'):continue
            target=unquote(target.split('#')[0])
            require((path.parent/target).exists(),f'Broken link: {path.relative_to(ROOT)} -> {target}')
    for ext in ('*.svg','*.pdf'):
        require(not list(ROOT.rglob(ext)),f'Unexpected final format: {ext}')
    diagrams=list(ROOT.glob('Task1/diagrams/*.puml'))
    require(len(diagrams)==3,'Expected three PlantUML diagrams')
    for path in diagrams:
        text=path.read_text()
        require(text.count('@startuml')==1 and text.count('@enduml')==1,f'Invalid delimiters: {path.name}')
        for inc in re.findall(r'^!include\s+(.+)$',text,re.M):
            require(not inc.startswith('http'),f'Remote dependency: {path.name}')
            require((path.parent/inc).is_file(),f'Missing include: {inc}')
        require(path.with_suffix('.png').is_file(),f'No PNG for {path.name}')
    png_files=list(ROOT.rglob('*.png'))
    for path in png_files:
        with Image.open(path) as img:
            require(img.format=='PNG',f'Not PNG: {path}')
            require(min(img.size)>100,f'Unexpected image dimensions: {path}')
            img.verify()
    pages=sorted(ROOT.glob('Task1/preview/plan-page-*.png'))
    require(len(pages)==3,'Expected three plan PNG pages')
    for p in pages:
        with Image.open(p) as im:require(im.size==(1191,1684),f'Unexpected A4 render: {p}')
    plan=(ROOT/'Task1/transformation-plan.md').read_text()
    require(plan.count('<!-- pagebreak -->')==2,'Expected two page breaks')
    for n in range(1,8):require(re.search(rf'^## {n}\. ',plan,re.M),f'Missing plan section {n}')
    matrix=(ROOT/'Task2/stakeholder-matrix.md').read_text()
    for role in ['Техлид','Архитектурный штаб','ИБ','Производственно-инфраструктурный','Операционный','Финансовый']:
        require(role in matrix,f'Missing stakeholder: {role}')
    for priority in ['Critical','Medium','Low']:require(priority in matrix,f'Missing priority: {priority}')
    objections=(ROOT/'Task2/objections.md').read_text()
    require(len(re.findall(r'^## [123]\. ',objections,re.M))==3,'Expected three objections')
    assert Decimal(365)*24*60*Decimal('.0005')==Decimal('262.8000')
    assert Decimal(30)*24*60*Decimal('.0005')==Decimal('21.6000')
    assert 3000*86400==259200000
    payload=Decimal(3000)*1024*86400/Decimal(10**9)
    assert payload==Decimal('265.4208')
    assert round(payload*3*3/1000,2)==Decimal('2.39')
    assert round(payload*3*3/1000/Decimal('.7'),2)==Decimal('3.41')
    root_index=(ROOT.parent/'README.md').read_text()
    require('Fast_Cargo/README.md' in root_index,'Missing root README entry')
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'PASS: {len(md_files)} Markdown files; 3 diagrams; 3 plan pages; {len(png_files)} PNG files; links, format, structure and arithmetic checked.')
    print('PlantUML rendering, pagination and visual review are separate checks; production KPI are not measured.')

if __name__=='__main__':main()
