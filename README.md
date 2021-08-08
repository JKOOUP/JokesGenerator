# Jokes generator
## Description

In this project I implemented jokes generator using n-gram language model. You can interact with the model through the web interface. There you can generate new jokes, save and read them. Also you can train new generator with your own text and then use it to generate new jokes. 

## Train generator
To train new generator go to the page `Train generator`. There you can specify generator name, description and the number of previous words that it will look at to generate a new one.

**The training process can take quite a long time.**

## Add new joke
On the `Generate joke` page you can generate new joke. Choose one of generators, that you trained, set the maximum number of words and the begging of the joke. Then you can save generated joke or generate a new one.

## Examples
Generator trained on VK posts from [this](https://vk.com/jumoreski) and [this](https://vk.com/kalikfan) VK groups.

```
Летят в самолете русский, британец и американец.
Американец руку вытаскивает, понюхал и говорит:
Америка.
— Как скажете.
— Я тебе сказал, сынок.
— Что?
```

```
Шла корова по лесу. Видит тарковский кино снимает. Снялась в кино и сгорела.
```