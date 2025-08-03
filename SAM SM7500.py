Konc = range(10,22,1)
Uroven = range(0,45,1)
res=[]
v_terget = 45
c_terget = 0.2
m_target = v_terget * 0.2


for i in Konc:
    res.append(f"Концентрация {str(i)}")
    for j in Uroven:
        x = m_target - (j * (i / 100))
        y = v_terget - j - x
        if x and y >= 0:
            res.append(f"Объем: {str(j)} Л | Добавить Гидронола В20: {str(round(x,1))} Л и Воды ДИ {str(round(y,1))}")
        else:
            next
filep = open("resultSM7500.txt", "w+")
filep.write("\n".join(res))