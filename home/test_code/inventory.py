from django.shortcuts import render,redirect
from home.models import Tank

def inventory_list(request):
  if request.user.is_authenticated:
    data={}
    mydata=Tank.objects.filter(is_deleted=False)
    data={'mydata':mydata}
    return render(request, 'stock/inventory.html', data)
  else:
    return redirect('signin')

# test views
'''
def inventory11(request):
    stocks = Stock.objects.filter(is_deleted=False)
    inventory_data = {}

    for stock in stocks:
        key = (stock.tank.name, stock.fuel, stock.price)
        if key in inventory_data:
            inventory_data[key] += stock.quantity
        else:
            inventory_data[key] = stock.quantity

    return render(request, 'stock/inventory.html', {'inventory_data': inventory_data})
  
def inventory255(request):
    stocks_lst1=[]
    stocks_lst2=[]
    index=None
    qtyp=None
    stocks = Stock.objects.filter(is_deleted=False)
    tanks = Tank.objects.filter(is_deleted=False)

    for index,value in enumerate(tanks):
        # print (index,value)

        pass

    for i in tanks:
        # print(i.id)
        stockss = Stock.objects.filter(tank=i.id,is_deleted=False)
        qty=stockss.aggregate(Sum('quantity'))
        # print(stockss)
        stocks_lst1.append(stockss)  
        stocks_lst1.append(qty)  
        for stock in stockss:
            # print(stock)
            # print(stock.fuel)
            price=stock.price 
            fuel=stock.fuel
            stocksp = Stock.objects.filter(price=price,fuel=fuel,is_deleted=False)
            qtyp=stocksp.aggregate(Sum('quantity'))
            stocks_lst2.append(stocksp)
            stocks_lst2.append(qtyp)
            # print(qtyp)

    print(stocks_lst1)
    # stocks_lst1[index]

    for i in stocks_lst1[0]:
        # print(i.price)
        price=i.price
        fuel=i.fuel
        is_deleted=False
        # stk=Stock.objects.get(price=price,fuel=fuel,is_deleted=False)
        stocksp = Stock.objects.filter(price=price,fuel=fuel,is_deleted=False)
        qtyp=stocksp.aggregate(Sum('quantity'))
        # print(qtyp)
       
    #     pass

    # for stk in stocks_lst:
    #   print(stk[0] , "i m skt")

    return render(request, 'stock/inventory.html', {'stocks': stocks_lst1})


def inventory123(request):
    stocks_lst=[]
    stocks = Stock.objects.filter(is_deleted=False)
    tanks = Tank.objects.filter(is_deleted=False)
    for index,value in enumerate(tanks):
        # print (index,value)
        pass
    for i in tanks:
        
        stockss = Stock.objects.filter(tank=i.id,is_deleted=False)
        qty=stockss.aggregate(Sum('quantity'))
        qtyp=None
        
        for stock in stockss:
          price=stock.price 
          fuel=stock.fuel
          stocksp = Stock.objects.filter(price=price,fuel=fuel,is_deleted=False).values()
          
          qtyp=stocksp.aggregate(Sum('quantity'))
          stocks_lst.append(stocksp,qtyp)

       
         

    for stk in stocks_lst:
      print(stk , "i m skt")

    return render(request, 'stock/inventory.html', {'stocks': stocks_lst})

    '''