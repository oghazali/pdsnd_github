import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
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
    while True:
        city = input("Please enter a city (Chicago, New York City, Washington): ").strip().lower()
        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            print("Invalid input. Please enter one of the provided cities.")

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Please enter a month (January, February, March, etc.) or 'all': ").strip().lower()
        if month in ['january','february','march','april','may','june','july','august','september','october','november','december','all']:
            break
        else:
            print("Invalid input. Please enter a full month name (ex. January).")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Please enter a day of the week (Monday, Tuesday, etc.) or 'all': ").strip().lower()
        if day in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']:
            break
        else:
            print("Invalid input. Please enter a day of the week.")

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
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    df['start-end'] = df['Start Station'] + " - " + df['End Station'] 

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june','july','august','september','october','november','december']
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

    # display the most common month
    common_month = df['month'].mode()[0]
    print('Most common month: ', common_month)

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most common day: ', common_day)

    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('Most common hour: ', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return df

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('Most common start: ', common_start)

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('Most common end: ', common_end)
    
    # display most frequent combination of start station and end station trip
    common_combination = df['start-end'].mode()[0]
    print('Most common combination: ', common_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return df


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print('Total travel time (seconds): ', total_time)

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('Average travel time (seconds): ', mean_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return df


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types (dataframe to simplify print)
    user_types = pd.DataFrame(df['User Type'].value_counts())
    print('Types of users: \n', user_types)

    # Display counts of gender (dataframe to simplify print)
    if 'Gender' in df.columns:
        genders = pd.DataFrame(df['Gender'].value_counts())
        print('\nGender count: \n', genders)
    else:
        print('Gender statistics cannot be calculated because Gender does not appear in the dataframe')
        
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_by = int(df['Birth Year'].min())
        most_recent_by = int(df['Birth Year'].max())
        common_by = int(df['Birth Year'].mode()[0])
        print('\nEarliest birth year: ', earliest_by)
        print('Most recent birth year: ', most_recent_by)
        print('Common birth year: ', common_by)
    else:
        print('Birth year statistics cannot be calculated because birth year does not appear in the dataframe')
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return df

def show_data(df):
    """Displays 5 rows of data at a time based on user input"""
    # starting index
    index = 0
    while True:
        
        # if new index is greater than size of filtered data
        if index >= len(df):
            print("End of the data reached. Exiting raw data...")
            break
    
        show_data = input("Do you want to see 5 lines of raw data? Enter yes or no.\n")
        
        if show_data == 'yes':
            # Display next 5 lines of raw data
            print(df.iloc[index:index+5])
            index += 5  # Update index for next iteration
        elif show_data == 'no':
            print("Exiting raw data...")
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")
    
    print('-'*40)
    return df

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("Closing program...")
            break

if __name__ == "__main__":
	main()
