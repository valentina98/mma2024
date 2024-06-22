## Running without Docker
### Setup
```
git clone https://github.com/GoncaloBFM/mma2024
cd mma2024
python -m venv .venv

#mac
source .venv/bin/activate

#windows:
.venv\Scripts\activate

pip install -r requirements.txt
```

### Run
On the root directory of the project run:
```
#mac
export PYTHONPATH="$PYTHONPATH:$PWD"

#windows
$env:PYTHONPATH = "$env:PYTHONPATH;$PWD"

python src/main.py
```

After the Dash server is running open http://127.0.0.1:8050/ on your browser.

## (Alternative) Running with Docker
### Setup
1) Install Docker
2) Run:
```
git clone https://github.com/GoncaloBFM/mma2024
cd mma2024
docker buildx build . -t mma2024
```

### Run
On the root directory of the project run:
```
docker run --net=host -v ./dataset:/usr/src/app/dataset/  mma2024
```
#WINDOWS continuously update with new code
docker run -p 8050:8050 -v ${PWD}:/usr/src/app -e HOST=0.0.0.0 mma2024

After the Dash server is running open http://127.0.0.1:8050/ on your browser.

## Plotly and Dash tutorials
- Dash in 20 minutes: https://dash.plotly.com/tutorial
- Plotly plots gallery: https://plotly.com/python/

## test:
You are an AI that strictly conforms to responses in Python code. 
Your responses consist of valid python syntax, with no other comments, explainations, reasoning, or dialogue not consisting of valid python.
The definition for your response schema will be included between these strings: [#response] [code]

Plot a scatterplot. Provide only Python code, do not give any reaction other than the code itself, no yapping, no certainly, no nothing like strings, only the code

# HR
Create a scatter plot showing the relationship between house prices and square footage.

plt.scatter(df['Salary'], df['MaritalDesc'])
plt.xlabel('Salary')
plt.ylabel('MaritalDesc')
plt.show()

# Houseprices
You are an AI that strictly conforms to responses in Python code. 
Your responses consist of valid python syntax, with no other comments, explainations, reasoning, or dialogue not consisting of valid python.
If you have any comments or remarks they will have a # in front of it. It has to be strict python code.
Use the dataset name, column names, and dataset itself as context for the correct visualization. The code implementation should make use of the correct variable names.
The dataset is already loaded as df, you don't have to load in matplotlib and pandas, any other packages you want to use should be imported.

Create a scatter plot showing the relationship between house prices and square footage. Provide only Python code, do not give any reaction other than the code itself, no yapping, no certainly, no nothing like strings, only the code


Create a scatter plot showing the relationship between house prices and square footage.


plt.scatter(df['area'], df['price'])
plt.xlabel('Area')
plt.ylabel('Price')
plt.show()

# Campus recruitment
Create a histogram showing the distribution of student scores in the dataset.

# Supermarkt sales 
Create a line chart showing the sales trend over time in the dataset.

# Hotel bookings
Create a bar chart showing the number of bookings per month in the dataset.



# bugs
there is a glitch if you press delete and then clear it duplicates the visualized thing until you press restore history twice then everything is normal again

also if you press restore history before making any code or pressing delete or clear history you remove the pie chart permanently. It shouldn't be cleared when you just press restore history.