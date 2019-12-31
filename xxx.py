


tabke_name='t_goods'
param='select'
list1 = ['code_id', 's_code', 'u_code', 's_link', 's_photo', 'type_id', 'unit_pinlei', 'threshold_remind']
resous=['111','']
if param=='select':
    tmp1 = ""
    tmp2=""
    tmpsql="insert into {0}(".format(tabke_name)
    for i in range(0,len(list1)):
        if i ==0:
            tmp1=list1[i]
        else:
            tmp1=tmp1+','+list1[i]
print(tmp1)



