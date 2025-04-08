from src.utils import get_all_data, read_nettskjema_data, read_participant_data


if __name__ == "__main__":
    nettskjema_df = read_nettskjema_data()
    experiments_df = read_participant_data()
    df = get_all_data(process_data=True)
    from IPython import embed
    embed()
