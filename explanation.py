exp = {"intro": '''Welcome to the explanation section! In here I will provide a **simplified explanation on what is Machine/Deep Learning**.
After that, I will explain with a bit more detail **how the model you're using here works!** \n
So let's get to it!\n
**NOTE**: This section is long and somewhat detailed. If not deeply interested, please avoid.''',
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
            "one-hot": "images/onehot.png",
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
            "model_general_exp1": ''' Now that we know what's coming into the model we need to find out how does it work! \n
To explain how a neural networks completely it's actually an area of active research (as of 2020. See: *Adaptive Explainable Neural Networks* (AxNNs) by Chen et al.) \n
However we can explain the *basic logic* of how a Neural Network learns. First we need to talk a bit about neurons, which are the
building blocks of neural networks. **Neurons** in deep/machine learning are extremely similar to their biological counterpart 
(They are modeled after them!) in the sense that they work as a bridge that connects one side to another until an outcome is reached. 
\n A neuron takes one or many inputs, "consolidates" them through an activation function and returns an outcome: 
A number, True/False, etc.''',
            "neuron": "images/Neuron.png",
            "model_general_exp2": ''' So that's a neuron. And what's a neural network? **It's just many neurons connected**. Now,
there are **MANY** ways to connect the Neurons (One of the key differences of different types of NN), but in our case we are using the
simplest form of NN: **A feed-forward neural network** which means every neuron is connected to all the inputs that came before it,
and all the neurons in the next layer. 
\n At the input layer those x you see in the image are the inputs we just discussed! But what happens later? Let us now discuss:
\n ** Hidden Layers**.''',
            "model_general_exp3": '''So what are hidden layers? They are still the same neurons, but hidden layers are 
** not directly connected to neither the inputs nor to the final output** this is why they're called "hidden". Hidden layers
only interact with other neurons, either the front of in the back, but are not *visible* to the user or to other applications.
Hidden layers are the ones that are actually responsible for the excellent performance and complexity of neural networks because they
perform **MANY** functions (data transformation, automatic feature creation, etc.).
Hidden layers are the subject of much research (how many layers? how many neurons?) So this will be all I'll say about Neural Networks.
\n The **Output layer** of a model is the output layer, which generates the final result of our model! Now, depending on what we want
this can be a label (Think dog, cat, etc) OR a number (like in here!). The output layer can be one neuron if we want a number
or a binary result (True / False), or if we want to identify categories (happy, sad, nervous, etc) we use many output neurons.
In our case since our end result is a number, the NN only has one output neuron!
\n Now we move on to our last section!''',
            "model_final_title": ''' How a neural network learns!''',
            "model_final_exp": ''' So far we have reviewed how a neural network is built but NOT how learns (which is the most important thing!)
Let's start at the beginning: **When a neural net is being trained, all of its weights, values, etc, are INITIALLY set to random values.** 
Training data is fed to the input layer, and it passes through the succeeding layers, getting multiplied and added together in complex ways, 
until it finally arrives, radically transformed, at the output layer. But there's a problem here, what if the NN is wrong?
Here comes the magic and the true power of neural networks. They learn by training, just like humans!
\n A neural network is trained by adjusting neuron input weights based on the network's performance on example inputs. 
If the network classifies an image correctly, or predicts the correct (closest) price for a vehicle,
the weights contributing to the correct answer are increased, while other weights are decreased. 
If the network misclassifies an image, or provides a wildly incorrect number, the weights are adjusted in the opposite direction.
\n This process of learning by mistakes is called, in ML, ** Backpropagation** and it looks like this:''',
            "backp": "images/backp.png",
            "model_final": ''' DA ENDING WORDS'''}
