import csv
from faker import Faker
import pandas as pd
from sklearn.neighbors import NearestNeighbors

fake = Faker()
user_data = []

for _ in range(10000):
    user_id = str(fake.random_int(0, 999))
    yt_id = str(fake.random_int(0, 999))
    views = str(fake.random_int(1, 20))
    category = fake.random_element(elements=('Technology', 'Sports', 'Food', 'Fashion', 'Travel'))

    user_data.append([user_id, yt_id, views, category])

with open('users_history.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['user_id', 'yt_id', 'views', 'category'])
    writer.writerows(user_data)


ad_data = []
for i in range(100):
    ad_id = i+1
    category = fake.random_element(elements=('Technology', 'Sports', 'Food', 'Fashion', 'Travel'))

    ad_data.append([ad_id, category])

with open('ad_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['ad_id', 'category'])
    writer.writerows(ad_data)


user_data = pd.read_csv('users_history.csv')
ad_data = pd.read_csv('ad_data.csv')

merged_data = pd.merge(user_data, ad_data, on='category')

X = merged_data[['user_id', 'yt_id', 'ad_id']].values

knn = NearestNeighbors(n_neighbors=5, metric='cosine')
knn.fit(X)

target_user = int(input("Enter user id:"))
for d in X:
    if d[0] == target_user:
        target_user = d.reshape(1, -1)
        break
distances, indices = knn.kneighbors(target_user)

recommended_ads = merged_data.iloc[indices[0]]['ad_id'].values
recommended_category = merged_data.iloc[indices[0]]['category'].values
print(f'Recommended Ads: {recommended_ads}')
print(f'Recommended Category: {recommended_category}')

user_watch_history = user_data[user_data['user_id'] == target_user[0][0]]
print(user_watch_history)