# 문제은행 검사: python3 check.py
# 1) 형식 검사 (보기 4개, 정답 번호, 대제목, 문항 수, 보기별 풀이 why: 정답 칸만 비우고 보기 번호 대신 내용으로)
# 2) check가 달린 문제는 R로 실제 실행해서 정답 보기와 결과가 같은지 확인 (Rscript 필요)
#    - r:  cat()으로 출력한 결과가 정답 보기와 같고, 나머지 보기와는 달라야 함
#    - rs: 보기 4개의 R 코드 중 정답 번호의 결과만 나머지 셋과 달라야 함
# 3) 공부 탭 예시: code를 R로 실행한 화면 출력이 out(글자)과 같은지 확인
# R 버전에 따라 결과가 달라지는 코드(난수 sample 등)는 문제로 쓰지 않기
import collections, json, os, re, subprocess, sys

src = subprocess.run(["node", "-e", "global.window={};require('./questions.js');"
                      "console.log(JSON.stringify({u:window.ADSP_UNITS,q:window.ADSP_QUESTIONS,t:window.ADSP_TRAPS||[],s:window.ADSP_STUDY||[]}))"],
                     capture_output=True, text=True, check=True, cwd=sys.path[0]).stdout
data = json.loads(src)
units = {u["id"]: u for u in data["u"]}
qs = data["q"]
traps = {t["id"] for t in data["t"]}
errors = []

def run(code):
    p = subprocess.run(["Rscript", "--vanilla", "-e", code], capture_output=True, text=True, timeout=60,
                       env={**os.environ, "LC_ALL": "C.UTF-8"})  # 한글 변수 이름을 읽으려면 UTF-8
    if p.returncode: raise RuntimeError((p.stderr.strip().splitlines() or ["R 오류"])[-1])
    return p.stdout

norm = lambda t: re.sub(r"\s+", " ", str(t)).strip()
ids = collections.Counter(q["id"] for q in qs)
checked = 0
for q in qs:
    where = q.get("id", "?")
    need = ["id", "unit", "freq", "subject", "topic", "q", "options", "answer", "exp"]
    miss = [k for k in need if not q.get(k)]
    if miss: errors.append(f"{where}: 빠진 항목 {miss}"); continue
    if ids[q["id"]] > 1: errors.append(f"{where}: id 중복")
    if q["unit"] not in units: errors.append(f"{where}: 없는 대제목 {q['unit']}")
    elif units[q["unit"]]["subject"] != q["subject"]: errors.append(f"{where}: 과목과 대제목이 안 맞음")
    if q.get("trap") and q["trap"] not in traps: errors.append(f"{where}: 없는 함정 {q['trap']}")
    if q["freq"] not in ("high", "mid", "low"): errors.append(f"{where}: freq 값 오류")
    o = q["options"]
    if len(o) != 4 or len({norm(x) for x in o}) != 4: errors.append(f"{where}: 보기는 서로 다른 4개여야 함")
    if q["answer"] not in (1, 2, 3, 4): errors.append(f"{where}: 정답 번호 오류")
    w = q.get("why")
    if not (isinstance(w, list) and len(w) == 4 and all(isinstance(x, str) for x in w)):
        errors.append(f"{where}: why는 보기 4개에 맞춘 풀이 4칸이어야 함")
    elif [bool(x.strip()) for x in w] != [i + 1 != q["answer"] for i in range(4)]:
        errors.append(f"{where}: why는 정답 칸만 비우고 나머지 보기 풀이를 채워야 함")
    elif any(re.search(r"[①②③④]|[1-4]번 보기", x) for x in w):
        errors.append(f"{where}: why에는 보기 번호 대신 내용으로 적기")
    ck = q.get("check")
    if not ck: continue
    try:
        if "r" in ck:
            got = norm(run(ck["r"]))
            if got != norm(o[q["answer"] - 1]):
                errors.append(f"{where}: 실행 결과 [{got}] ≠ 정답 보기 [{o[q['answer'] - 1]}]")
            others = [i + 1 for i, x in enumerate(o) if i + 1 != q["answer"] and norm(x) == got]
            if others: errors.append(f"{where}: 다른 보기 {others}도 실행 결과와 같음")
        else:
            res = [norm(run(c)) for c in ck["rs"]]
            odd = [i + 1 for i, r in enumerate(res) if res.count(r) == 1]
            if odd != [q["answer"]] or len(set(res)) != 2:
                errors.append(f"{where}: 보기별 결과 {res} → 다른 하나가 정답 {q['answer']}번이 아님")
        checked += 1
    except Exception as e:
        errors.append(f"{where}: 실행 오류 {e}")

ran = 0
for l in data["s"]:
    if l.get("unit") not in units: errors.append(f"공부 {l['id']}: 없는 대제목 {l.get('unit')}")
    for k, ex in enumerate(l["ex"]):
        for name, t in ex.get("data", {}).items():
            if any(len(r) != len(t["cols"]) for r in t["rows"]): errors.append(f"공부 {l['id']} 예시 {k + 1}: {name} 칸 수가 안 맞음")
        if not (ex.get("code") and isinstance(ex.get("out"), str)): continue
        try:
            got = run(ex["code"]).rstrip()
            if got != ex["out"].rstrip(): errors.append(f"공부 {l['id']} 예시 {k + 1}: 실행 결과\n{got}\n≠ out\n{ex['out']}")
            ran += 1
        except Exception as e:
            errors.append(f"공부 {l['id']} 예시 {k + 1}: 실행 오류 {e}")
print(f"공부 탭: {len(data['s'])}개 설명, 예시 {ran}개 실행 확인")

# 문항 수와 정답 번호 분포. 실전은 실제 시험처럼 1과목 10, 2과목 10, 3과목 30문항
sets = collections.defaultdict(list)
for q in qs: sets[f"실전 {q['exam']}" if q.get("exam") else "함정" if q.get("trap") else "연습"].append(q)
for name, lst in sorted(sets.items()):
    by_subj = collections.Counter(q["subject"] for q in lst)
    ans = collections.Counter(q["answer"] for q in lst)
    print(f"{name}: {len(lst)}문항 (1과목 {by_subj[1]}, 2과목 {by_subj[2]}, 3과목 {by_subj[3]}) · 정답 분포 {dict(sorted(ans.items()))}")
    if name.startswith("실전") and (by_subj[1], by_subj[2], by_subj[3]) != (10, 10, 30):
        errors.append(f"{name}: 1과목 10, 2과목 10, 3과목 30문항이어야 함")
print(f"R 실행 검증 {checked}문항")
print("\n".join(errors) if errors else "문제 없음")
sys.exit(1 if errors else 0)
