import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
cities =['chicago','new york city','washington']
months=['january','february','march','april','may','june','all']
days=['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']
possible_answers = ['y','yes','n','no']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('Cities are Chicago, new york city , washington, so... \n')
    while True:
        city = input("Select a city from {}, {} or {}:".format(*CITY_DATA.keys())).strip().lower()
        if city in CITY_DATA.keys():
            break
    # get user input for month (all, january, february, ... , june)
    print('months are january, february, march, april, may, june, so...\n')
    while True :
        month = str(input('Select a month from {}, {}, {}, {}, {}, {}, {} \n'.format(*months))).lower().strip()
        if month in months :
            break
    # get user input for day of week (all, monday, tuesday, ... sunday)
    print ('days are monday, tuesday, wednesday, thursday, friday, saturday, sunday, so...\n')
    while True:
        day = str(input('Select a day from {}, {}, {}, {}, {}, {}, {}, {}\n'.format(*days))).lower().strip()
        if day in days :
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
    df = pd.read_csv(CITY_DATA[city])
    df = df.dropna(axis = 0)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    if month != 'all' :
        month = int(months.index(month))+1
    if day != 'all' :
        day= day.title()
    if (month != 'all') & (day != 'all') :
        df= df.loc[(df['month'] == month) & (df['day_of_week'] == day)]
    elif month != 'all' :
        df= df.loc[df['month'] == month]
    elif day != 'all' :
        df= df.loc[df['day_of_week'] == day]
    return df

def data_printing(df):
    """ displys a sample of the raw data """
    while True:
        answer=input('do you want to show a sample 5 rows of the data ? y/n \n ').lower().strip()
        if answer in possible_answers :
            break
    if answer in ['y', 'yes'] :
        start = 0
        end = 5
        repeat = 'yes'
        while repeat in ['y', 'yes'] :
            print(df.iloc[start:end])
            start += 5
            end += 5
            while True :
                repeat = input('do you wnat to view the nest 5 rows ? y/n \n').lower().strip()
                if repeat in possible_answers :
                    break
    print('-'*40)


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = months[df['month'].mode()[0]-1]
    print('most common month is {}\n'.format(popular_month))

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('most common day of week is {}\n'.format(popular_day))
    # display the most common start hour
    df['hour']= df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('most common start hour is {}\n'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start= df['Start Station'].mode()[0]
    print('the most common used start station is {}\n'.format(popular_start))
    # display most commonly used end station
    popular_end= df['End Station'].mode()[0]
    print('the most common end station is {}\n'.format(popular_end))
    # display most frequent combination of start station and end station trip
    print ('so we can say that the most popular trip is from {} to {}\n'.format(popular_start, popular_end))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = (df['End Time']-df['Start Time']).sum()
    print('total travel time is {}\n'.format(total_time))
    # display mean travel time
    mean_time = (df['End Time']-df['Start Time']).mean()
    print('mean travel tyme is {}\n'.format(mean_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    users= df['User Type'].value_counts()
    print('User Types and their numbers are \n',users)
    # Display counts of gender
    if 'Gender' in df :
        genders= df['Gender'].value_counts()
        print('\nGenders and their numbers are \n',genders)
    else :
        print ("Sorry, But the data doesn't contatin information about the gender of the users. \n" )
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df :
        smallest = df['Birth Year'].max()
        oldest = df['Birth Year'].min()
        most_common = df['Birth Year'].mode()[0]
        print('the earliest year is {} and the most recent year is {} and the most common year of birth is {}\n'.format(oldest,smallest,most_common))
    else :
        print("Sorry, But the data doesn't contatin information about the birth year of the users. \n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        data_printing(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
