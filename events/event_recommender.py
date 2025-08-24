from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn

# Download NLTK data (first run only)
nltk.download("punkt")
nltk.download("wordnet")
nltk.download("omw-1.4")

lemmatizer = WordNetLemmatizer()

def normalize(text):
    tokens = re.findall(r"[a-z]+", text.lower())
    return [lemmatizer.lemmatize(t) for t in tokens]

# --------------------------
# 🔹 Query Expansion
# --------------------------
custom_synonyms = {
    "code": ["program", "software", "develop", "script", "python", "java"],
    "robot": ["robotics", "automation", "machine"],
    "game": ["gaming", "play", "video", "design"],
    "speech": ["talk", "presentation", "debate"],
    "build": ["construct", "design", "engineer"],
}

def expand_word(word):
    synonyms = {word}
    if word in custom_synonyms:
        synonyms.update(custom_synonyms[word])
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().replace("_"," "))
    return list(synonyms)

def expand_query(query):
    expanded = []
    for t in normalize(query):
        expanded.extend(expand_word(t))
    return " ".join(expanded)

events = [
    {"name": "Animatronics", "tags": ["robotics", "engineering", "design"], "desc": "To address the annual design challenge, participants exhibit and demonstrate their knowledge of mechanical and control systems by creating an animatronic device with a specific purpose (i.e., communicate an idea, entertain, demonstrate a concept, etc.) that includes sound, lights, and an appropriate surrounding environment (a display)."},
    {"name": "Architectural Design", "tags": ["architecture", "design", "modeling"], "desc": "In response to the annual design challenge, participants develop a set of architectural plans and related materials, and construct both a physical and computer-generated model to accurately depict their design. Semifinalists deliver a presentation and participate in an interview."},
    {"name": "Audio Podcasting", "tags": ["media", "communication", "audio"], "desc": "Participants use digital audio technology to create original content for a podcast piece that addresses the annual theme. The podcast must feature high level storytelling techniques, voice acting, and folly sound effects; the full entry must include documentation of the podcast development process and elements. Semifinalists participate in an interview."},
    {"name": "Biotechnology Design", "tags": ["biotechnology", "science", "innovation"], "desc": "Participants select a contemporary biotechnology problem that addresses the annual theme and demonstrates understanding of the topic through documented research, the development of a solution, a display (including an optional model or prototype), and an effective multimedia presentation. Semifinalists deliver a presentation and participate in an interview."},
    {"name": "Board Game Design", "tags": ["game design", "creativity", "strategy"], "desc": "Participants develop, build, and package a board game that focuses on a subject of their choice. Creative packaging, and the instructions, pieces, and cards associated with the pilot game will be evaluated. Semifinalists set up the game, demonstrate how the game is played, explain the game's features, and discuss the design process."},
    {"name": "Chapter Team", "tags": ["leadership", "teamwork", "presentation"], "desc": "Participants take a parliamentary procedure test to qualify for the semifinal round of competition. Semifinalists conduct an opening ceremony, items of business, parliamentary actions, and a closing ceremony."},
    {"name": "Children's Stories", "tags": ["writing", "literature", "creativity"], "desc": "In response to the annual theme, participants create an illustrated children's story of artistic, instructional, and social value, and submit documentation related to the development of the physical storybook. Semifinalists read their story aloud and participate in an interview."},
    {"name": "Coding", "tags": ["programming", "software", "technology"], "desc": "Participants take a test, which concentrates on aspects of coding, to qualify for the semifinal round of competition. Semifinalists develop a software program - in a designated amount of time - that accurately addresses an onsite problem."},
    {"name": "Computer-Aided Design (CAD), Architecture", "tags": ["CAD", "architecture", "design"], "desc": "Participants use complex computer graphic skills, tools, and processes to respond to a design challenge in which they develop representations of architectural subjects, such as foundation and/or floor plans, and/or elevation drawings, and/or details of architectural ornamentation or cabinetry. The solution to the design challenge and participant answers in an interview are evaluated."},
    {"name": "Computer-Aided Design (CAD), Engineering", "tags": ["CAD", "engineering", "design"], "desc": "Participants use complex computer graphic skills, tools, and processes to respond to a design challenge in which they develop three-dimensional representations of engineering subjects, such as a machine part, tool, device, or manufactured product. The solution to the design challenge and participant answers in an interview are evaluated."},
    {"name": "Data Science and Analytics", "tags": ["data", "analysis", "statistics"], "desc": "Participants identify a societal issue, collect or compile data from various sources about the issue, and then produce documentation and a digital scientific poster about their findings. Semifinalists create a synopsis and digital visual representation of a data set provided in an onsite challenge."},
    {"name": "Debating Technological Issues", "tags": ["debate", "technology", "communication"], "desc": "Participants research the annual topic and subtopics and prepare for a debate against a team from another chapter. Teams are instructed to take either the pro or con side of a selected subtopic, submit a summary of references, and use their research to support their assigned position. The quality of a team's debate determines semifinalists and finalists."},
    {"name": "Digital Video Production", "tags": ["media", "video", "production"], "desc": "Participants develop and submit a digital video and a documentation portfolio (including such items as a storyboard, script, summary of references and sources, and equipment list) that reflects the annual theme. Semifinalists participate in an interview."},
    {"name": "Dragster Design", "tags": ["engineering", "design", "speed"], "desc": "Participants design, draw, and construct a CO2-powered dragster that adheres to specifications, design and documentation requirements, and the annual theme. Semifinalists compete in a double-elimination race and participate in an interview."},
    {"name": "Drone Challenge (UAV)", "tags": ["drone", "technology", "flight"], "desc": "Participants design, build, assemble, document, and test fly an open-source Unmanned Arial Vehicle (UAV) according to the stated annual theme/problem specifications. The required documentation portfolio must include elements such as a photographic log, wiring schematics, and a description of the programming software used. Semifinalists participate in an interview."},
    {"name": "Engineering Design", "tags": ["engineering", "design", "innovation"], "desc": "Participants develop a solution to an annual theme that is based on a specific challenge noted by the National Academy of Engineering (NAE) in its compilation of the grand challenges for engineering in the 21st century. The solution will include a documentation portfolio, a display, and a model/prototype. Semifinalists deliver a presentation and participate in an interview."},
    {"name": "Extemporaneous Speech", "tags": ["public speaking", "communication", "impromptu"], "desc": "Participants select a technology-related or TSA topic from among three topic cards and prepare and give a three-to-five-minute speech that communicates their knowledge of the chosen topic. The quality of the speech determines advancement to the semifinalist level of competition, for which an identical competition procedure is followed to determine finalists."},
    {"name": "Fashion Design and Technology", "tags": ["fashion", "design", "technology"], "desc": "To address the annual theme, participants demonstrate expertise in fashion design principles by creating a wearable garment, garment patterns, and a documentation portfolio. Semifinalist teams present their garment designs (worn by team models), discuss the design process with evaluators, and respond to interview questions."},
    {"name": "Flight Endurance", "tags": ["engineering", "flight", "design"], "desc": "Participants design, build, fly, and adjust (trim) a rubber-band powered model aircraft to make long endurance flights inside a contained airspace. Documentation (including elements such as attributes of the model design, drawings, and an analysis of the trim modifications), an inspection of the model and the required model flight box, and official times for two flights are aspects of the evaluation"},
    {"name": "Forensic Science", "tags": ["science", "investigation", "analysis"], "desc": "Participants take a test of basic forensic science to qualify for the semifinal round of competition. Semifinalists examine a mock crime scene and demonstrate their knowledge of forensic science through crime scene analysis, with the findings synthesized in a written report/analysis."},
    {"name": "Future Technology Teacher", "tags": ["education", "technology", "presentation"], "desc": "Participants research a developing technology, prepare a video showing an application of the technology in the classroom, and create a lesson plan/activity that features the application and connects to the Standards for Technological and Engineering Literacy (STEL), as well as STEM initiatives and integration. Semifinalists demonstrate the lesson plan and answer questions about their presentation."},
    {"name": "Geospatial Technology", "tags": ["geography", "technology", "mapping"], "desc": "To address the issue presented in an annual theme, participants interpret geospatial data and develop a digital portfolio containing maps, data, and pertinent documentation. Semifinalists defend their projections and visual infographic during a presentation/interview."},
    {"name": "Manufacturing Prototype", "tags": ["manufacturing", "design", "prototype"], "desc": "Participants design, fabricate, and use Computer Integrated Manufacturing (CIM) to create a product that addresses the annual theme. A documentation portfolio and the completed product prototype are submitted for evaluation. Semifinalists give a product “sales pitch” and demonstration."},
    {"name": "Music Production", "tags": ["music", "production", "audio"], "desc": "Participants produce an original musical piece that reﬂects the annual theme on the TSA website under Themes & Problems. The quality of the musical piece and required documentation (including elements such as a plan of work, self-evaluation, and a list of hardware, software, and instruments used) determines advancement to the semifinal level of competition, during which semifinalist participants are interviewed."},
    {"name": "On Demand Video", "tags": ["media", "video", "production"], "desc": "Once participants receive the challenge details (required criteria, such as props and a line of dialogue) at the national TSA conference, they have 36 hours to produce a 60-second film that showcases video skills, tools, and communication processes. The quality of the completed video production determines the finalists."},
    {"name": "Photographic Technology", "tags": ["photography", "technology", "media"], "desc": "Participants produce a photographic portfolio - demonstrating expertise in photo and imaging technology processes - to convey a message based on the annual theme. Semifinalists have 24 hours to complete a portfolio of photos (with required documentation) taken onsite at the national TSA conference. Finalists are determined based on the quality of the semifinal portfolio, the portfolio presentation, and interview responses."},
    {"name": "Prepared Presentation", "tags": ["public speaking", "communication", "presentation"], "desc": "Participants deliver a three-to-five-minute oral presentation related to the current national TSA conference theme. Both semifinalists and finalists are determined based on the quality of the presentation and the appropriate use and content of the accompanying required slide deck."},
    {"name": "Promotional Design", "tags": ["design", "marketing", "creativity"], "desc": "Participants use computerized graphic communications layout and design skills to produce a promotional resource packet. The resource must address the annual theme/problem and include at least four printed publication items and required documentation. Semifinalists demonstrate publishing competency in an onsite technical design challenge."},
    {"name": "Robotics", "tags": ["robotics", "engineering", "technology"], "desc": "Participants design, build, document, and test a robot assembled using open-sourced parts according to stated specifications and to meet the challenge of the yearly theme/problem. "},
    {"name": "Senior Solar Sprint", "tags": ["engineering", "energy", "design"], "desc": "Students apply scientific understanding, creativity, experimentation, and teamwork to design, build, and race a model solar vehicle that carries a payload. Documentation of the process is required."},
    {"name": "Software Development", "tags": ["programming", "software", "technology"], "desc": "Participants use their knowledge of cutting-edge technologies, algorithm design, problem-solving principles, effective communication, and collaboration to design, implement, test, document, and present a software development project of educational or social value. Both semifinalists and finalists are determined based on the quality of the presentation and project."},
    {"name": "STEM Mass Media", "tags": ["media", "STEM", "communication"], "desc": "In response to an annual theme, participants use written and verbal communication skills to convey a news story in both a video broadcast (preliminary round) and a digital written format (semifinal round). Participants must demonstrate a strong understanding of journalism etiquette and the common practices of the field of mass media."},
    {"name": "Structural Design and Engineering", "tags": ["engineering", "design", "construction"], "desc": "Participants apply the principles of structural engineering to design and construct a structure that complies with the annual challenge. An assessment of the required documentation and the destructive testing of the structure (to determine its design efficiency) determine both semifinalists and finalists."},
    {"name": "System Control Technology", "tags": ["technology", "automation", "engineering"], "desc": "Participants develop a solution to a problem (typically one from an industrial setting) presented onsite at the conference. They analyze the problem, build a computer-controlled mechanical model, program the model, demonstrate the programming and mechanical features of the model-solution in an interview, and provide instructions for evaluators to operate the model."},
    {"name": "Technology Bowl", "tags": ["knowledge", "technology", "competition"], "desc": "Participants demonstrate their knowledge of TSA and concepts addressed in technology content standards by completing an objective test. Semifinalist teams participate in a question/response, head-to-head, team competition."},
    {"name": "Technology Problem Solving", "tags": ["problem-solving", "technology", "innovation"], "desc": "Participants use problem-solving skills to design and construct a finite solution to a challenge provided onsite at the conference. Solutions are evaluated at the end of 90 minutes using measures appropriate to the challenge, such as elapsed time, horizontal or vertical distance, and/or strength."},
    {"name": "Transportation Modeling", "tags": ["transportation", "engineering", "modeling"], "desc": "Participants research, design, and produce a scale model of a vehicle that complies with the annual design problem. A display for the model and a documentation portfolio - containing elements such as a description of the vehicle, photographs and commentary detailing the vehicle production, and technical illustrations - are required. Semifinalists participate in an interview."},
    {"name": "Video Game Design", "tags": ["game design", "programming", "creativity"], "desc": "Participants design, build, and launch an E-rated online video game - with accompanying required documentation - that addresses the annual theme. Semifinalists participate in an interview to demonstrate the knowledge and expertise they gained during the development of the game."},
    {"name": "Virtual Reality Simulation (VR)", "tags": ["virtual reality", "technology", "simulation"], "desc": "Participants use video and 3D computer graphics tools and design processes to create a two-to-three-minute VR visualization (accompanied by supporting documentation) that addresses the annual theme. Semifinalists deliver a presentation about their visualization and participate in an interview."},
    {"name": "Webmaster", "tags": ["web development", "programming", "design"], "desc": "Participants design, build, and launch a website that addresses the annual challenge. Semifinalists participate in an interview to demonstrate the knowledge and expertise gained during the development of the website."}
]

custom_synonyms = {
    "code": ["program", "software", "develop", "script", "python", "java"],
    "robot": ["robotics", "automation", "machine"],
    "game": ["gaming", "play", "video", "design"],
    "speech": ["speak", "talk", "presentation", "lecture", "debate", "orate"]
}

# Skill Map (domain knowledge)
skill_map = {
    "programming": [
        "Coding",
        "Software Development",
        "Video Game Design",
        "Webmaster",
        "Virtual Reality Simulation (VR)",
        "STEM Mass Media"
    ],
    "robotics": [
        "Robotics",
        "Animatronics",
        "Drone Challenge (UAV)",
        "System Control Technology"
    ],
    "design": [
        "Architectural Design",
        "Computer-Aided Design (CAD), Architecture",
        "Computer-Aided Design (CAD), Engineering",
        "Promotional Design",
        "Board Game Design",
        "Fashion Design and Technology",
        "Transportation Modeling",
        "Structural Design and Engineering"
    ],
    "media": [
        "Digital Video Production",
        "Audio Podcasting",
        "On Demand Video",
        "STEM Mass Media",
        "Music Production"
    ],
    "presentation": [
        "Prepared Presentation",
        "Extemporaneous Speech",
        "Debating Technological Issues",
        "Chapter Team"
    ],
    "writing": [
        "Children's Stories",
        "Audio Podcasting",
        "STEM Mass Media"
    ],
    "engineering": [
        "Engineering Design",
        "Manufacturing Prototype",
        "Senior Solar Sprint",
        "Flight Endurance",
        "Forensic Science",
        "Biotechnology Design",
        "Geospatial Technology",
        "Data Science and Analytics"
    ],
    "science": [
        "Biotechnology Design",
        "Forensic Science",
        "Data Science and Analytics",
        "Geospatial Technology"
    ],
    "technical knowledge": [
        "Technology Bowl",
        "Technology Problem Solving",
        "Coding",
        "Forensic Science",
        "Biotechnology Design"
    ]
}

# Event Preprocessing
def parse_event(e):
    name = " ".join(normalize(e["name"]))
    desc = " ".join(normalize(e["desc"]))
    tags = " ".join(normalize(" ".join(e["tags"])))
    # Weight: tags *4, name *2, desc *1
    boosted = (name + " ") * 2 + desc + " " + (tags + " ") * 4
    return boosted.strip()

event_texts = [parse_event(e) for e in events]

# Model
vectorizer = TfidfVectorizer(ngram_range=(1,3), min_df=1, stop_words="english")
event_matrix = vectorizer.fit_transform(event_texts)

# Scoring Helpers
def jaccard(a, b):
    return len(a & b) / len(a | b) if (a|b) else 0

def combined_score(prompt, event_text, tfidf_score):
    q_tokens = set(normalize(prompt))
    e_tokens = set(normalize(event_text))
    overlap = jaccard(q_tokens, e_tokens)
    return 0.8*tfidf_score + 0.2*overlap

def apply_hard_boosts(prompt, scores):
    p = prompt.lower()
    # programming boost
    if any(w in p for w in ["code","coding","program","python"]):
        scores["Coding"] = scores.get("Coding",0) + 0.3
        scores["Software Development"] = scores.get("Software Development",0) + 0.2
    # robotics boost
    if "robot" in p:
        scores["Robotics"] = scores.get("Robotics",0) + 0.3
    # presentation boost
    if any(w in p for w in ["speak","speech","present","talk","lecture","debate"]):
        for ev in ["Prepared Presentation","Extemporaneous Speech","Debating Technological Issues","Chapter Team"]:
            scores[ev] = scores.get(ev,0) + 0.3

def apply_skill_map(prompt, scores):
    for skill, evs in skill_map.items():
        if skill in prompt.lower():
            for e in evs:
                scores[e] = scores.get(e,0) + 0.1

def get_event_description(event_name):
    for event in events:
        if event["name"] != event_name: continue
        return event["desc"]

# def rank_events(prompt):
#     q_expanded = expand_query(prompt)
#     q_vec = vectorizer.transform([q_expanded])
#     tfidf_scores = cosine_similarity(q_vec, event_matrix)[0]

#     scores = {}
#     for e, tfidf in zip(events, tfidf_scores):
#         base_score = combined_score(q_expanded, parse_event(e), tfidf)
#         scores[e["name"]] = base_score

#     # Apply domain boosts
#     apply_hard_boosts(prompt, scores)
#     apply_skill_map(prompt, scores)

#     ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

#     return ranked

def rank_events(prompt):
    # Normalize and expand query
    q_expanded = expand_query(prompt)
    q_vec = vectorizer.transform([q_expanded])
    tfidf_scores = cosine_similarity(q_vec, event_matrix)[0]

    # Initialize score dictionary
    scores = {}
    for e, tfidf in zip(events, tfidf_scores):
        base_score = combined_score(q_expanded, parse_event(e), tfidf)
        scores[e["name"]] = base_score

    # Split prompt into “interests” for multi-interest boosting
    prompt_tokens = set(normalize(prompt))
    
    # --- Multi-interest hard boosts ---
    # Programming-related words
    programming_words = {"code","coding","program","python","software","develop","script","java"}
    if prompt_tokens & programming_words:
        for ev in ["Coding","Software Development","Video Game Design","Webmaster","Virtual Reality Simulation (VR)"]:
            scores[ev] = scores.get(ev,0) + 0.3

    # Robotics-related words
    robotics_words = {"robot","automation","mechanical","drone"}
    if prompt_tokens & robotics_words:
        for ev in ["Robotics","Animatronics","Drone Challenge (UAV)","System Control Technology"]:
            scores[ev] = scores.get(ev,0) + 0.3

    # Presentation-related words
    presentation_words = {"speak","speech","present","talk","lecture","debate","orate"}
    if prompt_tokens & presentation_words:
        for ev in ["Prepared Presentation","Extemporaneous Speech","Debating Technological Issues","Chapter Team"]:
            scores[ev] = scores.get(ev,0) + 0.3

    # Media-related words
    media_words = {"video","music","audio","podcast","film","photograph","media"}
    if prompt_tokens & media_words:
        for ev in ["Digital Video Production","Audio Podcasting","On Demand Video","STEM Mass Media","Music Production","Photographic Technology"]:
            scores[ev] = scores.get(ev,0) + 0.3

    # Design/engineering words
    design_words = {"design","engineering","construct","model","build","architecture","fashion","game"}
    if prompt_tokens & design_words:
        for ev in ["Architectural Design","Computer-Aided Design (CAD), Architecture","Computer-Aided Design (CAD), Engineering",
                   "Promotional Design","Board Game Design","Fashion Design and Technology","Transportation Modeling","Structural Design and Engineering",
                   "Engineering Design","Manufacturing Prototype","Senior Solar Sprint","Flight Endurance"]:
            scores[ev] = scores.get(ev,0) + 0.2

    # Apply skill_map boosts
    apply_skill_map(prompt, scores)

    # Rank events
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    return ranked
