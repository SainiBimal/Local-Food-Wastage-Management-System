use labmen;

select * from claim;
select * from foodlist;
select * from provider;
select * from receiver;

# How many food providers and receivers are there in each city?
select City, count(distinct Provider_ID) as Provider
from provider
group by City
order by Provider desc;


# Which type of food provider contributes the most food?
select Provider_Type, sum(Quantity) as Total_Quantity
from foodlist
group by Provider_Type
order by Total_Quantity desc
limit 1;


# What is the contact information of food providers in a specific city?
select Name, contact
from Provider
where City = "Adambury";


# Which receivers have claimed the most food?
select r.Name, COUNT(c.Claim_ID) as Total_Claims
from claim c
join receiver r on c.Receiver_ID = r.Receiver_ID
group by r.Name
order by Total_Claims desc
limit 5;

select r.Name, SUM(f.Quantity) as Total_Quantity
from claim c
join foodlist f on c.Food_ID = f.Food_ID
join receiver r on c.Receiver_ID = r.Receiver_ID
group by r.Name
order by Total_Quantity desc
limit 5;


# What is the total quantity of food available from all providers?
select  sum(Quantity) as Total_Quantity
from foodlist;


# Which city has the highest number of food listings?
select p.City, count(f.Food_ID) as Food_List
from foodlist f
join provider p on f.Provider_ID = p.Provider_ID
group by p.City
order by Food_List desc
limit 1;


# What are the most commonly available food types?
select Food_Type, count(Food_Type) as No_of_Food_Type
from foodlist
group by Food_Type
order by No_of_Food_Type desc;



# How many food claims have been made for each food item?
select f.Food_Name, count(c.Claim_ID) as Claim_count
from foodlist f
join claim c on f.Food_ID = c.Food_ID
group by f.Food_Name
order by Claim_count desc;


# Which provider has had the highest number of successful food claims?
select p.Provider_ID, p.Name, count(c.Claim_ID) as Claim_count
from claim c
join foodlist f on c.Food_ID = f.Food_ID
join provider p on f.Provider_ID = p.Provider_ID
where Status = "Completed"
group by p.Provider_ID, p.Name
order by Claim_count desc
limit 1;



# What percentage of food claims are completed vs. pending vs. canceled?
select  Status, count(Claim_ID) as Total, round((count(Claim_ID) *100)/ sum(count(Status))over()  , 2) as Percentage
from claim
group by Status;


# What is the average quantity of food claimed per receiver?
select r.Name, round(avg(Quantity),2) as Average_Quantity
from claim c
join foodlist f on c.Food_ID = f.Food_ID
join receiver r on c.Receiver_ID = r.Receiver_ID
group by r.Name;


# Which meal type (breakfast, lunch, dinner, snacks) is claimed the most?
select f.Meal_Type, count(c.Claim_ID) as Claim_count
from claim c
join foodlist f on c.Food_ID = f.Food_ID
group by f.Meal_Type
order by Claim_count desc;


# What is the total quantity of food donated by each provider?
select p.Name, sum(f.Quantity) as Total_Quantity
from foodlist f
join provider p on f.Provider_ID  = p.Provider_ID
group by p.Name
order by Total_Quantity desc;


