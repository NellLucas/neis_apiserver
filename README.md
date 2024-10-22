# NEIS API SERVER
> FastAPI와 neispy를 활용한 NEIS API 서버입니다.

## Getting Started / 어떻게 시작하나요?

### Prerequisites / 선행 조건

아래 사항들이 설치가 되어있어야합니다.

```
Python3
```

### How to run? / 실행 방법

```
fastapi run main.py
```
OR
```
uvicorn main:app --reload
```

### How to use? / 사용 방법

```
http://example.com/api/meal?school_name=능주고등학교&start_date=20241022&end_date=20241031
http://example.com/api/schedule?school_name=능주고등학교&start_date=20241022&end_date=20241031
http://example.com/api/timetable?school_name=능주고등학교&date=20241022&grade=1&class_name=1
```

## Issues / 이슈

동작에 문제가 있다면 사용환경과 오류코드를 꼭 남겨주세요.

## Contribution / 기여

소스 수정사항이 있다면 Pull requests 를 열어주세요.
여러분들의 Contribution 이 프로젝트 완성에 도움이 됩니다.

## License / 라이센스

**MIT License**가 적용되어 있습니다.
