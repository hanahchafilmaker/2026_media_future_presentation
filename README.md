# XCONDA 발표 덱 (2026.09.09 · 미디어의 미래)

큐브베리 XCONDA — AI 웹드라마/영화 하이브리드 제작 워크플로우 발표자료.
**하나의 `index.html`** 로 동작하며, 별도 서버 없이 브라우저에서 바로 열립니다.

## 폴더 구조

```
├── index.html          # 발표 덱 (단일 파일, 더블클릭으로 실행)
├── download_assets.py  # 영상·이미지 일괄 다운로더
├── videos/             # 영상 파일 (로컬 우선 재생)
│   ├── blockingboard_intro.mp4   # 블로킹보드 소개 v4 (1.6MB, 이미 있음)
│   └── flexboard_intro.mp4       # 플렉스보드 설명 (8.9MB, 이미 있음)
└── images/             # 이미지 파일 (로컬 우선 표시)
    ├── xconda_logo.png / xconda_qr_openchat.png
    ├── 1000yActor.jpg / 1000yActor2.png
    ├── thousandyears_character.png
    ├── coldsite_still.jpg / division_zero_still.jpg
    ├── eiel_poster.jpg / mokguryung_still.png
    └── ... (9개)
```

## 재생 원리 (로컬 우선 + Drive 폴백)

1. `videos/`, `images/` 의 로컬 파일이 있으면 → **그걸 재생/표시**
2. 없으면 → Google Drive 스트리밍으로 자동 대체
3. `leebyoungwook_selca.jpg`(이병욱 셀카)는 `index.html`에 내장되어 있어 항상 표시됩니다.

> 즉, 파일이 일부 빠져 있어도 발표는 깨지지 않습니다.

## Git 저장소에 올리기

### 1) 나머지 에셋 받기

```bash
python3 download_assets.py
```

총 용량: 영상 약 3.5GB(그중 트레일러 2편이 각 ~923MB) + 이미지 약 4MB

### 2) Git LFS 설정 (권장)

영상 파일이 커서 GitHub 기본 100MB 제한에 걸립니다.

```bash
git lfs track "videos/*.mp4"
git add .
git commit -m "XCONDA 발표 덱"
git push
```

### 대안 — 용량 줄이기

- 대용량(트레일러 2편, 6·25 재연, 씨앗전쟁, 천년의 사랑 본편, 토이팜)만 빼고 올려도
  나머지는 로컬 재생되고, 빠진 것들은 Drive 스트리밍으로 자동 대체됩니다.

## 조작법

| 키 | 동작 |
|---|---|
| `→` / `Space` | 다음 슬라이드 |
| `←` | 이전 슬라이드 |
| `]` | 플레이리스트 다음 영상 |
| `A` | 부록(Q&A) 진입 / `Esc` 복귀 |

## 참고

- 발표자 노트는 각 슬라이드의 `notes-src`에 내장되어 있습니다.
- `uploads/` 폴더는 원본 업로드 소스(수정 전 파일)입니다 — 발표 실행에는 필요 없습니다.
