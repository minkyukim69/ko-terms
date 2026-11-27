"""ko-terms 단위 시험 — hook `ko_guard` 가 설계(ko-terms 설계서 v0.2 §8-1)대로 판정하는가.

설계:
    - 무엇을 검증하나: hook 을 **제품과 같은 진입점**(하위 프로세스 `python3 -I hooks/ko_guard.py <이벤트>` + 표준 입력 JSON)으로
      띄워 표준 출력 · 종료코드를 측정한다(GR54 B — 함수를 직접 부르지 않는다).
        U1  SessionStart → 안내에 언어 규칙 · Skill 이름
        U2  Stop · 한국어 답(코드 블록 안은 영어) → 출력 없음
        U3  Stop · 영어 답 30낱말 → 재작성 요청 · 사유에 «한국어」
        U4  Stop · «이 버전은 …」 통과 / «새 판을 만든다」 재작성 요청(T01)
        U5  Stop · 판단 · 판정 · 판매 · 판별 · 판독 · 출판 · 판다 → 통과(오탐 없음)
        U6  Stop · «판」 을 인용 → 통과
        U7  Stop · stop_hook_active 참 + 영어 답 → 통과(한 번만)
        U8  PreToolUse · 설명 영어 거부 / 한국어 통과 · Bash 가 아닌 도구는 보지 않음
        U9  PreToolUse · `git commit -m "Fix bug"` 거부 / 한국어 heredoc + 영어 꼬리 줄 통과
        U10 PostToolUse · 영어 결과 100낱말 → 한 줄 / 한국어 결과 → 없음
        U11 마지막 사용자 글이 `!en …` → 모든 이벤트 통과
        U12 T09 «총계정원장」 통과 / «원장 테이블」 재작성 요청
        U13 rules.json 규칙 번호 ↔ references/it-terms.md «자동 검사」 칸의 규칙 번호가 같다(두 벌 어긋남 방지)
        U14 SubagentStop · 영어 보고 재작성 요청 / 한국어 보고는 용어(«판」)가 있어도 통과(D4 — 언어만) — 설계 표에 더한 케이스
        U15 SKILL.md 5절이 가리키는 참조 파일 ↔ references/ 의 md 파일이 같고 모두 있다(등록 누락 방지 — GR53 S3)
        U16 hooks/hooks.json 에 다섯 이벤트가 모두 있고, 명령마다 이벤트 인자 · `${CLAUDE_PLUGIN_ROOT}` · `|| exit 1` 이 있다
        U17 T03 «끝점」 — 그래프 뜻(엣지의 끝점 · 끝점 노드 · 끝점이 없으면) 통과 / API 뜻(API 끝점 · /v1 끝점 · 끝점 URL) 재작성 요청
        U18 T02 «레포」 — «레포에 있다」 · «두 레포의」 재작성 요청 / «레포지토리」 · «레포트」(report) 통과 · 인용 «레포」 통과
        U19 T10 — «표지 · 봉함 · 봉한다 · 봉투 · 자리표시 · 이름표 · 정리기 · 잰다」 재작성 요청 / 바꾼 말(구분자 · 암호화 저장 · 공통 구조 · 라벨 · 측정한다) · 롤백 뜻 «되돌린다」 통과
        U20 T11 — «단추 · 생존 신호 · 저장점 · 진행 위치 · 회로 차단」 재작성 요청 / 바꾼 말 · 인용 · 동사 «거른다」 · 일반 «차단」 통과
    - 분모: 케이스마다 몇 개를 확인했는지 찍는다(GR54 A3) · unittest 의 «Ran N tests」 가 전체 분모다.
    - 상태: hook 은 상태를 쓰지 않는다 — 시험이 만드는 것은 임시 폴더의 대화 기록 파일뿐이다(끝나면 지운다).

사용법:
    python3 -m unittest discover -s tests -p "test_ko_guard.py" -v
    - 레포지토리 루트에서 실행. 표준 라이브러리 + python3 만 쓴다(도커 · DB 없음).

참조하는 코드:
    - hooks/ko_guard.py (동적) : 하위 프로세스로 실행(제품과 같은 진입점)
    - 외부 의존: 표준 라이브러리 · `skills/ko-terms/rules.json` · `SKILL.md` · `references/*.md` · `hooks/hooks.json`(파일로 읽음)

참조되는 코드:
    - 없음 — 테스트 진입점

변경 이력:
    - 2026-11-27 · U20 — T11(G절 «가」 결정 · 단추 · 생존 신호 · 저장점 · 진행 위치 · 회로 차단)
    - 2026-11-27 · U19 추가 — T10(G절 «다」 결정) · 설명 글의 «되돌림」 → «재작성 요청」 · U17 그래프 예문의 «자리표시 노드」 → «skeleton 노드」(T10 에 걸림 — 예문이 낡음)
    - 2026-11-27 · U18 추가 — T02 를 켬(chat CLAUDE.md 정리 뒤) · «레포트」 는 잡지 않음
    - 2026-11-27 · U17 추가 — T03 을 «API 문맥의 끝점」 만 잡게 좁힘(그래프의 «끝점」 은 정상 — it-terms A1 · 사용자 결정)
    - 2026-11-27 · 플러그인 레포지토리 `ko-terms` 로 옮김(경로 `tests/` · `hooks/` · `skills/`) · U15(SKILL.md ↔ 참조 파일) · U16(hooks.json 배선) 추가
    - 2026-11-27 · 최초 작성(ko-terms 설계서 v0.2 §8-1 U1 ~ U13 + U14)
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOK = os.path.join(ROOT, "hooks", "ko_guard.py")
SKILL = os.path.join(ROOT, "skills", "ko-terms")
EVENT_ARG = {"SessionStart": "session-start", "PreToolUse": "pre-tool", "PostToolUse": "post-tool",
             "Stop": "stop", "SubagentStop": "subagent-stop"}

ENGLISH_30 = ("This answer is written entirely in English and it keeps going with plenty of ordinary words "
              "so that the hook sees well over twenty Latin words in the reply today.")


def call(payload, arg: str | None = None, hook: str = HOOK):
    """hook 을 띄워 (종료코드, 출력 JSON 또는 None, stderr) 를 돌려준다."""
    raw = payload if isinstance(payload, bytes) else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    if arg is None:
        arg = EVENT_ARG[payload["hook_event_name"]]
    p = subprocess.run([sys.executable, "-I", hook, arg], input=raw, capture_output=True, timeout=30)
    out = p.stdout.decode("utf-8").strip()
    return p.returncode, (json.loads(out) if out else None), p.stderr.decode("utf-8")


def stop(text, **extra):
    return call({"hook_event_name": "Stop", "last_assistant_message": text, **extra})


def bash(description=None, command="ls", **extra):
    inp = {"command": command}
    if description is not None:
        inp["description"] = description
    return call({"hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": inp, **extra})


def write_transcript(folder: str, user_text) -> str:
    """마지막 사용자 글이 user_text 인 대화 기록(JSONL)을 만든다 — 뒤에 도구 결과 로우를 붙여 «건너뛰기」 도 확인."""
    path = os.path.join(folder, "t.jsonl")
    rows = [
        {"type": "user", "message": {"role": "user", "content": "앞선 질문"}},
        {"type": "assistant", "message": {"role": "assistant", "content": [{"type": "text", "text": "답"}]}},
        {"type": "user", "message": {"role": "user", "content": user_text}},
        {"type": "user", "isMeta": True, "message": {"role": "user", "content": "<메타 로우>"}},
        {"type": "user", "message": {"role": "user", "content": [{"type": "tool_result", "content": "결과"}]}},
    ]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n")
    return path


class KoGuardUnit(unittest.TestCase):

    def test_u01_session_start(self):
        code, out, err = call({"hook_event_name": "SessionStart", "source": "startup"})
        self.assertEqual(code, 0, err)
        ctx = out["hookSpecificOutput"]["additionalContext"]
        self.assertEqual(out["hookSpecificOutput"]["hookEventName"], "SessionStart")
        self.assertIn("한국어", ctx)
        self.assertIn("ko-terms", ctx)
        self.assertLessEqual(len(ctx.splitlines()), 15)
        self.assertNotIn("규칙 파일을 읽지 못했다", ctx)
        print(f"\n[U1] 안내 {len(ctx.splitlines())}줄(상한 15) · 언어 규칙 · Skill 이름 확인")

    def test_u02_korean_with_code(self):
        text = "결과는 정상입니다.\n```python\nprint('this whole block is english code and must be ignored by the hook entirely')\n```\n`some_identifier` 도 그대로."
        self.assertEqual(stop(text)[:2], (0, None))
        print("\n[U2] 한국어 답 + 영어 코드 블록 1개 → 통과")

    def test_u03_english_reply(self):
        code, out, _ = stop(ENGLISH_30)
        self.assertEqual(code, 0)
        self.assertEqual(out["decision"], "block")
        self.assertIn("한국어", out["reason"])
        print("\n[U3] 영어 답 1개 → 재작성 요청")

    def test_u04_version_word(self):
        self.assertEqual(stop("이 버전은 정상입니다. 새 버전을 만든다.")[:2], (0, None))
        code, out, _ = stop("새 판을 만든다.")
        self.assertEqual(out["decision"], "block")
        self.assertIn("T01", out["reason"])
        self.assertIn("버전", out["reason"])
        print("\n[U4] «버전」 통과 1 · «판」 재작성 요청 1")

    def test_u05_no_false_positive(self):
        words = ["판단", "판정", "판매", "판별", "판독", "출판", "판다", "판결", "판촉"]
        for w in words:
            with self.subTest(w=w):
                self.assertEqual(stop(f"이것은 {w} 문제입니다.")[:2], (0, None), w)
        print(f"\n[U5] «판」 으로 시작 · 끝나는 다른 낱말 {len(words)}개 → 모두 통과")

    def test_u06_quoted(self):
        cases = ["«판」 을 버전으로 바꾼다.", "«판» 은 쓰지 않는다.", "「판」 대신 버전.", "“판” 이라는 말."]
        for t in cases:
            with self.subTest(t=t):
                self.assertEqual(stop(t)[:2], (0, None), t)
        print(f"\n[U6] 인용 모양 {len(cases)}가지 → 모두 통과")

    def test_u07_only_once(self):
        self.assertEqual(stop(ENGLISH_30, stop_hook_active=True)[:2], (0, None))
        self.assertEqual(stop("새 판을 만든다.", stop_hook_active=True)[:2], (0, None))
        print("\n[U7] stop_hook_active 참 → 영어 · 용어 2가지 모두 통과")

    def test_u08_bash_description(self):
        code, out, _ = bash("List files in directory")
        self.assertEqual(out["hookSpecificOutput"]["permissionDecision"], "deny")
        self.assertIn("설명", out["hookSpecificOutput"]["permissionDecisionReason"])
        self.assertEqual(bash("작업 트리 상태 확인")[:2], (0, None))
        self.assertEqual(bash(None)[:2], (0, None))                    # 설명 칸이 없으면 건너뜀
        self.assertEqual(bash("git status 확인")[:2], (0, None))       # 한글이 하나라도 있으면 통과
        other = call({"hook_event_name": "PreToolUse", "tool_name": "Read", "tool_input": {"description": "Read the file now"}})
        self.assertEqual(other[:2], (0, None))
        print("\n[U8] 설명 5가지(영어 거부 1 · 한국어 · 없음 · 섞임 · 다른 도구 통과 4)")

    def test_u09_commit_message(self):
        code, out, _ = bash("커밋", 'git commit -m "Fix bug in parser"')
        self.assertEqual(out["hookSpecificOutput"]["permissionDecision"], "deny")
        self.assertIn("커밋 메시지", out["hookSpecificOutput"]["permissionDecisionReason"])
        heredoc = ("git add -A && git commit -m \"$(cat <<'EOF'\n한국어 제목 줄 — 시험\n\n본문 줄\n\n"
                   "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nEOF\n)\"")
        self.assertEqual(bash("커밋", heredoc)[:2], (0, None))
        self.assertEqual(bash("커밋", 'git commit -am "Update README file"')[1]["hookSpecificOutput"]["permissionDecision"], "deny")
        self.assertEqual(bash("커밋", 'git commit --message="한국어 제목"')[:2], (0, None))
        self.assertEqual(bash("로그", 'git log --oneline -5')[:2], (0, None))
        print("\n[U9] 커밋 명령 5가지(영어 -m · -am 거부 2 · heredoc · --message= · 커밋 아님 통과 3)")

    def test_u10_post_tool(self):
        english = " ".join(["word"] * 100)
        code, out, _ = call({"hook_event_name": "PostToolUse", "tool_name": "Bash",
                             "tool_response": {"stdout": english, "stderr": ""}})
        self.assertEqual(code, 0)
        self.assertIn("한국어", out["hookSpecificOutput"]["additionalContext"])
        self.assertEqual(out["hookSpecificOutput"]["hookEventName"], "PostToolUse")
        korean = "결과는 정상입니다. " * 30
        self.assertEqual(call({"hook_event_name": "PostToolUse", "tool_name": "Read", "tool_response": korean})[:2], (0, None))
        print("\n[U10] 도구 결과 2가지(영어 100낱말 → 한 줄 · 한국어 → 없음)")

    def test_u11_escape(self):
        with tempfile.TemporaryDirectory() as d:
            tp = write_transcript(d, "!en please answer in English")
            checks = [
                stop(ENGLISH_30, transcript_path=tp),
                stop("새 판을 만든다.", transcript_path=tp),
                call({"hook_event_name": "SubagentStop", "last_assistant_message": ENGLISH_30, "transcript_path": tp}),
                bash("List files in directory", transcript_path=tp),
                call({"hook_event_name": "PostToolUse", "tool_name": "Bash", "transcript_path": tp,
                      "tool_response": {"stdout": " ".join(["word"] * 100)}}),
            ]
            for c in checks:
                self.assertEqual(c[:2], (0, None))
            # 같은 대화 기록인데 !en 이 없으면 재작성을 요청한다 — 위 통과가 !en 덕분임을 확인(GR54 C2)
            tp2 = write_transcript(d, "평범한 질문")
            self.assertEqual(stop(ENGLISH_30, transcript_path=tp2)[1]["decision"], "block")
            # 내용이 블록 목록인 사용자 글
            tp3 = write_transcript(d, [{"type": "text", "text": "선택 영역"}, {"type": "text", "text": "!en go"}])
            self.assertEqual(stop(ENGLISH_30, transcript_path=tp3)[:2], (0, None))
        print(f"\n[U11] !en 이벤트 {len(checks)}가지 통과 · 대조 1(없으면 재작성 요청) · 블록 목록 글 1")

    def test_u12_ledger(self):
        self.assertEqual(stop("총계정원장 과 보조원장, 원장 계정은 SAP 회계 용어다.")[:2], (0, None))
        code, out, _ = stop("원장 테이블을 읽는다.")
        self.assertEqual(out["decision"], "block")
        self.assertIn("T09", out["reason"])
        print("\n[U12] T09 예외 3가지 통과 · «원장 테이블」 재작성 요청 1")

    def test_u13_rule_ids_match(self):
        with open(os.path.join(SKILL, "rules.json"), encoding="utf-8") as fh:
            rule_ids = {t["id"] for t in json.load(fh)["terms"]}
        doc_ids: set[str] = set()
        with open(os.path.join(SKILL, "references", "it-terms.md"), encoding="utf-8") as fh:
            for line in fh:
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if line.startswith("|") and len(cells) >= 4 and not set(cells[0]) <= set("-: "):
                    doc_ids |= set(re.findall(r"\bT\d{2}\b", cells[-1]))
        self.assertTrue(rule_ids, "rules.json 에 규칙이 없다")
        self.assertEqual(rule_ids, doc_ids)
        print(f"\n[U13] 규칙 번호 {len(rule_ids)}개 — rules.json ↔ it-terms.md 같음")

    def test_u14_subagent(self):
        code, out, _ = call({"hook_event_name": "SubagentStop", "last_assistant_message": ENGLISH_30, "agent_type": "Explore"})
        self.assertEqual(out["decision"], "block")
        self.assertIn("보고", out["reason"])
        ok = call({"hook_event_name": "SubagentStop", "last_assistant_message": "새 판을 만들었습니다. 결과는 정상입니다."})
        self.assertEqual(ok[:2], (0, None))
        print("\n[U14] 하위 에이전트 보고 2가지(영어 재작성 요청 · 용어는 보지 않음)")


    def test_u15_skill_references(self):
        with open(os.path.join(SKILL, "SKILL.md"), encoding="utf-8") as fh:
            named = set(re.findall(r"references/([a-z-]+\.md)", fh.read()))
        on_disk = {f for f in os.listdir(os.path.join(SKILL, "references")) if f.endswith(".md")}
        self.assertTrue(named, "SKILL.md 가 참조 파일을 하나도 가리키지 않는다")
        self.assertEqual(named, on_disk)
        print(f"\n[U15] 참조 파일 {len(on_disk)}개 — SKILL.md ↔ references/ 같음")

    def test_u16_hooks_json(self):
        with open(os.path.join(ROOT, "hooks", "hooks.json"), encoding="utf-8") as fh:
            hooks = json.load(fh)["hooks"]
        self.assertEqual(set(hooks), set(EVENT_ARG))
        checked = 0
        for event, groups in hooks.items():
            for group in groups:
                for h in group["hooks"]:
                    cmd = h["command"]
                    self.assertEqual(h["type"], "command")
                    self.assertIn("${CLAUDE_PLUGIN_ROOT}/hooks/ko_guard.py", cmd)
                    self.assertTrue(cmd.rstrip().endswith("|| exit 1"), cmd)
                    self.assertIn(f" {EVENT_ARG[event]} ", cmd)
                    checked += 1
        self.assertEqual(checked, len(EVENT_ARG))
        print(f"\n[U16] hook 배선 {checked}개 — 이벤트 · 경로 · 종료코드 바꿈 확인")

    def test_u17_endpoint_word(self):
        graph = ["엣지의 끝점 노드를 skeleton 으로 만든다.", "끝점이 아직 없으면 skeleton 노드를 둔다.", "끝점 유형을 판정한다."]
        for t in graph:
            with self.subTest(t=t):
                self.assertEqual(stop(t)[:2], (0, None), t)
        api = ["API 끝점을 부른다.", "/v1 끝점 목록을 본다.", "끝점 URL 을 바꾼다."]
        for t in api:
            with self.subTest(t=t):
                code, out, _ = stop(t)
                self.assertEqual(out["decision"], "block", t)
                self.assertIn("T03", out["reason"])
                self.assertIn("엔드포인트", out["reason"])
        print(f"\n[U17] 그래프 뜻 «끝점」 {len(graph)}개 통과 · API 뜻 {len(api)}개 재작성 요청")


    def test_u18_repo_word(self):
        bad = ["코드는 레포에 있다.", "두 레포의 설계서에 적는다."]
        for t in bad:
            with self.subTest(t=t):
                code, out, _ = stop(t)
                self.assertEqual(out["decision"], "block", t)
                self.assertIn("T02", out["reason"])
                self.assertIn("레포지토리", out["reason"])
        ok = ["코드는 레포지토리에 있다.", "주간 레포트를 썼다.", "«레포」 는 쓰지 않는 줄임말이다."]
        for t in ok:
            with self.subTest(t=t):
                self.assertEqual(stop(t)[:2], (0, None), t)
        print(f"\n[U18] «레포」 {len(bad)}개 재작성 요청 · 레포지토리 · 레포트 · 인용 {len(ok)}개 통과")


    def test_u19_settled_words(self):
        bad = ["첨부 표지를 붙인다.", "비밀값은 봉함으로 둔다.", "키로 봉한다.", "응답 봉투를 읽는다.",
               "자리표시 노드가 있다.", "상태 이름표를 붙인다.", "SQL 정리기를 거친다.", "다시 잰다."]
        for t in bad:
            with self.subTest(t=t):
                code, out, _ = stop(t)
                self.assertEqual(out["decision"], "block", t)
                self.assertIn("T10", out["reason"])
        ok = ["첨부 구분자를 붙인다.", "비밀값은 암호화 저장으로 둔다.", "응답 공통 구조를 읽는다.", "상태 라벨을 붙인다.",
              "다시 측정한다.", "실패하면 트랜잭션을 되돌린다."]
        for t in ok:
            with self.subTest(t=t):
                self.assertEqual(stop(t)[:2], (0, None), t)
        print(f"\n[U19] T10 {len(bad)}개 재작성 요청 · 바꾼 말 · 롤백 뜻 {len(ok)}개 통과")

    def test_u20_settled_words_ga(self):
        bad = ["저장 단추를 누른다.", "생존 신호를 남긴다.", "저장점에서 다시 시작한다.", "진행 위치를 옮긴다.", "회로 차단기가 열린다."]
        for t in bad:
            with self.subTest(t=t):
                code, out, _ = stop(t)
                self.assertEqual(out["decision"], "block", t)
                self.assertIn("T11", out["reason"])
        ok = ["저장 버튼을 누른다.", "하트비트를 남긴다.", "체크포인트에서 다시 시작한다.", "커서를 옮긴다.", "서킷 브레이커가 열린다.",
              "«단추」 는 «버튼」 으로 바꾼다.", "날짜로 거른다.", "요청을 차단한다."]
        for t in ok:
            with self.subTest(t=t):
                self.assertEqual(stop(t)[:2], (0, None), t)
        print(f"\n[U20] T11 {len(bad)}개 재작성 요청 · 바꾼 말 · 인용 · 동사 · 일반 «차단」 {len(ok)}개 통과")


if __name__ == "__main__":
    unittest.main(verbosity=2)
