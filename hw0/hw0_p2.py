#!/usr/bin/env python
# coding: utf-8

# Problem 2: Movie Data Analysis ( *hw0_p2.py* )
#
# In this homework, you are asked to write a program for answering the following questions based on IMDB Movie data ( *IMDB‐Movie‐Data.csv* ).
#
# You are required to write a function for answering each question. You may want to use `Python’s File reading`, `List`, `Dictionary`, and `Functions`.
#
# **You cannot use any packages**. The output format of each question is free.

# In[1]:


class MyTable:

    def __init__(self):
        with open('IMDB-Movie-Data.csv', 'r') as f:
            self.contents = [line for line in f]
            self.columns_names = self.contents[0].strip('\n').split(',')
            self.rows = [content.strip('\n').split(',')
                         for content in self.contents[1:]]

    def describe(self):
        print(f'data\'s length without titles: {len(self.rows)}')
        print(f'Columns name: \n{self.columns_names}')

    def __repr__(self):
        text = ''
        for line in self.contents:
            text += line + '\n'
        return text

    def columns(self, col_name: str) -> list:
        assert col_name in self.columns_names, f'choose column from {self.columns_names}'

        col_index = self.columns_names.index(col_name)
        return [row[col_index] for row in self.rows]

    def multi_col_name_index(self, *col_name) -> list:
        col_names = []
        for i in col_name:
            assert i in self.columns_names, f'choose column from {self.columns_names}'
            col_names.append(i)

        return [df.columns_names.index(col_names[i]) for i in range(len(col_names))]

    def rows_with_column(self, col_name: str, data_type: str) -> list:
        assert col_name in self.columns_names, f'choose column from {self.columns_names}'

        col_index = self.columns_names.index(col_name)
        return [i for i in df.rows if i[col_index] == data_type]

    def total_revenue(self):
        def count_total(df): return sum(float(i) for i in df if i != '')
        total_revenue = round(count_total(
            df.columns(col_name='Revenue (Millions)')), 2)
        return total_revenue


# In[2]:


df = MyTable()
# df.describe()


# ## (1) Top-3 movies with the highest ratings in 2016?

# ##### check

# In[3]:


#print(len([i for i in df.rows_with_column(col_name='Year', data_type='2016')]), '\n')
#print('checking with first three:\n',[i for i in df.rows_with_column(col_name='Year', data_type='2016')][0:3])


# ##### answer

# In[4]:


df_2016_sorted = sorted(df.rows_with_column(
    col_name='Year', data_type='2016'), key=lambda x: int(x[0]))
df_2016_top3 = [each_movie[df.columns_names.index(
    'Title')] for each_movie in df_2016_sorted[:3]]
print(f'Top-3 movies with the highest ratings in 2016: {df_2016_top3}\n')


# ## (2) The actor generating the highest average revenue?

# - 有最高平均薪酬的演員？
# - 每部戲賺的錢 / 戲裡的演員 = 平均薪酬
# - 找出平均薪酬裡最高的演員？
#
# ？是這樣嗎？

# ##### 有被紀錄revenue的戲的數量

# In[5]:


count_have_revenue = 0
for i in df.columns(col_name='Revenue (Millions)'):
    if i != '':
        count_have_revenue += 1
# count_have_revenue


# ##### 每位演員演過多少部戲

# In[6]:


# 每部戲出現的演員
actors = [j.strip()
          for i in [actors.split('|') for actors in df.columns('Actors')]
          for j in i]
# print(len(actors))

actors_count = {}
for person in actors:
    if person not in actors_count:
        actors_count[person] = 1
    else:
        actors_count[person] += 1
# print(actors_count)


# In[7]:


# len(actors_count)


# In[8]:


actors_count_sorted = {k: v for k, v in sorted(
    actors_count.items(), key=lambda item: item[1], reverse=True)}
# print(actors_count_sorted)


# ##### answer
# ##### 每部戲讓演員們平均賺多少錢

# In[9]:


index_T_A_R = df.multi_col_name_index('Title', 'Actors', 'Revenue (Millions)')
t_a_r = [(i[index_T_A_R[0]], i[index_T_A_R[1]], i[index_T_A_R[2]])
         for i in df.rows if i[index_T_A_R[2]] != '']
highest_avg_money = 0
person_count = 1
movie = ''
who = ''
for i in t_a_r:
    #print(i, '\n')
    money = float(i[2])
    for j in i[1]:
        if j == '|':
            person_count += 1
    each = money / person_count
    if each > highest_avg_money:
        highest_avg_money = each
        movie = i[0]
        who = i[1]

print('The actor generating the highest average revenue:')
print(f'highest average money: {highest_avg_money}, {who}\n')


# ## (3) The average rating of Emma Watson’s movies?

# - 她有演過多少部戲？
# - 她演過的戲的rank的加總？再平均

# ##### check

# In[10]:


actors = [j.strip()
          for i in [actors.split('|') for actors in df.columns('Actors')]
          for j in i]
#print(f'{len(actors)} actors in total of all movies')
#print('Emma Watson' in actors)
#print(f"{actors_count['Emma Watson']} movies by Emma Watson")


# In[11]:


for movie in [actors.split('|') for actors in df.columns('Actors')]:
    # print(movie)
    for person in movie:
        if person.strip() == 'Emma Watson':
            # print(person)
            pass


# In[12]:


test_str = 'Christian Bale| Heath Ledger| Aaron Eckhart|Michael Caine'
#print('Christian Bale' in test_str)


# ##### answer

# In[13]:


index_R_T_A = df.multi_col_name_index('Rank', 'Title', 'Actors')
r_t_a = [(i[index_R_T_A[0]], i[index_R_T_A[1]], i[index_R_T_A[2]])
         for i in df.rows]

emma_watson_movies = [(rank, title)
                      for rank, title, actor in r_t_a if 'Emma Watson' in actor]
#print(emma_watson_movies, '\n')
print(
    f"The average rating of Emma Watson’s movies: {sum(int(rank) for rank, title in emma_watson_movies) / actors_count['Emma Watson']}\n")


# ## (4) Top-3 directors who collaborate with the most actors?

# ##### check

# In[14]:


#print(f"director in {len(df.columns(col_name='Director'))} of movies")
#print([director for director in df.columns(col_name='Director')][0:3])


# In[15]:


director_repeat = [director for director in df.columns(col_name='Director')]
director_nonrepeat = []
for d in director_repeat:
    if d not in director_nonrepeat:
        director_nonrepeat.append(d)
# print(len(director_repeat))
# print(len(director_nonrepeat))


# In[16]:


index_d, index_a = df.multi_col_name_index('Director', 'Actors')
d_a = []
for i in df.rows:
    i[index_a] = i[index_a].replace('|', ',')
    i[index_a] = i[index_a].replace(', ', ',')
    d_a.append((i[index_d], i[index_a]))
# d_a[0]


# In[17]:


collaborate = []
for da in d_a:
    for a in da[1].split(','):
        collaborate.append((da[0], a))
# print(collaborate)


# ##### check

# In[18]:


def director_work_with(target_director: str) -> list:
    return [actor
            for director, actor in collaborate
            if director == target_director]


def director_work_with_how_many(target_director: str) -> int:
    count_a = []
    for a in director_work_with(target_director):
        if a not in count_a:
            count_a.append(a)
    return len(count_a)

#director_work_with_how_many('Christopher Nolan')


# ##### answer

# In[19]:


all_director_with_with_how_many = []
for d in director_nonrepeat:
    director = ''
    count_collaborate = director_work_with_how_many(d)
    highest_collaborate = count_collaborate
    director = d
    all_director_with_with_how_many.append((director, highest_collaborate))

# all_director_with_with_how_many


# In[20]:


all_director_with_with_how_many = sorted(
    all_director_with_with_how_many, key=lambda x: x[1], reverse=True)
print(
    f'Top-3 directors who collaborate with the most actors:\n{[i[0] for i in all_director_with_with_how_many[:3]]}\n')


# # (5) Top-2 actors playing in the most genres of movies?

# In[21]:


index_g, index_a = df.multi_col_name_index('Genre', 'Actors')
g_a = []
for i in df.rows:
    i[index_a] = i[index_a].replace('|', ',')
    i[index_a] = i[index_a].replace(', ', ',')
    i[index_g] = i[index_g].replace('|', ',')
    g_a.append((i[index_g], i[index_a]))
# g_a[0]


# In[22]:


actor_genre = {}
for genres, actors in g_a:
    for actor in actors.split(','):
        if actor not in actor_genre:
            actor_genre[actor] = []
            for genre in genres.split(','):
                actor_genre[actor].append(genre)
        else:
            for genre in genres.split(','):
                if genre not in actor_genre[actor]:
                    actor_genre[actor].append(genre)
# actor_genre


# ##### answer

# In[23]:


count_actor_genre = {}
for k, v in actor_genre.items():
    count_actor_genre[k] = len(v)
count_actor_genre = {k: v for k, v in sorted(
    count_actor_genre.items(), key=lambda item: item[1], reverse=True)}
top_count_actor_genre = [(k, v) for k, v in count_actor_genre.items()]
print(
    f'Top actors playing in the most genres of movies:\n{[i for i, j in top_count_actor_genre if j >= 13]}\n')


# # (6) Top-3 actors whose movies lead to the largest maximum gap of years?

# Example of “maximum gap of years”:
#
# Tom Cruise has movies: “Edge of Tomorrow” in 2014, “Mission: Impossible - Rogue Nation” in 2015, “Oblivion” in 2013, “Jack Reacher” in 2012, “Mission: Impossible III” in 2006, “Jack Reacher: Never Go Back” in 2016, “Rock of Ages” in 2012, “Mission: Impossible - Ghost Protocol” in 2011.
#
# The maximum gap of years is 2016‐2006 = 10

# In[24]:


index_a, index_y = df.multi_col_name_index('Actors', 'Year')
g_a = []
for i in df.rows:
    i[index_a] = i[index_a].replace('|', ',')
    i[index_a] = i[index_a].replace(', ', ',')
    g_a.append((int(i[index_y]), i[index_a].split(',')))
# print(g_a[:3])


# In[25]:


actor_year = {}
for year, actors in g_a:
    for actor in actors:
        if actor not in actor_year:
            actor_year[actor] = [year]
        else:
            actor_year[actor].append(year)
# actor_year


# In[26]:


def maximum_gap_of_years(actor: str):
    assert actor in actor_year.keys(), 'This actor seems not to be in the IMDB list'
    return max(actor_year[actor]) - min(actor_year[actor])

#maximum_gap_of_years('Leonardo DiCaprio')


# In[27]:


actors_maximum_gap_of_years = {}
for actor in actor_year.keys():
    actors_maximum_gap_of_years[actor] = maximum_gap_of_years(actor)
actors_maximum_gap_of_years = {k: v for k, v in sorted(
    actors_maximum_gap_of_years.items(), key=lambda item: item[1], reverse=True)}
# actors_maximum_gap_of_years


# In[28]:


print(
    f'Actors whose movies lead to the largest maximum gap of years(10 years):\n{[i for i, j in actors_maximum_gap_of_years.items() if j == 10]}\n')


# # (7) Find all actors who collaborate with Johnny Depp in direct and indirect ways

# In[29]:


for i in actors:
    j = i.split(',')
    if 'Johnny Depp' in j:
        print(j)


# In[ ]:
