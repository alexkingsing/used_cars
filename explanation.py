exp = {"intro": '''Welcome to the explanation section! In here I will provide a **simplified explanation on what is Machine/Deep Learning**.
After that, I will explain with a bit more detail **how the model you're using here works!** \n
So let's get to it!\n
**WARNING**: This section is LONG and somewhat detailed. If not deeply interested, please avoid.''',
            "ml_title": "What is Machine / Deep Learning?",
            "ml_intro":'''So, what is Machine Learning? Long story short, machine learning can be summarized:
    **The process under which an algorithm, based on repeated data and statistic principles, 'learns' a task.** Abstract, right?
    So what does it *truly mean*? Let's try with an example! \n
(1) If I tell you that we have an animal with four legs and a tail, can you classify what animal this is?
most likely no, it could be a cat or a dog, or even horse, right? \n
(2) Then let's say I now tell you that this animal has white hair, can you figure it out now? \n
(3) Finally, let's say the animal weights 500 KG, do you know what is now? \n
No? click the button below!''',
            "horse": "images/horse.jpg",
            "ml_close": '''What we did just now is a **very simplified** version of machine learning!
We discussed characteristics (features in ML/DL) of the animal, and then you (the machine!) tried to guess what it was.\n 
With that said, let's move on to the model being used here!''',
            "model_title":'''What is the model behind this calculator?''',
            "model_intro":''' An image says more than a thousand words! So instead of describing it, let me share a picture of
            how the model looks like:''',
            "model_image": "images/ANN.png",
            "model_intro2": '''Now, this doesn't explain much by itself, so let me start by the beginning: **The model inputs**.''',
            "model_inputs_title": '''Model inputs''',
            "model_inputs_exp": ''' To start, let's discuss how do the model inputs look like normally:''',
            "model_inputs_exp2": '''But we have a mismatch here! The picture above says we have **1802 inputs**, but our table only has
            **11 columns**! What's going on? Well, what is happening is a process called **One-Hot Encoding**. \n
One-hot encoding transforms a categorical column (Think of color) and transforms each option into a binary (True/False) column. 
Why is this needed? For a simple reason **computers don't understand what colors are or how to work with them** so we need to
transform into something a computer understands: numbers. \n
That said, this is all too abstract, so once again let's see how One-hot encoding works in practice:''',
            "one-hot": "images\onehot.png",
            "model_inputs_exp3": ''' This explains what happens to our categorical columns (Model, color, etc), but what about our
numerical columns? Well in the case of numerical columns we don't need to one-hot encode, but we still need to **adjust them!**
The preferred adjustment is called **Standard Scaling**.\n
Standard scaling transforms ANY distribution of numbers and fits it into a standardized normal distribution.
We won't go into the details of *WHY* we do this adjustment, but let me state that this has two purposes:
* Scaling our numbers to a normal distribution helps **stabilize our model's results**.
* Most algorithmic Machine Learning models **assume the data is distributed normally**. \n
Standard scaling performs the following adjustment for every number: ''',
            "model_inputs_close": ''' Where: \n
* **z** is the z-score of the value that corresponds to the standard normal distribution.
* **x** is the value being evaluated.
* **u** is the mean (average) of the number distribution.
* **s** is the sample standard deviation of the observed numbers. 
With that, we understand what's happening to our inputs BEFORE they enter the model, but what happens in the model? \n
**Let's find out!**''',
            "model_general_title": ''' Model explanation''',
            "model_general_": ''' BLABLABLA'''}
