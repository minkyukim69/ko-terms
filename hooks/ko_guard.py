"""한국어 · 용어 hook — 답 · 도구 설명 · 커밋 메시지가 영어로 미끄러지거나 쓰지 않는 용어를 쓰면 Claude 에게 알리거나 되돌린다.

설계:
    - 역할: Claude Code 의 hook 다섯 자리에서 **판정만** 한다. 글을 고쳐 쓰는 것은 Claude 의 일이다.
        H1 SessionStart  — 언어 규칙 · 자동 검사 요약(15줄 이하)을 컨텍스트에 넣는다. 규칙 파일을 못 읽으면 그 사실도 넣는다(GR53 S3).
        H2 PreToolUse    — Bash 의 `description` 이 영어거나 `git commit -m` 메시지 첫 줄이 영어면 거부한다(D3).
        H3 PostToolUse   — 도구 결과에 영어가 많으면 «다음 글도 한국어로」 한 줄을 결과 옆에 붙인다.
        H4 Stop          — 최종 답이 한국어가 아니거나 자동 검사 용어(rules.json `terms`)가 있으면 한 번 되돌린다.
        H5 SubagentStop  — 하위 에이전트의 보고가 한국어가 아니면 한 번 되돌린다(용어 검사는 하지 않는다 — D4).
    - 맡지 않는 일: 사용자 입력을 바꾸지 않는다(UserPromptSubmit 없음) · 답을 직접 고쳐 쓰지 않는다 · 상태를 저장하지 않는다(파일 · DB 쓰기 없음).
    - 왜 이렇게:
        · 규칙 글만으로는 긴 작업 중의 진행 메시지 · 최종 보고가 영어로 나가는 것을 막지 못했다(chat CLAUDE.md 0-1 · 사용자 지적 2026-10-15).
        · 기준값 · 용어 규칙은 같은 플러그인의 `skills/ko-terms/rules.json` 하나가 정본이다 — 코드에 고정하지 않는다(설계 §6-3 · §6-10).
          경로는 이 파일 위치 기준(`../skills/ko-terms/rules.json`)이라 플러그인 캐시 · 로컬 폴더 어디서 돌아도 같다.
        · Python 표준 라이브러리만 쓴다 — 이 PC 에 Node 가 없고, 설치 없이 `python3 -I` 로 돈다.
        · 판정의 정본은 입력의 `hook_event_name` 이다. 명령줄 인자와 다르면 아무것도 하지 않고 stderr 에 알린다(배선 실수를 조용히 넘기지 않게).
    - 영어 판정(§6-3): 울타리 코드 블록 · 인라인 코드 · URL · 파일 경로 · 커밋 해시 · 꺾쇠 태그를 지운 뒤 잰다.
      무게 = 한글 1자 3 · 라틴 1자 1 · 그 밖의 글자(한자 · 가나 · 키릴 등) 1자 3. «외국어 비율」 = (라틴 + 그 밖) ÷ 전체.
      «외국어 낱말 수」 = 라틴 낱말 수 + 그 밖의 글자 수. 답은 비율 ≥ reply_foreign_ratio 그리고 낱말 ≥ reply_foreign_words 이면 외국어.
      한국어가 아닌 다른 문자로만 쓴 답(일본어 · 한자)도 같은 식으로 잡힌다(적대 시험 A12).
    - 용어 검사(§6-4): 코드 · 인용(«…」 · «…» · 「…」 · “…” · "…" · '…' — 한 줄 안 · quote_max_chars 이하 · 닫히지 않으면 인용 아님)을 지운 뒤 찾는다.
      찾은 말은 사유에 최대 max_findings 개(규칙 번호 · 찾은 글자 · 바꿀 말 · 앞뒤 context_chars 자), 넘으면 «외 N개」.
      앞뒤 글은 비밀값 모양을 가린 뒤에 자른다(CR5 — 적대 시험 A13).
    - 한 번만 되돌린다(§6-5): Stop · SubagentStop 입력의 `stop_hook_active` 가 참이면 검사하지 않는다. H2 거부는 매번 한다.
    - 영어를 쓰게 하는 길(§6-6 · D2): 마지막 사용자 글(대화 기록 끝 transcript_tail_bytes 에서 도구 결과 · 메타 로우를 건너뛰고 찾음)이
      `!en` 으로 시작하면 H2 ~ H5 는 아무것도 하지 않는다. 글 중간의 `!en` 은 무시한다(적대 시험 A10).
    - 실패하면(§6-7): 입력이 JSON 이 아님 · 규칙 파일 없음 · 그 밖의 예외 → 종료코드 1 + stderr 한 줄(Claude Code 가 hook 오류로 보여 준다 — 막지 않는다).
      대화 기록을 못 읽는 것은 오류가 아니다 — `!en` 이 없는 것으로 보고 판정한다(적대 시험 A6).
    - 지키는 규칙: Skill ko-terms 1절(한국어) · 3절(용어) · chat · 트로브 CLAUDE.md 의 GR53 S2 · S3(발동을 보이게 · 배선 점검) · chat CR5(비밀값을 내보내지 않음) · GR59(이름에 test 없음).
    - 주의: 출력 모양은 Claude Code 공식 hook 문서(2026-11-27 · 2.1.332 확인)를 따른다. Claude Code 를 올리면 실제 세션 확인(설계 §8-3 L1 ~ L6)을 다시 한다.

사용법:
    플러그인의 hooks/hooks.json 이 부른다(셸 문자열 형식 · 이벤트 인자 하나):
        python3 -I "${CLAUDE_PLUGIN_ROOT}/hooks/ko_guard.py" session-start | pre-tool | post-tool | stop | subagent-stop || exit 1
      🔴 끝의 `|| exit 1` 을 빼지 않는다 — 스크립트를 못 찾으면 파이썬이 종료코드 2 를 내고, PreToolUse 에서 2 는 «차단」 이라
      모든 Bash 호출이 막힌다. 이 hook 은 스스로 2 를 내지 않으므로 모든 실패를 1(막지 않는 오류)로 바꿔도 잃는 것이 없다.
    손으로 확인할 때:
        echo '{"hook_event_name":"Stop","last_assistant_message":"This is English ..."}' | python3 -I hooks/ko_guard.py stop   # 플러그인 레포지토리 루트에서
    - 입력 = 표준 입력의 hook JSON · 출력 = 표준 출력의 hook JSON(할 말이 없으면 출력 없음) · 종료코드 0(정상) / 1(hook 오류 — 막지 않음).

참조하는 코드:
    - 없음 — 표준 라이브러리만 쓴다(json · re · shlex · sys · os). 규칙은 `skills/ko-terms/rules.json` 을 파일로 읽는다.
    - 외부 의존: 표준 라이브러리

참조되는 코드:
    - 없음 — 진입점(플러그인 `hooks/hooks.json` 이 하위 프로세스로 실행)
    - 테스트: tests/test_ko_guard.py · tests/test_ko_guard_adversarial.py

변경 이력:
    - 2026-11-27 · 되돌림 사유 끝의 Skill 이름을 플러그인 이름 `ko-terms:ko-terms` 로(옛 이름이 남아 있었다 — chat 반영 확인에서 찾음)
    - 2026-11-27 · chat 레포지토리 `.claude/hooks/` 에서 플러그인 레포지토리 `ko-terms` 로 옮김(chat · 트로브 공유 — 사용자 결정) ·
      세션 시작 안내가 가리키는 Skill 을 플러그인 이름(`ko-terms:ko-terms`)으로 · 판정 동작은 그대로
    - 2026-11-27 · 최초 작성(ko-terms 설계서 v0.2 §6 · 결정 K1 ~ K6 · D1 ~ D7 추천안) — 기준값 이름은 다른 문자도 세므로 `reply_foreign_*` 로 정함 ·
      배선은 exec 형식 대신 셸 문자열 + `|| exit 1`(스크립트를 못 찾을 때의 종료코드 2 가 Bash 를 막지 않게)
"""
from __future__ import annotations

import json
import os
import re
import shlex
import sys

EVENTS = {
    "session-start": "SessionStart",
    "pre-tool": "PreToolUse",
    "post-tool": "PostToolUse",
    "stop": "Stop",
    "subagent-stop": "SubagentStop",
}
RULES_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "skills", "ko-terms", "rules.json")
_TAG = "[ko_guard]"


class HookError(Exception):
    """hook 이 판정할 수 없을 때 — 종료코드 1 + stderr 한 줄."""


# ---------------------------------------------------------------- 규칙

def load_rules(path: str = RULES_PATH) -> dict:
    """rules.json 을 읽고 모양을 검사한다. 틀리면 HookError(사유 한 줄)."""
    try:
        with open(path, encoding="utf-8") as fh:
            rules = json.load(fh)
    except FileNotFoundError:
        raise HookError(f"규칙 파일이 없습니다: {path}") from None
    except (OSError, ValueError) as exc:
        raise HookError(f"규칙 파일을 읽지 못했습니다: {path} ({type(exc).__name__})") from None
    th = rules.get("thresholds") if isinstance(rules, dict) else None
    need = ("reply_foreign_ratio", "reply_foreign_words", "tool_foreign_ratio", "tool_foreign_words", "tool_max_chars",
            "desc_foreign_words", "max_findings", "context_chars", "quote_max_chars", "transcript_tail_bytes")
    if not isinstance(th, dict) or any(not isinstance(th.get(k), (int, float)) or isinstance(th.get(k), bool) for k in need):
        raise HookError(f"규칙 파일의 thresholds 가 모자라거나 숫자가 아닙니다: {path}")
    if not isinstance(rules.get("escape_prefix"), str) or not rules["escape_prefix"]:
        raise HookError(f"규칙 파일의 escape_prefix 가 비었습니다: {path}")
    terms = rules.get("terms")
    if not isinstance(terms, list):
        raise HookError(f"규칙 파일의 terms 가 목록이 아닙니다: {path}")
    compiled = []
    for t in terms:
        if not isinstance(t, dict) or not isinstance(t.get("id"), str):
            raise HookError(f"규칙 파일의 terms 항목에 id 가 없습니다: {path}")
        pairs: list[tuple[re.Pattern, str, str]] = []
        try:
            if isinstance(t.get("map"), dict):
                for word, use in t["map"].items():
                    pairs.append((re.compile(re.escape(word)), str(use), word))
            elif isinstance(t.get("find"), str) and isinstance(t.get("use"), str):
                pairs.append((re.compile(t["find"]), t["use"], str(t.get("label") or t["find"])))
            else:
                raise HookError(f"규칙 {t['id']} 에 find+use 또는 map 이 없습니다: {path}")
        except re.error as exc:
            raise HookError(f"규칙 {t['id']} 의 정규식이 틀렸습니다: {exc}") from None
        allow = [a for a in t.get("allow", []) if isinstance(a, str) and a]
        compiled.append({"id": t["id"], "enabled": t.get("enabled", True) is True, "pairs": pairs, "allow": allow})
    rules["_terms"] = compiled
    return rules


# ---------------------------------------------------------------- 글 정리 · 무게

_FENCE = re.compile(r"(^|\n)[ \t]*(```|~~~)[^\n]*\n.*?(\n[ \t]*\2[^\n]*(?=\n|$)|$)", re.S)
_INLINE = re.compile(r"`[^`\n]*`")
_URL = re.compile(r"\b(?:https?|ftp|file)://\S+|\bwww\.\S+")
_PATH = re.compile(r"(?<![\w])(?:~|\.{1,2})?(?:/[\w.@+%~-]+){2,}/?|\b[\w.-]+/[\w./-]*\.[A-Za-z0-9]{1,6}\b|\b[\w-]+\.(?:py|md|json|ts|tsx|js|sh|sql|yml|yaml|toml|txt|html|css)\b")
_HASH = re.compile(r"\b[0-9a-f]{7,40}\b")
_ANGLE = re.compile(r"</?[A-Za-z][\w:-]*(?:\s[^<>\n]*)?/?>")

_HANGUL = re.compile(r"[가-힣ᄀ-ᇿ㄰-㆏]")
_LATIN_WORD = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)*")


def strip_code(text: str) -> str:
    """판정에서 뺄 것(코드 블록 · 인라인 코드 · URL · 경로 · 해시 · 꺾쇠 태그)을 공백으로 바꾼다."""
    text = _FENCE.sub(lambda m: m.group(1) + " ", text)
    for pat in (_INLINE, _URL, _ANGLE, _PATH, _HASH):
        text = pat.sub(" ", text)
    return text


def weigh(text: str) -> tuple[float, int]:
    """(외국어 비율, 외국어 낱말 수). 한국어 · 외국어 글자가 하나도 없으면 (0.0, 0)."""
    hangul = len(_HANGUL.findall(text))
    latin_letters = 0
    other = 0
    for ch in text:
        if ch.isalpha() and not _HANGUL.match(ch):
            if "a" <= ch.lower() <= "z":
                latin_letters += 1
            else:
                other += 1
    total = hangul * 3 + latin_letters + other * 3
    if total == 0:
        return 0.0, 0
    words = len(_LATIN_WORD.findall(text)) + other
    return (latin_letters + other * 3) / total, words


def is_foreign(text: str, ratio: float, words: int) -> bool:
    """정리한 글이 «한국어가 아니다」 인가 — 비율과 낱말 수가 둘 다 기준 이상."""
    r, w = weigh(strip_code(text))
    return r >= ratio and w >= words


# ---------------------------------------------------------------- 인용 · 비밀값 · 용어

_QUOTES = [("«", "」"), ("«", "»"), ("「", "」"), ("“", "”"), ('"', '"'), ("'", "'")]


def strip_quotes(text: str, limit: int) -> str:
    """한 줄 안에서 닫힌 인용(limit 자 이하)을 같은 길이의 공백으로 바꾼다 — 위치를 보존한다."""
    out = []
    for line in text.split("\n"):
        chars = list(line)
        i = 0
        while i < len(chars):
            ch = chars[i]
            closed = False
            for op, cl in _QUOTES:
                if ch != op:
                    continue
                j = line.find(cl, i + 1)
                if j != -1 and j - i - 1 <= limit:
                    for k in range(i, j + 1):
                        chars[k] = " "
                    i = j + 1
                    closed = True
                    break
            if not closed:
                i += 1
        out.append("".join(chars))
    return "\n".join(out)


_SECRETS = [
    re.compile(r"trv[a-z]?_[A-Za-z0-9_\-]+"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9._~+/=\-]+"),
    re.compile(r"\bsk-[A-Za-z0-9_\-]{8,}"),
    re.compile(r"(?i)(password|passwd|pwd|secret|token|api[_-]?key)\s*[:=]\s*\S+"),
    re.compile(r"\b[A-Za-z0-9+/_\-]{32,}={0,2}"),
]


def mask(text: str) -> str:
    """비밀값 모양을 `***` 로 — 길이를 지키지 않아도 된다(사유 글에만 쓴다)."""
    for pat in _SECRETS:
        text = pat.sub("***", text)
    return text


def find_terms(text: str, rules: dict) -> list[dict]:
    """켜진 용어 규칙에 걸린 자리를 찾는다(코드 · 인용 · 비밀값을 지운 글에서)."""
    th = rules["thresholds"]
    body = strip_quotes(strip_code(mask(text)), int(th["quote_max_chars"]))
    found = []
    for term in rules["_terms"]:
        if not term["enabled"]:
            continue
        allow_spans = []
        for a in term["allow"]:
            allow_spans += [(m.start(), m.end()) for m in re.finditer(re.escape(a), body)]
        for pat, use, label in term["pairs"]:
            for m in pat.finditer(body):
                if any(s <= m.start() and m.end() <= e for s, e in allow_spans):
                    continue
                found.append({"id": term["id"], "word": m.group(0), "use": use, "start": m.start(), "end": m.end(), "label": label})
    found.sort(key=lambda f: (f["start"], f["id"]))
    n = int(th["context_chars"])
    for f in found:
        before = body[max(0, f["start"] - n):f["start"]]
        after = body[f["end"]:f["end"] + n]
        f["context"] = re.sub(r"\s+", " ", f"{before}{f['word']}{after}").strip()
    return found


# ---------------------------------------------------------------- 대화 기록 · !en

def _user_texts(row: dict) -> list[str] | None:
    """사용자가 친 글 로우면 그 글 목록, 아니면 None(도구 결과 · 메타 · 다른 종류)."""
    if row.get("type") != "user" or row.get("isMeta"):
        return None
    content = (row.get("message") or {}).get("content")
    if isinstance(content, str):
        return [content]
    if isinstance(content, list):
        if any(isinstance(b, dict) and b.get("type") == "tool_result" for b in content):
            return None
        texts = [b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"]
        return texts or None
    return None


def escaped(payload: dict, rules: dict) -> bool:
    """마지막 사용자 글이 escape_prefix(`!en`)로 시작하는가. 대화 기록을 못 읽으면 False."""
    path = payload.get("transcript_path")
    if not isinstance(path, str) or not path:
        return False
    tail = int(rules["thresholds"]["transcript_tail_bytes"])
    try:
        with open(path, "rb") as fh:
            fh.seek(0, os.SEEK_END)
            size = fh.tell()
            fh.seek(max(0, size - tail))
            data = fh.read()
    except OSError:
        return False
    lines = data.decode("utf-8", errors="replace").split("\n")
    if len(data) == tail and size > tail:
        lines = lines[1:]                       # 잘린 첫 줄은 버린다
    prefix = rules["escape_prefix"]
    for line in reversed(lines):
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if not isinstance(row, dict):
            continue
        texts = _user_texts(row)
        if texts is None:
            continue
        return any(t.lstrip().startswith(prefix) for t in texts)
    return False


# ---------------------------------------------------------------- git commit 메시지

_SEPS = {"&&", "||", ";", "|", "&", ";;", "|&"}
_TRAILER = re.compile(r"^[A-Za-z][A-Za-z0-9-]*:\s")


def commit_subjects(command: str) -> list[str]:
    """명령 안의 `git … commit -m 메시지` 마다 첫 줄(꼬리 줄 · heredoc 틀 제외). 명령을 못 나누면 빈 목록."""
    try:
        lex = shlex.shlex(command, posix=True, punctuation_chars=";&|")
        lex.whitespace_split = True
        tokens = list(lex)
    except ValueError:
        return []
    segments, cur = [], []
    for tok in tokens:
        if tok in _SEPS:
            segments.append(cur)
            cur = []
        else:
            cur.append(tok)
    segments.append(cur)
    out = []
    for seg in segments:
        if not seg or os.path.basename(seg[0]) != "git" or "commit" not in seg:
            continue
        msgs = []
        i = seg.index("commit") + 1
        while i < len(seg):
            tok = seg[i]
            if tok in ("-m", "--message") and i + 1 < len(seg):
                msgs.append(seg[i + 1])
                i += 2
                continue
            if tok.startswith("--message="):
                msgs.append(tok[len("--message="):])
            elif tok.startswith("-") and not tok.startswith("--") and "m" in tok[1:]:
                pos = tok.index("m", 1)
                rest = tok[pos + 1:]
                if rest:
                    msgs.append(rest)
                elif i + 1 < len(seg):
                    msgs.append(seg[i + 1])
                    i += 1
            i += 1
        if msgs:
            subject = _subject(msgs[0])
            if subject:
                out.append(subject)
    return out


_HEREDOC_OPEN = re.compile(r"^\$\(\s*cat\s+<<-?\s*['\"]?(\w+)['\"]?\s*$")


def _subject(message: str) -> str:
    lines = message.split("\n")
    delim = None
    if lines and _HEREDOC_OPEN.match(lines[0].strip()):
        delim = _HEREDOC_OPEN.match(lines[0].strip()).group(1)
        lines = lines[1:]
    for line in lines:
        s = line.strip()
        if not s or s == ")" or (delim and s == delim) or _TRAILER.match(s):
            continue
        return s
    return ""


def english_short(text: str, words: int) -> bool:
    """짧은 글(설명 · 커밋 첫 줄)이 영어인가 — 한글이 한 글자도 없고 라틴 낱말이 words 개 이상."""
    body = strip_code(text)
    return not _HANGUL.search(body) and len(_LATIN_WORD.findall(body)) >= words


# ---------------------------------------------------------------- 이벤트

def on_session_start(rules: dict | None, error: str | None) -> dict:
    lines = [
        f"{_TAG} 한국어 · 용어 규칙 — 세부는 Skill `ko-terms:ko-terms`(플러그인 ko-terms)를 읽는다.",
        "- 사용자 눈에 보이는 글은 모두 한국어: 도구 호출 사이 진행 메시지 · 도구 호출 설명 · 최종 보고 · 질문 · 커밋 메시지 · 문서 · 주석 · docstring.",
        "- 코드 · 명령 · 식별자 · 바깥 도구 출력 원문만 그대로 둔다. 하위 에이전트에게 글을 시키면 «한국어로」 를 지시에 적는다.",
        "- 영어로 답한 것을 알아채면 다음 응답을 기다리지 말고 바로 한국어로 다시 쓴다.",
    ]
    if error:
        lines.append(f"- ⚠ ko_guard 규칙 파일을 읽지 못했다 — 자동 검사가 꺼져 있다({error}). 사용자에게 알린다.")
    else:
        lines.append("- 자동 검사(hook): 답 · 하위 에이전트 보고가 영어면 되돌림 · Bash 설명과 커밋 메시지 첫 줄이 영어면 거부.")
        words = []
        for t in rules["_terms"]:
            if t["enabled"]:
                words += [f"{label}→{use}" for _p, use, label in t["pairs"]]
        lines.append("- 답에서 바꿔 쓰는 말: " + " / ".join(words[:12]) + (f" 외 {len(words) - 12}개" if len(words) > 12 else ""))
        lines.append("- 용어 자체를 이야기할 때는 «…」 로 감싼다(인용 안은 검사하지 않는다).")
        lines.append(f"- 사용자가 글 앞에 `{rules['escape_prefix']}` 을 붙이면 그 턴은 검사하지 않는다.")
    return {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "\n".join(lines)}}


def on_pre_tool(payload: dict, rules: dict) -> dict | None:
    if payload.get("tool_name") != "Bash" or escaped(payload, rules):
        return None
    inp = payload.get("tool_input") or {}
    n = int(rules["thresholds"]["desc_foreign_words"])
    reasons = []
    desc = inp.get("description")
    if isinstance(desc, str) and english_short(desc, n):
        reasons.append("도구 호출 설명(description)이 영어입니다 — «무엇을 실행하는지」 를 한국어 한 줄로 다시 써서 부릅니다.")
    cmd = inp.get("command")
    if isinstance(cmd, str) and any(english_short(s, n) for s in commit_subjects(cmd)):
        reasons.append("커밋 메시지 첫 줄이 영어입니다 — 한국어로 다시 써서 부릅니다(Co-Authored-By 같은 꼬리 줄은 그대로).")
    if not reasons:
        return None
    return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                   "permissionDecisionReason": f"{_TAG} " + " ".join(reasons)}}


def _flatten(value) -> str:
    """도구 결과(문자열 · 객체)에서 글만 모은다 — 키 이름은 넣지 않는다."""
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return "\n".join(_flatten(v) for v in value.values())
    if isinstance(value, list):
        return "\n".join(_flatten(v) for v in value)
    return ""


def on_post_tool(payload: dict, rules: dict) -> dict | None:
    th = rules["thresholds"]
    text = _flatten(payload.get("tool_response"))[: int(th["tool_max_chars"])]
    if not text or not is_foreign(text, float(th["tool_foreign_ratio"]), int(th["tool_foreign_words"])):
        return None
    if escaped(payload, rules):
        return None
    note = f"{_TAG} 이 도구 결과는 영어가 많다 — 다음 진행 메시지 · 보고 · 설명은 한국어로 쓴다(코드 · 식별자 · 원문 인용만 그대로)."
    return {"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": note}}


def on_stop(payload: dict, rules: dict, subagent: bool) -> dict | None:
    if payload.get("stop_hook_active") is True:
        return None
    text = payload.get("last_assistant_message")
    if text is None:
        raise HookError("입력에 last_assistant_message 가 없어 판정하지 못했습니다")
    if not isinstance(text, str):
        raise HookError("last_assistant_message 가 문자열이 아닙니다")
    th = rules["thresholds"]
    foreign = is_foreign(text, float(th["reply_foreign_ratio"]), int(th["reply_foreign_words"]))
    findings = [] if subagent else find_terms(text, rules)
    if not foreign and not findings:
        return None
    if escaped(payload, rules):
        return None
    parts = []
    if foreign:
        who = "보고" if subagent else "답"
        parts.append(f"{_TAG} 방금 {who}이 한국어가 아닙니다. 같은 내용을 한국어로 다시 씁니다"
                     "(코드 · 명령 · 식별자 · 바깥 도구 출력 원문은 그대로). 이미 나간 글은 남으므로 사과 · «다시 씁니다」 없이 고친 글만 씁니다.")
    if findings:
        cap = int(th["max_findings"])
        head = f"{_TAG} 쓰지 않는 용어가 있습니다. 바꿔서 방금 답을 다시 씁니다:" if not foreign else "또 쓰지 않는 용어:"
        rows = [f"- {f['id']} «{f['word']}」 → {f['use']} · …{f['context']}…" for f in findings[:cap]]
        if len(findings) > cap:
            rows.append(f"- 외 {len(findings) - cap}개")
        rows.append("용어 자체를 설명하는 자리라면 그 말을 «…」 로 감쌉니다(인용 안은 검사하지 않습니다). 세부 = Skill `ko-terms:ko-terms`.")
        parts.append(head + "\n" + "\n".join(rows))
    return {"decision": "block", "reason": "\n".join(parts)}


# ---------------------------------------------------------------- 진입점

def run(event_arg: str, raw: bytes) -> tuple[dict | None, str | None]:
    """(stdout 에 쓸 JSON 또는 None, stderr 에 쓸 오류 또는 None). 오류면 종료코드 1."""
    expected = EVENTS.get(event_arg)
    if expected is None:
        return None, f"알 수 없는 이벤트 인자: {event_arg!r} (쓸 수 있는 값: {', '.join(EVENTS)})"
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return None, "hook 입력이 UTF-8 JSON 이 아닙니다"
    if not isinstance(payload, dict):
        return None, "hook 입력이 JSON 객체가 아닙니다"
    actual = payload.get("hook_event_name")
    if actual != expected:
        return None, f"이벤트가 맞지 않아 아무것도 하지 않았습니다(인자 {expected} · 입력 {actual!r}) — hooks.json 배선을 확인하세요"
    rules, error = None, None
    try:
        rules = load_rules()
    except HookError as exc:
        error = str(exc)
    if expected == "SessionStart":
        return on_session_start(rules, error), None
    if error:
        return None, error
    if expected == "PreToolUse":
        return on_pre_tool(payload, rules), None
    if expected == "PostToolUse":
        return on_post_tool(payload, rules), None
    return on_stop(payload, rules, subagent=(expected == "SubagentStop")), None


def main(argv: list[str]) -> int:
    """hook 진입점 — 판정 결과를 표준 출력으로, 오류는 stderr 한 줄 + 종료코드 1."""
    try:
        out, err = run(argv[1] if len(argv) > 1 else "", sys.stdin.buffer.read())
    except HookError as exc:
        out, err = None, str(exc)
    except Exception as exc:  # noqa: BLE001 — hook 은 작업을 막지 않는다(§6-7) · 사유는 stderr 로 보인다
        out, err = None, f"예상하지 못한 오류: {type(exc).__name__}"
    if err:
        sys.stderr.buffer.write(f"ko_guard: {err}\n".encode("utf-8"))
        return 1
    if out is not None:
        sys.stdout.buffer.write(json.dumps(out, ensure_ascii=False).encode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
