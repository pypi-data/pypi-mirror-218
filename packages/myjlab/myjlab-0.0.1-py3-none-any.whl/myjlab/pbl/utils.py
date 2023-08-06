def hex_to_int(h: str) -> int:
    return int(h, base=16)


def bytes_to_int(m: bytes) -> int:
    return hex_to_int(m.hex())


def str_to_int(m: str) -> int:
    return bytes_to_int(m.encode())


def int_to_str(m: int) -> str:
    return bytes.fromhex(f'{m:x}').decode()
