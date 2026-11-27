# ko-terms — SAP · IT 용어의 한국어 번역 기준 (Claude Code 플러그인)

**Claude Code 가 한국어로 쓰게 하고, SAP · IT 용어를 한국 현장에서 쓰는 말로 옮기게 하는 Claude Code 플러그인**이다.
chat · 트로브 두 레포지토리가 함께 쓴다. 용어 표(번역 기준)의 정본은 이 레포지토리 하나다.

- **무엇을 정하나**: 영어 IT 용어를 어떤 한국어로 쓰나(«Version → 버전」 · «Endpoint → 엔드포인트」 · «Prompt → 프롬프트」 …) · 어색한 번역은 무엇인가 · SAP 용어(TR · 데이터 요소 · BAdI · CDS …)를 어떻게 풀어 쓰나 · 각 프로젝트가 만든 말의 뜻.
- **어떻게 지키게 하나**: Skill 이 규칙과 용어 표를 주고, hook 이 Claude 의 글을 검사해 영어 답 · 영어 명령 설명 · 쓰지 않는 용어를 되돌린다.

| 무엇 | 위치 | 하는 일 |
|---|---|---|
| Skill `ko-terms:ko-terms` | `skills/ko-terms/SKILL.md` + `references/*.md` | 언어 규칙 · 문서 쓰기 규칙 · 용어 원칙 · 용어 표 넷(IT · SAP · chat · 트로브) |
| hook `ko_guard` | `hooks/hooks.json` + `hooks/ko_guard.py` | 답 · 하위 에이전트 보고가 영어면 한 번 되돌림 · Bash 명령 설명과 커밋 메시지 첫 줄이 영어면 거부 · 쓰지 않는 용어가 답에 있으면 한 번 되돌림 |

hook 은 `python3` 표준 라이브러리만 쓴다(설치할 패키지 없음). 자동 검사 규칙 · 기준값의 정본은 `skills/ko-terms/rules.json` 이다.

## 용어 표 — 어디에 무엇이 있나

| 파일 | 담는 것 |
|---|---|
| `skills/ko-terms/references/it-terms.md` | 영어 IT 용어 → 한국 현장 용어(일반 · LLM · git · 컨테이너 · 웹 · 시험) · 쓰지 않는 말 · 통계 · 수학 용어 바꿔 쓰기 · contract 옮기는 법 · 풀어 쓰는 IT 용어 |
| `skills/ko-terms/references/sap-terms.md` | SAP 용어 풀이(시스템 · 개발 객체 · DDIC · 프로그램 · 확장 · 업무 데이터) |
| `skills/ko-terms/references/chat-terms.md` | chat 이 만든 말 |
| `skills/ko-terms/references/trove-terms.md` | 트로브가 만든 말 |

## 1. 등록(설치) — 쓰는 레포지토리 · 서버마다 한 번

이 레포지토리는 **마켓플레이스이자 플러그인**이다(마켓플레이스 이름 `ko-terms` · 플러그인 이름 `ko-terms` · 설치 이름 `ko-terms@ko-terms`).
공개 레포지토리라 **등록 · 설치 · 업데이트에는 GitHub 자격 증명이 필요 없다.** 필요한 것은 `git` · `python3` · Claude Code 뿐이다.

프로젝트 레포지토리(chat · 트로브)의 폴더에서:

```bash
claude plugin marketplace add minkyukim69/ko-terms --scope project
claude plugin install ko-terms@ko-terms --scope project
```

- `--scope project` 는 그 레포지토리의 `.claude/settings.json` 에 아래 두 칸을 적는다. **이 파일을 커밋한다** — 같은 레포지토리를 받는 다른 서버 · 사람이 같은 플러그인을 쓰게 된다(그 서버에서는 위 `install` 한 줄만 다시 하면 된다).

  ```json
  {
    "extraKnownMarketplaces": {
      "ko-terms": { "source": { "source": "github", "repo": "minkyukim69/ko-terms" } }
    },
    "enabledPlugins": { "ko-terms@ko-terms": true }
  }
  ```

- 🔴 같은 hook 을 그 레포지토리의 `.claude/settings.json` `hooks` 에도 두었다면 지운다 — 플러그인 것과 따로 돌아 두 번 검사한다.
- 확인: 새 세션에서 `/hooks` 에 다섯 이벤트(SessionStart · PreToolUse · PostToolUse · Stop · SubagentStop)가 보이고, 세션 첫머리에 «[ko_guard] 한국어 · 용어 규칙」 안내가 들어온다. `claude plugin list` 에 `ko-terms@ko-terms` 가 enabled 로 보인다.
- 레포지토리가 아니라 **내 모든 프로젝트**에 쓰려면 `--scope user` 로 등록한다(`~/.claude/settings.json` 에 적힌다).

## 2. 새 버전 받기

`plugin.json` 에 `version` 을 적지 않았다 — **커밋마다 새 버전**으로 잡힌다. 누군가 push 하면 다른 곳은 받기만 하면 된다.

```bash
claude plugin marketplace update ko-terms     # 마켓플레이스(이 레포지토리)를 새로 받는다
claude plugin update ko-terms@ko-terms        # 플러그인을 새 버전으로 바꾼다
# 세션 안에서는: /plugin marketplace update ko-terms  →  /reload-plugins
```

자동으로 받게 하려면 `/plugin` 의 Marketplaces 화면에서 `ko-terms` 의 자동 업데이트를 켜거나, `.claude/settings.json` 의 `extraKnownMarketplaces.ko-terms` 에 `"autoUpdate": true` 를 더한다(세션을 시작할 때 받는다).

## 3. 발행 — 용어를 보강해 올리기

- 🔴 설치된 사본(`~/.claude/plugins/cache/ko-terms/…`)을 고치지 않는다 — 버전이 바뀌면 사라진다. **이 레포지토리를 clone 해서 고치고 push 한다.**
- **push 에는 쓰기 권한이 있는 GitHub 자격 증명이 필요하다**(공개 레포지토리라도). ssh 키를 쓴다면:

  ```bash
  git clone git@github.com:minkyukim69/ko-terms.git
  ```

- 어느 파일에 더하나:

  | 말의 종류 | 파일 |
  |---|---|
  | 두 프로젝트에 공통인 IT 용어 · 쓰지 않는 말 | `it-terms.md` |
  | SAP 용어 | `sap-terms.md` — 출처 «일반 SAP 지식」 인 행을 SAP 실물로 확인하면 출처를 «트로브 확인(날짜)」 로 바꾼다 |
  | chat 이 만든 말 | `chat-terms.md` |
  | 트로브가 만든 말 | `trove-terms.md` |

- 자동 검사 규칙(`rules.json` 의 `terms`)을 더하거나 빼면 `it-terms.md` 의 «자동 검사」 칸을 같은 커밋에서 고친다.
- 참조 파일을 더하거나 이름을 바꾸면 `SKILL.md` 5절 표를 같은 커밋에서 고친다.
- 커밋 전에 시험을 **각 2회** 돌린다(둘 다 종료코드 0 · `OK`).

  ```bash
  python3 -m unittest discover -s tests -p "test_ko_guard.py" -v               # 단위 U1 ~ U16
  python3 -m unittest discover -s tests -p "test_ko_guard_adversarial.py" -v   # 적대 A1 ~ A14
  claude plugin validate .                                                     # 정의 파일 검사(아이콘 경고 하나는 정상)
  ```

- 커밋 · push 한 뒤, 쓰는 쪽(chat · 트로브)은 2절대로 새 버전을 받는다. 두 쪽이 같은 날 함께 고치면 push 전에 `git pull --rebase` 로 받는다.

## 4. 영어로 써야 할 때

사용자가 글 앞에 `!en` 을 붙이면 그 턴은 hook 이 검사하지 않는다. 글 중간의 `!en` 은 효력이 없다.

## 5. 레포지토리 구조

```
.claude-plugin/plugin.json        플러그인 정의(name 만 필수 · version 없음 = 커밋마다 새 버전)
.claude-plugin/marketplace.json   이 레포지토리를 마켓플레이스로도 쓴다(source "./")
skills/ko-terms/SKILL.md          Skill 본문
skills/ko-terms/rules.json        자동 검사 규칙 · 기준값(정본)
skills/ko-terms/references/       it-terms · sap-terms · chat-terms · trove-terms
hooks/hooks.json                  hook 배선(셸 문자열 + `|| exit 1` — 스크립트를 못 찾아도 Bash 를 막지 않게)
hooks/ko_guard.py                 hook 본체(판정만 · 표준 라이브러리)
tests/                            단위 · 적대 시험
```
