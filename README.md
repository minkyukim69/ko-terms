# ko-terms — 한국어 쓰기 · 용어 규칙 플러그인

chat · 트로브 두 레포지토리의 Claude Code 가 함께 쓰는 플러그인이다. 둘이 들어 있다.

| 무엇 | 위치 | 하는 일 |
|---|---|---|
| Skill `ko-terms:ko-terms` | `skills/ko-terms/SKILL.md` + `references/*.md` | 언어 규칙 · 문서 쓰기 규칙 · 용어 원칙 · 용어 표(IT · SAP · chat · 트로브) |
| hook `ko_guard` | `hooks/hooks.json` + `hooks/ko_guard.py` | 답 · 하위 에이전트 보고가 영어면 한 번 되돌림 · Bash 설명과 커밋 메시지 첫 줄이 영어면 거부 · 쓰지 않는 용어가 답에 있으면 한 번 되돌림 |

hook 은 `python3` 표준 라이브러리만 쓴다(설치할 패키지 없음). 자동 검사 규칙 · 기준값의 정본은 `skills/ko-terms/rules.json` 이다.

## 1. 설치 — 서버마다 한 번

이 레포지토리가 마켓플레이스이자 플러그인이다(마켓플레이스 이름 = `ko-terms` · 플러그인 이름 = `ko-terms`).

1. 그 서버의 git 이 이 레포지토리를 읽을 수 있어야 한다. 비공개 레포지토리면 서버에 GitHub 자격 증명(ssh 키 또는 `gh auth login` + `gh auth setup-git`)이 있어야 한다 — `GITHUB_TOKEN` 환경 변수만으로는 부족하다.
2. 프로젝트 레포지토리(chat 또는 트로브)의 `.claude/settings.json` 에 아래를 넣고 커밋한다.

   ```json
   {
     "extraKnownMarketplaces": {
       "ko-terms": { "source": { "source": "github", "repo": "minkyukim69/ko-terms" }, "autoUpdate": true }
     },
     "enabledPlugins": { "ko-terms@ko-terms": true }
   }
   ```

3. 그 서버에서 한 번 설치한다(프로젝트 폴더를 Claude Code 가 신뢰한 뒤).

   ```bash
   claude plugin marketplace add minkyukim69/ko-terms --scope project   # 2 를 했으면 이미 등록돼 있다
   claude plugin install ko-terms@ko-terms --scope project
   ```

4. 🔴 같은 hook 을 프로젝트 `.claude/settings.json` 의 `hooks` 에도 두었다면 지운다 — 플러그인 것과 따로 돌아 두 번 검사한다.
5. 새 세션에서 확인한다: `/hooks` 에 다섯 이벤트(SessionStart · PreToolUse · PostToolUse · Stop · SubagentStop)가 보이고, 세션 첫머리에 «[ko_guard] 한국어 · 용어 규칙」 안내가 들어온다.

## 2. 새 버전 받기

`plugin.json` 에 `version` 을 적지 않았다 — 커밋마다 새 버전으로 잡힌다. push 만 하면 다른 서버가 받을 수 있다.

```bash
claude plugin update ko-terms@ko-terms        # 셸에서
# 또는 세션에서: /plugin marketplace update ko-terms  →  /reload-plugins
```

`autoUpdate: true` 면 세션을 시작할 때 저절로 받는다.

## 3. 보강하는 법 — 정본은 이 레포지토리

- 설치된 사본(`~/.claude/plugins/cache/ko-terms/…`)을 고치지 않는다 — 버전이 바뀌면 사라진다. 이 레포지토리를 clone 해 고치고 커밋 · push 한다.
- 어느 파일에 더하나:

  | 말의 종류 | 파일 |
  |---|---|
  | 두 프로젝트에 공통인 IT 용어 · 쓰지 않는 말 | `skills/ko-terms/references/it-terms.md` |
  | SAP 용어 | `skills/ko-terms/references/sap-terms.md` — «일반 SAP 지식」 행은 트로브 쪽에서 SAP 실물로 확인하면 출처를 «트로브 확인(날짜)」 로 바꾼다 |
  | chat 이 만든 말 | `skills/ko-terms/references/chat-terms.md` |
  | 트로브가 만든 말 | `skills/ko-terms/references/trove-terms.md` |

- 자동 검사 규칙(`rules.json` 의 `terms`)을 더하거나 빼면 `it-terms.md` 의 «자동 검사」 칸을 같은 커밋에서 고친다.
- 참조 파일을 더하거나 이름을 바꾸면 `SKILL.md` 5절 표를 같은 커밋에서 고친다.
- 커밋 전에 시험을 각 2회 돌린다(둘 다 종료코드 0 · `OK`).

  ```bash
  python3 -m unittest discover -s tests -p "test_ko_guard.py" -v               # 단위 U1 ~ U16
  python3 -m unittest discover -s tests -p "test_ko_guard_adversarial.py" -v   # 적대 A1 ~ A14
  claude plugin validate .                                                     # 정의 파일 검사(아이콘 경고 하나는 정상)
  ```

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
