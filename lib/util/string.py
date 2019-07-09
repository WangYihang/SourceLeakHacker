def fixLength(data, length=0x10):
    if len(data) > length:
        result = data[0:3] + "..."
        result += data[-(length - len(result)):]
        return result
    return data