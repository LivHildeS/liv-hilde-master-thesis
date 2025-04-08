from src.get_constants import get_constants

CONSTANTS = get_constants()
WEBSITES = CONSTANTS["websites"]
DEVICES = CONSTANTS["devices"]


def count_accept(answer):
    if "accept" in answer:
        return 1
    if "reject" in answer:
        return 0
    else:
        raise ValueError(f"Answer {answer} was neither accept or reject. ")


def get_website_averages(df):
    results = {}
    times = {}
    for device in DEVICES:
        results[device] = {}
        times[device] = {}
        for website in WEBSITES:
            answer_column_name = f"{device}.{website}.answer"
            time_column_name = f"{device}.{website}.time"
            answers = df[answer_column_name].apply(count_accept)
            results[device][website] = int(answers.sum())
            times[device][website] = round(float(df[time_column_name].mean()), 3)
    print(f"{results=}")
    print(f"{times=}")
    average_computer_clicks = 100 * sum(list(results['computer'].values())) / (len(WEBSITES) * len(df))
    average_phone_clicks = 100 * sum(list(results['phone'].values())) / (len(WEBSITES) * len(df))
    average_clicks = (average_computer_clicks + average_phone_clicks) / 2
    print(f"{average_computer_clicks=}")
    print(f"{average_phone_clicks=}")
    print(f"{average_clicks=}")
    print(f"{len(df)=}")
