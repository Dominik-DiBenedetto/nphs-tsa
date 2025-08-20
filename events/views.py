import json, traceback
from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, Http404, HttpResponse
from sentence_transformers import SentenceTransformer, util
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.decorators import user_passes_test

from .models import Event

event_descs = [
    "Animatronics: To address the annual design challenge, participants exhibit and demonstrate their knowledge of mechanical and control systems by creating an animatronic device with a specific purpose (i.e., communicate an idea, entertain, demonstrate a concept, etc.) that includes sound, lights, and an appropriate surrounding environment (a display). [programming, electrical, engineering, mechanical, robot, coding, electronics, hardware] Following the specified requirements, create an animatronic exhibit for a public library to excite young readers.",
    "Architectural Design: In response to the annual design challenge, participants develop a set of architectural plans and related materials, and construct both a physical and computer-generated model to accurately depict their design. Semifinalists deliver a presentation and participate in an interview. [construction, interior design] select a type and location for a museum of the team's choice and then design a museum that meets the following considerations and constraints.",
    "Audio Podcasting: Participants use digital audio technology to create original content for a podcast piece that addresses the annual theme. The podcast must feature high level storytelling techniques, voice acting, and folly sound effects; the full entry must include documentation of the podcast development process and elements. Semifinalists participate in an interview. [spotify, music, podcasting, audio, talking, funny, show, talkshow] Tissue Engineering. Tissue Engineering is a biomedical engineering discipline that uses a combination of cells, engineering, materials methods, and suitable biochemical and physicochemical factors to restore, maintain, improve, or replace different types of biological tissues.",
    "Biotechnology: Participants select a contemporary biotechnology problem that addresses the annual theme and demonstrates understanding of the topic through documented research, the development of a solution, a display (including an optional model or prototype), and an effective multimedia presentation. Semifinalists deliver a presentation and participate in an interview. [biology, science] Create a “touch and feel” or interactive storybook that introduces TSA and its benefits to young readers in an engaging manner.",
    "Board Game Design: Participants develop, build, and package a board game that focuses on a subject of their choice. Creative packaging, and the instructions, pieces, and cards associated with the pilot game will be evaluated. Semifinalists set up the game, demonstrate how the game is played, explain the game's features, and discuss the design process. [board game, game design, monopoly, creativity]",
    "Chapter Team: Participants take a parliamentary procedure test to qualify for the semifinal round of competition. Semifinalists conduct an opening ceremony, items of business, parliamentary actions, and a closing ceremony. [roberts rules, corporate, business, parliamentary procedure, meetings, leadership, court]",
    "Children's Stories: In response to the annual theme, participants create an illustrated children's story of artistic, instructional, and social value, and submit documentation related to the development of the physical storybook. Semifinalists read their story aloud and participate in an interview. [reading, books, storytelling, writing, poetry, creativity, english, cartoons]",
    "Coding: Participants take a test, which concentrates on aspects of coding, to qualify for the semifinal round of competition. Semifinalists develop a software program - in a designated amount of time - that accurately addresses an onsite problem. [programming, scripting, software engineering, computers, computer design, python]",
    "Computer-Aided Design (CAD), Architecture: Participants use complex computer graphic skills, tools, and processes to respond to a design challenge in which they develop representations of architectural subjects, such as foundation and/or floor plans, and/or elevation drawings, and/or details of architectural ornamentation or cabinetry. The solution to the design challenge and participant answers in an interview are evaluated. [3d modeling, construction, designing]",
    "Computer-Aided Design (CAD), Engineering: Participants use complex computer graphic skills, tools, and processes to respond to a design challenge in which they develop three-dimensional representations of engineering subjects, such as a machine part, tool, device, or manufactured product. The solution to the design challenge and participant answers in an interview are evaluated. [3d modeling, engineering, designing]",
    "Data Science and Analytics: Participants identify a societal issue, collect or compile data from various sources about the issue, and then produce documentation and a digital scientific poster about their findings. Semifinalists create a synopsis and digital visual representation of a data set provided in an onsite challenge. [analyst, numbers, data, science] open-source data set for your analyses and research. In the scientific poster, cite the source of the data, including the URL/domain and file format.",
    "Debating Technological Issues: Participants research the annual topic and subtopics and prepare for a debate against a team from another chapter. Teams are instructed to take either the pro or con side of a selected subtopic, submit a summary of references, and use their research to support their assigned position. The quality of a team's debate determines semifinalists and finalists. [public speaking, arguing, lawyer, court, trial, debating] Biotechnology Subtopic 1: Biometric identification poses a security threat within the digital world. Subtopic 2: Gene-editing biotechnologies such as the CRISPR-Cas9 system, set a dangerous precedent for science applications in healthcare. Subtopic 3: Brain interface technologies, such as Elon Musk’s Neuralink, provide a unique and beneficial solution to mental health issues.",
    "Digital Video Production: Participants develop and submit a digital video and a documentation portfolio (including such items as a storyboard, script, summary of references and sources, and equipment list) that reflects the annual theme. Semifinalists participate in an interview. [video production, director, producer, actor, actress, play, theater] Create a short film that includes at least 30 seconds of animation "
    "Dragster Design: Participants design, draw, and construct a CO2-powered dragster that adheres to specifications, design and documentation requirements, and the annual theme. Semifinalists compete in a double-elimination race and participate in an interview. [car, cars, rc, racing]",
    "Drone Challenge (UAV): Participants design, build, assemble, document, and test fly an open-source Unmanned Arial Vehicle (UAV) according to the stated annual theme/problem specifications. The required documentation portfolio must include elements such as a photographic log, wiring schematics, and a description of the programming software used. Semifinalists participate in an interview. [engineering, robotics, robots, electronics, flying, plane, drone, helicopter]",
    "Engineering Design: Participants develop a solution to an annual theme that is based on a specific challenge noted by the National Academy of Engineering (NAE) in its compilation of the grand challenges for engineering in the 21st century. The solution will include a documentation portfolio, a display, and a model/prototype. Semifinalists deliver a presentation and participate in an interview. [engineering, board] Manage the nitrogen cycle ",
    "Extemporaneous Speech: Participants select a technology-related or TSA topic from among three topic cards and prepare and give a three-to-five-minute speech that communicates their knowledge of the chosen topic. The quality of the speech determines advancement to the semifinalist level of competition, for which an identical competition procedure is followed to determine finalists. [public speaking, speech, president, lecture]",
    "Fashion Design and Technology: To address the annual theme, participants demonstrate expertise in fashion design principles by creating a wearable garment, garment patterns, and a documentation portfolio. Semifinalist teams present their garment designs (worn by team models), discuss the design process with evaluators, and respond to interview questions. [crochet, embroidery, fashion, modeling, jewls, runway] The prototype must include a type of wearable technology. No pyrotechnics or ignitable elements are permitted. Teams will submit one (1) or two (2) garments for judging (top and bottom or one [1]-piece.) All required components must fit inside a 32-quart plastic container. Any accessories (hats, gloves, boots, etc.) may be used during semifinalist presentations, however, they are not submitted in the preliminary round. ",
    "Flight Endurance: Participants design, build, fly, and adjust (trim) a rubber-band powered model aircraft to make long endurance flights inside a contained airspace. Documentation (including elements such as attributes of the model design, drawings, and an analysis of the trim modifications), an inspection of the model and the required model flight box, and official times for two flights are aspects of the evaluation. [planes, engineering, model planes]",
    "Forensic Science: Participants take a test of basic forensic science to qualify for the semifinal round of competition. Semifinalists examine a mock crime scene and demonstrate their knowledge of forensic science through crime scene analysis, with the findings synthesized in a written report/analysis. [police, investigation, detective, medicine]",
    "Future Technology Teacher: Participants research a developing technology, prepare a video showing an application of the technology in the classroom, and create a lesson plan/activity that features the application and connects to the Standards for Technological and Engineering Literacy (STEL), as well as STEM initiatives and integration. Semifinalists demonstrate the lesson plan and answer questions about their presentation. [teaching, lectures, presentations]",
    "Geospatial Technology: To address the issue presented in an annual theme, participants interpret geospatial data and develop a digital portfolio containing maps, data, and pertinent documentation. Semifinalists defend their projections and visual infographic during a presentation/interview. [science, earth science, atmosphere, board] Identity a disaster threat, natural or otherwise, that may impact your community. Develop an infographic that communicates hazard zones, evacuation routes, and resource distribution.",
    "Manufacturing Prototype: Participants design, fabricate, and use Computer Integrated Manufacturing (CIM) to create a product that addresses the annual theme. A documentation portfolio and the completed product prototype are submitted for evaluation. Semifinalists give a product “sales pitch” and demonstration. [factory, production, business, entrepreneur] An item that can be used as picture frames for a home or office while also serving another purpose",
    "Music Production: Participants produce an original musical piece that reﬂects the annual theme on the TSA website under Themes & Problems. The quality of the musical piece and required documentation (including elements such as a plan of work, self-evaluation, and a list of hardware, software, and instruments used) determines advancement to the semifinal level of competition, during which semifinalist participants are interviewed. [producer, musician, band, music, beats] musical piece that will be used as the background music for a role-playing game (RPG) video game. It will be played during the parts of the game when the player's character is visiting the blacksmith.",
    "On Demand Video: Once participants receive the challenge details (required criteria, such as props and a line of dialogue) at the national TSA conference, they have 36 hours to produce a 60-second film that showcases video skills, tools, and communication processes. The quality of the completed video production determines the finalists. [video, producer, director, scene, filming, movies]",
    "Photographic Technology: Participants produce a photographic portfolio - demonstrating expertise in photo and imaging technology processes - to convey a message based on the annual theme. Semifinalists have 24 hours to complete a portfolio of photos (with required documentation) taken onsite at the national TSA conference. Finalists are determined based on the quality of the semifinal portfolio, the portfolio presentation, and interview responses. [photography, pictures, camera, lens, video] Using five photographs, tell a story about your journey in TSA.  The type of photo (color, black and white, macro, still life, and student choice) should add to the impact of the story you are sharing.",
    "Prepared Presentation: Participants deliver a three-to-five-minute oral presentation related to the current national TSA conference theme. Both semifinalists and finalists are determined based on the quality of the presentation and the appropriate use and content of the accompanying required slide deck. [presentation, public speaking, speech, entrepreneurship, convincing] Develop a presentation that highlights the field of digital music production, including the timeline of its origin, development, fruition, and release of the technology on a global scale.",
    "Promotional Design: Participants use computerized graphic communications layout and design skills to produce a promotional resource packet. The resource must address the annual theme/problem and include at least four printed publication items and required documentation. Semifinalists demonstrate publishing competency in an onsite technical design challenge. [advertisement, business, design, graphics] Branding materials for a fictitious restaurant; the four (4) Promotional Folder items are student choice.",
    "Robotics: Participants design, build, document, and test a robot assembled using open-sourced parts according to stated specifications and to meet the challenge of the yearly theme/problem. [robots, engineering, electrical engineering, mechanical engineering]",
    "Senior Solar Sprint: The Senior Solar Sprint (SSS) competition is managed by TSA. Students apply scientific understanding, creativity, experimentation, and teamwork to design, build, and race a model solar vehicle that carries a payload; documentation of the process is required. Students must register via an  Army Educational Outreach Program (AEOP) portal to participate and begin the SSS journey. [electric, tesla, cars, solar power, green, energy, race, racing]",
    "Software Development: Participants use their knowledge of cutting-edge technologies, algorithm design, problem-solving principles, effective communication, and collaboration to design, implement, test, document, and present a software development project of educational or social value. Both semifinalists and finalists are determined based on the quality of the presentation and project. [coding, programming, computer scripting, binary, code, hexadecimal, assembly, programming language] Develop a program that enhances the environment and/or agriculture to be more sustainable and efficient.",
    "STEM Mass Media: In response to an annual theme, participants use written and verbal communication skills to convey a news story in both a video broadcast (preliminary round) and a digital written format (semifinal round). Participants must demonstrate a strong understanding of journalism etiquette and the common practices of the field of mass media. [video, news, information, presentation] Brain-computer interfaces (BCIs) are advanced technologies that enable direct communication between the brain and computers. Using electrodes placed on the scalp, BCIs detect brain signals that are then translated into commands for computers. These signals can control various applications, from typing messages to playing video games, solely through thought. BCIs have practical applications beyond entertainment; they assist individuals with disabilities by allowing them to operate prosthetic limbs or communicate when speech is impaired. BCIs represent a remarkable intersection of neuroscience and computer science, offering promising solutions for both medical and technological advancements. Based on the following headline (link below), develop a news broadcast that includes an introduction of the headline, a summary of the information in the news story, and an explanation of potential future implications of the highlighted work.",
    "Structural Design and Engineering: Participants apply the principles of structural engineering to design and construct a structure that complies with the annual challenge. An assessment of the required documentation and the destructive testing of the structure (to determine its design efficiency) determine both semifinalists and finalists. [construction, civil engineering, engineering, buildings, city]",
    "System Control Technology: Participants develop a solution to a problem (typically one from an industrial setting) presented onsite at the conference. They analyze the problem, build a computer-controlled mechanical model, program the model, demonstrate the programming and mechanical features of the model-solution in an interview, and provide instructions for evaluators to operate the model. [robotics, vex, engineering, mechanical engineering]",
    "Technology Bowl: Participants demonstrate their knowledge of TSA and concepts addressed in technology content standards by completing an objective test. Semifinalist teams participate in a question/response, head-to-head, team competition. [technology, quiz, jeopardy, game show, test]",
    "Technology Problem Solving: Participants use problem-solving skills to design and construct a finite solution to a challenge provided onsite at the conference. Solutions are evaluated at the end of 90 minutes using measures appropriate to the challenge, such as elapsed time, horizontal or vertical distance, and/or strength. [creative, problem solving, quiz, challenge, creation, engineering]",
    "Transportation Modeling: Participants research, design, and produce a scale model of a vehicle that complies with the annual design problem. A display for the model and a documentation portfolio - containing elements such as a description of the vehicle, photographs and commentary detailing the vehicle production, and technical illustrations - are required. Semifinalists participate in an interview. [engineering, modeling, 3d printing, painting, design]",
    "Video Game Design: Participants design, build, and launch an E-rated online video game - with accompanying required documentation - that addresses the annual theme. Semifinalists participate in an interview to demonstrate the knowledge and expertise they gained during the development of the game. [game, video game, programming, coding, scripting, 3d modeling, animation, sound, music production, graphics, ui, gui]",
    "Virtual Reality Simulation (VR): Participants use video and 3D computer graphics tools and design processes to create a two-to-three-minute VR visualization (accompanied by supporting documentation) that addresses the annual theme. Semifinalists deliver a presentation about their visualization and participate in an interview. [virtual reality, programming, coding, 3d modeling, meta quest, oculus, steam] Create a virtual reality (VR) simulation",
    "Webmaster: Participants design, build, and launch a website that addresses the annual challenge. Semifinalists participate in an interview to demonstrate the knowledge and expertise gained during the development of the website. [website, web design, web development, programming, coding, graphic design, art, pictures]"
]

ai_model = SentenceTransformer('all-MiniLM-L6-v2')
event_embeddings = ai_model.encode(event_descs, convert_to_tensor=True)

def is_officer(user):
    return user.is_superuser or user.groups.filter(name="Officer").exists()

# Create your views here.
def index(request):
    events_list = Event.objects.all()
    print('recieved get')
    return render(request, "events/index.html", {"Events": events_list})

def view_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    competitors = event.competitors
    try:
        competitors = json.loads(competitors)
    except:
        pass
    return render(request, "events/event.html", {"Event": event, "Teams": competitors})

@user_passes_test(is_officer)
def update_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == "POST":
        try:
            name = request.POST.get('Name')
            desc = request.POST.get('Description')
            prompt = request.POST.get('Prompt')
            ceg_file = request.FILES.get('CEG')
            teams_json = request.POST.get('Teams')

            event.name = name
            event.desc = desc
            event.prompt = prompt
            # event.CEG = ceg_file
            event.competitors = teams_json

            event.save()
            
            return redirect("/events/", permanent=True)
        except Exception as e:
            print(f"ERRORORO {e}")

    competitors = event.competitors
    try:
        competitors = json.loads(competitors)
    except:
        pass
    return render(request, "events/update_event.html", {"Event": event, "teams_json": competitors})

@xframe_options_exempt
def view_ceg_file(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        file_path = event.CEG.path
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')  # Adjust MIME if needed
    except (Event.DoesNotExist, FileNotFoundError):
        raise Http404("File not found.")

def event_matchmaker(request):
    if request.method == "POST":
        interests = request.POST.get('interests')
        student_embedding = ai_model.encode(interests, convert_to_tensor=True)
        cosine_scores = util.cos_sim(student_embedding, event_embeddings)

        sorted_events = sorted(zip(cosine_scores[0], event_descs), key=lambda x: x[0], reverse=True)
        sorted_events_list = []
        for event in sorted_events:
            og_split = event[1].split(":")
            sorted_events_list.append((og_split[0], og_split[1].split(" [")[0] ))

        return render(request, "events/matchmaker.html", {"Events": tuple(sorted_events_list)})

    return render(request, "events/matchmaker.html")

def add_event(request):
    if request.user.groups.filter(name="Officer").exists():
        if request.method == "POST":
            try:
                name = request.POST.get('Name')
                desc = request.POST.get('Description')
                prompt = request.POST.get('Prompt')
                ceg_file = request.FILES.get('CEG')
                teams_json = request.POST.get('Teams')

                newEvent = Event.objects.create(
                    name = name,
                    desc = desc,
                    prompt = prompt,
                    CEG = ceg_file,
                    competitors = teams_json
                )
                return redirect("/events/")
                
            except Exception as e:
                print(f"ERROR!!! {e}")
                traceback.print_exc()

        return render(request, "events/add_event.html")
    else:
        return redirect("/events/")

def delete_event(request, event_id):
    if request.method != "POST": return redirect("/events/")

    event = get_object_or_404(Event, pk=event_id)
    if not event: return redirect("/events/")

    event.delete()
    return redirect("/events/")
