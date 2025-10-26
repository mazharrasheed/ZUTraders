from django.contrib import messages
from django.shortcuts import redirect, render,get_object_or_404
from home.forms import  AccountForm,TransactionForm
from home.models import Account,Transaction,Sale

# Create your views here.

def add_account(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
      mydata = Account.objects.filter(is_deleted=False)
      form = AccountForm(request.POST)
      if form.is_valid():
        form.save()
        messages.success(request,"Accounts Added Succesfuly !!")
        return redirect('accounts')
    else:
      form = AccountForm()
      mydata = Account.objects.filter(is_deleted=False)
  else:
    return redirect('signin')
  data={'mydata':mydata,'form':form}
  return render(request,'accounts/accounts.html',data)

def edit_account(request,id):
  if request.user.is_authenticated: 
    data={}
    if request.method == 'POST':
      mydata=Account.objects.get(id=id)
      form = AccountForm(request.POST,instance=mydata)
      if form.is_valid():
        form.save()
        messages.success(request,"Accounts Updated Succesfuly !!")
        return redirect('accounts')
    else:
        mydata=Account.objects.get(id=id)
        form = AccountForm(instance=mydata)
    data={'form': form, 'mydata':mydata,'update':True}
    return render(request, 'accounts/accounts.html', data)
  else:
    return redirect('signin')
  
def delete_account(request,id):
  if request.user.is_authenticated:
    try:
      mydata=Account.objects.get(id=id)
      mydata.is_deleted=True
      mydata.save()
      messages.success(request,"Accounts Deleted Succesfuly !!")
      return redirect('accounts')
    except:
      pass
  else:
    return redirect('signin')
  
# views.py


def add_transaction(request):
    if request.user.is_authenticated: 
        transactions = Transaction.objects.all()
        if request.method == 'POST':
            form = TransactionForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('transaction')
        else:
            form = TransactionForm()
            transactions = Transaction.objects.all()
            accounts = Account.objects.filter(is_deleted=False)
            assets = {}
            liabilities = {}
            equity_account = {}
            revenue_account = {}
            expenses_account = {}

            equity = 0
            revenue = 0
            expenses = 0
        
            for account in accounts:
                balance = account.balance  # Use the balance field as the initial balance
                
                # Get all transactions where the account is either debited or credited
                debit_transactions = Transaction.objects.filter(debit_account=account)
                credit_transactions = Transaction.objects.filter(credit_account=account)
                
                # Calculate the net balance for the account
                for transaction in debit_transactions:
                    balance += transaction.amount  
                for transaction in credit_transactions:
                    balance -= transaction.amount
                    
                if balance != account.balance:  # Skip accounts with no transactions
                    if account.account_type == 'Asset':
                        assets[account] = balance
                    elif account.account_type == 'Liability':
                        liabilities[account] = -balance
                    elif account.account_type == 'Equity':
                        equity -= balance
                        equity_account[account] = -balance
                    elif account.account_type == 'Revenue':
                        revenue -= balance
                        revenue_account[account] = -balance
                    elif account.account_type == 'Expense':
                        expenses += balance
                        expenses_account[account] = balance
           
            total_assets = int(sum(assets.values()))
            total_liabilities = int(sum(liabilities.values()))
            total_equity = int(sum(equity_account.values()))

            if total_assets == total_liabilities+total_equity :
                messages.success(request,"Balance Sheet is Balanced  !!")
                
            else:
                messages.error(request," Balance Sheet is not Balanced Please check !!")
        return render(request, 'accounts/add_transaction.html', {'form': form,'mydata': transactions})
    else:
        return redirect('signin')

# views.py

def account_report(request,id):
    if request.user.is_authenticated:
        equity_account = {}
        revenue_account = {}
        credit_balance=0
        debit_balance=0
        account = get_object_or_404(Account, pk=id)
        print(account.debit_transactions.all(),"dffdsf")
        debit_transactions = account.debit_transactions.all()
        credit_transactions = account.credit_transactions.all()

        for transaction in debit_transactions:
            debit_balance += transaction.amount  
        for transaction in credit_transactions:
            credit_balance += transaction.amount
        if account.account_type=='Asset' :
            balance=int(debit_balance)-int(credit_balance)
        elif account.account_type=='Expense' :
            balance=int(debit_balance)-int(credit_balance)
        elif account.account_type== 'Revenue':
            balance=int(credit_balance)-int(debit_balance)
        elif account.account_type=='Liability' :
            balance=int(credit_balance)-int(debit_balance)
        elif account.account_type=='Equity' :
            balance=int(credit_balance)-int(debit_balance)
        elif account.account_type=='Gain' :
            balance=int(debit_balance)-int(credit_balance)
        elif account.account_type=='Loss' :
            balance=int(credit_balance)-int(debit_balance)

        return render(request, 'accounts/account_report.html', {'account': account,
        'debit_transactions': debit_transactions,
        'credit_transactions': credit_transactions,
        'balance':balance,
        })
    else:
        return redirect('signin')
        
'''
def balance_sheet111(request):
    if request.user.is_authenticated:
        accounts = Account.objects.all()
        assets = {}
        liabilities = {}
        equity = 0
        revenue = 0
        expenses = 0
        
        for account in accounts:
            balance = account.balance  # Use the balance field as the initial balance
            for transaction in account.transactions.all():
                if transaction.debit:
                    balance += transaction.amount
                else:
                    balance -= transaction.amount
            if balance != account.balance:  # Skip accounts with no transactions
                if account.account_type == 'Asset':
                    assets[account] = balance
                elif account.account_type == 'Liability':
                    liabilities[account] = balance
                elif account.account_type == 'Equity':
                    equity += balance
                elif account.account_type == 'Revenue':
                    revenue += balance
                elif account.account_type == 'Expense':
                    expenses += balance
        
        return render(request, 'balance_sheet.html', {'assets': assets, 'liabilities': liabilities, 'equity': equity, 'revenue': revenue, 'expenses': expenses})
    else:
        return redirect('signin')'''

def laddger_balance(request): #not used its iddle

        accounts = Account.objects.filter(is_deleted=False)
        assets = {}
        liabilities = {}
        equity_account = {}
        revenue_account = {}
        expenses_account = {}
        

        equity = 0
        revenue = 0
        expenses = 0
     
        for account in accounts:
            balance = account.balance  # Use the balance field as the initial balance
            
            # Get all transactions where the account is either debited or credited
            debit_transactions = Transaction.objects.filter(debit_account=account)
            credit_transactions = Transaction.objects.filter(credit_account=account)
            
            # Calculate the net balance for the account
            for transaction in debit_transactions:
                balance += transaction.amount  
            for transaction in credit_transactions:
                balance -= transaction.amount
                   
            if balance != account.balance:  # Skip accounts with no transactions
                if account.account_type == 'Asset':
                    assets[account] = balance
                elif account.account_type == 'Liability':
                    liabilities[account] = balance
                elif account.account_type == 'Equity':
                    equity -= balance
                    equity_account[account] = -balance
                elif account.account_type == 'Revenue':
                    revenue -= balance
                    revenue_account[account] = -balance
                elif account.account_type == 'Expense':
                    expenses += balance
                    expenses_account[account] = balance
                

            # sum(for i in assets.values):
        total_assets = int(sum(assets.values()))
        total_liabilities = int(sum(liabilities.values()))
        total_equity = int(sum(equity_account.values()))

        if total_assets == total_liabilities+total_equity :
            messages.success(request,"Balance Sheet is Balanced  !!")
            
        else:
            messages.error(request," Balance Sheet is not Balanced Please check !!")


def balance_sheet(request):

    if request.user.is_authenticated:
        
        accounts = Account.objects.filter(is_deleted=False)
        assets = {}
        liabilities = {}
        equity_account = {}
        revenue_account = {}
        expenses_account = {}
        gain_account = {}
        loss_account = {}
        liabilitie = 0
        asset=0
        equity = 0
        revenue = 0
        expenses = 0
        gain = 0
        loss = 0
     
        for account in accounts:
            balance = account.balance  # Use the balance field as the initial balance
            
            # Get all transactions where the account is either debited or credited
            debit_transactions = Transaction.objects.filter(debit_account=account)
            credit_transactions = Transaction.objects.filter(credit_account=account)
            
            # Calculate the net balance for the account
            for transaction in debit_transactions:
                balance += transaction.amount  
            for transaction in credit_transactions:
                balance -= transaction.amount
                   
            if balance != account.balance:  # Skip accounts with no transactions
                if account.account_type == 'Asset':
                    asset+=balance
                    assets[account] = balance
                elif account.account_type == 'Liability':
                    liabilitie-=balance
                    liabilities[account] = -balance
                elif account.account_type == 'Equity':
                    equity -= balance
                    equity_account[account] = -balance
                elif account.account_type == 'Revenue':
                    for transaction in credit_transactions:
                        revenue += transaction.amount 
                    # revenue -= balance
                    revenue_account[account] = -balance
                elif account.account_type == 'Expense':
                    expenses += balance
                    expenses_account[account] = balance
                elif account.account_type == 'Gain':
                    gain += balance
                    gain_account[account] = balance
                elif account.account_type == 'Loss':
                    loss += balance
                    loss_account[account] = balance
                    
        total_assets = int(sum(assets.values()))
        total_liabilities = int(sum(liabilities.values()))
        total_equity = int(sum(equity_account.values()))

        if total_assets == total_liabilities+total_equity :
            messages.success(request,"Balance Sheet is Balanced  !!")

        else:
            messages.error(request," Balance Sheet is not Balanced Please check !!")

        total_equity = sum(liabilities.values())
        mydata={'assets': assets,
        'liabilities': liabilities, 
        'revenue_account':revenue_account,
        'equity_account':equity_account,
        'expenses_account':expenses_account,
        'gain_account':gain_account,
        'loss_account':loss_account,
        'asset':asset,
        'liabilitie':liabilitie,
        'equity': equity,
        'revenue': revenue,
        'expenses': expenses,
        'gain': gain,
        'loss': loss,
        
        }

        net_prifit=revenue-expenses
       
        return render(request, 'accounts/balance_sheet.html', mydata)
    else:
        return redirect('signin')

def balance_sheet1111(request):

    if request.user.is_authenticated:
        accounts = Account.objects.all()
        assets = {}
        liabilities = {}
        for account in accounts:
            balance = 0
            for transaction in account.debit_transactions.all():
                balance += transaction.amount
            for transaction in account.credit_transactions.all():
                balance -= transaction.amount
            if account.account_type == 'Asset':
                assets[account] = balance
            elif account.account_type == 'Liability':
                liabilities[account] = balance
        equity = sum(balance for balance in assets.values()) - sum(balance for balance in liabilities.values())
        return render(request, 'accounts/balance_sheet.html', {'assets': assets, 'liabilities': liabilities, 'equity': equity})
        
    else:
        return redirect('signin')  

# def balance(request):
#     accounts = Account.objects.all()
#     balances = {}
#     for account in accounts:
#         credit_total = Ledger.objects.filter(account=account, transaction_type='credit').aggregate(models.Sum('amount'))['amount__sum'] or 0
#         debit_total = Ledger.objects.filter(account=account, transaction_type='debit').aggregate(models.Sum('amount'))['amount__sum'] or 0
#         balance = credit_total - debit_total
#         balances[account] = balance
#     return render(request, 'balance.html', {'balances': balances})