fin = open("city_data.txt", "r+", encoding="utf-8")
fout = open("moscow.txt", "w", encoding="utf-8")
s = set()
lines = fin.readlines()
for i in range(1, len(lines) - 1, 2):
    s.add((lines[i], lines[i + 1]))
for i in s:
    fout.write(i[0])
    fout.write(i[1])
