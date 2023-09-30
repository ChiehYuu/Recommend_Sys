CREATE TABLE IF NOT EXISTS POS.COMBINED (
	select 
		case when tStock_In.shop is NULL then tSale_qty.shop else tStock_In.shop end as shop, 
		case when tStock_In.prod is NULL then tSale_qty.prod else tStock_In.prod end as prod, 
		pos110.pname, pos110.pluno, pos116.lprc,
		case when tStock_In.stock_qty is NULL then 0 else tStock_In.stock_qty end as pre_stock_qty,
		case when tStock_In.in_qty is NULL then 0 else tStock_In.in_qty end as in_qty,
		case when tSale_qty.sale_qty is NULL then 0 else tSale_qty.sale_qty end as sale_qty,
		case 
		when tSale_qty.sale_qty is NULL then (tStock_In.stock_qty + tStock_In.in_qty) 
		when tStock_In.stock_qty is NULL and tStock_In.in_qty is NULL then -tSale_qty.sale_qty
		else (tStock_In.stock_qty + tStock_In.in_qty - tSale_qty.sale_qty) end as new_stock_qty
	from
	(	select 
			case when tStock_qty.shop is NULL then tInqty.shop else tStock_qty.shop end as shop, 
			case when tStock_qty.prod is NULL then tInqty.prod else tStock_qty.prod end as prod, 
			case when tStock_qty.stock_qty is NULL then 0 else tStock_qty.stock_qty end as stock_qty, 
			case when tInqty.in_qty is NULL then 0 else tInqty.in_qty end as in_qty
		from (
			select product_stock.shop, product_stock.prod, product_stock.stock_qty 
			from product_stock where supp = '{$supp}' and grade_date = '{$grade_date}' 
		) as tStock_qty
		full outer join
		(	select pos204.shop, pos116.prod, cast(sum(pos204.inqty) as integer) as in_qty
			from pos116 
			inner join pos204 
			on pos116.prod = pos204.prod and pos204.indate >= '{$sdate}' and pos204.indate <= '{$edate}' and pos204.gctrl = '4'
			where pos116.supp = '{$supp}' and pos116.ano = '{$ano}'
			group by pos204.shop, pos116.prod 
		) as tInqty
		on tStock_qty.shop = tInqty.shop and tStock_qty.prod = tInqty.prod 
	) as tStock_In
	full outer join 
	(	select pos324.shop, pos324.prod, sum(pos324.qty) as sale_qty
		from pos324
		inner join pos116 
		on pos324.prod = pos116.prod and pos116.ano = '{$ano}' and pos116.supp = '{$supp}'
		where pos324.ecrdate >= '{$sdate}' and pos324.ecrdate <= '{$edate}'
		group by pos324.shop, pos324.prod 
	) as tSale_qty
	on tStock_In.shop = tSale_qty.shop and tStock_In.prod = tSale_qty.prod
	inner join (pos110 
		inner join pos116 
		on pos110.prod = pos116.prod and pos116.ano = '{$ano}' and pos116.supp = '{$supp}') 
	on tStock_In.prod = pos116.prod or tSale_qty.prod = pos116.prod
	order by tStock_In.shop, tStock_In.prod
);