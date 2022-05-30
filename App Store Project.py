# For this project, we are acting as a Data Analyst for a company who is considering launching an app on the Google
# Playstore and the Apple App Store. We are tasked with extracting meaningful information from the apps on each store in
# order to determine what makes an app productive. I've linked the data sets utilized below in the "details" section on
# my project portfolio website.

# First things first, we import the reader function from the csv library to read our data sets.
from csv import reader

# We also define a reusable function that returns meaningful information about each data set automatically.


def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]
    for row in dataset_slice:
        print(row)
        print('\n')  # adds a new (empty) line after each row.

    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))


# These are the file paths for the data sets undergoing analysis.
IOS = r'C:\Python\Data Sets\AppleStore.csv'
Android = r'C:\Python\Data Sets\Google Playstore.csv'

# We now open the Apple App Store data set and assign the value to a list.
ios = open(IOS, encoding='utf8')
read_ios = reader(ios)
ios_apps_data = list(read_ios)
ios_header = ios_apps_data[0]

# We now open the Google Playstore and assign the values to a list as well.
android = open(Android, encoding='utf8')
read_android = reader(android)
android_apps_data = list(read_android)
android_header = android_apps_data[0]

# Using the function we created earlier, we can examine the header row as well as the first two apps to get an idea of
# how the data is set up.
print(explore_data(android_apps_data, 0, 3, True))

# Similarly, let us examine the App Store data set to see how this data has been lain out.
print(explore_data(ios_apps_data, 0, 3, True))

# Using the function from earlier, we know how many apps there are in each store. Subtract 1 to account for the header.
number_of_ios = 7197
number_of_android = 10841

# Obviously, no data set is clean upon first analysis. For example, based upon a discussion post of this data set, the
# following row has an error. When compared with a correct row, we see there is a problem in the "Reviews" and "Android
# Versions" of the data set.
print(android_apps_data[10473])
print('\n')
print(android_header)

# We remove this app from our data set in order to proceed with more quantitative analysis.
del android_apps_data[10473]

# We also should be cognizant of duplicate entries. For example, based upon another discussion post, let's see how many
# duplicate entries there are for Instagram.
for app in android_apps_data:
    name = app[0]
    if name == 'Instagram':
        print(app)

# We see that there are a total of 4 entries for Instagram, which can influence our future analysis.
# Creating a list of duplicate entries for android to see how many duplicates there are
android_dups = []
android_unique = []
for app in android_apps_data[1:]:
    name = app[0]
    if name in android_unique:
        android_dups.append(name)
    else:
        android_unique.append(name)
print('Number of duplicates:', len(android_dups))  # We see there are 1181 duplicate entries on the Google Playstore.

# We perform the same process on the App Store to check for any duplicate entries.
ios_dups = []
ios_unique = []
for app in ios_apps_data[1:]:
    name = app[0]
    if name in ios_unique:
        ios_dups.append(name)
    else:
        ios_unique.append(name)
print('Number of duplicates:', len(ios_dups))  # To our pleasant surprise, there are 0 duplicate apps on the App Store.

# Next, in order to be consistent with our analysis, we only wish to keep the apps that have the highest number of
# reviews. The logic behind this is that the entries with a low review number will tend to be more inaccurate.
android_reviews_max = {}  # Initialize a dictionary to hold each UNIQUE app name with the number of reviews.
for app in android_apps_data[1:]:
    name = app[0]
    n_reviews = float(app[3])
    if name in android_reviews_max and android_reviews_max[name] < n_reviews:
        android_reviews_max[name] = n_reviews
    elif name not in android_reviews_max:
        android_reviews_max[name] = n_reviews

# We found earlier that there were 1181 duplicates. We expect our current data set to hold 1181 less the original.
print('Expected length: ', len(android_apps_data[1:]) - 1181)
print('Actual length: ', len(android_reviews_max))

# Now, let's begin to create a clean data set. We start by initializing two separate lists.
android_clean = []  # This list will be the new source for our analysis.
already_added = []  # This list will hold the apps already added to the clean list, i.e. the duplicates.
for app in android_apps_data[1:]:  # Iterate over our data set from the CSV file.
    name = app[0]  # The name of the app.
    n_reviews = float(app[3])  # The number of reviews.
    # If the number of reviews in the data set is the same as the one already in the dictionary created in the previous
    # step and the name is not a duplicate, add it to our clean data set.
    if n_reviews == android_reviews_max[name] and (name not in already_added):
        android_clean.append(app)
        already_added.append(name)

# Let's utilize the function from the earlier on our new data set to confirm that we have 9659 apps (rows).
explore_data(android_clean, 0, 3, True)  # Spoiler, we get what we expect!

# Another issue that we will run into is that a few of the apps from either data set have non-English apps. For example,
# the following apps is in Mandarin...at least that is what I assume. We need a way to remove apps like these.
print(ios_apps_data[814][1])

# We can remove non-English speaking apps by using the fact that all English words are encoded inside of ASCII with
# values between 0 and 127. If a character has an order greater than that, we know it is not English, and can remove it.


def english_filter(string):
    for letter in string:
        if ord(letter) > 127:
            return False

    return True


# However, we need to create another function that also takes into account the fact that some app names include emojiis.
def better_english_filter(string):
    non_english_character = []
    for letter in string:
        if ord(letter) > 127:
            non_english_character.append(letter)
            if len(non_english_character) > 3:
                return False
    return True


# We know apply our updated function to each application in each app store (Google and Apple).
updated_android_clean = []
updated_ios_clean = []
for row in android_clean:
    name = row[0]
    if better_english_filter(name) == True:
        updated_android_clean.append(row)

for row in ios_apps_data[1:]:
    name = row[0]
    if better_english_filter(name) == True:
        updated_ios_clean.append(row)


# Now we are ready to begin our analysis. Let's begin by analyzing characteristics of Free apps. We do so by creating
# two lists to append each free app from either store.
android_free_apps = []
ios_free_apps = []
for row in updated_android_clean:
    price = row[7]
    if price == '0':
        android_free_apps.append(row)

for row in updated_ios_clean:
    price = row[4]
    if price == '0':
        ios_free_apps.append(row)

# One of the simplest ways to analyze data is via a frequency distribution. Luckily, we can create a reusable function
# that generates a frequency table for any data set we place inside the argument.


def freq_table(data_set, index):
    table = {}
    for column in data_set:
        category = column[index]
        if category in table:
            table[category] += 1
        else:
            table[category] = 1
    proportion_table = {}
    for key in table:
        percentage = (table[key]/len(data_set)) * 100
        proportion_table[key] = percentage
    return proportion_table

# We create another function that sorts our table in descending order of our query.


def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)

    table_sorted = sorted(table_display, reverse=True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])


# Now it's time to test out our functions to by having them help us answer questions. Specifically, which free
# application genres appear to be the most popular on the app store?
display_table(ios_free_apps, -5)  # It appears that Games make up the vast majority of Free apps on Apple's app store.

# What if we want to see which categories users think is the most popular? We can do that by taking the average of the
# number of downloads for each app category.
prime_genre_table = freq_table(ios_free_apps, 11)
for genre in prime_genre_table:
    total = 0
    len_genre = 0
    for app in ios_free_apps:
        genre_app = app[11]
        if genre_app == genre:
            user_ratings = float(app[5])
            total += user_ratings
            len_genre += 1
    avg = total/len_genre
    print(genre, ':', avg)

# It would appear that Navigation apps have the highest number of applications.

# We have to take a slightly different approach with the Playstore. Let's look at a distribution for the installation
# column.
display_table(android_free_apps, 5)  # Install column. Notice that the numbers are not precise NOR are they floats.

# Before we can perform a similar analysis on the Google Playstore, we need to convert the data type of installs to a
# float. Then we can perform a similar analysis.
category_table = freq_table(android_free_apps, 1)
for category in category_table:
    total = 0
    len_category = 0
    for app in android_free_apps:
        category_app = app[1]
        if category_app == category:
            installs = app[5]
            installs = installs.replace('+', '')
            installs = installs.replace(',', '')
            installs = float(installs)
            total += installs
            len_category += 1
    avg_category = total/len_category
    print(category, ':', avg_category)

# Communication apps appear to be the genre that users think is most popular by installation downloads.
