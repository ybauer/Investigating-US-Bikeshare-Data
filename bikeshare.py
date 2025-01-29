import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#created a list for month and days as user input options

MONTH_OPTIONS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

DAY_OPTIONS = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # used string to have user input the city of their interest
    # used while loop to exclude cities that aren't present in the current dataset or to have user reevaluate their input
    # used lower() function to make inputs case caseinsensitive
    city = input("Hey there! Please enter the city of your interest, please note that there is only data for Washington, New York City and Chicago available at this point. Please enter now: ")
    # city == "chicagO"
    # city.lower() == "chicago"
    while city.lower() not in CITY_DATA:
        print("Please check your input, it may not been in our portfolio yet")
        city = str(input("Hey there! Please enter your city: "))

    print(f"\nThank you for entering. You have chosen {city.title()} as your city")

    # created a list of months
    # used while loop to exclude months that aren't present in the current dataset or to have user reevaluate their input
    # used lower() function to make inputs case caseinsensitive

    month = str(input("Please enter the month between January and June you are seeking data for: "))

    while month.lower() not in MONTH_OPTIONS:
        print("Invalid input. Please select a month between January and June.")
        month = str(input("Please enter the month between January and June or select all: "))

    print(f"\nThank you for entering, you have chosen {month.title()} as your month")

    # used string to have user input the day of their interest
    # used while loop to have user reevaluate their input in case of typos
    # used lower() function to make inputs case caseinsensitive

    day = str(input("Please enter the specific day of your choice or if you want to get all days enter all: "))

    while day.lower() not in DAY_OPTIONS:
        print("Please check your input again. This format may not been accepted")
        day = str(input("Please enter the specific day of your choice or if you want to get all days enter all: "))

    print(f"\nThank you for entering, you have chosen {day.title()} as your day")

    print('-'*40)
    # added .lower() here as well to make sure that what's returned is always lower case
    return city.lower(), month.lower(), day.lower()


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
    print("\nLoading data...")

    # loaded CSV file into Pandas
    df = pd.read_csv(CITY_DATA[city])

    # used pd to datetime to convert the string representation of a date to an actual date format
    df['start_time'] = pd.to_datetime(df['Start Time'])

    # extracted month, day of week, and hour from Start Time as new columns
    df['month'] = df['start_time'].dt.month
    df['weekday'] = df['start_time'].dt.day_name
    df['hour'] = df['start_time'].dt.hour

    # Debug: Display unique months and weekdays in the data
    print(f"Unique months in data: {df['month'].unique()}")
    print(f"Unique weekdays in data: {df['weekday'].unique()}")

    # filter by month if applicable
    if month != 'all':
        # use the index of the month names list to get the corresponding int
        # since python lists are 0 indexed we need to add always +1 to get the actual month number
        month_number = MONTH_OPTIONS.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month_number]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        # added .title() since the weekday is capitalized
        df = df[df['weekday'] == day.title()]

    print(f"Data remaining after filtering: {df.shape[0]} rows.")
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    # used mode function to show the most common month
    # the mode can be multiple values, therefore I treat as a list
    most_common_months = list(df['month'].mode())
    print(f"\nThe most common month number(s): {most_common_months}")

    # used mode function to show the most common weekday
    most_common_days = list(df['weekday'].mode())
    print(f"\nThe most common day(s): {most_common_days}")

    # used mode function to show the most common start hour
    most_common_hours = list(df['hour'].mode())
    print(f"\nThe most common hour(s): {most_common_hours}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # used mode function to show the most common start station
    common_start_station = list(df['Start Station'].mode())
    print(f"\nThe most common start station is: {common_start_station}")


    # used mode function to show the most common end station
    common_end_station = list(df['End Station'].mode())
    print(f"\nThe most common end station is: {common_end_station}")

    # used groupby function to combine start station with end station and show
    # the most frequent combination of stations for start and ending a trip
    # used .size to receive a number of how often this combination got used
    # used n.largest(1) as a method to receive the first highest value combination
    freq_stat_comb = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print(f"\nThe most frequent combination of start station and end station trip is: {freq_stat_comb}")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # used sum function to get the total travel time
    total_travel_time = df['Trip Duration'].sum()
    # to get days, hour, minutes and seconds from total_travel_time, I used the timedelta function
    total_travel_time = df['Trip Duration'].sum()
    import datetime
    total_travel_time_rev = datetime.timedelta(seconds = int(total_travel_time))
    print(f"\nTotal travel time is: {total_travel_time_rev}")


    # used mean function to picture the average travel time
    average_travel_time = df['Trip Duration'].mean()
    if pd.notna(average_travel_time):
        average_travel_time_rev = datetime.timedelta(seconds=int(average_travel_time))
    else:
        average_travel_time_rev = datetime.timedelta(seconds=0)

    # to get days, hour, minutes and seconds from average_travel_time, I used the timedelta function
    average_travel_time_rev = datetime.timedelta(seconds = int(average_travel_time))
    print(f"Average travel time is: {average_travel_time_rev}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # used value_counts function to display number of the user_types
    user_types = df['User Type'].value_counts()
    print(f"\nThe number of user types is: {user_types}")

    # used value_counts function to display number of males and females
    # gender column is only included for new york city and chicago, therefor I used if/else function to account for washington which doesn't include a gender column

    if 'Gender' in df.columns:
        user_gender = df['Gender'].value_counts()
        print(f"\nHere are the gender counts: {user_gender}")
    else:
        print("There is no Gender column for this city")


    # DOB column is only included for new york city and chicago, therefor I used if/else function to account for washington which doesn't include a DOB column
    if 'Birth Year' in df.columns:
        #used min function to display earliest birth year
        earliest_dob = int(df['Birth Year'].min())
        #used max function to display most recent birth year
        most_recent_dob = int(df['Birth Year'].max())
        #used mode function to display most common Birth Year
        most_common_dob = int(df['Birth Year'].mode()[0])
        print(f"\nThe earliest date of birth is: {earliest_dob}, the most recent date of birth is: {most_recent_dob} and the most common date of birth is: {most_common_dob}")

    else:
        print("There is no Birth Year column for this city")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# created new dataframe for showing data to the user
def print_raw_data(df):
    """ Asks user to display 5 data rows at a time."""
    # the shape method returns two numbers, so I picked the first one which reflects always the rows of a dataframe.
    number_of_rows = df.shape[0]

    print(f"\nThe provided dataframe has {number_of_rows} rows")
    user_input_raw_data = str(input("Would you like to view 5 rows of individual data at a time? yes/no: "))
    index = 0

    # used while loop with two end condition.First the user needs to answer yes in order to show raw data. Second, we need to limit         the loop to the number
    # rows of the dataframe the user provided as input to this function, therefore we need to check if the index is smaller or equal         to it.
    while ((user_input_raw_data.lower() == 'yes') and (index < number_of_rows)):

        print(f"\nHere are rows {index} to {index + 5}")
        # defined the index so the program returns always the next 5 rows If user condition is 'yes'
        print(df[index:(index + 5)])
        user_input_raw_data = str(input(f"\nWould you like to see the next rows? yes/no: "))
        index += 5

        print("Now we continue to show some key statitics on the bikeshare data")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        print_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
