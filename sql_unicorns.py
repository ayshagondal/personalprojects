%%bigquery --project your_project_id
 
 WITH top_industries AS (
 	Select i.industry,
 		COUNT(*)
 	FROM industries AS i
 	INNER JOIN dates as d
 		on i.company_id = d.company_id
 	where extract(year FROM d.date_joined) in (2019, 2020, 2021)
 	group by i.industry
 	order by COUNT(*) desc
 	limit 3
 ),
 yearly_rankings AS (
 	SELECT Count (i.*) as num_unicorns,
 		i.industry,
 		extract(year FROM d.date_joined) AS year,
 		AVG(f.valuation) as average_valuation_billions
 	From industries as i
 	Inner Join dates as d
 		on i.company_id = d.company_id
 	Inner join funding as f
 		on d.company_id = f.company_id
 	Group by i.industry, year
 )
 
 Select industry,
 	year,
 	num_unicorns,
 	Round(AVG(average_valuation_billions / 1000000000 ), 2) AS average_valuation_billions
 From yearly_rankings
 WHERE year in (2019, 2020, 2021)
 	and industry in (Select industry from top_industries)
 group by industry, num_unicorns, year
 order by year desc, num_unicorns desc;
