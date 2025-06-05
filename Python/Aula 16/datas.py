import datetime

for i in range(10):
    x = datetime.datetime.now()
    print(x)

print(x.year)
print(x.strftime("%A"))

#criando uma data

niver = datetime.datetime(1988, 7, 7, 18, 55, 00, 000000)

print(niver)
print(niver.strftime("%a"))
print(niver.strftime("%A"))
print(niver.strftime("%w"))
print(niver.strftime("%d"))
print(niver.strftime("%b"))
print(niver.strftime("%B"))
print(niver.strftime("%m"))
print(niver.strftime("%y"))
print(niver.strftime("%Y"))
print(niver.strftime("%H"))
print(niver.strftime("%I"))
print(niver.strftime("%p"))
print(niver.strftime("%M"))
print(niver.strftime("%S"))
print(niver.strftime("%f"))
print(niver.strftime("%z"))
print(niver.strftime("%Z"))
print(niver.strftime("%j"))
print(niver.strftime("%U"))
print(niver.strftime("%W"))
print(niver.strftime("%c"))
print(niver.strftime("%C"))
print(niver.strftime("%x"))
print(niver.strftime("%X"))
print(niver.strftime("%%"))
print(niver.strftime("%G"))
print(niver.strftime("%u"))
print(niver.strftime("%V"))
