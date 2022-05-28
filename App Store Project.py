from csv import reader


def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]
    for row in dataset_slice:
        print(row)
        print('\n')  # adds a new (empty) line after each row

    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))


IOS = r'C:\Python\Data Sets\AppleStore.csv'
Android = r'C:\Python\Data Sets\Google Playstore.csv'

# Open Apple Store data and assign values to a list
ios = open(IOS, encoding='utf8')
read_ios = reader(ios)
ios_apps_data = list(read_ios)
ios_header = ios_apps_data[0]

# Open Google Playstore data and assign values to a list
android = open(Android, encoding='utf8')
read_android = reader(android)
android_apps_data = list(read_android)
android_header = android_apps_data[0]

'''print(android_header)
print('\n')
print(explore_data(android_apps_data, 0, 3, True))

print(ios_header)
print('\n')
print(explore_data(ios_apps_data, 0, 3, True))'''

# Find the number of rows and columns of the data sets
number_of_ios = 7198
number_of_android = 10841

# Determining errors in android data set
# print(android_apps_data[10473])
# print('\n')
# print(android_header)
del android_apps_data[10473]

# Looking at the instagram duplicate entry
'''for app in android_apps_data:
    name = app[0]
    if name == 'Instagram':
        print(app)'''

# Creating a list of duplicate entries for android to see how many duplicates there are
'''android_dups = []
android_unique = []
for app in android_apps_data[1:]:
    name = app[0]
    if name in android_unique:
        android_dups.append(name)
    else:
        android_unique.append(name)
print('Number of duplicates:', len(android_dups))'''

# Creating a list of duplicate entries for ios to see how many duplicates there are
'''ios_dups = []
ios_unique = []
for app in ios_apps_data[1:]:
    name = app[0]
    if name in ios_unique:
        ios_dups.append(name)
    else:
        ios_unique.append(name)
print(len(ios_dups))'''

# Removing the duplicate rows with less than the highest amount of ratings as the highest will be most recent
android_reviews_max = {}
for app in android_apps_data[1:]:
    name = app[0]
    n_reviews = float(app[3])
    if name in android_reviews_max and android_reviews_max[name] < n_reviews:
        android_reviews_max[name] = n_reviews
    elif name not in android_reviews_max:
        android_reviews_max[name] = n_reviews
print('Expected length: ', len(android_apps_data[1:]) - 1181)
print('Actual length: ', len(android_reviews_max))

# Creating a clean data set
android_clean = []
already_added = []
for app in android_apps_data[1:]:  # Iterate over our data set from the CSV file
    name = app[0]
    n_reviews = float(app[3])
    # If the number of reviews in the data set is the same as the one already in the dictionary created in the previous
    # step and the name is not a duplicate, add it to our clean data set.
    if n_reviews == android_reviews_max[name] and (name not in already_added):
        android_clean.append(app)
        already_added.append(name)

# Get rid of non-english apps in the IOS data set by creating a function that filters non-english words
print(ios_apps_data[873][1])


def english_filter(string):
    for letter in string:
        if ord(letter) > 127:
            return False

    return True


# Updated function to not lose apps with less than 3 non-english characters
def better_english_filter(string):
    non_english_character = []
    for letter in string:
        if ord(letter) > 127:
            non_english_character.append(letter)
            if len(non_english_character) > 3:
                return False
    return True


# Apply the function to filter out non-english apps from each data set and append app data to clean list
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


# Isolate the free apps from each dataset
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

#  We create a frequency distribution function that returns the percentage of apps that fit our query


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

# We create another function that sorts our table in descending order of our query


def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)

    table_sorted = sorted(table_display, reverse=True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])


# Find the average number of user ratings per genre on the app store using a nested loop

'''prime_genre_table = freq_table(ios_free_apps, 11)
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
    print(genre, ':', avg)'''

# Need to format entries in the Google Playstore data set to be floats to calculate averages
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



