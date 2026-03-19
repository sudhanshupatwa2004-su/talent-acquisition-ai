import os
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

load_dotenv()

MOCK_CANDIDATES = [
    {"name":"Priya Sharma",         "email":"priya.sharma@email.com",      "skills":["Python","ML","TensorFlow","NLP"],                "experience":4, "education":"B.Tech CSE, IIT Delhi",           "linkedin":"linkedin.com/in/priya-sharma",      "location":"Bangalore"},
    {"name":"Arjun Mehta",          "email":"arjun.m@email.com",           "skills":["C++","System Design","Kubernetes","Go"],          "experience":7, "education":"B.Tech CSE, IIIT Hyderabad",      "linkedin":"linkedin.com/in/arjun-mehta",       "location":"Hyderabad"},
    {"name":"Vikram Nair",          "email":"vikram.n@email.com",          "skills":["Data Science","Python","SQL","Power BI"],         "experience":5, "education":"M.Sc Data Science, BITS Pilani",  "linkedin":"linkedin.com/in/vikram-nair",       "location":"Pune"},
    {"name":"Ananya Krishnan",      "email":"ananya.k@email.com",          "skills":["React","TypeScript","Next.js","GraphQL"],         "experience":4, "education":"B.Tech IT, NIT Trichy",           "linkedin":"linkedin.com/in/ananya-k",          "location":"Chennai"},
    {"name":"Rohan Kapoor",         "email":"rohan.kap@email.com",         "skills":["AWS","DevOps","Docker","Terraform"],              "experience":6, "education":"B.E CSE, Delhi University",       "linkedin":"linkedin.com/in/rohan-kapoor",      "location":"Delhi"},
    {"name":"Rahul Verma",          "email":"rahul.v@email.com",           "skills":["Java","Spring Boot","AWS","Docker"],              "experience":6, "education":"M.Tech, NIT Trichy",              "linkedin":"linkedin.com/in/rahul-verma",       "location":"Mumbai"},
    {"name":"Sneha Patel",          "email":"sneha.p@email.com",           "skills":["Python","Django","PostgreSQL","REST API"],        "experience":2, "education":"B.Tech IT, GTU",                  "linkedin":"linkedin.com/in/sneha-patel",       "location":"Ahmedabad"},
    {"name":"Kiran Reddy",          "email":"kiran.r@email.com",           "skills":["Android","Kotlin","Firebase","MVVM"],             "experience":3, "education":"B.Tech ECE, Osmania Univ",        "linkedin":"linkedin.com/in/kiran-reddy",       "location":"Hyderabad"},
    {"name":"Divya Menon",          "email":"divya.m@email.com",           "skills":["UI/UX","Figma","React","CSS"],                   "experience":4, "education":"B.Des, NID Ahmedabad",            "linkedin":"linkedin.com/in/divya-menon",       "location":"Bangalore"},
    {"name":"Siddharth Roy",        "email":"sid.roy@email.com",           "skills":["Scala","Spark","Hadoop","Kafka"],                 "experience":5, "education":"M.Tech CS, IIT Kharagpur",        "linkedin":"linkedin.com/in/sid-roy",           "location":"Kolkata"},
    {"name":"Pooja Iyer",           "email":"pooja.i@email.com",           "skills":["Python","Flask","MySQL","Redis"],                 "experience":2, "education":"B.Tech CS, Anna University",      "linkedin":"linkedin.com/in/pooja-iyer",        "location":"Chennai"},
    {"name":"Aditya Singh",         "email":"aditya.s@email.com",          "skills":["Node.js","MongoDB","Express","Vue.js"],           "experience":3, "education":"B.Tech IT, Amity University",     "linkedin":"linkedin.com/in/aditya-singh",      "location":"Noida"},
    {"name":"Kavya Suresh",         "email":"kavya.su@email.com",          "skills":["Data Analysis","Tableau","Excel","Python"],       "experience":2, "education":"MBA Analytics, XLRI",             "linkedin":"linkedin.com/in/kavya-suresh",      "location":"Pune"},
    {"name":"Nikhil Joshi",         "email":"nikhil.j@email.com",          "skills":["iOS","Swift","Objective-C","CoreData"],           "experience":4, "education":"B.Tech CSE, VJTI Mumbai",         "linkedin":"linkedin.com/in/nikhil-joshi",      "location":"Mumbai"},
    {"name":"Megha Sharma",         "email":"megha.sh@email.com",          "skills":["QA","Selenium","JIRA","Agile"],                   "experience":3, "education":"B.Tech CSE, Pune University",     "linkedin":"linkedin.com/in/megha-sharma",      "location":"Pune"},
    {"name":"Abhishek Das",         "email":"abhi.das@email.com",          "skills":["Blockchain","Solidity","Web3","Ethereum"],        "experience":3, "education":"B.Tech ECE, IIT BHU",             "linkedin":"linkedin.com/in/abhishek-das",      "location":"Bangalore"},
    {"name":"Isha Gupta",           "email":"isha.g@email.com",            "skills":["ML","Scikit-learn","Pandas","NumPy"],             "experience":2, "education":"M.Sc Statistics, Delhi University","linkedin":"linkedin.com/in/isha-gupta",        "location":"Delhi"},
    {"name":"Ravi Shankar",         "email":"ravi.sh@email.com",           "skills":["PHP","Laravel","MySQL","jQuery"],                 "experience":5, "education":"BCA, Bangalore University",       "linkedin":"linkedin.com/in/ravi-shankar",      "location":"Bangalore"},
    {"name":"Tanvi Desai",          "email":"tanvi.d@email.com",           "skills":["Product Management","Agile","JIRA","OKRs"],       "experience":4, "education":"MBA, IIM Ahmedabad",              "linkedin":"linkedin.com/in/tanvi-desai",       "location":"Ahmedabad"},
    {"name":"Manish Kumar",         "email":"manish.k@email.com",          "skills":["C#",".NET","Azure","SQL Server"],                 "experience":6, "education":"B.Tech CS, VIT Vellore",          "linkedin":"linkedin.com/in/manish-kumar",      "location":"Hyderabad"},
    {"name":"Shreya Pillai",        "email":"shreya.p@email.com",          "skills":["Data Engineering","Airflow","dbt","BigQuery"],    "experience":3, "education":"B.Tech IT, COEP Pune",            "linkedin":"linkedin.com/in/shreya-pillai",     "location":"Pune"},
    {"name":"Kartik Bose",          "email":"kartik.b@email.com",          "skills":["Golang","Microservices","gRPC","Redis"],          "experience":4, "education":"B.Tech CS, Jadavpur University",  "linkedin":"linkedin.com/in/kartik-bose",       "location":"Kolkata"},
    {"name":"Anita Rao",            "email":"anita.r@email.com",           "skills":["SAP","ERP","Business Analysis","SQL"],            "experience":7, "education":"MBA, Symbiosis Pune",             "linkedin":"linkedin.com/in/anita-rao",         "location":"Pune"},
    {"name":"Deepak Nanda",         "email":"deepak.n@email.com",          "skills":["Rust","Systems Programming","LLVM","C"],          "experience":5, "education":"B.Tech CS, IIT Madras",           "linkedin":"linkedin.com/in/deepak-nanda",      "location":"Chennai"},
    {"name":"Sonal Trivedi",        "email":"sonal.t@email.com",           "skills":["Digital Marketing","SEO","Google Ads","CRM"],     "experience":3, "education":"BBA Marketing, Mumbai University", "linkedin":"linkedin.com/in/sonal-trivedi",     "location":"Mumbai"},
    {"name":"Varun Malhotra",       "email":"varun.m@email.com",           "skills":["Unity","C#","AR/VR","Game Dev"],                  "experience":3, "education":"B.Tech CS, Manipal University",   "linkedin":"linkedin.com/in/varun-malhotra",    "location":"Bangalore"},
    {"name":"Preeti Agarwal",       "email":"preeti.a@email.com",          "skills":["HR Tech","Workday","Recruiting","Analytics"],     "experience":5, "education":"MBA HR, XLRI Jamshedpur",         "linkedin":"linkedin.com/in/preeti-agarwal",    "location":"Delhi"},
    {"name":"Suresh Babu",          "email":"suresh.b@email.com",          "skills":["Network","CCNA","Linux","Security"],              "experience":4, "education":"B.Tech ECE, SRM Chennai",         "linkedin":"linkedin.com/in/suresh-babu",       "location":"Chennai"},
    {"name":"Ritu Verma",           "email":"ritu.v@email.com",            "skills":["Python","OpenCV","Computer Vision","YOLO"],       "experience":3, "education":"M.Tech AI, IIT Roorkee",          "linkedin":"linkedin.com/in/ritu-verma",        "location":"Roorkee"},
    {"name":"Harsh Vardhan",        "email":"harsh.v@email.com",           "skills":["React Native","JavaScript","Redux","APIs"],        "experience":3, "education":"B.Tech CS, LPU Punjab",           "linkedin":"linkedin.com/in/harsh-vardhan",     "location":"Chandigarh"},
    {"name":"Nalini Subramanian",   "email":"nalini.s@email.com",          "skills":["Embedded C","RTOS","ARM","IoT"],                  "experience":4, "education":"B.Tech ECE, PSG Coimbatore",      "linkedin":"linkedin.com/in/nalini-s",          "location":"Coimbatore"},
    {"name":"Gaurav Tiwari",        "email":"gaurav.t@email.com",          "skills":["MLOps","Kubeflow","MLflow","Docker"],             "experience":4, "education":"M.Tech CS, IIT Guwahati",         "linkedin":"linkedin.com/in/gaurav-tiwari",     "location":"Guwahati"},
    {"name":"Swathi Krishna",       "email":"swathi.k@email.com",          "skills":["Tableau","Power BI","SQL","Excel"],               "experience":2, "education":"B.Com, Bangalore University",     "linkedin":"linkedin.com/in/swathi-k",          "location":"Bangalore"},
    {"name":"Mohit Saxena",         "email":"mohit.s@email.com",           "skills":["Penetration Testing","Kali","OWASP","CTF"],       "experience":3, "education":"B.Tech CS, DTU Delhi",            "linkedin":"linkedin.com/in/mohit-saxena",      "location":"Delhi"},
    {"name":"Lavanya Nair",         "email":"lavanya.n@email.com",         "skills":["Flutter","Dart","Firebase","BLoC"],               "experience":2, "education":"B.Tech CS, TKM Kollam",           "linkedin":"linkedin.com/in/lavanya-nair",      "location":"Kochi"},
    {"name":"Pankaj Dubey",         "email":"pankaj.d@email.com",          "skills":["Salesforce","CRM","Apex","Visualforce"],          "experience":5, "education":"BCA, Lucknow University",         "linkedin":"linkedin.com/in/pankaj-dubey",      "location":"Lucknow"},
    {"name":"Archana Pillai",       "email":"archana.p@email.com",         "skills":["Technical Writing","API Docs","DITA","XML"],      "experience":4, "education":"M.A English, Kerala University",  "linkedin":"linkedin.com/in/archana-pillai",    "location":"Trivandrum"},
    {"name":"Yash Mehrotra",        "email":"yash.me@email.com",           "skills":["Hadoop","Hive","Pig","Spark"],                    "experience":3, "education":"B.Tech IT, HBTU Kanpur",          "linkedin":"linkedin.com/in/yash-mehrotra",     "location":"Kanpur"},
    {"name":"Preethi Sundaram",     "email":"preethi.su@email.com",        "skills":["Python","LangChain","LLM","RAG"],                 "experience":2, "education":"M.Tech AI, IIT Bombay",           "linkedin":"linkedin.com/in/preethi-s",         "location":"Mumbai"},
    {"name":"Rahul Choudhary",      "email":"rahul.ch@email.com",          "skills":["Java","Android","Firebase","SQLite"],             "experience":4, "education":"B.Tech CS, MNIT Jaipur",          "linkedin":"linkedin.com/in/rahul-ch",          "location":"Jaipur"},
    {"name":"Smita Kulkarni",       "email":"smita.k@email.com",           "skills":["Selenium","Cypress","TestNG","BDD"],              "experience":3, "education":"B.Tech IT, Pune University",      "linkedin":"linkedin.com/in/smita-k",           "location":"Pune"},
    {"name":"Dev Anand",            "email":"dev.a@email.com",             "skills":["Redis","Cassandra","MongoDB","ElasticSearch"],     "experience":5, "education":"B.Tech CS, Amrita Coimbatore",   "linkedin":"linkedin.com/in/dev-anand",         "location":"Coimbatore"},
    {"name":"Meenakshi Rajan",      "email":"meena.r@email.com",           "skills":["NLP","BERT","Transformers","HuggingFace"],        "experience":3, "education":"M.Tech AI, IIIT Hyderabad",       "linkedin":"linkedin.com/in/meena-rajan",       "location":"Hyderabad"},
    {"name":"Tarun Bhatt",          "email":"tarun.b@email.com",           "skills":["CI/CD","Jenkins","GitHub Actions","Ansible"],     "experience":4, "education":"B.Tech CS, Thapar University",   "linkedin":"linkedin.com/in/tarun-bhatt",       "location":"Patiala"},
    {"name":"Nisha Chatterjee",     "email":"nisha.c@email.com",           "skills":["Finance","Python","Quant","Bloomberg"],           "experience":3, "education":"M.Sc Finance, IIM Calcutta",      "linkedin":"linkedin.com/in/nisha-c",           "location":"Kolkata"},
    {"name":"Vivek Pandey",         "email":"vivek.p@email.com",           "skills":["Kubernetes","Helm","Service Mesh","AWS EKS"],     "experience":6, "education":"B.Tech CS, BHU Varanasi",         "linkedin":"linkedin.com/in/vivek-pandey",      "location":"Varanasi"},
    {"name":"Ritika Saxena",        "email":"ritika.s@email.com",          "skills":["Python","FastAPI","PostgreSQL","Docker"],         "experience":3, "education":"B.Tech CS, IIIT Allahabad",       "linkedin":"linkedin.com/in/ritika-s",          "location":"Allahabad"},
    {"name":"Sameer Khan",          "email":"sameer.k@email.com",          "skills":["Machine Learning","PyTorch","OpenAI","LLM"],      "experience":4, "education":"M.Tech AI, IIT Bombay",           "linkedin":"linkedin.com/in/sameer-khan",       "location":"Mumbai"},
    {"name":"Deepika Rao",          "email":"deepika.r@email.com",         "skills":["Angular","TypeScript","RxJS","Material UI"],      "experience":3, "education":"B.Tech IT, PES Bangalore",        "linkedin":"linkedin.com/in/deepika-rao",       "location":"Bangalore"},
    {"name":"Amit Tiwari",          "email":"amit.t@email.com",            "skills":["DevOps","Kubernetes","Jenkins","Prometheus"],     "experience":5, "education":"B.Tech CS, NIT Bhopal",           "linkedin":"linkedin.com/in/amit-tiwari",       "location":"Bhopal"},
    {"name":"Shruti Verma",         "email":"shruti.v@email.com",          "skills":["Data Science","R","SAS","Stata"],                 "experience":3, "education":"M.Sc Statistics, IIT Kanpur",     "linkedin":"linkedin.com/in/shruti-verma",      "location":"Kanpur"},
    {"name":"Pranav Joshi",         "email":"pranav.j@email.com",          "skills":["Java","Microservices","Spring","Kafka"],          "experience":5, "education":"B.Tech CS, DAIICT Gandhinagar",   "linkedin":"linkedin.com/in/pranav-joshi",      "location":"Gandhinagar"},
    {"name":"Ankita Singh",         "email":"ankita.s@email.com",          "skills":["Content Writing","SEO","WordPress","Copywriting"],"experience":2, "education":"B.A English, DU Delhi",           "linkedin":"linkedin.com/in/ankita-singh",      "location":"Delhi"},
    {"name":"Rohit Mishra",         "email":"rohit.m@email.com",           "skills":["Python","Airflow","Spark","Databricks"],          "experience":4, "education":"B.Tech CS, NIT Raipur",           "linkedin":"linkedin.com/in/rohit-mishra",      "location":"Raipur"},
    {"name":"Nandini Krishnan",     "email":"nandini.k@email.com",         "skills":["UX Research","Wireframing","Figma","Usability"],  "experience":3, "education":"M.Des, IIT Bombay",              "linkedin":"linkedin.com/in/nandini-k",         "location":"Mumbai"},
    {"name":"Akash Gupta",          "email":"akash.g@email.com",           "skills":["Go","gRPC","Docker","Kubernetes"],                "experience":4, "education":"B.Tech CS, IIT Roorkee",          "linkedin":"linkedin.com/in/akash-gupta",       "location":"Roorkee"},
    {"name":"Shalini Menon",        "email":"shalini.m@email.com",         "skills":["Tableau","SQL","Power BI","Excel"],               "experience":2, "education":"BBA, Christ University Bangalore", "linkedin":"linkedin.com/in/shalini-menon",     "location":"Bangalore"},
    {"name":"Rajesh Iyer",          "email":"rajesh.i@email.com",          "skills":["AWS","Lambda","DynamoDB","CloudFormation"],       "experience":6, "education":"B.Tech ECE, College of Engg Pune", "linkedin":"linkedin.com/in/rajesh-iyer",      "location":"Pune"},
    {"name":"Poornima Reddy",       "email":"poornima.r@email.com",        "skills":["Python","TensorFlow","Keras","CNN"],              "experience":3, "education":"M.Tech AI, IIIT Bangalore",       "linkedin":"linkedin.com/in/poornima-r",        "location":"Bangalore"},
    {"name":"Vishal Sharma",        "email":"vishal.sh@email.com",         "skills":["Node.js","GraphQL","MongoDB","Redis"],            "experience":4, "education":"B.Tech CS, Chandigarh University", "linkedin":"linkedin.com/in/vishal-sh",        "location":"Chandigarh"},
    {"name":"Aditi Bhatt",          "email":"aditi.b@email.com",           "skills":["Cybersecurity","Ethical Hacking","CISSP","Kali"], "experience":4, "education":"B.Tech CS, VIT Chennai",          "linkedin":"linkedin.com/in/aditi-bhatt",       "location":"Chennai"},
    {"name":"Sunil Patil",          "email":"sunil.p@email.com",           "skills":["SAP ABAP","SAP HANA","ERP","FICO"],              "experience":7, "education":"B.Tech MCA, Pune University",      "linkedin":"linkedin.com/in/sunil-patil",       "location":"Pune"},
    {"name":"Kavitha Raman",        "email":"kavitha.r@email.com",         "skills":["Java","Hibernate","Spring MVC","Oracle"],         "experience":5, "education":"B.Tech CS, Thiagarajar College",  "linkedin":"linkedin.com/in/kavitha-raman",     "location":"Madurai"},
    {"name":"Nitin Agarwal",        "email":"nitin.a@email.com",           "skills":["Python","OpenAI","LangChain","Vector DB"],        "experience":3, "education":"B.Tech CS, NIT Warangal",         "linkedin":"linkedin.com/in/nitin-agarwal",     "location":"Warangal"},
    {"name":"Swapna Pillai",        "email":"swapna.p@email.com",          "skills":["Marketing Analytics","Google Analytics","CRM","SQL"],"experience":3,"education":"MBA Marketing, IIMK",           "linkedin":"linkedin.com/in/swapna-pillai",     "location":"Kozhikode"},
    {"name":"Dinesh Babu",          "email":"dinesh.b@email.com",          "skills":["C","Embedded Systems","FPGA","VHDL"],             "experience":5, "education":"B.Tech ECE, Anna University",     "linkedin":"linkedin.com/in/dinesh-babu",       "location":"Chennai"},
    {"name":"Pallavi Sharma",       "email":"pallavi.sh@email.com",        "skills":["React","Redux","Jest","Webpack"],                 "experience":3, "education":"B.Tech IT, Symbiosis Pune",       "linkedin":"linkedin.com/in/pallavi-sh",        "location":"Pune"},
    {"name":"Karthik Murali",       "email":"karthik.mu@email.com",        "skills":["Data Engineering","PySpark","Snowflake","AWS"],   "experience":4, "education":"B.Tech CS, CEG Chennai",          "linkedin":"linkedin.com/in/karthik-mu",        "location":"Chennai"},
    {"name":"Bhavna Jain",          "email":"bhavna.j@email.com",          "skills":["HR Analytics","Excel","SAP HR","Recruitment"],    "experience":4, "education":"MBA HR, NMIMS Mumbai",            "linkedin":"linkedin.com/in/bhavna-jain",       "location":"Mumbai"},
    {"name":"Prashanth Nair",       "email":"prashanth.n@email.com",       "skills":["Kotlin","Android","Jetpack Compose","Room DB"],   "experience":3, "education":"B.Tech CS, Model Engg College",   "linkedin":"linkedin.com/in/prashanth-n",       "location":"Kochi"},
    {"name":"Tanya Malhotra",       "email":"tanya.m@email.com",           "skills":["Python","BERT","HuggingFace","NLP"],              "experience":2, "education":"M.Sc AI, Delhi University",       "linkedin":"linkedin.com/in/tanya-m",           "location":"Delhi"},
    {"name":"Girish Kulkarni",      "email":"girish.k@email.com",          "skills":["Terraform","AWS","GCP","Infrastructure as Code"], "experience":6, "education":"B.Tech CS, BITS Pilani",          "linkedin":"linkedin.com/in/girish-k",          "location":"Goa"},
    {"name":"Shilpa Rao",           "email":"shilpa.r@email.com",          "skills":["Business Intelligence","SSRS","SSIS","SQL"],      "experience":5, "education":"B.Tech IT, Manipal University",   "linkedin":"linkedin.com/in/shilpa-rao",        "location":"Mangalore"},
    {"name":"Manoj Tripathi",       "email":"manoj.t@email.com",           "skills":["Java","Apache Kafka","Flink","Storm"],            "experience":6, "education":"B.Tech CS, HBTI Kanpur",          "linkedin":"linkedin.com/in/manoj-t",           "location":"Kanpur"},
    {"name":"Rekha Pillai",         "email":"rekha.p@email.com",           "skills":["Manual Testing","Test Cases","JIRA","TestRail"],  "experience":3, "education":"B.Tech IT, TKM College",          "linkedin":"linkedin.com/in/rekha-pillai",      "location":"Trivandrum"},
    {"name":"Sanjay Mehta",         "email":"sanjay.m@email.com",          "skills":["Python","Pandas","NumPy","Matplotlib"],           "experience":2, "education":"B.Sc Statistics, Mumbai Univ",   "linkedin":"linkedin.com/in/sanjay-mehta",      "location":"Mumbai"},
    {"name":"Chandana Reddy",       "email":"chandana.r@email.com",        "skills":["Full Stack","React","Node.js","PostgreSQL"],      "experience":4, "education":"B.Tech CS, JNTU Hyderabad",       "linkedin":"linkedin.com/in/chandana-r",        "location":"Hyderabad"},
    {"name":"Rajeev Menon",         "email":"rajeev.m@email.com",          "skills":["Cloud Architect","Azure","GCP","Multi-cloud"],    "experience":8, "education":"B.Tech ECE, NIT Calicut",         "linkedin":"linkedin.com/in/rajeev-menon",      "location":"Kochi"},
    {"name":"Sunita Verma",         "email":"sunita.v@email.com",          "skills":["Project Management","PMP","Scrum","Agile"],       "experience":7, "education":"MBA Operations, FMS Delhi",       "linkedin":"linkedin.com/in/sunita-verma",      "location":"Delhi"},
    {"name":"Arjun Pillai",         "email":"arjun.pi@email.com",          "skills":["Swift","iOS","ARKit","CoreML"],                   "experience":4, "education":"B.Tech CS, College of Engg TVM", "linkedin":"linkedin.com/in/arjun-pi",          "location":"Trivandrum"},
    {"name":"Deepa Subramaniam",    "email":"deepa.su@email.com",          "skills":["Data Analysis","Python","Seaborn","Plotly"],      "experience":2, "education":"M.Sc Data Science, Loyola Chennai","linkedin":"linkedin.com/in/deepa-su",         "location":"Chennai"},
    {"name":"Kunal Sharma",         "email":"kunal.sh@email.com",          "skills":["AWS Architect","Solution Design","EC2","RDS"],    "experience":7, "education":"B.Tech CS, IIT Indore",           "linkedin":"linkedin.com/in/kunal-sh",          "location":"Indore"},
    {"name":"Varsha Iyer",          "email":"varsha.i@email.com",          "skills":["Django REST","Python","Celery","RabbitMQ"],       "experience":3, "education":"B.Tech CS, PSG Tech Coimbatore",  "linkedin":"linkedin.com/in/varsha-i",          "location":"Coimbatore"},
    {"name":"Harish Gupta",         "email":"harish.g@email.com",          "skills":["ML Engineer","PyTorch","CUDA","Model Serving"],   "experience":5, "education":"M.Tech CS, IIT Delhi",            "linkedin":"linkedin.com/in/harish-g",          "location":"Delhi"},
    {"name":"Meghna Das",           "email":"meghna.d@email.com",          "skills":["Scrum Master","Agile","Kanban","Jira"],           "experience":4, "education":"MBA IT, Calcutta University",     "linkedin":"linkedin.com/in/meghna-d",          "location":"Kolkata"},
    {"name":"Balaji Krishnan",      "email":"balaji.k@email.com",          "skills":["DevOps","GitLab CI","Helm","Kubernetes"],         "experience":5, "education":"B.Tech ECE, NIT Trichy",          "linkedin":"linkedin.com/in/balaji-k",          "location":"Trichy"},
    {"name":"Simran Kaur",          "email":"simran.k@email.com",          "skills":["Python","Airflow","ETL","Data Warehouse"],        "experience":3, "education":"B.Tech CS, Panjab University",    "linkedin":"linkedin.com/in/simran-k",          "location":"Chandigarh"},
    {"name":"Venkat Raman",         "email":"venkat.r@email.com",          "skills":["Oracle DBA","PL/SQL","RAC","Data Guard"],         "experience":8, "education":"B.Tech CS, Andhra University",   "linkedin":"linkedin.com/in/venkat-r",          "location":"Vizag"},
    {"name":"Priyanka Joshi",       "email":"priyanka.j@email.com",        "skills":["React","Vue.js","CSS3","Tailwind"],               "experience":3, "education":"B.Tech IT, MITS Gwalior",         "linkedin":"linkedin.com/in/priyanka-j",        "location":"Gwalior"},
    {"name":"Arun Kumar",           "email":"arun.k@email.com",            "skills":["Java","Multithreading","JVM","Performance"],      "experience":6, "education":"B.Tech CS, REC Trichy",           "linkedin":"linkedin.com/in/arun-kumar",        "location":"Trichy"},
    {"name":"Geeta Sharma",         "email":"geeta.sh@email.com",          "skills":["Business Analyst","SQL","Requirement Gathering","BPMN"],"experience":5,"education":"MBA Finance, XLRI",          "linkedin":"linkedin.com/in/geeta-sh",          "location":"Delhi"},
    {"name":"Sudarshan Rao",        "email":"sudarshan.r@email.com",       "skills":["Hadoop","Spark","HBase","HDFS"],                  "experience":5, "education":"B.Tech CS, Osmania University",   "linkedin":"linkedin.com/in/sudarshan-r",       "location":"Hyderabad"},
    {"name":"Amrita Singh",         "email":"amrita.s@email.com",          "skills":["Python","Generative AI","Stable Diffusion","GANs"],"experience":2,"education":"M.Tech AI, IIT Hyderabad",       "linkedin":"linkedin.com/in/amrita-s",          "location":"Hyderabad"},
    {"name":"Vikash Sharma",        "email":"vikash.sh@email.com",         "skills":["Power Platform","Power Apps","Power Automate","SharePoint"],"experience":4,"education":"B.Tech CS, Amity Noida","linkedin":"linkedin.com/in/vikash-sh",         "location":"Noida"},
    {"name":"Bhargavi Nair",        "email":"bhargavi.n@email.com",        "skills":["Clinical Data","SAS","R","Biostatistics"],        "experience":4, "education":"M.Sc Biostatistics, CMC Vellore", "linkedin":"linkedin.com/in/bhargavi-n",       "location":"Vellore"},
    {"name":"Srinivas Murthy",      "email":"srinivas.mu@email.com",       "skills":["Mainframe","COBOL","JCL","DB2"],                  "experience":9, "education":"B.Tech CS, Mysore University",    "linkedin":"linkedin.com/in/srinivas-mu",       "location":"Mysore"},
    {"name":"Anjali Mehta",         "email":"anjali.m@email.com",          "skills":["Figma","Adobe XD","Prototyping","Design Systems"],"experience":3, "education":"B.Des, Srishti Bangalore",        "linkedin":"linkedin.com/in/anjali-mehta",      "location":"Bangalore"},
    {"name":"Prakash Reddy",        "email":"prakash.r@email.com",         "skills":["Selenium","Appium","TestNG","API Testing"],       "experience":4, "education":"B.Tech CS, JNTUH",               "linkedin":"linkedin.com/in/prakash-reddy",     "location":"Hyderabad"},
    {"name":"Roshni Kapoor",        "email":"roshni.k@email.com",          "skills":["Python","CrewAI","LangChain","Agentic AI"],       "experience":2, "education":"M.Tech AI, IIT Madras",           "linkedin":"linkedin.com/in/roshni-k",          "location":"Chennai"},
    {"name":"Gopal Krishna",        "email":"gopal.k@email.com",           "skills":["GCP","BigQuery","Dataflow","Pub/Sub"],            "experience":5, "education":"B.Tech CS, NIT Karnataka",        "linkedin":"linkedin.com/in/gopal-k",           "location":"Surathkal"},
    {"name":"Lakshmi Devi",         "email":"lakshmi.d@email.com",         "skills":["Finance","Tally","GST","Accounting"],             "experience":4, "education":"B.Com, Osmania University",       "linkedin":"linkedin.com/in/lakshmi-d",         "location":"Hyderabad"},
    {"name":"Rohit Nair",           "email":"rohit.n@email.com",           "skills":["Prompt Engineering","GPT-4","RAG","Vector DB"],   "experience":2, "education":"B.Tech CS, CUSAT Kochi",          "linkedin":"linkedin.com/in/rohit-nair",        "location":"Kochi"},
    {"name":"Madhuri Patil",        "email":"madhuri.p@email.com",         "skills":["Operations","Supply Chain","ERP","Six Sigma"],    "experience":6, "education":"MBA Operations, SIBM Pune",       "linkedin":"linkedin.com/in/madhuri-patil",     "location":"Pune"},
    {"name":"Ajay Verma",           "email":"ajay.v@email.com",            "skills":["Python","ML","XGBoost","Feature Engineering"],   "experience":3, "education":"B.Tech CS, NIT Allahabad",        "linkedin":"linkedin.com/in/ajay-verma",        "location":"Allahabad"},
    {"name":"Sudha Raman",          "email":"sudha.r@email.com",           "skills":["Java","Apache Spark","Scala","Hive"],             "experience":5, "education":"B.Tech CS, Bharathiar University", "linkedin":"linkedin.com/in/sudha-raman",      "location":"Coimbatore"},
    {"name":"Nikhil Rao",           "email":"nikhil.r@email.com",          "skills":["Rust","WebAssembly","Systems","Low Latency"],     "experience":4, "education":"B.Tech CS, IIT Kharagpur",        "linkedin":"linkedin.com/in/nikhil-rao",        "location":"Kolkata"},
    {"name":"Divyanka Sharma",      "email":"divyanka.s@email.com",        "skills":["Interior Design","AutoCAD","SketchUp","3ds Max"],  "experience":3, "education":"B.Des Interior, CEPT Ahmedabad", "linkedin":"linkedin.com/in/divyanka-s",        "location":"Ahmedabad"},
]

JOB_PLATFORMS = ["LinkedIn","Naukri.com","Indeed","GitHub Jobs","AngelList","Internshala","Glassdoor","Dice"]


def get_chroma_collection():
    """
    Initialize ChromaDB with HuggingFace sentence-transformers embeddings.
    Uses all-MiniLM-L6-v2 model from HuggingFace for semantic search.
    """
    client = chromadb.Client()

    ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    collection = client.get_or_create_collection(
        name="candidates",
        embedding_function=ef
    )

    for i, c in enumerate(MOCK_CANDIDATES):
        doc = (
            f"{c['name']} has {c['experience']} years experience. "
            f"Skills: {', '.join(c['skills'])}. "
            f"Education: {c['education']}"
        )
        safe_metadata = {
            "name":       c["name"],
            "email":      c["email"],
            "skills":     ", ".join(c["skills"]),
            "experience": c["experience"],
            "education":  c["education"],
            "linkedin":   c["linkedin"],
            "location":   c.get("location", "India"),
        }
        collection.add(
            documents=[doc],
            ids=[f"candidate_{i}"],
            metadatas=[safe_metadata]
        )
    return collection


def search_candidates(collection, query, n=6):
    """Semantic search using HuggingFace embeddings via ChromaDB."""
    return collection.query(query_texts=[query], n_results=n)