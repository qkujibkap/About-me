tro = 50.25
trvi = 9.55
trvo = 40.7
op = 0.67
p = []
for tek in range (13,23):
  p.append("Концентрация: " + str(tek))
  for teu in range (45,75):
   tevi = op * teu * tek / 100
   tevo = op * teu * (100-tek) / 100
   vigon = " Гидронол В20: "+ str(round(trvi - tevi,2))
   voda = " Вода ДИ: " + str(round(trvo - tevo,2))
   p.append("Уровень: " + str(teu) +" | Надо"+ vigon +" Л" + voda+" Л")
filep = open("result.txt", "w+")
filep.write("\n".join(p))