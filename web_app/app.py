from flask import Flask, render_template, request, redirect, url_for
import json
import get_features
from werkzeug import security

app = Flask(__name__)

pdf_path = '/home/shaurya/PycharmProjects/findMyAdvisor/pdf/'


@app.route("/")
def index():
    return "Welcome!"


@app.route("/home")
def home():
    return render_template('startbootstrap-landing-page-gh-pages/index.html')


@app.route('/searchresults', methods=['POST'])
def handle_data():
    fileName = request.form['img[]']

    # data = '{"dict_cite": {"Xiang Zhang": 44129, "Dongwon Lee": 6203, "Lynette (Kvasny) Yarger": 2286, "Nicklaus A. Giacobe": 304, "Vasant  Honavar": 11829}, "dict_link": {"Xiang Zhang": "https://faculty.ist.psu.edu/xzz89/", "Dongwon Lee": "http://pike.psu.edu/dongwon/", "Lynette (Kvasny) Yarger": "http://faculty.ist.psu.edu/lyarger", "Nicklaus A. Giacobe": "http://personal.psu.edu/nxg13", "Vasant  Honavar": "http://faculty.ist.psu.edu/vhonavar"}, "dict_affiliation": {"Xiang Zhang": "pppppAssociate Professor of Information Sciences and TechnologypppppData MiningpppppMachine LearningpppppBig Data AnalyticspppppDatabasespppppBiomedical Informatics", "Dongwon Lee": "pppppAssociate Professor of Information Sciences and TechnologypppppData ManagementpppppData Mining & Machine LearningpppppFraud InformaticspppppHuman Computation & Crowdsourcing", "Lynette (Kvasny) Yarger": "pppppAssociate Professor of Information Sciences and TechnologypppppSocial InformaticspppppCommunity InformaticspppppCritical TheorypppppFeminist TheorypppppDigital Inequality", "Nicklaus A. Giacobe": "pppppAssistant Teaching Professor of Information Sciences and TechnologypppppCybersecuritypppppSituation AwarenesspppppSecurity MetricspppppCybersecurity Education", "Vasant  Honavar": "pppppProfessor and Edward Frymoyer Chair of Information Sciences and TechnologypppppArtificial IntelligencepppppData SciencepppppMachine LearningpppppBioinformaticspppppHealth Informatics"}, "dict_image": {"Xiang Zhang": "https://ist.psu.edu/sites/default/files/styles/thumbnail/public/EECS-Xiang%20Zhang-C1_0.jpg?itok=Fl82B2MI", "Dongwon Lee": "https://ist.psu.edu/sites/default/files/styles/thumbnail/public/lee.jpg?itok=YP7oVS9z", "Lynette (Kvasny) Yarger": "https://ist.psu.edu/sites/default/files/styles/thumbnail/public/yarger_lynette_web2.jpg?itok=gLHXjulw", "Nicklaus A. Giacobe": "https://ist.psu.edu/sites/default/files/styles/thumbnail/public/NickGiacobe-sm.jpg?itok=n21H3wA2", "Vasant  Honavar": "https://ist.psu.edu/sites/default/files/styles/thumbnail/public/Honavar-Vasant_0.jpg?itok=DhZUTTaW"}, "list_name_ordered": ["Vasant  Honavar", "Dongwon Lee", "Xiang Zhang", "Lynette (Kvasny) Yarger", "Nicklaus A. Giacobe"]}';
    data = get_features.return_json(pdf_path + fileName)
    data = json.loads(data)
    return render_template('startbootstrap-1-col-portfolio-gh-pages/index.html', data=data)


if __name__ == "__main__":
    app.run()
