# FindViser
___
![N|Solid](https://watsonidenti-tee.resourceammirati.com/images/powered-by-ibm-watson.png)

___
## Inspiration
Students planning for a graduate degree like Masters or a PhD face this important decision of choosing an adviser for their research. 
Right now the way to do this online, is to - 
- Go to your department's website's faculty page
- scroll down the whole list of faculties (usually more than 60)
- go to their about page by the department
- from that page go to their personal webpage for more concrete and latest information
- then google about their citations and work
- if you dont like them, repeat the above steps . . 

Trying to find an adviser offline is even worse. You can talk to other faculties and senior students for advice to find one, but there is no common consensus among them, which makes this processs more frustating.
What if there is a smart intelligent system which can suggest you the best adviser possible. A system which on the basis of your profile gives you suggestions for potential research advisers. We feel getting the right research adviser is a very important decision of a graduate student's  life and their future.
P.S. The creators of this project are both international graduate students, who had to go through this ordeal of finding the adviser.
___
## What it does
###### TLDR; It takes your portfolio/ resume/ curriculum vitae and then gives you the top 5 suggestions for your potential future research advisers. 
- ###### What do the users see ?
    1. Landing Page has browse button through which the user submits their resume/CV in pdf format(for now). 
    2. In the next page they are greeted with their potential advisers, ranked in an order of relevanec. On the screen have the useful meta information about them, including-
        - Research Interests
        - Citation count from Google Scholar
        - Link to their personal homepage
        - Their thumbnail :D
___
## How we built it
###### TLDR;  Uses IBM Watson's Natural Language Understanding api to extract useful features from the professor's work and your resume, and then uses a smilarity measure to rank the professors.

##### We took a data and AI driven approach to this problem.
- ###### Data Collection
    - We collected the professor's protfolio data for our Information Sciences Department only (for now), because we wanted to verify the results of our system as we are now familiar with their work.
    - We did 2 level web scraping, fetching department page of the professor as well as their personal pages.
    - We even scraped google scholar to get the citations count for that professor.
- ###### Intelligence by IBM Watson
    - We used IBM Watson's powerful and easy to use Natural Language Understanding API to get the important representative features of the professor such as, keywords, entities and concepts mentioned in their portfolios
    - We reduce this huge data into small representative features and load them into a lookup dictionary for faster access.
- ###### Similarity Measure and Ranking
    - Once the user enters their resume/CV we parse the text from the pdf, we get the meaningful and representative features using the IBM watson API.
    - Now we have feature vectors to compare, a set of professors to the user's resume. We accomplish this by using basic cosine similarity measures based on the frequency of the occuring text.
    - We now rank the professors on the basis of this similarity measure and show them to the user with useful meta information on the next page.
___
## Challenges We ran into
- Data Scraping is challenge for this problem. We think that this is the reason as to why there are no existing solutions out there. Every department has their own web interface which makes it difficult to automate this task.
- Scraping data from professors personal pages and parsing that through Watson takes time. We partially solved problem this by caching the features extracted using Watson. As the scale of operations increase, this approach is not viable. We beleive that there is a better way to do this.
- We had limited time, so we could showcase our work only on one department, given the time we want to explore our approach on more departments and larger number of professors.
- There is a lack of evaluation metric or ground truth data, which is a problem with all information retrieval systems.
___
## Accomplishments that we are proud of
- We even tried this for other existing students of our department (for whom we know the adviser) and the results are spot on !
- We tried to submit our resume's to the system and it was 100% accurate ! Our current advisers are the same as the system.
- The results are surprisingly good.
- The system is really fast for now (maybe beacause we have less data).
___
## What we learned
- We are Machine Learning Researchers, and we are surprised by the power of IBM's Watson. It can do wonders, while being accesible.
- Data scraping is a challenge, maybe that's why nobody has done a similar thing before. But if we are focussed and we aim only for the departments in Penn State this is achievable.
- There is a lot of redudant and stale information out there about the professors.
___
## What's next for FindVisor
We think the future of such an application is huge. These days you can find jobs with your resume but nobody talks about finding the right person for your research when you are going into an academic program. 
There is a ton of improvement which needs to be done to make this system even more useful.
Some important future directions for our system are -
- Add ratings for the professor by the peers. Similar to what rate my professor is doing.
- Funding information ! Graduate students are always on the lookout for funding. Maybe if we could get this information to them, that would be very useful.
- Vacancies with professors ! Is the professor looking for more graduate students to work with, do they have projects for them. Are those projects funded ?
- Active Projects of the professors. As new research oppurtunities or projects are coming up or closing down, there is no way to track active research projects for now. There is a lot of stale work posted by the professors which now may not be relevant to the students.
- Smaller features -
    - Office Hour information
    - Contact information of other students working with that Professor

