# Personality to Plant Classification - main idea

This project is an NLP-based personality classification application that maps user responses from a quiz to a symbolic “inner plant” archetype. The system analyzes free-text answers using sentiment analysis powered by a fine-tuned DistilBERT model and a k-nearest neighbors classifier.

### Access the aplication: https://what-is-your-inner-plant.streamlit.app/


# What is the logic behind the classificatiton?
The questions in the quiz are mapped to specific traits of plants. <br /><br/>
There are five groups of traits: Growth, Soil, Sunlight, Watering and Fertilizer <br /><br/>
Each of the groups describe specifications of the plants, eg. how often do you need to water them. <br /><br/>
Each of the groups also correspond to specific human traits: <br /><br/>
**Growth** - how fast can one learn.<br />
**Soil** - how much of an extrovert or a conformist one is.<br />
**Sunlight** - how much does one like sunny and hot weather.<br />
**Watering** - how much does one like water related activities such as swimming, etc. <br />
**Fertilization** - how good and balanced is ones diet.<br />
 <br />
Via five question form, user is asked to answer one question from each group. The questions are created in a way that forces user to explain their attitude or liking towards the conserned topic, eg. Trait: Growth, Question: "How eager are you to learn new technologies?".
 <br /><br/>
After form is submitted, the answers are encoded via fine-tuned DistilBert model (more about fine-tuning below) into sentiment analysis result where -1 stands for complitly negative, 0 for neutral and 1 for positive attitude.
 <br /><br/>
Then using k-NN classifier that was trained on dataset consisting of over 200 entries of plants and their traits.
 <br /><br/>
After the appropariate plant is selected, the results are displayed to user.
 <br /><br/>
<br/>
Along with the verdict user also gets to see the photo of the plant along with DataFrame showing the results of sentimnet analysis along with apropariate question, answer and trait of the plant it concerns. The app also displays first paragraph of wikipedia page, briefly describing the obtained plant.
 <br /> <br />
 **Example results:**<br/>
 <img width="560" height="606" alt="image" src="https://github.com/user-attachments/assets/0ca9a41f-ca26-45b6-abbe-dd8ff373894e" /> <br />
 <img width="440" height="460" alt="image" src="https://github.com/user-attachments/assets/a72ede71-7674-4ac6-bee3-57ef9b7e7ac0" />


# Technologies used in project
## Machine Learning
### DistilBert fine-tuning
The fine tuning of DistilBert was performed using dataset of short answers that were obtained from responses to forms. To make the dataset bigger, similar responses were then added.

 <br /><br/>
### k-Nearest Neighbours
The model was trained on a dataset from kaggle: https://www.kaggle.com/datasets/aribashafaqat/plants-growth-and-care-recommendations. Before training the model, appropariate data cleansing was performed. (the code can be seen in file 'data_cleansing.py' in catalog 'scripts') <br /> <br />

After performing the data cleansing I used knn model available in sklearn python library with number of neighbours set to one to always obtain only one result, I chose minkowski method with p = 4 as I wanted to penalize large differencess between traits to prevent significant mismatching of traits as the goal is to get result in which each of the traits matches all user answers best. <br />
<br><br>
###
**Contribute to the project by answering short, 7 questions form: https://forms.office.com/e/rstjrBe3Cy**
