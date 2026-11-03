#!/usr/bin/env python3
"""Render the full Markdown plan to exactly three A4 PNG pages; PDF is temporary."""
import argparse
from html import escape
from pathlib import Path
import re
import tempfile
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
import pypdfium2 as pdfium
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]

def inline(text):
    text = escape(text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    return text

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--font', type=Path, default=Path('/System/Library/Fonts/Supplemental/Arial.ttf'))
    parser.add_argument('--bold-font', type=Path, default=Path('/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
    args = parser.parse_args()
    for name,path in [('Body',args.font),('BodyBold',args.bold_font)]:
        pdfmetrics.registerFont(TTFont(name,str(path)))
    pdfmetrics.registerFontFamily('Body',normal='Body',bold='BodyBold',italic='Body',boldItalic='BodyBold')
    styles={
      'p':ParagraphStyle('p',fontName='Body',fontSize=10.5,leading=14,spaceAfter=7,textColor=colors.HexColor('#243447')),
      'h1':ParagraphStyle('h1',fontName='BodyBold',fontSize=19,leading=23,spaceAfter=12,textColor=colors.HexColor('#153b61')),
      'h2':ParagraphStyle('h2',fontName='BodyBold',fontSize=13,leading=17,spaceBefore=9,spaceAfter=7,textColor=colors.HexColor('#153b61')),
      'h3':ParagraphStyle('h3',fontName='BodyBold',fontSize=11,leading=14,spaceBefore=7,spaceAfter=6,textColor=colors.HexColor('#153b61')),
      'cell':ParagraphStyle('cell',fontName='Body',fontSize=9.2,leading=12,textColor=colors.HexColor('#243447')),
      'bullet':ParagraphStyle('bullet',fontName='Body',fontSize=10.5,leading=14,leftIndent=10,firstLineIndent=-8,spaceAfter=8,textColor=colors.HexColor('#243447'))
    }
    text=(ROOT/'Task1/transformation-plan.md').read_text()
    parts=text.split('<!-- pagebreak -->')
    assert len(parts)==3,'Expected exactly three explicit pages'
    story=[]
    for part_no,part in enumerate(parts):
        lines=part.strip().splitlines();i=0
        while i<len(lines):
            line=lines[i].strip();i+=1
            if not line: continue
            if line.startswith('|'):
                rows=[]
                while True:
                    if not re.fullmatch(r'[| :\-]+',line):
                        rows.append([Paragraph(inline(c.strip()),styles['cell']) for c in line.strip('|').split('|')])
                    if i>=len(lines) or not lines[i].strip().startswith('|'):break
                    line=lines[i].strip();i+=1
                table=Table(rows,colWidths=[58,110,163,172],repeatRows=1,hAlign='LEFT')
                table.setStyle(TableStyle([
                    ('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dce9f5')),
                    ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#f5f8fb'),colors.white]),
                    ('BOX',(0,0),(-1,-1),.4,colors.HexColor('#b5c6d8')),
                    ('INNERGRID',(0,0),(-1,-1),.3,colors.HexColor('#c9d4df')),
                    ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
                    ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
                story.extend([table,Spacer(1,8)]);continue
            style='p'
            for marker,key in [('### ','h3'),('## ','h2'),('# ','h1'),('- ','bullet')]:
                if line.startswith(marker):
                    line=('• ' if key=='bullet' else '')+line[len(marker):];style=key;break
            story.append(Paragraph(inline(line),styles[style]))
        if part_no<2:story.append(PageBreak())
    out=ROOT/'Task1/preview';out.mkdir(exist_ok=True)
    def footer(c,doc):
        c.setStrokeColor(colors.HexColor('#c9d4df'));c.line(46,39,A4[0]-46,39)
        c.setFont('Body',8);c.setFillColor(colors.HexColor('#52677c'))
        c.drawString(46,26,'FAST CARGO  /  Sprint 8  /  План трансформации')
        c.drawRightString(A4[0]-46,26,f'{doc.page} / 3')
    with tempfile.TemporaryDirectory(prefix='fastcargo-plan-') as temp:
        path=Path(temp)/'plan.pdf'
        doc=SimpleDocTemplate(str(path),pagesize=A4,leftMargin=46,rightMargin=46,topMargin=40,bottomMargin=52,title='Fast Cargo — План архитектурной трансформации')
        doc.build(story,onFirstPage=footer,onLaterPages=footer)
        reader=PdfReader(path)
        if len(reader.pages)!=3:raise RuntimeError(f'Plan overflow: {len(reader.pages)} pages, expected 3')
        # The explicit section boundaries must be retained, not merely the total count.
        for page,expected in zip(reader.pages,['1. Выгоды бизнеса','5. Transition Architecture','7. Дорожная карта']):
            if expected not in page.extract_text():raise RuntimeError(f'Unexpected pagination: {expected}')
        pdf=pdfium.PdfDocument(path)
        for i in range(len(pdf)):
            page=pdf[i];bitmap=page.render(scale=2)
            bitmap.to_pil().save(out/f'plan-page-{i+1}.png')
            bitmap.close();page.close()
        pdf.close()
    print('Plan: exactly 3 A4 pages; PNG exports written, temporary PDF removed.')
if __name__=='__main__':main()
