create view dimension_account as 
select dbo.account.account_id,Year(dbo.account.date) as create_year,dbo.account.district_id,dbo.account.frequency
from dbo.account

create view dimemsion_card as 
select dbo.card.card_id,dbo.card.disp_id,dbo.card_type.type_id,dbo.card.issued
from dbo.card,dbo.card_type
where dbo.card.type=dbo.card_type.type_name

create view dimemsion_client as 
select dbo.client.client_id,dbo.client.district_id,dbo.client_gender.gender_id,
cast((2000-YEAR(dbo.client.birth_day))/10 *10 as varchar(50))+'-'+cast((2000-YEAR(dbo.client.birth_day))/10*10+10 as varchar(50)) as age
from dbo.client, dbo.client_gender
where dbo.client.gender=dbo.client_gender.gender_name