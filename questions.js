// ADsP 문제은행: 연습 문제와 실전 모의고사 (exam: 1)
// 필드: id, exam?(실전 회차), trap?(함정 id), unit(대제목), freq(출제빈도 high/mid/low, 최근 경향 기준 추정), subject(과목 1~3),
//       topic, q, code?(보여 줄 R 코드), options(보기 4개), answer(정답 번호 1~4), exp(해설),
//       why(보기별 풀이 4칸, options와 같은 순서, 정답 칸은 빈 문자열),
//       check?(정답 검증용 R 코드, 앱은 쓰지 않음. python3 check.py로 실행)
// 공부 탭(ADSP_STUDY): id, part, title, sum, unit, body[], ex[{say, data?, code?, out?}], tip
// 저작권: 모든 문제·보기·해설은 새로 작성했습니다. 기출·교재 문장을 옮겨 오지 않습니다.
window.ADSP_UNITS = [
  { "id": "data", "subject": 1, "freq": "high", "title": "데이터와 데이터베이스", "desc": "데이터의 유형, 지식 피라미드, 데이터베이스의 특징과 활용" },
  { "id": "bigdata", "subject": 1, "freq": "high", "title": "빅데이터의 가치와 위기", "desc": "빅데이터의 특징과 가치, 비즈니스 모델, 위기 요인과 통제 방안" },
  { "id": "science", "subject": 1, "freq": "mid", "title": "데이터 사이언스와 인사이트", "desc": "데이터 사이언스, 데이터 사이언티스트의 역량, 전략 인사이트" },
  { "id": "plan", "subject": 2, "freq": "high", "title": "분석 기획과 방법론", "desc": "분석 대상과 방법에 따른 분석 유형, 분석 방법론 모델" },
  { "id": "task", "subject": 2, "freq": "mid", "title": "분석 과제 발굴과 프로젝트 관리", "desc": "하향식·상향식 과제 발굴, 분석 프로젝트 관리" },
  { "id": "master", "subject": 2, "freq": "high", "title": "마스터 플랜과 거버넌스", "desc": "우선순위 평가, 로드맵, 분석 성숙도와 거버넌스 체계" },
  { "id": "rbasic", "subject": 3, "freq": "mid", "title": "R 기초", "desc": "R의 자료 구조와 기본 함수, 코드 실행 결과 읽기" },
  { "id": "mart", "subject": 3, "freq": "mid", "title": "데이터 마트·결측값·이상값", "desc": "데이터 마트, 요약 변수와 파생 변수, 결측값 처리와 이상값 찾기" },
  { "id": "stat", "subject": 3, "freq": "high", "title": "확률·추정·가설검정", "desc": "표본추출, 확률분포, 추정, 가설검정과 비모수 검정" },
  { "id": "reg", "subject": 3, "freq": "high", "title": "상관·회귀분석", "desc": "상관계수, 회귀분석 결과 해석, 변수 선택" },
  { "id": "ts", "subject": 3, "freq": "mid", "title": "시계열·주성분분석", "desc": "정상성과 시계열 모형, 다차원 척도법, 주성분분석" },
  { "id": "classify", "subject": 3, "freq": "high", "title": "분류 분석", "desc": "로지스틱 회귀, 의사결정나무, 앙상블, 신경망, 모형 평가" },
  { "id": "cluster", "subject": 3, "freq": "high", "title": "군집·연관 분석", "desc": "거리 계산, 계층적 군집과 k-평균, 연관 규칙의 지표" }
];
window.ADSP_QUESTIONS = [];
window.ADSP_TRAPS = [];
window.ADSP_STUDY = [];
