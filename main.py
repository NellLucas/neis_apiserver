from fastapi import FastAPI
from neispy import Neispy
from neispy.error import DataNotFound

app = FastAPI()

# 급식메뉴 API endpoint
@app.get("/api/meal")
async def get_meal(school_name: str, start_date: str, end_date: str):
    async with Neispy() as neis:
        scinfo = await neis.schoolInfo(SCHUL_NM=school_name)
        if scinfo.schoolInfo[1].row:
            row = scinfo.schoolInfo[1].row[0]
            AE = row.ATPT_OFCDC_SC_CODE  # 교육청 코드
            SE = row.SD_SCHUL_CODE       # 학교 코드
        else:
            return {'error': 'School not found'}

        meals = []

        # 1 - 조식, 2 - 중식, 3 - 석식
        meal_codes = ['1', '2', '3']

        for meal_code in meal_codes:
            try:
                scmeal = await neis.mealServiceDietInfo(
                    ATPT_OFCDC_SC_CODE=AE,
                    SD_SCHUL_CODE=SE,
                    MMEAL_SC_CODE=meal_code,
                    MLSV_FROM_YMD=start_date,
                    MLSV_TO_YMD=end_date
                )

                # 전처리
                for meal_info in scmeal.mealServiceDietInfo[1].row:
                    meal_date = meal_info.MLSV_YMD
                    meal_name = meal_info.MMEAL_SC_CODE  # 조식/중식/석식
                    dish_name = meal_info.DDISH_NM.replace("<br/>", "\n")  # <br/> => 줄바꿈
                    meals.append({
                        'date': meal_date,
                        'meal_name': meal_name,
                        'dishes': dish_name
                    })
            except DataNotFound:
                continue
            except Exception as e:
                return {'error': str(e)}

        if not meals:
            return {'error': 'No meal data found for the given dates'}

        # Sort
        meals.sort(key=lambda x: (x['date'], x['meal_name']))

        return {'meals': meals}

# 학사일정 API endpoint
@app.get("/api/schedule")
async def get_schedule(school_name: str, start_date: str, end_date: str):
    async with Neispy() as neis:
        scinfo = await neis.schoolInfo(SCHUL_NM=school_name)
        if scinfo.schoolInfo[1].row:
            row = scinfo.schoolInfo[1].row[0]
            AE = row.ATPT_OFCDC_SC_CODE  # 교육청 코드
            SE = row.SD_SCHUL_CODE       # 학교 코드
        else:
            return {'error': 'School not found'}

        try:
            scschedule = await neis.SchoolSchedule(
                ATPT_OFCDC_SC_CODE=AE,
                SD_SCHUL_CODE=SE,
                AA_FROM_YMD=start_date,
                AA_TO_YMD=end_date
            )

            # 전처리
            schedules = []
            for schedule_info in scschedule.SchoolSchedule[1].row:
                event_name = schedule_info.EVENT_NM
                event_date = schedule_info.AA_YMD
                schedules.append({
                    'date': event_date,
                    'event_name': event_name
                })

            return {'schedules': schedules}
        except DataNotFound:
            return {'error': 'No schedule data found for the given dates'}
        except Exception as e:
            return {'error': str(e)}

# 시간표 API endpoint
@app.get("/api/timetable")
async def get_timetable(school_name: str, date: str, grade: str, class_name: str):
    async with Neispy() as neis:
        scinfo = await neis.schoolInfo(SCHUL_NM=school_name)
        if scinfo.schoolInfo[1].row:
            row = scinfo.schoolInfo[1].row[0]
            AE = row.ATPT_OFCDC_SC_CODE  # 교육청 코드
            SE = row.SD_SCHUL_CODE       # 학교 코드
        else:
            return {'error': 'School not found'}

        # 학년 및 학기 결정
        AY = date[:4]  # 연도

        # 학기 결정 로직
        month = int(date[4:6])
        SEM = "1" if month < 8 else "2"

        try:
            sctimetable = await neis.hisTimetable(
                ATPT_OFCDC_SC_CODE=AE,
                SD_SCHUL_CODE=SE,
                AY=AY,
                SEM=SEM,
                GRADE=grade,
                CLASS_NM=class_name,
                ALL_TI_YMD=date
            )

            # 전처리
            timetables = []
            for timetable_info in sctimetable.hisTimetable[1].row:
                date = timetable_info.ALL_TI_YMD
                period = timetable_info.PERIO
                subject = timetable_info.ITRT_CNTNT
                timetables.append({
                    'date': date,
                    'period': period,
                    'subject': subject
                })

            return {'timetables': timetables}
        except DataNotFound:
            return {'error': 'No timetable data found for the given dates'}
        except Exception as e:
            return {'error': str(e)}
