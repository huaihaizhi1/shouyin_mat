

aaa='125'
print(len(aaa))
bbb=13-len(aaa)
print(bbb)
ccc=''
for i in range(0,bbb):
    if i==bbb-1:
        ccc=ccc+'1'
    else:
        ccc=ccc+'0'
ddd=aaa+ccc
print(ddd)