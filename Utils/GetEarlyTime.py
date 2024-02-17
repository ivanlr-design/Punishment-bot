from datetime import datetime

def GetEarlyTime(strings):
    max_fecha_hora = None
    max_string = None
    
    for string in strings:
        fecha_hora = datetime.strptime(string, "%d %m %Y %H %M")
        
        
        if max_fecha_hora is None or fecha_hora > max_fecha_hora:
            max_fecha_hora = fecha_hora
            max_string = string
    
    return max_string