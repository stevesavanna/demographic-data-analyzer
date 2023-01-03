import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df["race"].value_counts()

    # What is the average age of men?
    average_age_men = df[df["sex"] == 'Male']["age"].mean().round(1)

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = round(len(df[df["education"] == "Bachelors"]) / len(df) * 100, 1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = df["education"].isin(["Bachelors", "Masters", "Doctorate"])
    lower_education = ~higher_education

    rich = df["salary"] == ">50K"

    # percentage with salary >50K
    higher_education_rich = round(len(df[higher_education & rich]) / len(df[higher_education]) * 100, 1)
    lower_education_rich = round(len(df[lower_education & rich]) / len(df[lower_education]) * 100, 1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df["hours-per-week"].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers = df["hours-per-week"] == min_work_hours

    rich_percentage = round(len(df[num_min_workers & rich]) / len(df[num_min_workers]) * 100, 1)

    # What country has the highest percentage of people that earn >50K?
    countries_by_earnings = df[rich].groupby("native-country", as_index=False).size()
    countries_by_earnings.rename(columns={"size": "rich-count"}, inplace=True)
    countries_by_earnings["count"] = countries_by_earnings["native-country"].apply(lambda x: len(df[df["native-country"] == x]))
    countries_by_earnings["percentage"] = round(countries_by_earnings["rich-count"] / countries_by_earnings["count"] * 100, 1)

    highest_earning_country = countries_by_earnings.nlargest(1, "percentage").iloc[0]["native-country"]
    highest_earning_country_percentage = countries_by_earnings.nlargest(1, "percentage").iloc[0]["percentage"]

    # Identify the most popular occupation for those who earn >50K in India.
    occupations = df[rich & (df["native-country"] == "India")].groupby("occupation", as_index=False).size()
    occupations.rename(columns={"size": "count"}, inplace=True)
    top_IN_occupation = occupations.nlargest(1, "count").iloc[0]["occupation"]

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count)
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
