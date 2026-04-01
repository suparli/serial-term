import datetime

def format_log(data: bytes, as_hex: bool = False, include_time: bool = True) -> str:
    """Mengubah byte data jadi text dengan opsi hex dan waktu"""
    prefix = ""
    if include_time:
        now = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        prefix = f"[{now}] "

    if as_hex:
        text = data.hex(" ")
    else:
        text = data.decode("utf-8", errors="replace").replace("\r\n", "\n")
        
    return f"{prefix}{text}"
