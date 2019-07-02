import time
import pandas as pd
import numpy as np
import json

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Which city would you to see data from: Chicago, New York or Washington?\n> ").lower()
    while city not in ['chicago', 'new york', 'washington']:
        city = input("Oops! That's not a valid input. Try typing: Chicago, New York, or Washington\n> ").lower()

    # get user input for month (all, january, february, ... , june)
    month = input("Which month? All, January, February, March, April, May, or June?\n> ").lower()
    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
        month = input("Oops! That's not a valid input. Try typing full month name\n> ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Which day? All, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday or Saturday?\n> ").lower()
    while day not in ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']:
        day = input("Oops! That's not a valid input. Try typing: Sunday, Monday, and so on or 'all' for whole week.\n> ").lower()

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    df['month'] = df['Start Time'].dt.month
    month = df['month'].mode()[0]
    common_month = months[month-1]
    print('\nMost Common Month:', common_month)

    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    common_day_of_week = df['day_of_week'].mode()[0]
    print('\nMost Common Day of Week:', common_day_of_week)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('\nMost Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print("\nThe most commonly used start station: {}".format(most_common_start_station))

    # display most commonly used end station
    most_common_stop_station = df['End Station'].mode()[0]
    print("\nThe most commonly used stop station: {}".format(most_common_stop_station))

    # display most frequent combination of start station and end station trip
    most_frequent_start_end_station = df[['Start Station', 'End Station']].mode().loc[0]
    print("\nThe most frequent combination of start and end station trip: {}".format(most_frequent_start_end_station[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("\nThe total trip duration is: {}".format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("\nThe mean trip duration is: {}".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("\nCounts of User Types:\n{}".format(user_types))

    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print("\nCounts of Gender:\n{}".format(gender))
    except:
        print("\nNo gender data available.")

    # Display earliest, most recent, and most common year of birth
    try:
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()[0]
        print("""\nThe oldest user was born in: {}\nThe most recent user was born in: {}\nThe most common year of birth is: {}""".format(int(earliest),int(most_recent),int(most_common)))
    except:
        print("\nNo birth data available.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays raw bikeshare data."""
    rows = df.shape[0]

    for i in range(0, rows):
        user_input = input("\nWould you like to view raw user trip data? Type 'yes' or 'no'\n> ").lower()
        if user_input != 'yes':
            break
        
        # retrieve and convert data to json format
        rows_data = df.iloc[i: i + 5].to_json(orient='records', lines=True).split('\n')
        for row in rows_data:
            json_load = json.loads(row)
            json_dumps = json.dumps(json_load, indent=4)
            print(json_dumps)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n> ')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
