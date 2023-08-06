from datetime import datetime, timedelta, date

def get_first_day_of_week(date : date ) -> date:
    # 找到给定日期所在周的第一天（星期一）
    start_of_week = date - timedelta(days=date.weekday())

    return start_of_week


if __name__ == "__main__":
    n = datetime.now()
    d = get_first_day_of_week(n.date())
    print(d)