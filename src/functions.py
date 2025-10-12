def format_timedelta(td_series):
    """Convert timedelta to readable format '00 hours and 00 minutes' """
    total_seconds = td_series.dt.total_seconds()
    hours = (total_seconds // 3600).astype(int)
    minutes = ((total_seconds % 3600) // 60).astype(int)
    return hours.astype(str) + ' hours and ' + minutes.astype(str).str.zfill(2) + ' minutes'