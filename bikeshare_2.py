import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': '/Users/mahmoudbadr/Desktop/Python/Project_1/bikeshare-2/chicago.csv',
              'new york city': '/Users/mahmoudbadr/Desktop/Python/Project_1/bikeshare-2/new_york_city.csv',
              'washington': '/Users/mahmoudbadr/Desktop/Python/Project_1/bikeshare-2/washington.csv' }

Months = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'all': 7}

Days = {'monday': 1, 'tuesday': 2, 'wednesday': 3, 'thursday': 4, 'friday': 5, 'saturday': 6, 'sunday': 7, 'all': 8}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city = ''
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city.lower() not in CITY_DATA.keys():
        print("\nWelcome to US bikeshare exploring program. Please choose one of the following cities: ")
        print("[Chicago, New York City, Washington]")
        city = input().lower()

        if city not in CITY_DATA.keys():
            print("\nIncorrect city. Please enter one of the following cities: ")
            print("[Chicago, New York City, Washington]")

    print("\nYou have chosen {} as your city.".format(city.title()))


    # get user input for month (all, january, february, ... , june)
    month = ''
    while month not in Months.keys():
        month = input("\nPlease enter the month name between January to June, or type 'all' to display all months: \n").lower()

        if month not in Months.keys():
            print("\nInvalid month. Please enter the month name between January to June, or type 'all' to display all months: \m")

    print(f"\nYou have selected {month.title()} as your month input.")
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("\nPlease enter the day name between Monday and Friday, or type 'all' to display all days: \n").lower()
    while True:
        if day not in Days:
            print("\nInvalid day. Please enter the day name between Monday and Friday, or type 'all' to display all days: \n")
            break
        else:
            
            print(f"\nYou have selected {day.title()} as your day input.")
            break


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
    print('\nLoading the selected data file ....')
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    # rename first unnamed column
    df.rename(columns={ df.columns[0]: "Trip ID" }, inplace = True)

    #Filter by month if applicable
    if month != 'all':
        #Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        #Filter by month to create the new dataframe
        df = df[df['month'] == month]

    #Filter by day of week if applicable
    if day != 'all':
        #Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('\nThe Most Common Month is: {}'.format(list(Months.keys())[list(Months.values()).index(common_month)]).title()) # getting the month name

    # display the most common day of week
    common_dayofweek = df['day_of_week'].mode()[0]
    print('\nThe Most Common Day of Week is: {}'.format(common_dayofweek))

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # display the most common start hour
    popular_start_hour = df['hour'].mode()[0]
    print('\nThe Most Common Start Hour is: {}'.format(popular_start_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('\nThe Most Common Start Station is: {}'.format(common_start))

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('\nThe Most Common End Station is: {}'.format(common_end))

    # display most frequent combination of start station and end station trip
    print('\nMost frequent combination of stations are from ',(df['Start Station'] + ' to ' + df['End Station']).mode()[0])    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('\nTotal time travelled: {} {}.'.format(total_travel_time,'seconds'))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nAverage travel time: {} {}'.format(mean_travel_time,'seconds'))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nCounts of user types: \n{}.'.format(user_types))


    # Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print('\nCounts of gender: \n{}.'.format(gender))


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\nEarliest year of birth: {}'.format(int(df['Birth Year'].min())))
        print('\nThe most recent year of birth: {}'.format(int(df['Birth Year'].max())))
        print('\nThe most common year of birth: {}'.format(int(df['Birth Year'].mode()[0])))
    else:
        print("\nThere is no birth year data in this file. ")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def view_data(df):
    """
    Arguments
    ---------------------
    df : Pandas filtered city bike data DataFrame.
        
    Returns
    --------------------
    None.
    """
    show_rows = 5
    row_start = 0
    row_end = show_rows - 1 
    
    print('\nWould you like to see some raw data from the dataset?\n')
    while True:
        raw_data = input('(y or n):\n').lower()
        if raw_data == 'y':
            print('\nDisplaying rows {} to {}:'.format(row_start + 1, row_end + 1))
            print('\n', df.iloc[row_start : row_end + 1])
            row_start += show_rows
            row_end += show_rows
            print('-'*200)
            print('\nWould you like to see the next {} rows?'.format(show_rows))
            continue
        elif raw_data != 'y' and raw_data != 'n':
            print('\nInvalid entry.\n')
        else:
            break
        
    print('-'*200)
    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_data(df)
        

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart == 'no':
            break


if __name__ == "__main__":
	main()
