"""Export historical Markdown hypotheses as draft v1 contracts. No network or LLM."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re


def export(path: Path, repo_root: Path) -> list[dict]:
    relative = path.resolve().relative_to(repo_root.resolve()).as_posix()
    text = path.read_text(encoding='utf-8')
    match = re.search(r'> Generated: (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}) JST', text)
    if not match:
        raise ValueError('Generated timestamp missing; do not substitute export time for source age')
    observed = datetime.fromisoformat(f'{match[1]}T{match[2]}:00+09:00').isoformat()
    items = []
    for m in re.finditer(r'^## (\d+)\. ([^\n]+)\n(.*?)(?=^## \d+\.|\Z)', text, re.M | re.S):
        number, title, body = m.groups()
        def field(name):
            hit = re.search(rf'^- {name}: (.+)$', body, re.M)
            if not hit: raise ValueError(f'{title}: missing {name}')
            return hit[1].strip()
        pain = re.search(r'### 解決する痛み\n+(.+?)(?=\n###|\Z)', body, re.S)
        if not pain: raise ValueError(f'{title}: missing pain')
        locator = f'{relative}#{number}'
        key = hashlib.sha256(locator.encode()).hexdigest()[:12]
        items.append({'schema_version':1,'id':f'lazy-{key}','title':title.strip(),
          'target_user':field('対象ユーザー'),'problem':pain[1].strip(),'solution':field('一行で'),
          'kind':'tool','origin':{'repo':'kaionn/lazy-product-lab','locator':locator,
          'url':f'https://github.com/kaionn/lazy-product-lab/blob/main/{relative}',
          'observed_at':observed,'classification':'hypothesis'},'evidence':[],
          'build':{'core_flow':field('一行で'),'demo_input':'要レビュー: 合成入力を指定',
          'acceptance':[],'non_goals':['公開・投稿・決済・実データ収集'],
          'max_minutes':120,'max_iterations':3,'allowed_tools':['local-files','local-tests']},
          'distribution':{'channel':'要レビュー','audience':field('対象ユーザー'),'rationale':'要レビュー: 到達可能な配布先を確認'},
          'measurement':{'primary_event':'tool_use','graduate_threshold':20,'observation_days':21,
          'minimum_exposures':20,'kill_below':2,'stop_rule':'要レビュー: 計測確認と十分な露出の後に判定'}})
    if not items: raise ValueError('No candidates found')
    return items


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',type=Path)
    parser.add_argument('--repo-root',type=Path,default=Path(__file__).resolve().parents[1])
    args=parser.parse_args(argv)
    print(json.dumps(export(args.source,args.repo_root),ensure_ascii=False,indent=2))
    return 0

if __name__=='__main__':
    try: raise SystemExit(main())
    except (ValueError,OSError) as exc: raise SystemExit(str(exc))
