thislist = ['apple', 'banana', 'cherry']
# for i in range(len(thislist)):
#     print(thislist[i])
# i=0
# while i < len(thislist):
#     print(thislist[i])
#     i += 1

newlist = [x for x in thislist if 'b' in x]
print(newlist)

frutas = ['banana', 'maçã', 'laranja', 'uva', 'abacaxi']
semUva = [x for x in frutas if x != 'uva']
print(semUva)