from django.contrib import messages
from django.shortcuts import redirect, render,get_object_or_404
from home.forms import  AccountForm,Employee_AccountForm,Customer_AccountForm,Supplier_AccountForm,Cheque_AccountForm,TransactionForm,AccountStatementForm
from home.models import Account,Transaction
from django.contrib.auth.decorators import login_required,permission_required
from django.db.models import Sum
from datetime import datetime, timedelta
from django.utils import timezone

# Create your views here.



@login_required
@permission_required('home.view_account', login_url='/login/')
def accounts(request):
    mydata = Account.objects.filter(is_deleted=False).order_by("-id")
    data={'mydata':mydata}
    return render(request,'accounts/index.html',data)

@login_required
@permission_required('home.add_account', login_url='/login/')
def create_accounts(request):
    mydata = Account.objects.filter(is_deleted=False).order_by("-id")
    data={'mydata':mydata}
    return render(request,'accounts/create_accounts.html',data)

@login_required
@permission_required('home.add_account', login_url='/login/')
def add_account(request):

    account_type=(request.GET.get('account_type'))
    if request.method == 'POST':
            mydata = Account.objects.filter(is_deleted=False).order_by("-id")
            if account_type=="employee":
                form = Employee_AccountForm(request.POST)
                mydata = Account.objects.filter(is_deleted=False,employee__isnull=False).order_by("-id")
            elif account_type=="customer": 
                mydata = Account.objects.filter(is_deleted=False,customer__isnull=False).order_by("-id")
                form = Customer_AccountForm(request.POST)
            elif account_type=="supplier":
                mydata = Account.objects.filter(is_deleted=False,supplier__isnull=False).order_by("-id")
                form = Supplier_AccountForm(request.POST)
            elif account_type=="cheque":
                mydata = Account.objects.filter(is_deleted=False,cheque__isnull=False).order_by("-id")
                form = Cheque_AccountForm(request.POST)
                if form.is_valid():
                    form.save(commit=False)
                    cheque=form.cleaned_data.get('cheque')
                    print(cheque.cheque_amount,'4444')
                    messages.success(request,"Accounts Added Succesfuly !!")
                    return redirect('createaccounts')
            else:
                form = AccountForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,"Accounts Added Succesfuly !!")
                return redirect('createaccounts')
    else:
        mydata = Account.objects.filter(is_deleted=False).order_by("-id")
        if account_type=="employee":
            form = Employee_AccountForm()
            mydata = Account.objects.filter(is_deleted=False,employee__isnull=False).order_by("-id")
        elif account_type=="customer":
            mydata = Account.objects.filter(is_deleted=False,customer__isnull=False).order_by("-id")
            form = Customer_AccountForm()
        elif account_type=="supplier":
            mydata = Account.objects.filter(is_deleted=False,supplier__isnull=False).order_by("-id")
            form = Supplier_AccountForm()
        elif account_type=="cheque":
            mydata = Account.objects.filter(is_deleted=False,cheque__isnull=False).order_by("-id")
            form = Cheque_AccountForm()
        else:
            form = AccountForm()

    data={'mydata':mydata,'form':form,'account_type':account_type}
    return render(request,'accounts/accounts.html',data)

@login_required
@permission_required('home.change_account', login_url='/login/')
def edit_account(request,id):

    mydata=Account.objects.get(id=id)
    data={}

    if request.method == 'POST':
        mydata=Account.objects.get(id=id)
        if mydata.employee=="employee":
            form = Employee_AccountForm(request.POST)
        if mydata.customer:
            form = Customer_AccountForm(request.POST,instance=mydata)
        elif mydata.supplier:
            form = Supplier_AccountForm(request.POST,instance=mydata)
        elif mydata.cheque:
            form = Cheque_AccountForm(request.POST,instance=mydata)
            if form.is_valid():
                    account=form.save(commit=False)
                    cheque=form.cleaned_data.get('cheque')
                    print(cheque.cheque_amount,'66666')
                    account.balance=cheque.cheque_amount
                    account.save()
                    print(account.balance,'7777')

                    messages.success(request,"Accounts Added Succesfuly !!")
                    return redirect('createaccounts')
        else:
            form = AccountForm(request.POST,instance=mydata)
        if form.is_valid():
            form.save()
            messages.success(request,"Account Updated Succesfuly !!")
            return redirect('createaccounts')
    else:
        mydata=Account.objects.get(id=id)
        if mydata=="employee":
            form = Employee_AccountForm(instance=mydata)
        if mydata.customer:
            form = Customer_AccountForm(instance=mydata)
        elif mydata.supplier:
            form = Supplier_AccountForm(instance=mydata)
        elif mydata.cheque:
            form = Cheque_AccountForm(instance=mydata)
        else:
            form = AccountForm(instance=mydata)
    data={'form': form, 'mydata':mydata,'update':True}
    return render(request, 'accounts/accounts.html', data)

@login_required
@permission_required('home.delete_account', login_url='/login/')
def delete_account(request,id):
    try:
        mydata=Account.objects.get(id=id)
        mydata.is_deleted=True
        mydata.save()
        messages.success(request,"Accounts Deleted Succesfuly !!")
        return redirect('accounts')
    except:
        pass

@login_required
@permission_required('home.view_transaction', login_url='/login/')
def list_transaction(request):

    transactions = Transaction.objects.all()
    return render(request, 'accounts/transactions_list.html', {'mydata': transactions})

@login_required
@permission_required('home.add_transaction', login_url='/login/')
def add_transaction(request):

    transactions = Transaction.objects.all()
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction=form.save(commit=False)
            transaction.made_by=request.user
            transaction.transaction_ref="TRX"+str(transaction.id)+str(datetime.now().strftime("%Y%m%d%H%M%S"))
            transaction.save()
            return redirect('transaction')
    else:
        form = TransactionForm()
        transactions = Transaction.objects.all()

        # to check balance sheeet is balanced or not
        accounts = Account.objects.filter(is_deleted=False)
        assets = {}
        liabilities = {}
        equity_account = {}
        revenue_account = {}
        expenses_account = {}
        commitment_account = {}

        equity = 0
        revenue = 0
        expenses = 0
        commitment=0
    
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
                elif account.account_type == 'Commitment':
                    commitment += balance
                    commitment_account[account] = balance
        total_assets = int(sum(assets.values()))
        total_liabilities = int(sum(liabilities.values()))
        total_equity = int(sum(equity_account.values()))
        # if total_assets == total_liabilities+total_equity :
        #     messages.success(request,"Balance Sheet is Balanced  !!")    
        # else:
        #     messages.error(request," Balance Sheet is not Balanced Please check !!")
    return render(request, 'accounts/add_transaction.html', {'form': form,'mydata': transactions})

@login_required
@permission_required('home.change_transaction', login_url='/login/')
def edit_transaction(request,id):
    
    if request.method=="POST":
        transaction = Transaction.objects.get(id=id)
        form = TransactionForm(request.POST,instance=transaction)
        if form.is_valid():
            transaction=form.save(commit=False)
            transaction.made_by=request.user
            transaction.transaction_ref="TRX"+str(transaction.id)+str(datetime.now().strftime("%Y%m%d%H%M%S"))
            transaction.save()
            messages.success(request,"Transaction Updated successfully !!")
            return redirect('transaction')
    else:
        transaction = Transaction.objects.get(id=id)
        form = TransactionForm(instance=transaction)

    return render(request, 'accounts/add_transaction.html', {'form': form,'mydata': transaction, 'update':True})


@login_required
@permission_required('home.delete_transaction', login_url='/login/')
def delete_transaction(request,id):
    transaction = Transaction.objects.filter(id=id)
    transaction.delete()
    # transaction.save()
    return redirect('transaction')
    pass

# views.py
from django.db.models import Q
@login_required
@permission_required('home.view_account', login_url='/login/')
def account_report(request,id):
    if request.user.is_authenticated:
        equity_account = {}
        revenue_account = {}
        credit_balance=0
        debit_balance=0
        
        account = get_object_or_404(Account, pk=id)
        balance=account.balance
        debit_transactions = account.debit_transactions.all()
        credit_transactions = account.credit_transactions.all()
        # transactions = account.debit_transactions.all().union(account.credit_transactions.all()).order_by('date')
        transactions = Transaction.objects.filter(Q(debit_account=account) | Q(credit_account=account)).order_by('date')
        # print(transactions)

        for transaction in debit_transactions:
            debit_balance += transaction.amount  
        for transaction in credit_transactions:
            credit_balance += transaction.amount
        if account.account_type=='Asset' :
            balance+=int(debit_balance)-int(credit_balance)
        elif account.account_type=='Expense' :
            balance+=int(debit_balance)-int(credit_balance)
        elif account.account_type== 'Revenue':
            balance+=int(credit_balance)-int(debit_balance)
        elif account.account_type=='Liability' :
            balance+=int(credit_balance)-int(debit_balance)
        elif account.account_type=='Equity' :
            balance+=int(credit_balance)-int(debit_balance)
        elif account.account_type=='Gain' :
            balance+=int(debit_balance)-int(credit_balance)
        elif account.account_type=='Loss' :
            balance+=int(credit_balance)-int(debit_balance)
        elif account.account_type=='Commitment' :
            balance+=(debit_balance)-int(credit_balance)
        elif account.account_type=='Commitment_Received' :
            balance+=int(credit_balance)-int(debit_balance)

        return render(request, 'accounts/account_report.html', {'account': account,
        'debit_transactions': debit_transactions,
        'credit_transactions': credit_transactions,
        'balance':balance,
         'transactions': transactions,
        
        })
    else:
        return redirect('signin')
        

@login_required
@permission_required('home.view_account', login_url='/login/')
def balance_sheet(request):
    accounts = Account.objects.filter(is_deleted=False)
    assets = {}
    liabilities = {}
    equity_account = {}
    revenue_account = {}
    expenses_account = {}
    gain_account = {}
    loss_account = {}
    commitment_account = {}
    commitment_received_account = {}

    liabilitie = 0
    asset=0
    equity = 0
    revenue = 0
    expenses = 0
    gain = 0
    loss = 0
    commitment=0
    commitment_received=0

    for account in accounts:
        balance = account.balance  # Use the balance field as the initial balance
        # Get all transactions where the account is either debited or credited
        debit_transactions = Transaction.objects.filter(debit_account=account)
        credit_transactions = Transaction.objects.filter(credit_account=account)          
        if account.customer !=None:
            ct=account.customer
            for tr in debit_transactions:
                cust=tr.debit_account.customer
                if ct==cust:
                    amt=tr.amount
                    # print(amt)
            

        # Calculate the net balance for the account
        for transaction in debit_transactions:
            balance += transaction.amount  
        for transaction in credit_transactions:
            balance -= transaction.amount
        if balance != account.balance:  # Skip accounts with no transaction
        
            if account.account_type == 'Asset' :
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
            elif account.account_type == 'Commitment':
                commitment += balance
                commitment_account[account] = balance
            elif account.account_type == 'Commitment_Received':
                commitment_received += balance
                commitment_received_account[account] = balance
    total_assets = int(sum(assets.values()))
    total_liabilities = int(sum(liabilities.values()))
    total_equity = int(sum(equity_account.values()))

    # if total_assets == total_liabilities+total_equity :
    #     messages.success(request,"Balance Sheet is Balanced  !!")
    # else:
    #     messages.error(request," Balance Sheet is not Balanced Please check !!")

    # total_equity = sum(liabilities.values())

    net_profit=revenue-expenses

    mydata={'assets': assets,
    'liabilities': liabilities, 
    'revenue_account':revenue_account,
    'equity_account':equity_account,
    'expenses_account':expenses_account,
    'gain_account':gain_account,
    'loss_account':loss_account,
    'commitment_account':commitment_account,
    'commitment_received_account':commitment_received_account,
    'asset':asset,
    'liabilitie':liabilitie,
    'equity': equity,
    'revenue': revenue,
    'expenses': expenses,
    'gain': gain,
    'loss': loss,
    'commitment':commitment,
    'commitment_received':commitment_received,
    'net_profit':net_profit
    }

    return render(request, 'accounts/balance_sheet.html', mydata)

from django.utils import timezone
from datetime import datetime

@login_required
@permission_required('home.view_account', login_url='/login/')


def account_statement(request):
    form = AccountStatementForm(request.GET or None)
    transactions = []
    opening_balance = 0
    total_debit = 0
    total_credit = 0
    closing_balance = 0
    running_balances = []

    if form.is_valid():
        account = form.cleaned_data['account']
        from_date = form.cleaned_data['from_date']
        to_date = form.cleaned_data['to_date']
        print(to_date)

        # Convert from_date and to_date to datetime objects at midnight
        from_datetime = datetime.combine(from_date, datetime.min.time())
        to_datetime = datetime.combine(to_date, datetime.min.time())+ timedelta(days=1)
        print(to_datetime)
        # Ensure from_datetime and to_datetime are timezone-aware
        if timezone.is_naive(from_datetime):
            from_datetime = timezone.make_aware(from_datetime)
        if timezone.is_naive(to_datetime):
            to_datetime = timezone.make_aware(to_datetime)

        # Calculate opening balance
        opening_debits = Transaction.objects.filter(
            debit_account=account, date__lt=from_datetime
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        opening_credits = Transaction.objects.filter(
            credit_account=account, date__lt=from_datetime
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        opening_balance = account.balance + opening_credits - opening_debits

        # Filter transactions within the date range
        transactions = Transaction.objects.filter(
        Q(debit_account=account) | Q(credit_account=account),
        date__gte=from_datetime,
        date__lt=to_datetime
        ).order_by('date')
        
        # transactions = Transaction.objects.filter(
        #     date__gte=from_datetime, date__lte=to_datetime
        # ).filter(
        #     debit_account=account
        # ) | Transaction.objects.filter(
        #     date__gte=from_datetime, date__lte=to_datetime, credit_account=account
        # ).order_by('date')

        # Calculate running balance
        current_balance = opening_balance
        for transaction in transactions:
            if transaction.debit_account == account:
                current_balance -= transaction.amount
            elif transaction.credit_account == account:
                current_balance += transaction.amount
            running_balances.append((transaction, current_balance))

        # Calculate total debit and credit within the date range
        total_debit = transactions.filter(debit_account=account).aggregate(Sum('amount'))['amount__sum'] or 0
        total_credit = transactions.filter(credit_account=account).aggregate(Sum('amount'))['amount__sum'] or 0

        # Calculate closing balance
        closing_balance = current_balance

    return render(request, 'accounts/account_statement.html', {
        'form': form,
        'running_balances': running_balances,
        'opening_balance': opening_balance,
        'total_debit': total_debit,
        'total_credit': total_credit,
        'closing_balance': closing_balance,
    })
