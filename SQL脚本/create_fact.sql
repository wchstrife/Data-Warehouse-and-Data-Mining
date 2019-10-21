create view fact_disp as 
select dbo.account.account_id,dbo.client.client_id,dbo.card.card_id,dbo.disp.type
from dbo.account,dbo.client,dbo.card,dbo.disp
where dbo.account.account_id=dbo.disp.account_id and dbo.client.client_id=dbo.disp.client_id and dbo.card.disp_id=dbo.disp.disp_id

create view fact_loan as 
select dbo.loan.loan_id,dbo.loan.account_id,dbo.client.client_id,dbo.loan.[date], dbo.loan.duration,dbo.loan.amount,dbo.loan.payduration,dbo.loan.payments,dbo.loan.[status]
from dbo.account,dbo.loan,dbo.disp,dbo.client
where dbo.loan.account_id=dbo.account.account_id and dbo.account.account_id=dbo.disp.account_id and dbo.client.client_id=dbo.disp.client_id

create view fact_tran as
select 
dbo.[tran].trans_id, dbo.account.account_id,
dbo.client.client_id,dbo.[tran].[date],
dbo.[tran].[type],dbo.tran_operation.operation_id,dbo.[tran].amount,
dbo.[tran].balance,dbo.[tran].k_symbol,dbo.[tran].bank
from dbo.account,dbo.disp,dbo.client,dbo.[tran],dbo.tran_operation
where dbo.account.account_id=dbo.disp.account_id and dbo.client.client_id=dbo.disp.client_id 
and dbo.[tran].account_id=dbo.account.account_id and dbo.tran_operation.operation_name=dbo.[tran].operation