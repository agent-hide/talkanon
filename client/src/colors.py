resetColor  = "\33[0m"

def rgb(r: int, g: int, b: int):
    return "\033[38;2;{};{};{}m".format(r, g, b)

mainColor   = rgb(51, 97, 255)
errorColor  = rgb(255, 51, 51)
