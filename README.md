## NFTMe
![NFTME](https://user-images.githubusercontent.com/53923200/134110201-69fc0b4c-30f3-4e31-944c-40f743e76b04.png)
![NFTMe](https://user-images.githubusercontent.com/53923200/134114284-e227df12-0a4b-4652-8da1-52b51e9e45e9.gif)

## What is NFTMe?

NFTMe is the result of a challenge that Shopify posed to it's Backend Developer applicants. <br/>
Originally, the task asked the programmer to create an image repository. I decided to have some fun with the idea, and thats where NFTs come into play! </br>
NFTs have been a super hot topic, and I've always wanted to code something surrounding the topic. <br/>
NFTs (non-fungible tokens) are simply data on a blockchain, meaning they are all individual. <br/>
So, you can think of NFTMe as a marketplace where users would go to buy/sell NFTs! <br/>

NFTMe allows users to:
- Authenticate with an account
- Choose their balance, aka money to spend (go ahead, buy all of the NFTs you'd like)
- Upload NFTs
- List NFTs for sale on the market
- Purchase NFTs from other users
- Update NFTs to set their price, title, and selling status
- And much more!

## Getting Setup
Note: If you have any issues setting up NFTMe, please do not hesitate to reach out to me by phone or email! <br/>
Phone: 519-277-3287 <br/>
Email: tstauffe@uwaterloo.ca <br/>

`git clone https://github.com/trentstauff/NFTMe.git`<br />
`cd NFTMe` <br />
`set FLASK_APP=run.py` (on windows) `export FLASK_APP=run.py` (on unix) <br />
`pip install -r requirements.txt` <br />
`flask run` <br />

Then, you'll see a link where the application is running (should look like `http://127.0.0.1:5000/`). </br>
Navigate to said link in the browser, and have fun!

### For Shopify Recruiters:
**You can either register a new account, or you can log in to an existing one made for you:**

**username:** recruiter@shopify.com </br>
**password:** password


## Testing
Testing this flask application is extremely easy for any developers. Just navigate to the top level project folder and type:
`pytest`
To the console after installing the requirements above.

![image](https://user-images.githubusercontent.com/53923200/134114531-ccb315a2-f7d2-49fb-9dde-aee7912e60f2.png)
![image](https://user-images.githubusercontent.com/53923200/134114555-b9351e42-ed3e-4611-abdd-91f57260da95.png)


This application is tested both on it's models and it's routes.<br />
Pytest gives the developer the option to test actions of the code that require user authentication!<br />
In the future, the code is ready to be expanded to test the HTML files as well!<br />
Due to the extremely modular nature of unit tests and pytest, it is very easy for the developer to add tests later.<br />

