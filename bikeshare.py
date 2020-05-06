import time
import calendar as ca
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
month_names=[""]
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    while True:
        city = input("Choose a city in following format:\nc = Chicago\nny = New York\nw = Washington\n").lower()
        if city in ("c","ny","w"):
            if city == "c":
                city = "chicago"
            elif city == "ny":
                city = "new york city"
            elif city == "w":
                city = "washington"
            print("City accepted\n")
            break
        else:
            city = "none"
            month = 0
            print("Wrong input\n")
    
    if city != "none":
        while True:    
            month = input("Choose a month in following format:\n1 = January\n2 = February\n3 = March\n4 = April\n5 = May\n6 = June\n\n'press ENTER' for no filter\n")
            if month in ("1","2","3","4","5","6",""):
                print("Input accepted\n")
                break
            else:
                month = "none"
                print("Wrong input\n")

    if month != "none":
        while True:    
            day = input("Choose a day of week in following format:\n1 = Monday\n2 = Tuesday\n3 = Wednesday\n4 = Thursday\n5 = Friday\n6 = Saturday\n7 = Sunday\n\n'press ENTER' for no filter\n")
            if day in ("1","2","3","4","5","6","7",""):
                print("Input accepted\n")
                break 
            else:
                day = "none"
                print("Wrong input\n")
   

    
    
    print('-'*40) 
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df["hour"] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    # filter by month if applicable
    if month != '':
        df = df[df['month'] == int(month)]

    # filter by day of week if applicable
    if day != '':
        df = df[df['day_of_week'] == int(day)-1]
    
    while True:
        preview = input('\nWould you like to see preview of data? (Y/N)\n')
        if preview.lower() == 'Y':
            print(df.head())
            break
        elif preview.lower() == 'N':  
            break
        else:
            print("'"+preview+"' is not correct command. Please use 'Y' or 'N' command.")
    
    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print("Most common month is: "+ca.month_name[int(df["month"].mode()[0])])

    # TO DO: display the most common day of week
    print("Most common day of week is: "+ca.day_name[int(df["day_of_week"].mode()[0])])

    # TO DO: display the most common start hour
    print("Most common start hour is: {}".format(df["hour"].mode()[0]))

    print('-'*40)
    


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    # TO DO: display most commonly used start station
    print("Most commonly used start station is: {}".format(df["Start Station"].mode()[0]))

    # TO DO: display most commonly used end station
    print("Most commonly used end station is: {}".format(df["End Station"].mode()[0]))

    # TO DO: display most frequent combination of start station and end station trip
    print("Most frequent combination of start station and end station is: "+(df["Start Station"]+" and "+df["End Station"]).mode()[0])
    
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    h = df["Trip Duration"].sum()//3600
    m = (df["Trip Duration"].sum() - h*3600)//60
    s = df["Trip Duration"].sum() - h*3600 - m*60
    print("Total travel time: "+str(h)+":"+str(m)+":"+str(s))

    # TO DO: display mean travel time
    h = df["Trip Duration"].mean()//3600
    m = (df["Trip Duration"].mean() - h*3600)//60
    s = df["Trip Duration"].mean() - h*3600 - m*60
    print("Mean travel time: "+str(int(h))+":"+str(int(m))+":"+str(int(s)))

    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    if "Gender" in df.columns:
        df["Gender"].fillna("Male",inplace=True)
    
    if "Birth Year" in df.columns:  
        df["Birth Year"].fillna(method="ffill",inplace=True) 
   
    # TO DO: Display counts of user types
    print("Counts of user types:")
    if "User Type" in df.columns:
        print(df["User Type"].value_counts())
    else:
        print("There is no information about Users in this database")
        
    # TO DO: Display counts of gender
    print("\nCounts of gender:")
    if "Gender" in df.columns:
        print(df["Gender"].value_counts())
    else:
        print("There is no information about Genders in this database")    

    # TO DO: Display earliest, most recent, and most common year of birth
    print("\nYear of birth:")
    if "Birth Year" in df.columns:
        print("earliest: "+str(df["Birth Year"].min()))
        print("most recent: "+str(df["Birth Year"].max()))
        print("most common: "+str(df["Birth Year"].mode()[0]))
    else:
        print("There is no information about Birth Years in this database")
        
    
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        while True:
            restart = input("\nWould you like to restart? Enter 'Y' or 'N'.\n")
            if restart.lower() == 'N' or restart.lower() == 'Y':
                break
            else:
                print("'"+restart+"' is not correct command. Please use 'Y' or 'N' command.")
                
        if restart.lower() == 'N':  
            break
            


if __name__ == "__main__":
	main()
