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
    city = input("\nWhich city would you like to view data for?\n\n\
You can choose one of Chicago, New York City or Washington. \
\nPlease enter the name with no capital letters: ")
    while city not in ['chicago', 'new york city', 'washington']:
        city = input("\nOops, there was a problem with your input! Please re-enter the city name\
but make sure to choose from the options provided above and do not use capital letters: ")
    # get user input for month (all, january, february, ... , june)
    month = input("\nWhich Month would you like to view data for? \
    \n\nYou can choose any month from January to June, \
or all available months!\nPlease enter the name with no capital letters, \
or enter all if you wish to view data for all available months: ")
    while month not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
        month = input("\nOops, there was a problem with your input! Please re-enter the Month name\
, but make sure to choose from the options provided above and do not use capital letters: ")
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("\nWhich day of the week would you like to view data for?\n\n\
You can choose any day from Monday to Sunday, or all available days!\
\nPlease enter the name with no capital letters, or enter all if you wish to view data for all days: ")
    while day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
        day = input("\nPlease re-enter the day of the week, make sure to choose from the list provided above \
and do not use capital letters: ")

    print('\n\nYou have requested data for ***{}***, the month you have selected is ***{}*** and \n\
the day(s) of the week you have selected is ***{}***\n'.format(city.title(), month.title(), day.title()))

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

    # load data file into a dataframe named 'df'
    df = pd.read_csv(CITY_DATA.get(city))

    df['date'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['date'].dt.month
    df['day_of_week'] = df['date'].dt.dayofweek

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        day_dict = {'monday': 0,
                    'tuesday': 1,
                    'wednesday': 2,
                    'thursday': 3,
                    'friday': 4,
                    'saturday': 5,
                    'sunday': 6}
        day = day_dict[day]
        df = df[df['day_of_week'] == day]

    return df



def time_stats(df):

    print('\nCalculating The Most Frequent Times of Travel...\n')

    start_time = time.time()

    # display the most common month in the terminal
    month_name = ['January', 'February', 'March', 'April', 'May', 'June'][df['month'].mode()[0]-1]

    print('The most common month was {}.\n'.format(month_name))

    # display the most common day of week in the terminal
    day_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][df['day_of_week'].mode()[0]-1]
    print('The most common day of the week was {}.\n'.format(day_name))

    # display the most common start hour in the terminal

    df['hour'] = df['date'].dt.hour
    print('The most common starting hour was {}.\n'.format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station in the terminal

    print('The most common station to start a journey was {}.\n'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station in the terminal

    print('The most common station to end a journey was {}.\n'.format(df['End Station'].mode()[0]))

    # Add a new column to data frame 'df' with the start and end station for each journey

    df['Full Journey'] = df['Start Station'] + ' to ' + df['End Station']

    # display most frequent combination of start station and end station trip in the terminal

    print('The most common journey combination was {}.\n'.format(df['Full Journey'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """"Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time in the terminal

    print('The total travel time was {} days\n'.format(df['Trip Duration'].sum()/(24*60**2)))

    # display mean travel time in the terminal

    print('The average travel time was {} minutes\n'.format(df['Trip Duration'].mean()/60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """"Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    if city == 'washington':

        subscribers = df['User Type'].value_counts()['Subscriber']
        customers = df['User Type'].value_counts()['Customer']
        print('There were {} subscribers and {} customers.\n'.format(subscribers, customers))

        print('Unfortunately, there is no information held for Washington on the type or gender of users of the bike share stations.\n\
If you are interested, this information is held for Chicago and New York City.')

    else:
        # Display counts of user types in the terminal
        subscribers = df['User Type'].value_counts()['Subscriber']
        customers = df['User Type'].value_counts()['Customer']
        print('There were {} subscribers and {} customers.\n'.format(subscribers, customers))

        # Display counts of gender in the terminal

        males = df['Gender'].value_counts()['Male']
        females = df['Gender'].value_counts()['Female']
        print('There were {} males and {} females.\n'.format(males, females))


        # Display earliest, most recent, and most common year of birth in the terminal
        max_year = int(df['Birth Year'].max())
        min_year = int(df['Birth Year'].min())
        mode_year = int(df['Birth Year'].mode(dropna=True)[0])
        print('The most recent year of birth for bike share users was {}, the least recent year of birth was {} \
and the most common year of birth was {}.\n'.format(max_year, min_year, mode_year))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()

        test = input('If you would like to choose again, please type Y.\n\
If you are happy with your selection, please type anything else:  \n')
        if test.lower() == 'y':
            city, month, day = get_filters()

        df = load_data(city, month, day)

        raw_data_query = input('Would you like to view raw trip data for the filter selected?\n\
Please type Y if you do, type anything else if you do not:')

        n=0

        while raw_data_query.lower() == 'y':
            n+=5
            print(df.head(n))
            raw_data_query = input('Would you like to view more raw trip data?\n \
Please type Y if you do, type anything else if you do not: ')

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter Y if you do or enter anything else if you do not: \n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
