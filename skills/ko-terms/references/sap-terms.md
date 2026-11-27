# SAP 용어 — 풀어 쓰는 법

> Skill `ko-terms` 의 참조 파일이다. chat · 트로브 두 레포지토리가 함께 쓴다. SAP 쪽 뜻만 적는다 — 각 프로젝트가 정한 것(chat 은 접속 이름을 열쇠로 쓴다 등)은 `chat-terms.md` · `trove-terms.md` 에 있다.
> 표의 열: **용어 · 풀이(현장에서 부르는 말 포함) · 쓰는 법(예) · 출처**.
> 출처 «일반 SAP 지식」 인 행은 2026-11-27 chat 쪽에서 처음 채웠다. **같은 날 트로브 쪽에서 트로브 개발 시스템(S/4HANA · ABAP 816) 실물(트로브 MCP tool 결과 · SAP 문서)로 확인했다** — 확인한 행은 출처 열이 «트로브 확인(날짜 · 근거)」 이고, 확인하지 못한 행만 «일반 SAP 지식」 으로 남는다.
> 출처가 «트로브 확인」 인 행에서 근거로 적은 SAP 표준 객체는 그 시스템에 실제로 있다. `Z…` · `ACME-…` 같은 고객 객체 이름과 값(회사 코드 `1000` · GUI 상태 `MAIN` 등)은 설명용 예다.
> SAP 이름 · 값은 **원문 그대로** 적는다(대소문자 · 앞자리 0 · 앞쪽 공백을 바꾸지 않는다 — 두 레포지토리 CLAUDE.md GR55).

## A. 시스템 · 접속

| 용어 | 풀이 | 쓰는 법(예) | 출처 |
|---|---|---|---|
| 고객사 SAP 시스템 | 한 고객사의 SAP 시스템 하나와 **그 시스템에만 있는 사실**(객체 · 소스 · 데이터 · 설정 · 커스텀 · 사용 현황) | «고객사 SAP 시스템의 `ZSD_ORDER` 소스」 — 표준 설명과 다를 수 있는 사실을 말할 때 | chat CLAUDE.md 0-5-2 |
| 일반 SAP 지식 | 어느 고객사에도 같은 **SAP 표준의 지식**(표준 문서 · SAP help · 표준 객체 · 트랜잭션 설명 · 베스트 프랙티스) | «일반 SAP 지식으로는 VBAK 에 이 필드가 있다(이 고객사 시스템에 있는지는 따로 확인)」 | chat CLAUDE.md 0-5-2 |
| SAP 접속 · 접속 이름 | 고객사 SAP 시스템 하나로 가는 **접속**과 그 이름(예 `ACME-PRD-100`). SID · client · host · port 는 그 접속의 속성이다 | «접속 `ACME-PRD-100` 에서 조회」 — SID 만으로 시스템을 가리키지 않는다 | chat CLAUDE.md 0-5-2 · U62 |
| SID · client | **SID** = SAP 시스템 ID(세 글자 — 예 `PRD`) · **client** = 한 시스템 안의 업무 단위 번호(세 자리 — 예 `100`). 고객사끼리 겹칠 수 있다 | «SID `PRD` · client `100`」 — 원문 그대로 · 앞자리 0 을 지우지 않는다 | chat CLAUDE.md 0-5-2 · GR55 |
| 시스템 랜드스케이프 · DEV · QAS · PRD | 개발 → 품질(시험) → 운영으로 이어지는 시스템 묶음. 바뀐 객체는 TR 로 차례로 옮긴다(이송 경로 관리 T-code `STMS`) | «DEV 에서 만들고 QAS 에서 확인한 뒤 PRD 로 이송」 | 일반 SAP 지식 |
| 트랜잭션 코드(T-code) | 화면 하나로 들어가는 코드(예 `SE11` · `VA01`). 현장에서 «티코드」. 정의는 테이블 `TSTC`, 이름은 `TSTCT` 에 있다 | «T-code `VA01`」 — DB 의 «트랜잭션」 과 헷갈리면 «T-code」 로 쓴다 | 트로브 확인(2026-11-27 · validate_refs TRAN SE11 · VA01 · DD02T TSTC) |

## B. 개발 객체 · 이송

| 용어 | 풀이 | 쓰는 법(예) | 출처 |
|---|---|---|---|
| 객체 유형 · 하위유형 | SAP 객체의 종류(ADT 기준 — 예 `TABL` 테이블 · `PROG` 프로그램 · `CLAS` 클래스)와 그 안의 세부 종류(예 `TABL/DT` 투명 테이블). `유형/하위유형` 모양으로 함께 쓴다 | «`TABL/DT` 인 `ZSD_HEAD`」 — 트로브가 돌려준 값을 바꾸지 않고 그대로 넘긴다 | chat CLAUDE.md CR3 |
| skeleton / full | SAP 객체 응답의 노드 표식 — **skeleton** = 이름만 있는 노드(skeleton 노드) / **full** = 내용까지 채워진 노드. skeleton 이 «없는 객체」 라는 뜻은 아니다 | «skeleton 노드라 내용은 아직 없다(없는 객체가 아니다)」 | chat CLAUDE.md 0-5-2 · CR3 |
| 고객 객체 · 이름 공간 · CBO | 고객이 만든 객체. 이름이 `Z` · `Y` 로 시작하거나 등록한 이름 공간(`/ABC/…`) 안에 있다. 한국 현장에서는 고객 개발 객체를 «CBO」 라고 부른다 | «CBO 프로그램 `ZSDR0010`」 · 이름 공간이 든 이름은 `/ABC/CL_ORDER` 처럼 그대로 | 트로브 확인(2026-11-27 · 트로브 MCP 서버 설명 «CBO = 이름이 Z · Y 로 시작」) · chat 역설계 설계서 §0 |
| 패키지(DEVC) | 개발 객체를 묶는 단위(옛 이름 «개발 클래스」 · 정의 테이블 `TDEVC`). `$TMP` 는 로컬 패키지라 이송하지 않는다 | «패키지 `VA` 의 객체」 · «`$TMP` 에 만든 시험 객체」 | 트로브 확인(2026-11-27 · validate_refs DEVC $TMP · VA · DD02T TDEVC) |
| TR(트랜스포트 요청) · 작업 | 바뀐 객체 · 설정을 다음 시스템으로 옮기는 묶음. 현장에서 «TR」 · «트랜스포트」. 워크벤치 요청(`K` — 개발 객체)과 커스터마이징 요청(`W` — 설정)이 있고, 그 아래 사람마다 **작업**(task — `S` 개발 · `Q` 커스터마이징)이 달린다. 번호는 `<SID>K9nnnnn` 모양 | «TR `DEVK900123` 에 넣는다」 · «작업 `DEVK900124` 는 TR `DEVK900123` 아래」 | 트로브 확인(2026-11-27 · E070 TRKORR `EQAK900002` 등 · 도메인 TRFUNCTION 고정값) |
| ADT | ABAP Development Tools — Eclipse 의 ABAP 개발 도구와 그것이 쓰는 SAP REST API(`/sap/bc/adt/…`) | «ADT 로 소스를 읽는다」 | 트로브 확인(2026-11-27 · describe_object NROB RF_BELEG 의 `/sap/bc/adt/numberranges/…` 주소) · chat CLAUDE.md CR8 |
| 활성화 · 활성 버전 | ABAP 객체는 저장만 하면 **비활성 버전**이고, 활성화해야 실행에 쓰인다. 비활성 버전만 있는 객체는 개발 중인 객체다 | «저장했지만 아직 활성화하지 않았다」 | 트로브 확인(2026-11-27 · describe_object 응답의 `version: active` · 트로브 MCP `sap_state=inactive_only`) |
| 응용 컴포넌트 · 모듈 | 패키지 · 객체가 속한 업무 영역(예 `FI-GL` · `SD-SLS` — 테이블 `DF14L`) · 그 첫 마디(`FI` · `CO` · `SD` · `MM` · `PP`) | «응용 컴포넌트 `SD-SLS`」 | 트로브 확인(2026-11-27 · DF14L SD-SLS · FI-GL) · chat 역설계 설계서 §0 |

## C. 데이터 사전(DDIC)

| 용어 | 풀이 | 쓰는 법(예) | 출처 |
|---|---|---|---|
| 투명 테이블 · 구조 · 테이블 유형 | DB 에 실제로 있는 테이블(`TABL/DT` — DD02L TABCLASS `TRANSP`) · DB 에 없고 모양만 정한 것(`TABL/DS` — `INTTAB` · append 구조) · 내부 테이블의 모양(`TTYP`) | «구조 `BAPIRET2` 는 DB 테이블이 아니다(`TABL/DS`)」 · «`VBAK` 는 `TABL/DT`」 | 트로브 확인(2026-11-27 · describe_object TABL BAPIRET2 · VBAK) |
| 데이터 요소 · 도메인 | **데이터 요소** = 필드의 뜻(라벨 · 검색 도움말 · 문서)이고 현장에서 «데이터 엘리먼트」 / **도메인** = 기술 형식(유형 · 길이 · 고정값 · 값 테이블). 데이터 요소 여럿이 도메인 하나를 함께 쓴다 | «`VBAK-KUNNR` 의 데이터 요소는 `KUNAG`(Sold-to Party) · 도메인은 `KUNNR`」 | 트로브 확인(2026-11-27 · get_field_details VBAK) |
| 고정값 · 값 테이블 | 도메인에 적어 둔 허용 값 목록(`DD07L` · 글은 `DD07T`) · 허용 값을 담은 테이블 | «도메인 `SUBC` 고정값 `1`(Executable program) · `M`(Module pool)」 · «도메인 `WAERS` 의 값 테이블 `TCURC`」 | 트로브 확인(2026-11-27 · describe_object DOMA SUBC · get_field_details VBAK-WAERK) |
| 검색 도움말(search help) | 필드 입력 때 F4 로 뜨는 값 찾기 화면. 현장에서 «서치 헬프」. 여러 검색 도움말을 묶은 **묶음 검색 도움말**(collective)도 있다 | «묶음 검색 도움말 `DEBI`(Search help for customers)」 | 트로브 확인(2026-11-27 · describe_object SHLP DEBI) |
| 전달 클래스 | 테이블이 무엇을 담는지 정한 표시(DD02L `CONTFLAG`) — `A` 응용 데이터(마스터 · 트랜잭션) · `C` 고객 설정(고객만 관리 · SAP 이 내용을 넣지 않음) · `L` 임시 데이터(비어서 납품) · `G` 고객 설정(SAP 은 추가만) · `E` 제어 테이블(SAP · 고객 키 영역이 나뉨) · `S` 시스템 테이블(SAP 만 고침) · `W` 시스템 테이블(별도 전송 객체로 이송) | «`T001` 은 전달 클래스 `C`, `VBAK` 은 `A`」 | 트로브 확인(2026-11-27 · describe_object DOMA CONTFLAG · DD02L) |
| 유지보수 뷰 · SM30 | 테이블 내용을 화면에서 고치게 만든 뷰(`VIEW` 하위 종류 `C` — Maintenance View (For SM30))와 그것을 여는 T-code(`SM30` Call View Maintenance) | «`V_T001` 은 SM30 으로 관리」 · «`ZSD_CFG` 는 SM30 으로 관리」 | 트로브 확인(2026-11-27 · search_objects V_T001 · TSTCT SM30) |
| CHAR 빈 값 · 공백 | SAP 은 `''` · `' '` · `IS INITIAL` 을 같게 본다. **뒤쪽 공백은 없는 것**으로 보고 **앞쪽 공백은 값의 일부**다. 대소문자를 가린다 | SAP 으로 가는 SQL 의 빈 값은 `' '` | 두 레포지토리 CLAUDE.md GR55 |
| NUMC | 숫자만 담는 **문자** 유형. 앞자리 0 을 포함한 원문이 값이다 | «`0001` 을 `1` 로 바꾸지 않는다」 | GR55 |
| DATS · TIMS | 날짜 `YYYYMMDD` · 시각 `HHMMSS` 를 담는 문자 유형. 빈 날짜는 `00000000` | 화면에서 빈 날짜는 빈칸으로 보인다 | GR55 |
| CURR · QUAN | 금액 · 수량 유형. **참조 필드**(통화 키 `CUKY` · 단위 `UNIT`)가 있어야 뜻이 정해진다(DD03L `REFTABLE` · `REFFIELD`) — 통화에 따라 소수점 자리가 다르다 | «`VBAK-NETWR` 은 `VBAK-WAERK` 를 참조한다」 | 트로브 확인(2026-11-27 · DD03L VBAK-NETWR REFFIELD) |

## D. 프로그램 · 인터페이스

| 용어 | 풀이 | 쓰는 법(예) | 출처 |
|---|---|---|---|
| 리포트 · 모듈 풀 · Dynpro | 실행 프로그램(프로그램 유형 SUBC `1`) · 화면 중심 프로그램(SUBC `M`) · 화면 하나(번호 · PBO · PAI 흐름 — 원천 테이블 `D020S`). **ADT 하위유형은 둘 다 `PROG/P`** 이고 SUBC 로 가른다 | «모듈 풀 `SAPMV45A`(SUBC `M`)의 화면 `0100`」 | 트로브 확인(2026-11-27 · TRDIR SAPMV45A SUBC · 트로브 등록부 subtype_map) |
| 함수 모듈 · 함수 그룹 | 이름으로 부르는 ABAP 함수(목록 `TFDIR`) · 그것을 묶는 단위. 함수 그룹의 주 프로그램 이름은 `SAPL<그룹>`(SUBC `F`) | «함수 그룹 `V45A` 의 주 프로그램 `SAPLV45A`」 · «함수 모듈 `Z_SD_GET_ORDER`」 | 트로브 확인(2026-11-27 · validate_refs FUGR V45A · TRDIR SAPLV45A SUBC `F`) |
| RFC · BAPI | **RFC** = 다른 시스템에서 부를 수 있는 함수 모듈(원격 호출 — 처리 유형 Remote-Enabled Module) / **BAPI** = 업무 객체의 메서드로 SAP 이 공개한 표준 RFC 함수 모듈 | «BAPI `BAPI_SALESORDER_CREATEFROMDAT2`(remote-enabled)」 | 트로브 확인(2026-11-27 · validate_refs FUNC — remote_callable=true · FMODE `R`) |
| 메시지 클래스 | 메시지 번호 · 글을 묶은 단위(객체 유형 `MSAG` · 글은 테이블 `T100`). 글에 `&1` ~ `&4` 플레이스홀더가 들어간다 | «메시지 `V1` `311`(`&1 &2 has been saved.`)」 | 트로브 확인(2026-11-27 · get_message V1 311) |
| 권한 객체 | 권한 검사의 단위(필드 몇 개 · `AUTHORITY-CHECK` 로 검사 · 객체 유형 `SUSO` · 권한 클래스 `SUSC` 아래 · 정의 T-code `SU21`). 정의 테이블 이름이 `TOBJ` 라서 고객화 객체 유형 `TOBJ` 와 헷갈리기 쉽다 | «권한 객체 `V_VBAK_VKO`(필드 `VKORG` · `VTWEG` · `SPART` · `ACTVT`)」 | 트로브 확인(2026-11-27 · get_auth_object V_VBAK_VKO · DD02T TOBJ) |
| SPA/GPA 파라미터 | 사용자 기억값(`SET` · `GET PARAMETER ID` · 객체 유형 `PARA`) — 화면 사이에 값을 넘긴다. 파라미터 자체에는 글이 없고, 그것을 쓰는 데이터 요소로 뜻을 안다 | «파라미터 ID `AUN`(Sales order number — 데이터 요소 `VBELN` · `KDAUF` 등이 쓴다)」 | 트로브 확인(2026-11-27 · get_parameter AUN) |
| 잠금 객체 | 같은 데이터를 둘이 함께 고치지 못하게 하는 SAP 잠금(객체 유형 `ENQU` · 만들면 `ENQUEUE_<이름>` · `DEQUEUE_<이름>` 함수가 생긴다) | «잠금 객체 `EVVBAKE`(Sales document (exclusive)) — 함수 `ENQUEUE_EVVBAKE`」 — DB 잠금과 구분 | 트로브 확인(2026-11-27 · describe_object ENQU EVVBAKE · validate_refs FUNC ENQUEUE_EVVBAKE) |
| include | 혼자 실행되지 않고 다른 프로그램에 끼워 넣는 소스 조각(SUBC `I` · `PROG/I`) | «include `MV45AFZZ`」 | 트로브 확인(2026-11-27 · TRDIR MV45AFZZ SUBC `I`) |
| 서브루틴 풀 | `FORM` 서브루틴 · 메서드만 담는 프로그램(SUBC `S` · 하위유형 `PROG/P`). 화면 · 선택 화면이 없다 | «서브루틴 풀 `ZSD_FORMS`」 | 트로브 확인(2026-11-27 · describe_object DOMA SUBC · search_help abapdocu Program Type) |
| 클래스 풀 · 클래스 include | 전역 클래스의 프로그램(SUBC `K` · 이름 = 클래스 이름을 30자까지 `=` 로 채우고 `CP`). 소스는 include 로 나뉜다 — `CCDEF`(로컬 타입 정의) · `CCIMP`(로컬 클래스 구현) · `CCMAC`(매크로) · `CCAU`(테스트 클래스 — ABAP Unit · **테스트 include**) | «`CL_ABAP_BEHAVIOR_HANDLER======CCIMP`」 | 트로브 확인(2026-11-27 · TRDIR CL_ABAP_BEHAVIOR_HANDLER======CP · CCIMP) · 트로브 docs/mcp_api_design.md AV197 |
| 인터페이스(INTF) | 메서드 모양만 정한 전역 인터페이스(인터페이스 풀 — SUBC `J`). 클래스가 구현한다 | «인터페이스 `IF_EX_BADI_SD_SALES`」 | 트로브 확인(2026-11-27 · validate_refs INTF IF_EX_BADI_SD_SALES · DOMA SUBC) |
| 프로그램 유형(SUBC) | `TRDIR-SUBC` 의 한 글자 — `1` 실행 프로그램 · `I` include · `M` 모듈 풀 · `F` 함수 그룹 · `S` 서브루틴 풀 · `J` 인터페이스 풀 · `K` 클래스 풀 · `T` 타입 풀 · `X` 변환(XSLT · ST) · `Q` DB 프로시저 프록시 · `B` 행동 정의 | «SUBC `M` 이라 모듈 풀이다」 | 트로브 확인(2026-11-27 · describe_object DOMA SUBC) |
| 이벤트 블록 | 실행 프로그램에서 정해진 때 도는 처리 블록(`INITIALIZATION` · `AT SELECTION-SCREEN` · `START-OF-SELECTION` 등). SAP 은 새 코드에서 이 방식 대신 메서드 호출만 두라고 권한다 | «`START-OF-SELECTION` 에서 메인 메서드를 부른다」 | 트로브 확인(2026-11-27 · search_help abapdocu Program Type) |
| PBO · PAI | 화면(Dynpro) 흐름 로직의 두 단계 — **PBO**(Process Before Output · 화면을 보이기 전) · **PAI**(Process After Input · 사용자가 입력한 뒤). 각 단계에서 `MODULE` 을 부른다 | «PAI 의 `MODULE user_command_0100`」 | 트로브 확인(2026-11-27 · search_help abapdocu Messages - Behavior «PAI」) · 트로브 docs/adt_design.md |
| GUI 상태 | 화면 위 메뉴 · 단추 · 기능 키 묶음(`SET PF-STATUS` · 만드는 T-code `SE41` Menu Painter) | «GUI 상태 `MAIN` 의 단추 `SAVE`」 | 트로브 확인(2026-11-27 · TSTCT SE41) · 트로브 docs/javagui_bdc_design.md |
| 선택 화면 · 변형(variant) | **선택 화면** = 실행 프로그램이 돌기 전에 조건을 받는 화면(`PARAMETERS` · `SELECT-OPTIONS`) / **변형** = 그 화면에 넣을 값을 이름 붙여 저장한 것(배치 작업에 쓴다). «변형」 은 트랜잭션 변형 · 뷰 변형에도 쓰이니 무엇의 변형인지 붙여 쓴다 | «선택 화면 변형 `ZDAILY` 로 배치 실행」 | 트로브 docs/mcp_api_design.md · docs/reverse_reading_design.md |
| Remote-Enabled Module | 함수 모듈의 처리 유형 «원격 호출 가능」(`TFDIR-FMODE` = `R`) — 이것이 RFC 함수다. 시스템 안에서도 부를 수 있다 | «`BAPI_SALESORDER_CREATEFROMDAT2` 는 Remote-Enabled Module」 | 트로브 확인(2026-11-27 · validate_refs FUNC fmode `R`) |
| RFC Destination | 다른 시스템으로 RFC 를 보낼 접속 정의(T-code `SM59`). **저장소 객체가 아니다** | «RFC Destination `ZCRM_PRD` 로 부른다」 | 트로브 확인(2026-11-27 · TSTCT SM59 · 트로브 MCP 서버 설명) |
| 메시지 유형 | `MESSAGE` 문의 한 글자 — `A` 중단 · `E` 오류 · `I` 정보 · `S` 상태 · `W` 경고 · `X` 종료(덤프). 어떻게 보이고 다음에 무엇이 되는지는 처리 맥락(대화 · 배치 · RFC 등)마다 다르다 | «`MESSAGE s311(v1) WITH …`」 | 트로브 확인(2026-11-27 · search_help abapdocu Messages - Behavior) |

## E. 확장 · 새 개발 모델

| 용어 | 풀이 | 쓰는 법(예) | 출처 |
|---|---|---|---|
| IMG · SPRO · 커스터마이징 | **IMG** = 설정 안내 트리 · **SPRO** = 그 진입 T-code(Customizing - Execute Project) · **커스터마이징** = 고객사마다 하는 설정. 설정값은 시스템 · client 마다 다른 **값**이다 | «IMG 경로 영업 › 판매 문서 …」 | 트로브 확인(2026-11-27 · TSTCT SPRO · get_img_doc T001) |
| User Exit | SAP 표준 include 안에 비워 둔 서브루틴(`USEREXIT_…`)에 고객이 코드를 넣는 가장 옛 확장 자리. 고치는 것이 수정(modification)이다 | «include `MV45AFZZ` 의 User Exit」 | 트로브 확인(2026-11-27 · TRDIR MV45AFZZ) |
| Customer Exit(SMOD · CMOD) | SAP 이 미리 열어 둔 확장 자리(SMOD 확장 — 함수 `EXIT_…` · 화면 · 메뉴) · 그것을 고객 프로젝트로 묶어 켜는 곳(CMOD — T-code `CMOD`). 정의 테이블 `MODSAP` | «Customer Exit `V45A0002`(Predefine sold-to party in sales document) — 함수 `EXIT_SAPMV45A_002`」 | 트로브 확인(2026-11-27 · describe_object SMOD V45A0002 · MODSAP) |
| BAdI · 확장 스팟 | 클래스 방식의 확장 자리 · 그것을 묶는 단위(enhancement spot — `ENHS`). 옛 방식 BAdI 는 정의 `SXSD`(SE18) · 구현 `SXCI`(SE19)이고, 같은 이름의 확장 스팟이 함께 있을 수 있다 | «BAdI `BADI_SD_SALES`(옛 방식 `SXSD` · 확장 스팟 `ENHS/XSB` 둘 다 있다)」 | 트로브 확인(2026-11-27 · validate_refs ENHS · SXSD BADI_SD_SALES · TSTCT SE18 · SE19) |
| 확장 구현(ENHO) | 고객이 확장 자리에 넣은 구현. 하위유형으로 소스 코드 끼워 넣기(hook — `XHH`) · BAdI 구현(`XHB`) · 클래스 · 함수 그룹 확장(`XH`) 등이 있다 | «ENHO `ZEI_SD_ORDER`(XHH)」 | 트로브 확인(2026-11-27 · 트로브 등록부 subtype_map ENHO) · chat 역설계 확장 설계서 |
| 암묵적 확장 · 명시적 확장 | 소스 코드 확장의 두 자리 — **암묵적**(implicit — 프로그램 · 서브루틴 · 메서드의 처음 · 끝처럼 SAP 이 따로 만들지 않아도 있는 자리) / **명시적**(explicit — SAP 이 `ENHANCEMENT-POINT` · `ENHANCEMENT-SECTION` 으로 만든 자리). 넣은 구현은 스위치에 묶인다 | «표준 서브루틴 끝의 암묵적 확장에 ENHO 를 넣었다」 | 트로브 확인(2026-11-27 · search_help abapdocu Source Code Enhancements) |
| Switch Framework · 업무 기능 · 스위치 | 확장 · 기능을 켜고 끄는 SAP 장치 — **업무 기능**(business function — `SFW_BF`)을 켜면(T-code `SFW5`) 그 아래 **스위치**(`SFW_SWITCH`)가 켜지고, 스위치에 묶인 패키지 · 확장이 살아난다 | «업무 기능이 꺼져 있어 그 스위치에 묶인 패키지의 객체는 비활성」 | 트로브 확인(2026-11-27 · DD02T SFW_BF · SFW_SWITCH · TSTCT SFW5) |
| CDS 뷰 · VDM | ABAP 의 데이터 모델 정의(`DDLS`) · SAP 표준 CDS 의 계층과 이름 접두 — `I_` 인터페이스 뷰(기본 · 복합) · `C_` 소비 뷰 · `R_` 제한 재사용 뷰(고객 · 파트너의 재사용 대상이 아님) · `P_` 비공개 뷰 · `A_` 원격 API 뷰 | «CDS 뷰 `I_SalesOrder`」 — 이름 대소문자 그대로 | 트로브 확인(2026-11-27 · describe_object DDLS I_SALESORDER · search_help help «Naming Conventions in the Virtual Data Model」) |
| RAP · BDEF | ABAP RESTful 애플리케이션 프로그래밍 모델 — CDS · 행동 정의(BDEF) · 행동 풀 클래스로 만든 업무 객체와 그 서비스 | «표준 RAP 업무 객체 `I_SalesOrderTP`」 · «RAP 업무 객체 `ZI_ORDER`」 | 트로브 확인(2026-11-27 · validate_refs BDEF I_SALESORDERTP) · chat 역설계 설계서 §0 |
| OData · SEGW · 서비스 바인딩 | 웹 API 표준 · OData V2 서비스를 만드는 Gateway 빌더(T-code `SEGW` · 모델 클래스 MPC · 처리 클래스 DPC) · RAP 서비스를 내보내는 설정(`SRVB`) | «표준 OData V2 서비스 `API_SALES_ORDER_SRV`」 · «SEGW 프로젝트 `ZSD_ORDER_SRV`」 | 트로브 확인(2026-11-27 · TSTCT SEGW · validate_refs IWSV API_SALES_ORDER_SRV — SAP 에 있음) · chat 역설계 설계서 §0 |
| Fiori | SAPUI5 로 만든 SAP 웹 화면 · 앱. 앱 파일은 시스템에 BSP 애플리케이션(`WAPA`)으로 저장된다. 앱 ID(`F…`)는 SAP Fiori apps reference library 의 번호라 시스템 객체 이름과 다르다 | «Fiori 앱 `SD_SO_MANAGES1`(Manage Sales Orders)」 | 트로브 확인(2026-11-27 · search_objects WAPA SD_SO_MANAGES1) |
| Released API · Clean Core | SAP 이 쓰라고 공개한(release) 객체 · 표준을 고치지 않고 공개 API 로만 확장한다는 원칙. 바로 써도 되는 것은 계약 C1 · C2 가 RELEASED 인 객체다(계약 = I 절) | «이 테이블은 release 되지 않아 Clean Core 에 맞지 않는다」 · «`I_SalesOrder` 는 C1 RELEASED」 | 트로브 확인(2026-11-27 · describe_object DDLS I_SALESORDER facet release · 트로브 check_clean_core 설명) |

## F. 업무 데이터

| 용어 | 풀이 | 쓰는 법(예) | 출처 |
|---|---|---|---|
| 조직 단위 | 회사 코드(`T001`) · 플랜트(`T001W`) · 영업 조직(`TVKO`) · 구매 조직(`T024E`) · 관리 회계 영역(`TKA01`)처럼 업무를 나누는 단위. 고객화 IMG 의 Enterprise Structure 에서 정의 · 연결한다 | «회사 코드 `1000`」 · «영업 조직 `1000` 은 회사 코드 `1000` 에 속한다」 | 트로브 확인(2026-11-27 · DD02T T001 · T001W · TVKO · T024E · TKA01) |
| 마스터 데이터 · 트랜잭션 데이터 | 오래 쓰는 기준 정보(고객 `KNA1` · 자재 `MARA` · 거래처 `LFA1`) · 업무가 일어날 때마다 생기는 데이터(판매 문서 `VBAK` · 회계 전표 `BKPF`). 둘 다 전달 클래스 `A` 테이블이다 | «고객 마스터」 · «판매 문서(트랜잭션 데이터)」 | 트로브 확인(2026-11-27 · DD02T KNA1 · MARA · LFA1 · VBAK · BKPF · DOMA CONTFLAG `A`) |
| 총계정원장 · 보조원장 | 회계 용어 — 모든 계정의 원장(G/L 계정 마스터 `SKA1` · `SKB1`) · 고객 · 거래처 같은 보조 원장. **«원장」 을 원본 테이블 뜻으로 쓰지 않는 규칙(it-terms T09)의 예외** | «총계정원장 계정」 | 트로브 확인(2026-11-27 · DD02T SKA1 · SKB1) |

## G. 고객화 · IMG

| 용어 | 풀이 | 쓰는 법(예) | 출처 |
|---|---|---|---|
| IMG activity(CUS0) | IMG 트리의 실행 항목 하나(객체 유형 `CUS0`). 헤더 `CUS_IMGACH` · 이름 `CUS_IMGACT`. 고객화 객체 · T-code · IMG 문서가 딸린다 | «IMG activity `SIMG_CFMENUSAPCOX02`(Edit, Copy, Delete, Check Company Code)」 | 트로브 확인(2026-11-27 · get_img_doc T001 · DD02T CUS_IMGACH · CUS_IMGACT) |
| 고객화 객체(OBJH · TOBJ) | 유지보수 · 전송 단위로 정의한 객체(헤더 `OBJH` · 유형 `V` 뷰 · `S` 테이블 · `C` 뷰 클러스터 등 · 속성 T-code `SOBJ`). 저장소 객체 유형은 `TOBJ` 이고 이름은 OBJH 이름(10자보다 짧으면 공백으로 채움) + 유형 글자다. 테이블 `TOBJ`(권한 객체)와 다르다 | «고객화 객체 `V_T001`(유형 `V`)」 | 트로브 확인(2026-11-27 · OBJH V_T001 · TSTCT SOBJ) · 트로브 CLAUDE.md §11(`tobj_name`) |
| 뷰 클러스터(VCLS) · SM34 | 유지보수 뷰 여럿을 위아래로 묶어 한 화면 흐름으로 고치게 한 것 · 그것을 여는 T-code(`SM34` Call View Cluster Maintenance) | «뷰 클러스터 `VC_TPAR_VK`(Partner Customizing - Sales Document Header)」 | 트로브 확인(2026-11-27 · search_objects VCLS · TSTCT SM34) |
| 유지보수 대화 | 유지보수 뷰 · 테이블을 SM30 으로 고칠 수 있게 생성한 화면 · 함수 그룹(T-code `SE54` Generate table view · 등록 테이블 `TVDIR`) | «`V_T001` 의 유지보수 대화를 다시 생성」 | 트로브 확인(2026-11-27 · TSTCT SE54 · DD02T TVDIR) · 트로브 docs/config_analysis.md |
| 뷰 변형 | 다른 뷰의 필드 · 선택 조건을 좁혀 만든 DDIC 뷰(`VIEW` 하위 종류 `V` — View Variant). 고객화에서 activity 가 테이블의 일부 키만 고치게 할 때 쓴다 | «이 activity 는 뷰 변형으로 회사 코드별 로우만 고친다」 | 트로브 등록부 subtype_map VIEW · 트로브 docs/config_analysis.md |
| client 000 · 표준 Template | SAP 이 납품한 기준 client(`T000` 의 `000` — SAP SE · 역할 `S` SAP reference). 고객 client 의 설정과 비교하는 표준 Template 로 쓴다 | «client 000 과 비교해 바뀐 로우만 해석」 | 트로브 확인(2026-11-27 · T000 · DOMA CCCATEGORY) · 트로브 docs/config_analysis.md |
| SCC4 · client 설정 | client 를 관리하는 T-code(`SCC4` Client Administration). client 마다 역할(`T000-CCCATEGORY` — `P` 운영 · `T` 시험 · `C` 커스터마이징 · `S` SAP 기준 …)과 바뀐 설정의 자동 기록 여부(`CCCORACTIV`)를 정한다 | «client `100` 은 변경 자동 기록(`1`)」 | 트로브 확인(2026-11-27 · TSTCT SCC4 · T000 · DD07T CCCATEGORY · CCCORACTIV) |
| 번호 범위(SNUM · NROB · NRIV) | 전표 · 문서 번호를 매기는 규칙. 번호 범위 객체(`NROB` · 정의 `TNRO` · T-code `SNUM`) 아래 구간(`NRIV`)마다 현재 번호를 가진다 | «번호 범위 객체 `RF_BELEG`(회계 전표)」 | 트로브 확인(2026-11-27 · describe_object NROB RF_BELEG · DD02T TNRO · NRIV · TSTCT SNUM) |
| 전송 기록(E070 · E071 · E071K) | TR · 작업의 헤더(`E070`) · 담긴 객체(`E071` — PGMID `R3TR` · `LIMU` · `LANG` …) · 담긴 테이블 키(`E071K` — 고객화 로우를 키로 가리킴) | «E071K 로 이 TR 이 바꾼 `T001` 로우를 찾는다」 | 트로브 확인(2026-11-27 · DD02T E070 · E071 · E071K · E071 PGMID 집계) |
| Enterprise Structure | IMG 맨 앞의 조직 구조 설정 묶음 — 조직 단위 정의(Definition)와 서로 연결(Assignment) | «Enterprise Structure › Assignment › 영업 조직을 회사 코드에」 | 트로브 docs/config_analysis.md · docs/config_doc_design.md |

## H. 저장소 · 사전 테이블

| 용어 | 풀이 | 쓰는 법(예) | 출처 |
|---|---|---|---|
| TADIR · PGMID(R3TR · LIMU) | 저장소 객체 목록(Directory of Repository Objects — 키 `PGMID` · `OBJECT` · `OBJ_NAME` · 패키지 `DEVCLASS`). **PGMID** `R3TR` = 객체 전체 · `LIMU` = 객체의 일부(함수 모듈 · 메서드 · 문서 등). TADIR 은 거의 `R3TR` 이고 `LIMU` 는 주로 전송 기록 `E071` 에 나온다 | «TADIR `R3TR PROG SAPMV45A`」 · «E071 `LIMU FUNC`」 | 트로브 확인(2026-11-27 · TADIR · E071 PGMID 집계 — TADIR R3TR 6,309,413 · LIMU 584) |
| TRDIR · TRDIRT | 프로그램 속성(유형 SUBC · 변경일) · 프로그램 제목. S/4HANA 에서는 TRDIR 이 테이블이 아니라 뷰다(DD02L `TABCLASS` = `VIEW`) | «TRDIR 로 SUBC 를 읽는다」 | 트로브 확인(2026-11-27 · validate_refs TRDIR → VIEW · DD02L · DD02T TRDIRT) |
| DD02L · DD02T | 테이블 정의(종류 `TABCLASS` · 전달 클래스 `CONTFLAG` · client 의존 `CLIDEP`) · 테이블 이름 글 | «DD02L 에서 `T001` 의 `CLIDEP` 확인」 | 트로브 확인(2026-11-27 · DD02L · DD02T) |
| DD03L · DD03T | 테이블 필드 정의(위치 · 키 · 유형 · 길이 `LENG` · 참조 필드 `REFTABLE` · `REFFIELD`) · 필드 글 | «DD03L `LENG` 대로 PG 컬럼 길이를 정한다」 | 트로브 확인(2026-11-27 · DD03L VBAK · DD02T DD03T) |
| DD04L · DD04T | 데이터 요소 정의 · 데이터 요소 글(라벨) | «DD04T 의 짧은 라벨」 | 트로브 확인(2026-11-27 · DD02T DD04L · DD04T) |
| DD01L · DD07L · DD07T | 도메인 정의 · 도메인 고정값 · 고정값 글 | «DD07T 로 `CONTFLAG` 값의 뜻을 읽는다」 | 트로브 확인(2026-11-27 · DD02T DD01L · DD07L · DD07T · DD07T 조회) |
| TSTC · TSTCT · TSTCP | T-code 정의(부르는 프로그램 · 화면) · T-code 이름 · T-code 파라미터(`PARAM` — 다른 T-code · 변형 · 화면 필드 값) | «T-code `V_T001` 의 TSTCP `PARAM` = `/*SM30 VIEWNAME=V_T001;UPDATE=X;`」 | 트로브 확인(2026-11-27 · DD02T TSTC · TSTCT · TSTCP · TSTCP V_T001) |
| T100 | 메시지 글 테이블(언어 · 메시지 클래스 · 번호 · 글) | «T100 의 `V1` `311`」 | 트로브 확인(2026-11-27 · DD02T T100 · get_message) |
| TDEVC | 패키지 정의 테이블(응용 컴포넌트 · 상위 패키지) | «TDEVC 로 패키지의 상위 패키지를 따라간다」 | 트로브 확인(2026-11-27 · DD02T TDEVC) |
| 텍스트 테이블 | 언어 키 + 원본 테이블 키로 이름 · 설명을 담는 테이블(예 `TSTC` 의 이름 `TSTCT`) | «`TSTCT` 에서 `SPRSL = 'E'` 이름」 | 트로브 CLAUDE.md §11(`ddic_read.pick_text_tables`) · 트로브 확인(2026-11-27 · DD02T TSTCT) |
| 체크 테이블 · 외래 키 | 필드에 들어갈 수 있는 값을 다른 테이블의 키로 검사하는 연결(필드마다 키 대응). 도메인의 값 테이블은 체크 테이블을 정할 때의 제안이다 | «`VBAK-KUNNR` 의 체크 테이블 `KNA1`(외래 키 `MANDT` · `KUNNR`)」 | 트로브 확인(2026-11-27 · get_field_details VBAK) |
| client 의존 · 독립 테이블 · MANDT | 첫 키 필드가 client(`MANDT` — 유형 `CLNT` · 길이 3)인 테이블은 client 마다 따로 로우를 가진다(DD02L `CLIDEP` = `X`). 없으면 시스템 전체가 한 벌이다 | «`T001` · `VBAK` 는 client 의존 · `TADIR` · `T000` 은 독립」 | 트로브 확인(2026-11-27 · DD02L CLIDEP · DD03L VBAK-MANDT) |

## I. API release · Clean Core · 새 모델 객체

| 용어 | 풀이 | 쓰는 법(예) | 출처 |
|---|---|---|---|
| DDLS · CDS SQL 뷰 · DDIC 뷰(VIEW) | **DDLS** = CDS 정의 소스(view entity · 투영 · 추상 · 사용자 정의 엔터티 등). 옛 방식 CDS(DDIC-based view)는 따로 **CDS SQL 뷰**가 생긴다 / **VIEW** = SE11 의 DDIC 뷰(DB 뷰 · 유지보수 뷰 · 도움말 뷰 · 뷰 변형). 둘을 섞어 부르지 않는다 | «CDS 뷰(`DDLS`) `I_SalesOrder`」 · «DDIC 뷰(`VIEW`) `V_T001`」 | 트로브 등록부 subtype_map DDLS · VIEW · 트로브 MCP 서버 설명 «CDS 뷰 = DDLS(VIEW 는 DDIC 뷰)」 |
| SRVD · SRVB | **서비스 정의**(`SRVD` — 내보낼 CDS 엔터티 목록) · **서비스 바인딩**(`SRVB` — 서비스 정의를 OData V2 · V4 로 게시) | «SRVB 가 SRVD 를 OData V4 로 게시」 | 트로브 등록부 object_type SRVD · SRVB |
| IWSV · G4BA | 게시된 OData 서비스 — `IWSV` = OData V2 서비스(SEGW 프로젝트 `IWPR` 또는 SRVB 가 게시) · `G4BA` = OData V4 서비스 그룹(SRVB 가 게시). 유형만 보고 V2 · V4 를 가른다 | «IWSV `API_SALES_ORDER_SRV`」 | 트로브 확인(2026-11-27 · validate_refs IWSV API_SALES_ORDER_SRV) · 트로브 등록부 object_type |
| BDEF · 행동 풀 | **행동 정의**(`BDEF` — RAP 업무 객체가 받는 동작 · 검증 · 결정 · 잠금 등) · **행동 풀**(behavior pool — 그 동작을 구현한 ABAP 클래스 · 핸들러는 `CL_ABAP_BEHAVIOR_HANDLER` 를 상속한 로컬 클래스) | «BDEF `I_SalesOrderTP` 의 행동 풀」 | 트로브 확인(2026-11-27 · validate_refs BDEF I_SALESORDERTP · CLAS CL_ABAP_BEHAVIOR_HANDLER) |
| RAP 투영 | 바탕 업무 객체 위에 용도별로 필드 · 동작을 골라 내놓는 층(DDLS 하위 종류 `P` Projection view + 투영 BDEF) | «투영 `C_…TP` 가 바탕 `I_…TP` 를 감싼다」 | 트로브 등록부 subtype_map DDLS `P` · 트로브 docs/mcp_api_design.md §7-27 |
| DCLS · DDLX | **접근 제어**(`DCLS` — CDS 로우 권한 `define role … grant`) · **메타데이터 확장**(`DDLX` — CDS 에 UI 주석을 따로 붙임 `annotate view`) | «`I_SalesOrder` 의 DCLS」 | 트로브 등록부 object_type DCLS · DDLX |
| API release 상태 · 계약 C0 ~ C4 | SAP 이 객체마다 매긴 공개 약속 — **C0** 확장(정해진 자리에 필드 추가) · **C1** 시스템 안 사용 · **C2** 원격 API 로 사용 · **C3** 설정 내용 관리 · **C4** AMDP 에서 사용. 상태는 RELEASED · DEPRECATED 등 | «`I_SalesOrder` 는 C0 · C1 RELEASED」 | 트로브 확인(2026-11-27 · search_help abapdocu «release contract」 · describe_object DDLS I_SALESORDER facet release) |
| ARS(API Release State) | release 상태 · 계약을 담은 SAP 기록(테이블 `ARS_W_API_STATE` API State Contract Data · C0 등록은 `SCFD_REGISTRY`). 트로브는 이 기록을 객체 유형 `APIS` 로 싣는다 | «ARS 기록에 후속이 적혀 있다」 | 트로브 확인(2026-11-27 · DD02T ARS_W_API_STATE · TSTCT SCFD_REGISTRY) |
| 후속(successor) | DEPRECATED 된 객체를 대신하라고 SAP 이 ARS 기록에 적은 객체. 이름 · 뜻이 비슷한 객체는 후속이 아니다(«뜻으로 찾은 대체 후보」) | «`X` 의 후속은 `Y`(ARS 기록)」 | 트로브 docs/mcp_api_design.md · CLAUDE.md §11(`release_read`) |
| Clean Core 레벨 | 확장이 Clean Core 에 얼마나 맞는지 나눈 등급 — A(공개 API 만) · B(classic API) · C(내부 객체) · D(수정 등 권하지 않음) | «이 확장은 레벨 C」 | 일반 SAP 지식 |
| BSP · UI5 앱(WAPA) | 웹 앱 파일을 담는 저장소 객체(`WAPA` BSP 애플리케이션). UI5 · Fiori 앱의 `manifest.json` 도 여기 있고 파일 목록은 `O2PAGDIR` 에 있다 | «WAPA `SD_SO_MANAGES1` 의 manifest」 | 트로브 확인(2026-11-27 · search_objects WAPA) · 트로브 CLAUDE.md GR14 |
| Web Dynpro(WDYA) | ABAP 의 옛 웹 화면 기술 — 애플리케이션(`WDYA`) · 컴포넌트로 만든다 | «Web Dynpro 애플리케이션 `ZSD_ORDER_APP`」 | 트로브 등록부 object_type WDYA |

## J. 도구 · 원천

| 용어 | 풀이 | 쓰는 법(예) | 출처 |
|---|---|---|---|
| ADT freesql(datapreview) | ADT 로 SELECT 한 문장을 보내 결과를 받는 SAP 기능(데이터 미리보기). 바인딩이 없어 리터럴을 문장에 넣고, 한 줄 255자 · 리터럴 안 연속 공백 · 큰따옴표 같은 SAP 쪽 규칙이 있다 | «freesql 로 `DD03L` 을 읽는다」 | 트로브 확인(2026-11-27 · query_live_data — 255자 줄 나눔 확인) · 트로브 CLAUDE.md GR23 |
| ABAP SQL(옛 Open SQL) | ABAP 안에서 쓰는 DB 독립 SQL. «Open SQL」 은 옛 이름이다. 괄호 양옆 공백 · `테이블~컬럼` 표기 같은 문법이 있다 | «ABAP SQL `SELECT … FROM vbak`」 | 트로브 확인(2026-11-27 · search_help abapdocu «Open SQL — Former name for ABAP SQL」) |
| USING CLIENT | ABAP SQL 에서 다른 client 의 로우를 읽는 추가 문구(`… USING CLIENT '000'`) | «client 000 로우는 `USING CLIENT '000'` 으로 받는다」 | 트로브 CLAUDE.md §11(`client_diff`) · docs/config_analysis.md §13-15 |
| 사용처 색인(where-used) | «이 객체를 누가 쓰나」 의 SAP 색인 — 배치 프로그램 `SAPRSEUB` · `SAPRSEUC` 가 채우고 `WBCROSSI`(include 색인) · `CROSS`(밖에서 쓰는 모듈 색인) 등에 담는다. 돌리지 않은 시스템은 결과가 빠진다 | «사용처 색인을 `SAPRSEUC` 로 다시 만든다」 | 트로브 확인(2026-11-27 · validate_refs PROG SAPRSEUC · DD02T WBCROSSI · CROSS) |
| F1 문서(DE · DZ) | 필드에서 F1 을 누르면 보이는 글 — 데이터 요소 문서(`DE`) + 화면 필드에 따로 걸린 대화 문서(`DZ` · 연결 테이블 `THLPF`). 문서 종류 ID 로 가른다 | «필드 F1 = 데이터 요소의 `DE` 문서 + 그 화면 필드의 `DZ` 문서」 | 트로브 확인(2026-11-27 · DOKIL ID 집계 DE · DZ · DD02T THLPF) |
| SAP 문서 테이블(DOKHL · DOKIL · DOKTL) · ITF | 문서 헤더 · 색인 · 글 줄. 글 줄은 SAPscript 의 **ITF** 형식(줄마다 형식 표시 + 글)이다. IMG activity 문서는 종류 `HY` | «DOKTL 줄을 ITF 규칙으로 단락으로 바꾼다」 | 트로브 확인(2026-11-27 · DD02T DOKHL · DOKIL · DOKTL · DOKIL ID HY) · 트로브 docs/config_analysis.md §9-3 |
| SAP Help Portal · ABAP 키워드 문서 | SAP 제품 문서 사이트(help.sap.com — S/4HANA · ABAP Platform 등 릴리스마다) · ABAP 문법 문서(ABAP Keyword Documentation — ABAP 릴리스마다, 예 `ABAP_816`) | «ABAP 키워드 문서 `ABAP_816` 의 `MESSAGE`」 | 트로브 확인(2026-11-27 · search_help help `S4HANA_2025_FPS01` · abapdocu `ABAP_816`) |
| SU24 · PFCG · TSTCA | **SU24** = T-code · 앱마다 권한 객체 제안값(고객 쪽 `USOBX_C`) · **PFCG** = 역할(role) 관리(`AGR_DEFINE`) · **TSTCA** = T-code 시작 권한 | «PFCG 역할에 SU24 제안값을 끌어온다」 | 트로브 확인(2026-11-27 · TSTCT SU24 · PFCG · DD02T USOBX_C · TSTCA · AGR_DEFINE) |
| 개발 T-code | `SE11` 사전 · `SE80` 객체 탐색 · `SE38` ABAP 편집기 · `SE37` 함수 모듈 · `SE24` 클래스 · `SE51` 화면 · `SE41` 메뉴 · `SE91` 메시지 · `SE93` T-code 편집 · `SE09` 이송 관리 | «SE93 으로 T-code 의 프로그램을 본다」 | 트로브 확인(2026-11-27 · TSTCT 조회) |
| 설정 T-code | `SPRO` IMG · `SM30` 뷰 유지보수 · `SM34` 뷰 클러스터 · `SE54` 유지보수 대화 생성 · `SNUM` 번호 범위 · `SCC4` client 관리 · `SOBJ` 고객화 객체 속성 | «SM30 으로 `V_T001` 을 연다」 | 트로브 확인(2026-11-27 · TSTCT 조회) |
| SICF · ICF 서비스 | SAP 이 HTTP 로 내놓는 서비스 트리(T-code `SICF` · 테이블 `ICFSERVICE`). ADT · OData · WebGUI 도 이 아래 경로다 | «ICF 서비스 `/sap/bc/adt` 가 켜져 있어야 ADT 가 된다」 | 트로브 확인(2026-11-27 · TSTCT SICF · DD02T ICFSERVICE) |
| SMW0 | 웹 저장소(T-code `SMW0` · 테이블 `WWWDATA`) — 템플릿 · 그림 같은 바이너리 파일을 SAP 안에 둔다 | «SMW0 의 엑셀 템플릿을 내려받는다」 | 트로브 확인(2026-11-27 · TSTCT SMW0 · DD02T WWWDATA) |
| WebGUI · SAP GUI for Java | SAP 화면을 웹 브라우저로 여는 SAP GUI for HTML(WebGUI) · 자바로 만든 SAP GUI(리눅스 등에서 쓴다 · 스크립트로 화면을 읽을 수 있다) | «WebGUI 로 SM30 화면을 시험」 | 트로브 docs/javagui_bdc_design.md · docs/sap_sandbox_design.md |

## 더할 자리

> 행을 더할 때는 위 표와 같은 열로 쓰고, 출처(사용자 결정 날짜 · 설계서 절 · «트로브 확인」)를 적는다. 맞는 절이 없으면 여기에 둔다.

| 용어 | 풀이 | 쓰는 법(예) | 출처 |
|---|---|---|---|
| | | | |
